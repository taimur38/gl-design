# Open questions and follow-ups

Working notes for the `nil-design` branch — points that need a decision, a
conversation with nil, or future iteration. Not for the merged spec.

## 1. Heading depth — we need an H3

Nil's typography spec defines three heading tiers: **display** (cover only),
**H1 section**, **H2 subsection**. Long-form research reports almost always
need at least one more level (H3) for sub-subsections. The current
`recipes/report.md` follows nil strictly and so has no H3 definition.

**Resolution options:**
- Ask nil to extend the spec with an H3.
- Improvise an H3 — Source Serif 4 ~16pt weight 600, or sentence-case Inter
  600 at 13pt, sit it somewhere between H2 (20pt) and chart title (14pt).
  Both options risk colliding with chart title styling.
- Use the lead paragraph as a soft section break, and rely on visual rhythm
  instead of an explicit H3.

## 2. Body baseline doesn't align to the 1.25" vertical module grid

Previously: body at 11pt / 15pt leading = 0.208" per baseline. Six baselines
= 1.25" = one vertical module. Body lines and figure placements snapped to
the same rhythm.

Under nil: body at 12pt / 1.6 line-height = 19.2pt leading = 0.267" per
baseline. Six baselines = 1.6" — does not divide 1.25". Body has its own
rhythm; the module grid is still useful for figure placement but the two no
longer share a baseline.

**Resolution options:**
- Accept the decoupling (current state). Figures snap; body flows.
- Tighten body leading to ~1.49 (17.86pt) to recover the snap — overrides
  nil's `line-height: 1.6`.
- Recompute the vertical module on the body baseline (would shrink modules
  to ~1.07", break the 7-module fit into 8.75" live height).

## 3. opsz numbers live in grammar but technically track size

`grammar.md` §2 includes specific opsz values (60 / 36 / 22 / 18 / 14) tied
to usage roles. By the grammar/recipe split rule, those values should live
in the recipe alongside size. The argument for keeping them in grammar:
opsz is a *glyph-cut intent*, not an absolute size — a slide cover and a
report cover both want opsz 60 even at different absolute sizes.

**Decision:** keep in grammar for now (user call). Revisit if a slide
recipe picks different opsz values.

## 4. Slide mode under nil's grammar

Nil's spec is report-only. `theme_gl()` currently exposes `mode = "slide"`
and `mode = "report"`. The slide mode renders titles inside the chart;
report mode suppresses them.

Under nil, the families and palette are the same, but the in-chart text
roles (chart title, subtitle, source) all want serif vs italic-serif
treatment. The default base size for slide-rendered charts will need to be
bigger (~16pt vs 12pt body) to read at a distance.

**Resolution:** specify slide recipe when one becomes a real artifact. For
now, `mode = "slide"` falls back to sensible defaults using the new fonts.

**Verification when that happens:** chart subtitle color migrated from old
`ink-3` (`#6B645A`) to new `ink-3` (`#4F4A42`) — visually cooler and darker.
Report mode suppresses the subtitle entirely, so this only matters once
slide mode is exercised again. Confirm the new tone reads correctly against
the slide background before declaring done.

## 5. Paper color rendering in Word

The recipe specifies `paper #FAF8F4` (warm white) for content pages and
`cover-bg #F3F2EA` for the cover. Word supports a page background color but
it doesn't print by default — readers see white pages unless they enable
"Print background colors and images." Most PDF exports respect it.

**Resolution options:**
- Set the page background in the docx; accept that Word-screen and printed
  Word may differ from the intended look.
- Drop the warm paper for the docx pipeline; only honor it in HTML / PDF
  generated via LaTeX where backgrounds render reliably.
- Generate the final PDF from HTML (Chromium / wkhtmltopdf) and accept
  the docx as an intermediate.

## 6. Figure block density

Nil's figure block has five elements: figure label, chart title, chart
subtitle (optional), image, source. The previous recipe had three (title,
image, caption). On small inset charts the five-element block may feel
heavy.

**Resolution options:**
- Treat figure label + subtitle as optional for `minor` / `half` figures.
- Keep the full block for `full` and `major`; collapse to title + image +
  source for smaller sizes.
- Follow nil strictly everywhere.

## 7. Sector palettes vs nil's 6-color categorical

The Atlas HS sector palette
(`assets/design-library/visualization_colors/atlas/hs_product_sectors.csv`)
is an external Growth Lab standard. It does not match nil's 6-color
categorical palette. We need a rule for when to use which.

**Tentative rule:** use the Atlas / sector palette when the chart is about
trade or product data (the colors carry sector semantics). Use the
6-color categorical otherwise. This mirrors how Atlas / Metroverse pages
themselves work.

## 8. Should growthlabbify.lua be format-agnostic?

Status: **not now.** The original idea was to refactor the lua filter to emit
format-agnostic AST so both `md2pdf` (HTML) and `md2docx` (DOCX) could share
it. After building the pandoc-based `md2pdf`, the filter turned out to be
**unnecessary** on the HTML path:

| Feature                          | DOCX (lua filter)           | HTML (pandoc + CSS) |
|----------------------------------|-----------------------------|---------------------|
| `:::` callout box                | OpenXML table with shading  | `<div class="box">` + CSS |
| Figure title above image         | Reorders AST + custom-style | `figure { flex-direction: column-reverse }` |
| `Source:` paragraph styling      | Custom-style "Figure Source"| `figure + p` selector |
| Side-by-side figures             | OpenXML side-by-side table  | Could be `figure + figure` CSS later |
| References H1                    | Inserts Header before `#refs` div | `--reference-section-title` |

The two pipelines now do the same job from the same markdown input via
totally different mechanisms. That's acceptable — each renderer plays to
its strengths (pandoc's HTML writer is already rich; the DOCX writer needs
the Lua kick).

**When to revisit:** if we introduce a third output target (e.g. a slide
recipe), refactoring the filter to emit AST + classes that both targets
style natively starts to pay for itself.

## 10. Docx template lags the new cover spec

`recipes/report.md` §5 now documents the cover with:
- pre-title hairline (1px `ink-3` at 0.3 opacity)
- 3px `accent` title rule at 50% content width, left-anchored
- byline in `ink-2` (was `ink-3`)
- pattern artwork (`assets/design-library/cover-patterns/rect-pattern.svg`
  or `circle-pattern.svg`) at the bottom of the cover

None of this exists in `assets/gl-report.docx` or `assets/build_gl_template.py`
yet. Word-export fidelity of the cover page will lag the spec until the
template is regenerated. Similarly, the colophon page's desaturated echo
of the cover pattern (35% opacity, grayscale) is not in the template.

**Resolution:** treat the cover/colophon as an HTML-or-PDF-first artifact
for now; rebuild `gl-report.docx` to include cover-page art when the cover
becomes a routine deliverable from the docx pipeline.

## 9. Typography size history — px vs pt

Nil's typography-spec.html writes sizes in **CSS px** (12 / 17 / 20 / 34 /
56). An earlier pass of `recipes/report.md` copied those numerical values
into **pt**, which inflated everything by ~33% in print (1 CSS px =
0.75pt at 96 dpi). After review against the rendered PDF, the recipe was
rescaled to anchor body at 12pt (print readability) and convert the
heading values literally (×0.75, rounded):

| Role     | Nil HTML | Old recipe (pt) | New recipe (pt) |
|----------|----------|-----------------|-----------------|
| Display  | 56 px    | 56              | 44              |
| H1       | 34 px    | 34              | 26              |
| H2       | 20 px    | 20              | 16              |
| H3       | 16 px    | 16              | 14              |
| Lead     | 17 px    | 17              | 14              |
| Body     | 12 px    | 12              | 12 (kept)       |
| Footnote |  9 px    |  9              |  9 (kept)       |

Body and footnote are anchored to print readability rather than literal
conversion — Nil's 12px → 9pt would be illegibly small for a research
report.

## 10. Old font retention on merge

Three font families are still on the branch from the previous system:
Source Sans 3, JetBrains Mono, Crimson Pro. None are referenced by the new
grammar / recipe / tooling.

**Resolution options:**
- Remove on merge — clean break.
- Keep them in `assets/fonts/` indefinitely as historical reference / for
  any inherited Rmd that hasn't migrated.
- Move to a separate `assets/fonts/legacy/` subfolder.
