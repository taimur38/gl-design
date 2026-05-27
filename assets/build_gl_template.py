#!/usr/bin/env python3
"""
build_gl_template.py

Takes the existing md2docx template.docx and transforms it into a
Growth Lab-branded reference document (gl-report.docx).

Changes:
  - Theme: GL color scheme + Source Sans 3 / JetBrains Mono fonts
  - Styles: font names, sizes, colors, spacing per grammar.md + recipes/report.md
  - Page setup: 1" top/left/right, 1.25" bottom → 6.5 × 8.75" live area
  - Header: GL logo + simplified running head
  - Footer: page number in JetBrains Mono

Usage:
    python3 build_gl_template.py
"""

import zipfile
import shutil
import re
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.expanduser("~/dev/taimur-skills/md2docx/assets/template.docx")
OUTPUT = os.path.join(SCRIPT_DIR, "gl-report.docx")

# ---------------------------------------------------------------------------
# GL Design Tokens (nil-design)
# ---------------------------------------------------------------------------
#
# Office theme slots: dk1/lt1 are "Text/Background dark/light" — system
# colors at the user's level. dk2/lt2 are "Text/Background 2". accent1-6
# feed Word's color picker and Office chart defaults.
#
# Note on weight: Word's <w:b/> is a boolean — there's no native weight 500.
# Styles that nil specifies at weight 500 (H1, H2, chart title) are rendered
# with <w:b/>, which the user's Word installation maps to whatever bold face
# the font system can provide (typically weight 700 for Source Serif 4). The
# visual hierarchy is still carried mostly by size; the 500-vs-700 mismatch
# is a known compromise — see followups.md.

GL_COLORS = {
    "dk1":      "1A1714",  # ink — primary text / headings
    "lt1":      "FFFFFF",  # white background
    "dk2":      "015C9C",  # accent blue (dark slot)
    "lt2":      "F4F1EA",  # paper-warm
    "accent1":  "015C9C",  # c-1 primary blue
    "accent2":  "C77A20",  # c-2 amber (highlight / lead-finding)
    "accent3":  "CEC96B",  # c-3
    "accent4":  "51B196",  # c-4
    "accent5":  "A8352C",  # c-5
    "accent6":  "918BED",  # c-6
    "hlink":    "015C9C",  # hyperlinks → accent
    "folHlink": "6B645A",  # followed links → ink-3
}

# Fonts: Source Serif 4 for headings/display ("major"); Inter for body ("minor").
MAJOR_FONT = "Source Serif 4"
MINOR_FONT = "Inter"

# Sizes in half-points (Word convention: 24 = 12pt, 28 = 14pt, 68 = 34pt, etc.)
# Spacing in twips (20 twips = 1pt).
STYLES = {
    # styleId: (font, size_halfpt, color, bold, italic, space_before_twips, space_after_twips)
    # None = don't change that attribute

    # Body and document title
    "Normal":         (MINOR_FONT,  24, "2C2823", False, False, None, 120),  # 12pt Inter ink-2
    "Title":          (MAJOR_FONT, 112, "1A1714", False, False, None, 480),  # 56pt Display (cover only)
    "Subtitle":       (MAJOR_FONT,  34, "2C2823", False, False, None, 240),  # 17pt lead-paragraph style

    # Section headings (nil specifies 3 levels; H4–H6 are mild fallbacks)
    "Heading1":       (MAJOR_FONT,  68, "1A1714", True,  False, 480, 160),   # 34pt H1
    "Heading2":       (MAJOR_FONT,  40, "1A1714", True,  False, 560, 160),   # 20pt H2
    "Heading3":       (MAJOR_FONT,  28, "1A1714", True,  False, 280, 160),   # 14pt H3 — improvised, followups #1
    "Heading4":       (MINOR_FONT,  24, "6B645A", True,  False, 240, 120),
    "Heading5":       (MINOR_FONT,  24, "6B645A", False, False, 240, 120),
    "Heading6":       (MINOR_FONT,  24, "6B645A", False, True,  240, 120),

    # Quotes
    "Quote":          (MAJOR_FONT,  28, "2C2823", False, True,  120, 120),   # 14pt italic serif blockquote
    "IntenseQuote":   (MAJOR_FONT,  34, "015C9C", False, False, 120, 120),   # 17pt accent lead-style emphasis

    # Figures
    "FigureTitle":    (MAJOR_FONT,  28, "1A1714", True,  False, 240, 60),    # 14pt chart title (Source Serif 4 500)
    "FigureSource":   (MAJOR_FONT,  20, "2C2823", False, True,  60, 240),    # 10pt italic serif chart source
    "Source":         (MAJOR_FONT,  20, "2C2823", False, True,  60, 240),    # alias
    "Caption":        (MAJOR_FONT,  20, "2C2823", False, True,  60, 120),    # 10pt italic serif generic caption

    # Page chrome
    "FootnoteText":   (MINOR_FONT,  18, "6B645A", False, False, None, 60),   # 9pt Inter ink-3
    "Header":         (MINOR_FONT,  18, "6B645A", False, False, None, None), # 9pt Inter running head
    "Footer":         (MINOR_FONT,  18, "6B645A", False, False, None, None), # 9pt Inter folio

    # Table of contents
    "TOCHeading":     (MAJOR_FONT,  68, "1A1714", True,  False, 480, 160),   # Like H1
    "TOC1":           (MAJOR_FONT,  28, "1A1714", True,  False, 120, 60),    # 14pt TOC major (Source Serif 4 600)
    "TOC2":           (MINOR_FONT,  24, "2C2823", False, False, 60, 60),     # 12pt Inter TOC sub
    "TOC3":           (MINOR_FONT,  24, "6B645A", False, True,  60, 60),     # 12pt Inter italic TOC sub-sub
}

# Also update the corresponding "Char" styles for linked styles
CHAR_STYLES = {sid + "Char": vals for sid, vals in STYLES.items()}


# ---------------------------------------------------------------------------
# Theme XML builder
# ---------------------------------------------------------------------------

def build_theme_xml():
    """Build a complete GL theme1.xml."""

    def color_element(tag, val):
        if tag in ("dk1", "lt1"):
            # System colors for dark1/light1
            sys_name = "windowText" if tag == "dk1" else "window"
            return f'<a:{tag}><a:sysClr val="{sys_name}" lastClr="{val}"/></a:{tag}>'
        return f'<a:{tag}><a:srgbClr val="{val}"/></a:{tag}>'

    colors = "".join(color_element(k, v) for k, v in GL_COLORS.items())

    # Minimal font fallback list (just the essentials)
    def font_list(typeface):
        return (
            f'<a:latin typeface="{typeface}"/>'
            '<a:ea typeface=""/>'
            '<a:cs typeface=""/>'
            '<a:font script="Arab" typeface="Arial"/>'
            '<a:font script="Hebr" typeface="Arial"/>'
        )

    theme = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Growth Lab">'
        '<a:themeElements>'
        f'<a:clrScheme name="Growth Lab">{colors}</a:clrScheme>'
        '<a:fontScheme name="Growth Lab">'
        f'<a:majorFont>{font_list(MAJOR_FONT)}</a:majorFont>'
        f'<a:minorFont>{font_list(MINOR_FONT)}</a:minorFont>'
        '</a:fontScheme>'
        # Keep the standard Office format scheme (fills, lines, effects)
        '<a:fmtScheme name="Office">'
        '<a:fillStyleLst>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '</a:fillStyleLst>'
        '<a:lnStyleLst>'
        '<a:ln w="6350" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln>'
        '<a:ln w="12700" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln>'
        '<a:ln w="19050" cap="flat" cmpd="sng" algn="ctr"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln>'
        '</a:lnStyleLst>'
        '<a:effectStyleLst>'
        '<a:effectStyle><a:effectLst/></a:effectStyle>'
        '<a:effectStyle><a:effectLst/></a:effectStyle>'
        '<a:effectStyle><a:effectLst/></a:effectStyle>'
        '</a:effectStyleLst>'
        '<a:bgFillStyleLst>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
        '</a:bgFillStyleLst>'
        '</a:fmtScheme>'
        '</a:themeElements>'
        '<a:objectDefaults/>'
        '<a:extraClrSchemeLst/>'
        '</a:theme>'
    )
    return theme


# ---------------------------------------------------------------------------
# Style XML transformer
# ---------------------------------------------------------------------------

def ensure_rpr(xml):
    """Ensure the style has a <w:rPr> block, creating one if needed."""
    if '<w:rPr>' in xml:
        return xml
    # Insert rPr before </w:style> — after pPr if present, else after metadata
    if '</w:pPr>' in xml:
        return xml.replace('</w:pPr>', '</w:pPr><w:rPr></w:rPr>', 1)
    # Find the last metadata element to insert after
    insert_after = None
    for tag in ['</w:rsid>', '</w:unhideWhenUsed>', '</w:uiPriority>',
                '</w:qFormat>', '</w:next>', '</w:link>', '</w:basedOn>', '</w:name>']:
        pos = xml.rfind(tag)
        if pos >= 0:
            insert_after = pos + len(tag)
            break
    if insert_after:
        return xml[:insert_after] + '<w:rPr></w:rPr>' + xml[insert_after:]
    return xml


def transform_style(style_xml, sid, font, size, color, bold, italic, sp_before, sp_after):
    """Transform a single <w:style> element's properties."""
    xml = style_xml

    # Ensure rPr exists for font/size/color injection
    if font or size or color or bold or italic:
        xml = ensure_rpr(xml)

    # --- Font ---
    if font:
        rfont_new = (
            f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" '
            f'w:eastAsia="{font}" w:cs="{font}"/>'
        )
        if re.search(r'<w:rFonts[^/]*/>', xml):
            xml = re.sub(r'<w:rFonts[^/]*/>', rfont_new, xml)
        else:
            xml = xml.replace('<w:rPr>', f'<w:rPr>{rfont_new}', 1)

    # --- Size ---
    # Strategy: strip ALL existing sz/szCs, then inject fresh ones.
    if size:
        xml = re.sub(r'<w:sz\b[^/]*/>', '', xml)
        xml = re.sub(r'<w:szCs\b[^/]*/>', '', xml)
        sz_pair = f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
        xml = xml.replace('</w:rPr>', f'{sz_pair}</w:rPr>', 1)

    # --- Color ---
    # Match color elements with optional themeColor/themeShade/themeTint attrs
    if color:
        xml = re.sub(r'<w:color\b[^/]*/>', '', xml)
        color_el = f'<w:color w:val="{color}"/>'
        xml = xml.replace('</w:rPr>', f'{color_el}</w:rPr>', 1)

    # --- Bold ---
    # Strip ALL existing bold markers first, then optionally re-add
    xml = re.sub(r'<w:b\b[^/]*/>', '', xml)
    xml = re.sub(r'<w:bCs\b[^/]*/>', '', xml)
    if bold:
        xml = xml.replace('<w:rPr>', '<w:rPr><w:b/><w:bCs/>', 1)

    # --- Italic ---
    xml = re.sub(r'<w:i\b[^/]*/>', '', xml)
    xml = re.sub(r'<w:iCs\b[^/]*/>', '', xml)
    if italic:
        xml = xml.replace('<w:rPr>', '<w:rPr><w:i/><w:iCs/>', 1)

    # --- Spacing ---
    if sp_before is not None or sp_after is not None:
        # Ensure pPr exists
        if '<w:pPr>' not in xml:
            if '</w:rPr>' in xml:
                xml = xml.replace('</w:rPr>', '</w:rPr><w:pPr></w:pPr>', 1)
            else:
                # Insert after metadata
                for tag in ['</w:rsid>', '</w:unhideWhenUsed>', '</w:uiPriority>',
                            '</w:qFormat>', '</w:next>', '</w:link>', '</w:basedOn>', '</w:name>']:
                    pos = xml.rfind(tag)
                    if pos >= 0:
                        ins = pos + len(tag)
                        xml = xml[:ins] + '<w:pPr></w:pPr>' + xml[ins:]
                        break

        spacing_match = re.search(r'<w:spacing([^/]*)/>', xml)
        if spacing_match:
            sp_xml = spacing_match.group(0)
            if sp_before is not None:
                if 'w:before=' in sp_xml:
                    sp_xml = re.sub(r'w:before="\d+"', f'w:before="{sp_before}"', sp_xml)
                else:
                    sp_xml = sp_xml.replace('<w:spacing', f'<w:spacing w:before="{sp_before}"')
            if sp_after is not None:
                if 'w:after=' in sp_xml:
                    sp_xml = re.sub(r'w:after="\d+"', f'w:after="{sp_after}"', sp_xml)
                else:
                    sp_xml = sp_xml.replace('<w:spacing', f'<w:spacing w:after="{sp_after}"')
            xml = xml[:spacing_match.start()] + sp_xml + xml[spacing_match.end():]
        else:
            parts = []
            if sp_before is not None:
                parts.append(f'w:before="{sp_before}"')
            if sp_after is not None:
                parts.append(f'w:after="{sp_after}"')
            sp_el = f'<w:spacing {" ".join(parts)}/>'
            xml = xml.replace('</w:pPr>', f'{sp_el}</w:pPr>', 1)

    return xml


def transform_styles_xml(content):
    """Apply GL styles to the entire styles.xml content."""

    # 1. Update docDefaults — set base font to Source Sans 3, 11pt
    #    docDefaults sets the fallback for everything
    content = re.sub(
        r'<w:docDefaults>.*?</w:docDefaults>',
        '<w:docDefaults>'
        '<w:rPrDefault><w:rPr>'
        f'<w:rFonts w:ascii="{MINOR_FONT}" w:hAnsi="{MINOR_FONT}" '
        f'w:eastAsia="{MINOR_FONT}" w:cs="{MINOR_FONT}"/>'
        '<w:sz w:val="24"/><w:szCs w:val="24"/>'  # 12pt
        '<w:color w:val="2C2823"/>'  # ink-2
        '</w:rPr></w:rPrDefault>'
        '<w:pPrDefault><w:pPr>'
        '<w:spacing w:after="120" w:line="384" w:lineRule="auto"/>'  # 1.6 line-height at 12pt
        '<w:jc w:val="both"/>'  # Justified text
        '</w:pPr></w:pPrDefault>'
        '</w:docDefaults>',
        content,
        flags=re.DOTALL
    )

    # 2. Transform individual styles
    all_mods = {**STYLES, **CHAR_STYLES}

    for sid, (font, size, color, bold, italic, sp_before, sp_after) in all_mods.items():
        # Find this style's XML block
        pattern = rf'(<w:style [^>]*w:styleId="{sid}"[^>]*>)(.*?)(</w:style>)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            full = match.group(0)
            new = transform_style(full, sid, font, size, color, bold, italic, sp_before, sp_after)
            content = content.replace(full, new, 1)

    # 3. Post-process: fix Quote/FigureSource alignment
    #    Quote should be left-aligned with indent (not centered)
    #    FigureSource should be left-aligned (not centered)
    for sid in ['Quote', 'QuoteChar', 'FigureSource']:
        pattern = rf'(<w:style [^>]*w:styleId="{sid}"[^>]*>)(.*?)(</w:style>)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            block = match.group(0)
            # Remove center justification
            new_block = re.sub(r'<w:jc w:val="center"\s*/>', '', block)
            # Add left indent to Quote for blockquote feel (360 twips = 0.25")
            if sid == 'Quote' and '<w:ind' not in new_block:
                new_block = new_block.replace('</w:pPr>',
                    '<w:ind w:left="360" w:right="360"/></w:pPr>', 1)
            content = content.replace(block, new_block, 1)

    return content


# ---------------------------------------------------------------------------
# Page margins
# ---------------------------------------------------------------------------

def transform_document_xml(content):
    """Update page margins: 1" top/left/right, 1.25" bottom → 6.5 × 8.75" live area.

    Twips: 1440 = 1", 1800 = 1.25". The 1.25" bottom margin optically centers
    the text block, hosts page numbers and footnotes, and makes the 8.75" live
    height resolve into exactly 7 vertical modules of 1.25".
    """
    content = re.sub(
        r'<w:pgMar[^/]*/>',
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1800" w:left="1440" '
        'w:header="720" w:footer="720" w:gutter="0" />',
        content
    )
    return content


# ---------------------------------------------------------------------------
# Header: remove the "Internal Document" text, keep logo
# ---------------------------------------------------------------------------

def transform_header_xml(content):
    """Simplify header — remove 'Internal Document' highlight, keep clean."""
    # Remove the yellow-highlighted "Internal Document" run
    content = re.sub(
        r'<w:r w:rsidRPr="[^"]*"><w:rPr><w:highlight w:val="yellow"/></w:rPr>'
        r'<w:t>[^<]*</w:t></w:r>',
        '',
        content
    )
    return content


# ---------------------------------------------------------------------------
# Main: unzip → transform → rezip
# ---------------------------------------------------------------------------

def build_template():
    tmp = OUTPUT + ".tmp"

    with zipfile.ZipFile(SOURCE, 'r') as zin, \
         zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:

        for item in zin.infolist():
            data = zin.read(item.filename)

            if item.filename == 'word/theme/theme1.xml':
                data = build_theme_xml().encode('utf-8')

            elif item.filename == 'word/styles.xml':
                text = data.decode('utf-8')
                text = transform_styles_xml(text)
                data = text.encode('utf-8')

            elif item.filename == 'word/document.xml':
                text = data.decode('utf-8')
                text = transform_document_xml(text)
                data = text.encode('utf-8')

            elif item.filename == 'word/header2.xml':
                text = data.decode('utf-8')
                text = transform_header_xml(text)
                data = text.encode('utf-8')

            zout.writestr(item, data)

    shutil.move(tmp, OUTPUT)
    print(f"Built: {OUTPUT}")


def main():
    if not os.path.exists(SOURCE):
        print(f"Error: Source template not found at {SOURCE}")
        sys.exit(1)
    build_template()


if __name__ == "__main__":
    main()
