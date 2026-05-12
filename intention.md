# Growth Lab Design System — Intention

## Purpose

Establish a **visual grammar** for all Growth Lab outputs — reports, slide
decks, briefs, standalone charts, web pages, social cards — so that anything
the lab ships feels coherent and identifiably ours. The grammar codifies the
shared parts (color, type, chart conventions); **recipes** apply the grammar
to specific media (each artifact has a clear home on its page or screen); and
**tools** encode both as runnable artifacts that researchers can use without
design training.

## Problem

Lab outputs don't currently feel like they come from the same place. Each
medium reinvents its typography, sizing, and figure conventions ad-hoc.
Reports have one set of chart sizes, slides another; brand colors get
re-picked by hand; the relationship between page geometry and figure
dimensions is loose; researchers without design background have no
opinionated default to fall back on.

## Approach

Three layers, each separable:

1. **Grammar** ([`grammar.md`](grammar.md)) — medium-agnostic primitives.
   Color tokens, type stack, type scale ratio, role hierarchy, in-chart
   typography. The decisions that hold true across every artifact.

2. **Recipes** ([`recipes/`](recipes/)) — applications of the grammar to a
   specific medium. Each recipe pins page geometry, body anchor, figure
   sizes, spacing, and element patterns. Today: long-form report. Future:
   slide deck, one-page brief, web/standalone chart, possibly LaTeX paper.

3. **Tools** — codified, runnable artifacts that implement grammar + recipe
   so other people can absorb them by using them, not by reading
   specifications:
   - **R functions** in [`skills/gl-ggplot/`](skills/gl-ggplot/) — theme,
     palettes, named figure sizes.
   - **Pandoc filters and templates** in [`skills/md2docx/`](skills/md2docx/)
     and [`assets/gl-report.docx`](assets/gl-report.docx) — markdown to Word
     with GL styling.
   - **Claude skills** — `gl-ggplot`, `md2docx`, `chart-audit` — so AI
     assistants apply the grammar automatically.
   - **Static assets** in [`assets/`](assets/) — fonts, logos, color CSVs
     consumed by all of the above.

## Design inspirations

- **Foreign Affairs** — clean, authoritative layouts; strong typographic
  hierarchy; generous margins that let the text breathe.
- **World Bank flagship reports** — professional data presentation; effective
  use of sidebars, call-out boxes, and structured figure placement.
- **The Economist** — data-dense but highly readable; disciplined use of
  color; excellent chart typography.
- **QJE (Quarterly Journal of Economics)** — academic rigor; clean,
  no-nonsense typesetting; well-integrated figures and tables.

## Existing assets

- **Growth Lab Design Library** (`growthlab.app/design-library`) — brand
  colors, visualization palettes, logos, flags. Downloaded to
  [`assets/design-library/`](assets/design-library/).
- **Source Sans 3** — GL's primary typeface, bundled locally in
  [`assets/fonts/`](assets/fonts/).
- **JetBrains Mono** — for captions, axis labels, technical annotations.
- **Pakistan FM meeting materials** ([`playground/`](playground/)) — a
  working dogfood example of the report recipe, with embedded ggplot code
  and rendered output.

## Constraints

- Output formats vary by recipe: PDF (reports, briefs), PPTX/PDF (slides),
  PNG/SVG (charts), HTML (web). The grammar holds across all of them.
- Researchers author in Markdown / Rmd / Quarto; figures are generated in R
  (ggplot2) and saved as PNG at 300 DPI.
- References managed via Zotero → CSL/BibTeX.
- The system must be simple enough that a researcher can follow it without
  design training — the tools should make the right defaults automatic.
