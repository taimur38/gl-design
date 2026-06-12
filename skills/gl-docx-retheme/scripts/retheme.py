#!/usr/bin/env python3
"""
retheme.py — transplant the Growth Lab design system into an existing .docx.

The deterministic half of gl-docx-retheme:

  1. Replaces word/theme/theme1.xml with the GL theme (fonts + palette).
  2. Replaces word/styles.xml with the GL style set, then re-appends any
     target-only styles (custom styles, numbering-linked styles) so nothing
     the document references goes undefined. Re-appended styles keep their
     look until Claude remaps the paragraphs that use them.
  3. Sets GL page geometry (1" top/left/right, 1.25" bottom) on every section
     unless --keep-margins.
  4. With --strip-direct: removes run-level font/size/color overrides from
     the document body and footnotes/endnotes, so the transplanted styles
     actually show through. Bold/italic/underline/superscript are kept —
     they carry meaning. Headers/footers are left untouched.

What this does NOT do (Claude's judgment half, see SKILL.md): remap
direct-formatted pseudo-headings to Heading styles, rebuild figure blocks,
apply the Table style to tables, or flag content-level Nil violations.

Usage:
    python3 retheme.py input.docx output.docx [--strip-direct]
        [--keep-margins] [--template path/to/gl.docx]
"""

import argparse
import os
import re
import shutil
import sys
import zipfile

DEFAULT_TEMPLATE = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "md2docx", "assets", "templates", "gl.docx"))

GL_PGMAR = ('<w:pgMar w:top="1440" w:right="1440" w:bottom="1800" '
            'w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>')

STYLE_RE = re.compile(r'<w:style [^>]*w:styleId="([^"]+)"[^>]*>.*?</w:style>',
                      re.DOTALL)


def merge_styles(gl_styles, target_styles, used_ids):
    """GL styles wholesale + the target-only styles the document actually
    uses (plus their basedOn/link/next chains). Unused latent styles —
    Word templates carry ~100 — are dropped."""
    gl_ids = set(STYLE_RE.findall(gl_styles))
    target_blocks = {m.group(1): m.group(0)
                     for m in STYLE_RE.finditer(target_styles)}

    keep = set()
    frontier = [sid for sid in used_ids
                if sid in target_blocks and sid not in gl_ids]
    while frontier:
        sid = frontier.pop()
        if sid in keep:
            continue
        keep.add(sid)
        for ref in re.findall(r'<w:(?:basedOn|link|next) w:val="([^"]+)"',
                              target_blocks[sid]):
            if ref in target_blocks and ref not in gl_ids and ref not in keep:
                frontier.append(ref)

    extra = [target_blocks[sid] for sid in sorted(keep)]
    if extra:
        gl_styles = gl_styles.replace(
            "</w:styles>", "".join(extra) + "</w:styles>")
    return gl_styles, sorted(keep)


def collect_used_style_ids(zin):
    """Style ids referenced anywhere in the document's content parts."""
    used = set()
    for name in zin.namelist():
        if re.match(r'word/(document|footnotes|endnotes|header\d*|footer\d*)\.xml$',
                    name):
            xml = zin.read(name).decode("utf-8", errors="replace")
            used |= set(re.findall(
                r'<w:(?:pStyle|rStyle|tblStyle) w:val="([^"]+)"', xml))
    return used


def strip_direct_formatting(xml):
    """Remove run-level font/size/color overrides; keep semantic formatting
    (bold, italic, underline, vertAlign, highlight)."""
    for pat in (r'<w:rFonts\b[^>]*/>', r'<w:sz\b[^>]*/>',
                r'<w:szCs\b[^>]*/>', r'<w:color\b[^>]*/>'):
        xml = re.sub(pat, '', xml)
    # Drop run-property containers left empty by the strip
    xml = re.sub(r'<w:rPr>\s*</w:rPr>', '', xml)
    return xml


def set_margins(xml):
    return re.sub(r'<w:pgMar[^/]*/>', GL_PGMAR, xml)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--template", default=DEFAULT_TEMPLATE,
                    help="GL reference doc (default: md2docx templates/gl.docx)")
    ap.add_argument("--strip-direct", action="store_true",
                    help="strip run-level font/size/color overrides from the "
                         "body, footnotes and endnotes")
    ap.add_argument("--keep-margins", action="store_true",
                    help="leave the target's page geometry untouched")
    args = ap.parse_args()

    if not os.path.exists(args.template):
        sys.exit(f"GL template not found: {args.template}")

    with zipfile.ZipFile(args.template) as z:
        gl_theme = z.read("word/theme/theme1.xml")
        gl_styles = z.read("word/styles.xml").decode("utf-8")

    strip_parts = {"word/document.xml", "word/footnotes.xml",
                   "word/endnotes.xml"}
    tmp = args.output + ".tmp"
    kept = []

    with zipfile.ZipFile(args.input) as zin, \
         zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        names = set(zin.namelist())
        used_ids = collect_used_style_ids(zin)
        for item in zin.infolist():
            data = zin.read(item.filename)

            if item.filename == "word/theme/theme1.xml":
                data = gl_theme
            elif item.filename == "word/styles.xml":
                merged, kept = merge_styles(gl_styles,
                                            data.decode("utf-8"), used_ids)
                data = merged.encode("utf-8")
            elif item.filename == "word/document.xml":
                xml = data.decode("utf-8")
                if not args.keep_margins:
                    xml = set_margins(xml)
                if args.strip_direct:
                    xml = strip_direct_formatting(xml)
                data = xml.encode("utf-8")
            elif args.strip_direct and item.filename in strip_parts:
                data = strip_direct_formatting(
                    data.decode("utf-8")).encode("utf-8")

            zout.writestr(item, data)

        if "word/theme/theme1.xml" not in names:
            print("warning: target has no theme part; GL theme not added")

    shutil.move(tmp, args.output)
    print(f"Rethemed: {args.output}")
    if kept:
        print(f"Target-only styles kept (review whether their paragraphs "
              f"should be remapped to GL styles): {', '.join(sorted(kept))}")


if __name__ == "__main__":
    main()
