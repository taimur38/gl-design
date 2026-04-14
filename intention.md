# Growth Lab Report Design Framework — Intention

## Purpose

Establish a cohesive design framework for Growth Lab reports. These reports are
typically long-form documents containing prose, data visualizations (ggplot
charts), tables, and Zotero-managed references. The authoring pipeline is
Markdown → Word/PDF via pandoc (using the `/md2docx` skill), but the **final
deliverable is always a PDF**.

## Problem

The current Word theme works but lacks the visual refinement expected of a
flagship research output. There is no systematic grid, no defined relationship
between figure dimensions and page layout, and typography choices are ad-hoc
across headings, captions, and body text.

## Goals

1. **Modular grid for PDF pages** — a spatial system that governs margins,
   column widths, and vertical rhythm so every element (text blocks, figures,
   tables, pull quotes) has a clear home on the page.

2. **Typographic scale** — a coherent set of font choices and sizes for every
   text role: H1–H4 headings, body text, figure titles, figure captions, table
   headers, footnotes, block quotes, and page headers/footers. Built on the GL
   design library's primary font (Source Sans 3) with JetBrains Mono for
   technical/caption elements.

3. **Figure specification system** — defined aspect ratios and pixel/inch
   dimensions for charts so they snap cleanly to the grid. Currently slides use
   11 × 5.5 in and standalone reports default to 9 × 6 in; the framework should
   unify these into a small set of named figure sizes.

4. **Color system alignment** — ensure the report palette is consistent with
   the Growth Lab design library (brand colors, product-space clusters,
   Atlas/Metroverse/Greenplexity palettes).

5. **Practical templates** — a reference Rmd/Quarto setup and a pandoc/Word
   reference document that implement the framework, so new reports start right.

## Design Inspirations

- **Foreign Affairs** — clean, authoritative layouts; strong typographic
  hierarchy; generous margins that let the text breathe
- **World Bank flagship reports** — professional data presentation; effective
  use of sidebars, call-out boxes, and structured figure placement
- **The Economist** — data-dense but highly readable; disciplined use of color;
  excellent chart typography
- **QJE (Quarterly Journal of Economics)** — academic rigor; clean, no-nonsense
  typesetting; well-integrated figures and tables

## Existing Assets

- **Growth Lab Design Library** (`growthlab.app/design-library`) — brand colors,
  visualization palettes, logos, flags. Downloaded to `design-library/`.
- **Pakistan FM meeting materials** (`~/dev/pakistan-explore/`) — a real-world
  example of GL slides and consolidated Rmd with `theme_gl()`, design tokens,
  and figure output conventions.
- **Source Sans 3** — GL's primary typeface (Google Fonts).
- **JetBrains Mono** — used for captions, axis labels, technical annotations.

## Constraints

- Final output is PDF (via Word/pandoc or direct LaTeX).
- Authors write in Markdown or Rmd/Quarto.
- Figures are generated in R (ggplot2) and saved as PNG at 300 DPI.
- References managed via Zotero → CSL/BibTeX.
- The framework must be simple enough that a researcher can follow it without
  design training.
