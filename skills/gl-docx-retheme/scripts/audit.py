#!/usr/bin/env python3
"""
audit.py — heuristic triage of a .docx against the GL design system.

Prints a markdown report of what retheme.py will fix mechanically, what
Claude should remap by judgment, and what must be flagged for the author.
Run it on the original document (to plan) and on the rethemed output
(to verify nothing legacy survived).

Usage:
    python3 audit.py document.docx
"""

import collections
import re
import sys
import zipfile

GL_FONTS = {"Inter", "Source Serif 4"}
MONO_HINTS = ("Mono", "Courier", "Consolas", "Menlo")
CAPTION_RE = re.compile(r'^\s*(figure|table|chart|exhibit)\s+\d+[.:]?\s',
                        re.IGNORECASE)
SOURCE_RE = re.compile(r'^\s*(sources?|notes?)\s*:', re.IGNORECASE)

P_RE = re.compile(r'<w:p\b[^>]*>.*?</w:p>', re.DOTALL)
PSTYLE_RE = re.compile(r'<w:pStyle w:val="([^"]+)"')
TEXT_RE = re.compile(r'<w:t[^>]*>([^<]*)</w:t>')


def para_text(p):
    return "".join(TEXT_RE.findall(p))


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    z = zipfile.ZipFile(path)
    doc = z.read("word/document.xml").decode("utf-8")
    names = set(z.namelist())

    print(f"# GL audit — {path}\n")

    # ---- Run-level direct formatting --------------------------------------
    fonts = collections.Counter(re.findall(r'<w:rFonts [^>]*w:ascii="([^"]+)"',
                                           doc))
    sizes = collections.Counter(re.findall(r'<w:sz w:val="(\d+)"', doc))
    colors = collections.Counter(re.findall(r'<w:color w:val="([0-9A-Fa-f]{6})"',
                                            doc))
    print("## Direct formatting in the body (retheme.py --strip-direct clears "
          "fonts/sizes/colors)\n")
    if fonts:
        non_gl = {f: n for f, n in fonts.items() if f not in GL_FONTS}
        print(f"- Run fonts: " + ", ".join(
            f"{f} ×{n}" for f, n in fonts.most_common()))
        if any(h in f for f in fonts for h in MONO_HINTS):
            print("- **MONOSPACE detected** — Nil forbids mono anywhere; "
                  "check code blocks are genuinely code")
        if non_gl:
            print(f"- Non-GL fonts present: {', '.join(sorted(non_gl))}")
    else:
        print("- No run-level font overrides")
    if sizes:
        print("- Direct sizes (half-pt): " + ", ".join(
            f"{s} ×{n}" for s, n in sizes.most_common(8)))
    if colors:
        print("- Direct colors: " + ", ".join(
            f"#{c} ×{n}" for c, n in colors.most_common(8)))

    # ---- Paragraph inventory ----------------------------------------------
    paras = P_RE.findall(doc)
    styles = collections.Counter()
    pseudo_headings, captions, sources, all_caps = [], [], [], []
    for i, p in enumerate(paras):
        m = PSTYLE_RE.search(p)
        sid = m.group(1) if m else "(none/Normal)"
        styles[sid] += 1
        text = para_text(p).strip()
        if not text:
            continue
        plain = m is None or sid in ("Normal", "BodyText", "(none/Normal)")
        bold_runs = "<w:b/>" in p or '<w:b ' in p
        if plain and bold_runs and len(text) < 90 and not text.endswith(".") \
                and not CAPTION_RE.match(text):
            pseudo_headings.append((i, text))
        if plain and CAPTION_RE.match(text):
            captions.append((i, text))
        if plain and SOURCE_RE.match(text):
            sources.append((i, text))
        letters = [c for c in text if c.isalpha()]
        if len(letters) > 8 and all(c.isupper() for c in letters):
            all_caps.append((i, text))

    print("\n## Paragraph styles in use\n")
    for sid, n in styles.most_common():
        print(f"- {sid} ×{n}")

    def section(title, items, note):
        print(f"\n## {title}\n")
        if items:
            print(note + "\n")
            for i, t in items[:25]:
                print(f"- p{i}: “{t[:90]}”")
            if len(items) > 25:
                print(f"- … and {len(items) - 25} more")
        else:
            print("- none found")

    section("Pseudo-headings (bold body paragraphs)", pseudo_headings,
            "Candidates to remap to Heading 1/2/3 — judge each by context:")
    section("Caption-like plain paragraphs", captions,
            "Candidates for the GL figure block (Figure Label + Title + "
            "Subtitle) or Table Caption with SEQ numbering:")
    section("Source/Note lines", sources,
            "Candidates for the Figure Source style:")
    section("ALL-CAPS paragraphs", all_caps,
            "Nil forbids all-caps headings/body (uppercase is chrome-only). "
            "Retype in sentence case, or restyle if it's an eyebrow:")

    # ---- Objects ------------------------------------------------------------
    n_img = len(re.findall(r'<w:drawing>', doc))
    tbls = re.findall(r'<w:tblPr>.*?</w:tblPr>', doc, re.DOTALL)
    tbl_styles = collections.Counter()
    for t in tbls:
        m = re.search(r'<w:tblStyle w:val="([^"]+)"', t)
        tbl_styles[m.group(1) if m else "(direct formatting)"] += 1
    print("\n## Objects\n")
    print(f"- Images: {n_img} — baked-in charts can't be restyled; flag any "
          "that predate the GL chart spec (regenerate via gl-ggplot)")
    print(f"- Tables: {len(tbls)}" + (" — styles: " + ", ".join(
        f"{s} ×{n}" for s, n in tbl_styles.most_common()) if tbls else ""))
    if any(s != "Table" for s in tbl_styles):
        print("  - Remap tables to the GL `Table` style "
              "(`<w:tblStyle w:val=\"Table\"/>`, drop direct tblBorders, "
              "ensure `<w:tblLook w:firstRow=\"1\">` + header row)")
    print(f"- SEQ fields: {len(re.findall(r'SEQ', doc))} | "
          f"TOC field: {'yes' if 'TOC \\\\o' in doc or 'TOC \\o' in doc else 'no'} | "
          f"Footnotes part: {'yes' if 'word/footnotes.xml' in names else 'no'}")

    # ---- Sections -----------------------------------------------------------
    margins = re.findall(r'<w:pgMar[^/]*/>', doc)
    print(f"- Sections: {len(margins)} — retheme.py sets GL margins "
          "(1\"/1\"/1\"/1.25\") on all unless --keep-margins")


if __name__ == "__main__":
    main()
