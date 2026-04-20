#!/usr/bin/env python3
"""
build_gl_template.py

Takes the existing md2docx template.docx and transforms it into a
Growth Lab-branded reference document (gl-report.docx).

Changes:
  - Theme: GL color scheme + Source Sans 3 / JetBrains Mono fonts
  - Styles: font names, sizes, colors, spacing per framework.md
  - Page setup: 1" margins all sides → 6.5" live width
  - Header: GL logo + simplified running head
  - Footer: page number in JetBrains Mono

Usage:
    python3 build_gl_template.py              # builds gl-report.docx
    python3 build_gl_template.py --editorial  # builds gl-report-editorial.docx
    python3 build_gl_template.py --all        # builds both
"""

import zipfile
import shutil
import re
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.expanduser("~/dev/taimur-skills/md2docx/assets/template.docx")

# ---------------------------------------------------------------------------
# GL Design Tokens
# ---------------------------------------------------------------------------

GL_COLORS = {
    "dk1": "333333",       # Primary text
    "lt1": "FFFFFF",       # White background
    "dk2": "266798",       # Brand blue (dark variant)
    "lt2": "F3F3F3",       # Light background
    "accent1": "266798",   # Brand blue
    "accent2": "C64646",   # Red (highlight)
    "accent3": "36B250",   # Green
    "accent4": "EAC218",   # Yellow
    "accent5": "D1852A",   # Orange
    "accent6": "52E2DE",   # Teal
    "hlink": "266798",     # Hyperlink = brand blue
    "folHlink": "7c7c7c",  # Followed link = muted
}

# Typography variants
VARIANTS = {
    "default": {
        "major": "Source Sans 3",
        "minor": "Source Sans 3",
        "output": "gl-report.docx",
    },
    "editorial": {
        "major": "Crimson Pro",
        "minor": "Source Sans 3",
        "output": "gl-report-editorial.docx",
    },
}

# Font: Source Sans 3 for both heading and body (default, overridden per variant)
MAJOR_FONT = "Source Sans 3"
MINOR_FONT = "Source Sans 3"

# Sizes in half-points (Word convention: 22 = 11pt, 28 = 14pt, etc.)
STYLES = {
    # styleId: (font, size_halfpt, color, bold, italic, space_before_twips, space_after_twips)
    # None = don't change that attribute
    "Normal":         (MINOR_FONT, 22, "333333", False, False, None, 120),
    "Heading1":       (MAJOR_FONT, 43, "333333", True,  False, 480, 120),  # 21.5pt
    "Heading2":       (MAJOR_FONT, 34, "333333", True,  False, 360, 120),  # 17pt
    "Heading3":       (MAJOR_FONT, 28, "333333", True,  False, 240, 120),  # 14pt
    "Heading4":       (MAJOR_FONT, 22, "333333", True,  False, 240, 120),  # 11pt semibold
    "Heading5":       (MAJOR_FONT, 22, "7c7c7c", False, False, 240, 120),
    "Heading6":       (MAJOR_FONT, 22, "7c7c7c", False, True,  240, 120),
    "Title":          (MAJOR_FONT, 52, "333333", True,  False, None, 120),  # 26pt
    "Subtitle":       (MAJOR_FONT, 32, "7c7c7c", False, False, None, 240),  # 16pt
    "Quote":          (MINOR_FONT, 22, "7c7c7c", False, True,  120, 120),
    "IntenseQuote":   (MINOR_FONT, 22, "266798", False, True,  120, 120),
    "FigureTitle":    (MINOR_FONT, 22, "333333", True,  False, 240, 60),
    "FigureSource":   ("JetBrains Mono", 17, "7c7c7c", False, True, 60, 240),  # 8.5pt
    "Source":         ("JetBrains Mono", 17, "7c7c7c", False, True, 60, 240),
    "Caption":        ("JetBrains Mono", 17, "7c7c7c", False, False, 60, 120),
    "FootnoteText":   (MINOR_FONT, 18, "7c7c7c", False, False, None, 60),  # 9pt
    "Header":         ("JetBrains Mono", 16, "7c7c7c", False, False, None, None),  # 8pt
    "Footer":         ("JetBrains Mono", 16, "7c7c7c", False, False, None, None),
    "TOCHeading":     (MAJOR_FONT, 34, "333333", True,  False, 480, 120),
    "TOC1":           (MINOR_FONT, 22, "333333", True,  False, 120, 60),
    "TOC2":           (MINOR_FONT, 22, "333333", False, False, 60, 60),
    "TOC3":           (MINOR_FONT, 20, "7c7c7c", False, False, 60, 60),
}

# Also update the corresponding "Char" styles for linked styles
CHAR_STYLES = {}
for sid, vals in list(STYLES.items()):
    CHAR_STYLES[sid + "Char"] = vals


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
        '<w:sz w:val="22"/><w:szCs w:val="22"/>'  # 11pt
        '<w:color w:val="333333"/>'
        '</w:rPr></w:rPrDefault>'
        '<w:pPrDefault><w:pPr>'
        '<w:spacing w:after="120" w:line="300" w:lineRule="auto"/>'  # ~15pt leading at 11pt
        '<w:jc w:val="both"/>'  # Justified text
        '</w:pPr></w:pPrDefault>'
        '</w:docDefaults>',
        content,
        flags=re.DOTALL
    )

    # 2. Transform individual styles
    all_mods = {}
    all_mods.update(STYLES)
    all_mods.update(CHAR_STYLES)

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
    """Update page margins to 1" all sides (1440 twips) → 6.5" live width."""
    content = re.sub(
        r'<w:pgMar[^/]*/>',
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
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
    # Update header style font
    content = re.sub(
        r'(<w:pStyle w:val="Header"/>)',
        r'\1',
        content
    )
    return content


# ---------------------------------------------------------------------------
# Box styling: update the Lua filter's box colors to match GL tokens
# The box colors are hardcoded in the Lua filter, but we can update the
# shading color in existing boxes in the template showcase document.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Main: unzip → transform → rezip
# ---------------------------------------------------------------------------

def apply_variant(variant_name):
    """Set the global MAJOR_FONT/MINOR_FONT and rebuild STYLES for a variant."""
    global MAJOR_FONT, MINOR_FONT, STYLES, CHAR_STYLES

    v = VARIANTS[variant_name]
    MAJOR_FONT = v["major"]
    MINOR_FONT = v["minor"]

    STYLES = {
        "Normal":         (MINOR_FONT, 22, "333333", False, False, None, 120),
        "Heading1":       (MAJOR_FONT, 43, "333333", True,  False, 480, 120),
        "Heading2":       (MAJOR_FONT, 34, "333333", True,  False, 360, 120),
        "Heading3":       (MAJOR_FONT, 28, "333333", True,  False, 240, 120),
        "Heading4":       (MAJOR_FONT, 22, "333333", True,  False, 240, 120),
        "Heading5":       (MAJOR_FONT, 22, "7c7c7c", False, False, 240, 120),
        "Heading6":       (MAJOR_FONT, 22, "7c7c7c", False, True,  240, 120),
        "Title":          (MAJOR_FONT, 52, "333333", True,  False, None, 120),
        "Subtitle":       (MAJOR_FONT, 32, "7c7c7c", False, False, None, 240),
        "Quote":          (MINOR_FONT, 22, "7c7c7c", False, True,  120, 120),
        "IntenseQuote":   (MINOR_FONT, 22, "266798", False, True,  120, 120),
        "FigureTitle":    (MINOR_FONT, 22, "333333", True,  False, 240, 60),
        "FigureSource":   ("JetBrains Mono", 17, "7c7c7c", False, True, 60, 240),
        "Source":         ("JetBrains Mono", 17, "7c7c7c", False, True, 60, 240),
        "Caption":        ("JetBrains Mono", 17, "7c7c7c", False, False, 60, 120),
        "FootnoteText":   (MINOR_FONT, 18, "7c7c7c", False, False, None, 60),
        "Header":         ("JetBrains Mono", 16, "7c7c7c", False, False, None, None),
        "Footer":         ("JetBrains Mono", 16, "7c7c7c", False, False, None, None),
        "TOCHeading":     (MAJOR_FONT, 34, "333333", True,  False, 480, 120),
        "TOC1":           (MINOR_FONT, 22, "333333", True,  False, 120, 60),
        "TOC2":           (MINOR_FONT, 22, "333333", False, False, 60, 60),
        "TOC3":           (MINOR_FONT, 20, "7c7c7c", False, False, 60, 60),
    }

    CHAR_STYLES = {}
    for sid, vals in list(STYLES.items()):
        CHAR_STYLES[sid + "Char"] = vals


def build_variant(variant_name):
    """Build a single template variant."""
    apply_variant(variant_name)

    output = os.path.join(SCRIPT_DIR, VARIANTS[variant_name]["output"])
    tmp = output + ".tmp"

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

    shutil.move(tmp, output)
    print(f"Built: {output}")


def main():
    if not os.path.exists(SOURCE):
        print(f"Error: Source template not found at {SOURCE}")
        sys.exit(1)

    if "--all" in sys.argv:
        for name in VARIANTS:
            build_variant(name)
    elif "--editorial" in sys.argv:
        build_variant("editorial")
    else:
        build_variant("default")


if __name__ == "__main__":
    main()
