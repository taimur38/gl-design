---
name: gl-docx-retheme
description: Convert an existing Word document to the Growth Lab design system. Use this skill when the user asks to apply the GL theme to a .docx, restyle or retheme a Word document, migrate a legacy report to the new design, or make a Word doc compliant with Nil's typography/data-viz rules. Applies the theme mechanically, remaps mis-styled content by judgment, and flags what only the author can fix.
compatibility: Requires the gl.docx template (skills/md2docx/assets/templates/). Word-comment flagging uses the docx skill's comment machinery when available.
metadata:
  author: taimur-shah
  version: "1.0"
---

# GL docx retheme

Converts an existing Word document to the Growth Lab design system
([`grammar.md`](../../grammar.md), [`recipes/report.md`](../../recipes/report.md),
Nil's specs under [`nil/`](../../nil/)). Three layers of work:

1. **Mechanical** (scripted): theme + styles transplant, page geometry,
   direct-formatting strip.
2. **Judgment** (you, editing XML): remap mis-styled paragraphs to GL roles.
3. **Flags** (the author): content-level Nil compliance no tool can fix.

Never deliver a silently "converted" doc — the deliverable is the rethemed
file **plus** the flag list (as Word comments, or a markdown report).

## Workflow

### 1. Audit the original

```bash
python3 scripts/audit.py original.docx
```

Read the report: which fonts/styles are in use, pseudo-headings, caption-like
paragraphs, source lines, all-caps text, unstyled tables, image count.
This is your work plan.

### 2. Mechanical transplant

```bash
python3 scripts/retheme.py original.docx output.docx --strip-direct
```

- Replaces theme (fonts + GL palette) and styles with the GL set; target-only
  styles are kept and listed — decide per style whether its paragraphs should
  be remapped to a GL role.
- `--strip-direct` removes run-level font/size/color overrides (bold, italic,
  underline, superscript survive). **Skip it only** if the doc relies on
  intentional colored text — then strip selectively by hand in step 3.
- `--keep-margins` if the document must keep its page geometry.

### 3. Judgment remaps (unpack → Edit → pack)

Unpack `output.docx` (use the docx skill's `unpack.py`/`pack.py`) and work
through the audit findings in `word/document.xml`:

| Finding | Remap to |
|---------|----------|
| Bold/large paragraph posing as a heading | `<w:pStyle w:val="Heading1/2/3"/>`; strip leftover bold runs; sentence case, no trailing period |
| "Figure N: Title text" plain paragraph | The GL figure block (below) |
| "Source: …" / "Note: …" line near a figure | `FigureSource` |
| Caption typed below a table | `TableCaption` paragraph *above* the table, `Table N:` as a `SEQ Table` field |
| Hand-formatted table | `<w:tblStyle w:val="Table"/>`, delete direct `tblBorders`/`shd`, ensure `<w:tblLook w:firstRow="1" …/>`; numeric columns right-aligned; cell paragraphs → `Compact` |
| All-caps heading/body text | Retype sentence case (uppercase is reserved for eyebrow/label chrome, which the styles produce via `w:caps`) |
| Manually typed figure/table numbers | `SEQ Figure` / `SEQ Table` fields |
| Lists with literal "•" characters | Real list paragraphs (`numPr` / `ListParagraph`) |

**The GL figure block** (five paragraphs, in order — the styles carry
uppercase, keep-together, and spacing):

```xml
<w:p><w:pPr><w:pStyle w:val="FigureLabel"/></w:pPr>
  <w:r><w:t xml:space="preserve">Figure </w:t></w:r>
  <w:r><w:fldChar w:fldCharType="begin"/></w:r>
  <w:r><w:instrText xml:space="preserve"> SEQ Figure \* ARABIC </w:instrText></w:r>
  <w:r><w:fldChar w:fldCharType="separate"/></w:r>
  <w:r><w:t>1</w:t></w:r>
  <w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>
<w:p><w:pPr><w:pStyle w:val="FigureTitle"/></w:pPr>…title, ends with a period…</w:p>
<w:p><w:pPr><w:pStyle w:val="FigureSubtitle"/></w:pPr>…units/period (optional)…</w:p>
<w:p><w:pPr><w:pStyle w:val="FigureImage"/></w:pPr>…the existing w:drawing run…</w:p>
<w:p><w:pPr><w:pStyle w:val="FigureSource"/></w:pPr>…Source: … (required)…</w:p>
```

Split an existing "Figure 3: GDP has stagnated" caption at the colon: number
→ SEQ field in the label; remainder → title. If the caption mixes title and
units, put units in the subtitle.

### 4. Flag what only the author can fix

Insert Word comments (docx skill: `scripts/comment.py`, author "Claude") at
each spot; if comments are impractical, write `<output>-retheme-report.md`
instead. Flag against this checklist:

- **Chart images** — baked-in charts keep their old colors/fonts; regenerate
  with `gl-ggplot` (`theme_gl()`). Flag every chart that visibly predates the
  GL spec (wrong palette, monospace axis text, titles burned into the image —
  in GL reports the title lives in the figure block, not the PNG).
- **Chart titles** must state a *finding* and end with a period
  ("Exports stagnated after 2014.", not "Export trends").
- **Missing source lines** — every figure requires one.
- **Heading periods / case** — no trailing periods, sentence case.
- **Cover page** — the GL cover (cover paper, hairline, accent rule, pattern
  artwork) is HTML/PDF-first and can't be reproduced mechanically; flag for
  rebuild from the starter template (`templates/gl.dotx`) if the doc needs one.
- **Monospace anywhere** outside genuine code blocks.
- **Colored text** that isn't a GL role (accent is for eyebrows/labels/dates).
- **TOC** — re-insert via References → Table of Contents if the old one was
  hand-typed; fields need updating (Ctrl+A, F9) either way.

### 5. Validate and deliver

```bash
python3 <docx-skill>/scripts/office/validate.py output.docx
python3 scripts/audit.py output.docx   # legacy fonts/colors should be gone
```

Optionally convert to PDF for a visual spot-check — but remember LibreOffice
preview quirks (side-by-side figures stack, fields show cached values); real
Word is the reference. Deliver: the rethemed docx + the flag list, with a
short summary of what was changed mechanically vs. what needs the author.

## Known limits

- Sizes are the Word approximation (1px→1pt; body 12pt) — see
  `followups.md` §10 for all Word-fidelity limits.
- `--strip-direct` removes *all* direct font/size/color, including
  intentional ones; audit first.
- Embedded OLE objects (Excel charts) and text boxes are not restyled —
  flag them.
- Headers/footers are left as-is; replacing them with the GL running head
  (logo right) is manual — copy from `templates/gl.docx` if wanted.
