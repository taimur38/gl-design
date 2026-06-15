# Growth Lab Design System

A visual grammar for all Growth Lab outputs — reports, slides, briefs, charts,
web — codified as recipes (per-medium applications) and runnable tools
(R functions, pandoc filters, docx themes, Claude skills) so researchers can
absorb the system by using it, not by reading specifications.

See [`intention.md`](intention.md) for the why.

## Three layers

- **Grammar** ([`grammar.md`](grammar.md)) — medium-agnostic primitives:
  color, type stack, type scale ratio, role hierarchy, in-chart typography.
- **Recipes** ([`recipes/`](recipes/)) — applications of the grammar to a
  specific medium. Today: [`recipes/report.md`](recipes/report.md) (long-form
  Word/PDF). Slide / brief / standalone-chart recipes to come.
- **Assets** + **Skills** — the encoded, runnable form of grammar + recipe.

## Source of truth & propagation

Design values (colors, fonts, type scale, sizes) are **not** kept in sync
automatically — there is no generated tokens file. Consistency is maintained by
convention, so the authority order must be explicit. **Values flow downward;
they never flow back up.**

```
nil/            UPSTREAM INSPIRATION — Nil's original deliverables
                (data vis.html, typography-spec.html, *-rules.md).
                Read-only reference. We distill from it; we do not edit it,
                and it is not authoritative once distilled.
  ↓ distilled into
grammar.md      SOURCE OF TRUTH — the canonical, medium-agnostic values:
                color ramps + palettes, type stack, weights, type scale,
                in-chart conventions. If a value disagrees anywhere, grammar.md
                wins. Change a token HERE FIRST.
  ↓ applied per medium
recipes/        Medium APPLICATIONS — page geometry, grid, figure sizes, type
                sizes for one output (report.md, slide.md). May add medium-only
                values (margins, DPI) but must not contradict grammar.md.
  ↓ encoded as runnable form
DOWNSTREAM       Must MATCH grammar.md + the relevant recipe. Never a source.
ENCODINGS        When a grammar/recipe value changes, update every file below
                 that carries it, then re-render the playground to verify:

   skills/gl-ggplot/assets/theme_gl.R      — R: `gl` list, palettes, save_fig sizes, geom defaults
   skills/md2docx/assets/build_gl_template.py — Python constants → gl.docx / gl.dotx (note: deliberate
                                              px→pt + boolean-bold compromises, documented in-file)
   skills/md2pdf/assets/md2pdf-style.css   — CSS `:root` vars (shared by md2html)
   skills/md2pdf-minimal/assets/md2pdf-style.css
   skills/md2slides/assets/themes/gl.css   — Marp theme CSS
   showcase/framework-visual.html          — illustrative walkthrough (must look current)

playground/      DERIVED OUTPUTS — dogfood renders (demo-report.*, imgs/). Never
                 a source; regenerate from the above, don't hand-edit values.
```

**Auditing for drift (for LLMs):** treat `grammar.md` as ground truth. For each
color hex / font family / type size it defines, grep the downstream encodings
above and flag any that differ. A mismatch is a bug in the downstream file, not
in grammar.md — unless the downstream file documents a deliberate per-medium
compromise (as `build_gl_template.py` does for Word). `nil/` and `playground/`
are out of scope for drift checks: the former is upstream, the latter derived.

## Repo structure

```
nil/                  # Upstream inspiration — Nil's original spec deliverables
                      #   (data vis + typography HTML/MD). Read-only; not authoritative.
grammar.md            # SOURCE OF TRUTH — color, type, chart conventions
intention.md          # Purpose, problem, approach, inspirations
recipes/
  report.md           # Long-form report: page, grid, figure sizes, patterns
  slide.md            # 16:9 slide deck: canvas, type sizes, slide classes

assets/               # Static embodiments of grammar + recipe
  fonts/              # Source Serif 4 + Inter (local copies; legacy/ holds retired faces)
  design-library/     # GL brand assets: logos, flags, color palettes (CSV)

skills/               # Runnable, Claude-consumable tools
  gl-ggplot/          # GL design system for R/ggplot2 (theme, scales, sizes)
    assets/theme_gl.R   # Sourceable R file — the portable runtime
  md2docx/            # Markdown → Word conversion (pandoc + Lua filters)
    assets/templates/gl.docx       # GL Word reference doc (the live --theme gl)
    assets/templates/gl.dotx       # Template twin for manual Word users
    assets/build_gl_template.py    # Rebuilds gl.docx + gl.dotx from Nil tokens
  gl-docx-retheme/    # Convert an existing Word doc to the GL theme
                      #   (audit → transplant → judgment remaps → flags)
  md2pdf/             # Markdown → PDF via pandoc + headless Chromium
  md2html/            # Markdown → self-contained HTML (shares md2pdf assets)
  md2slides/          # Markdown → 16:9 PDF deck via Marp + gl theme
  chart-audit/        # Visual audit checklist for ggplot charts

showcase/             # Interactive presentations of the framework
  framework-visual.html # Walkthrough of the design system (open in browser)

playground/           # Working dogfood example
  demo-report.md      # Sample report (Pakistan FM brief) in markdown
  report.Rmd          # R Markdown version with embedded chart code
  render_report_charts.R  # Standalone R script to regenerate charts
  imgs/fm_meeting/    # Chart PNGs at recipe dimensions (300 DPI)
```

## ggplot conventions

Every R script that produces charts should start with:

```r
source("~/dev/gl-design/skills/gl-ggplot/assets/theme_gl.R")
gl_setup()
```

This loads fonts, sets `theme_gl(mode = "report")`, and configures default
color/fill palettes. See [`skills/gl-ggplot/SKILL.md`](skills/gl-ggplot/SKILL.md)
for full usage.

Key rules:

- **Two-family stack**: Source Serif 4 (voice) + Inter (function). Never
  monospace — neither JetBrains Mono nor any `family = "mono"` fallback.
- **Do not override the theme per chart** — only adjust `legend.position` or
  `guides()` when needed.
- **Highlight by muting**: untyped geoms default to muted grey, so the
  pattern is *overpainting* the focus series on top in `highlight` (main blue
  `#2F87C8`, = `c_1`). Fills and lines use the main tone; a highlighted point
  is `fill = highlight, color = highlight_dark` and its label uses
  `highlight_dark` (`#1A5A8E`). For stark "lead finding" emphasis use
  `lead_finding` (red `#CC4948`, = `c_2`) sparingly. Never use `"red"`,
  `accent`, or arbitrary hex for emphasis.
- **Highlighted points are painted once**: lines and bars are opaque, so the
  overpaint pattern is fine — but the `geom_point` default carries `alpha = 0.8`,
  which dilutes a highlight dot (through its own transparency and the grey dot
  beneath). So exclude the focus from the muted backdrop and draw it a single
  time at `alpha = 1`: `geom_point(data = \(d) filter(d, !focus), alpha = 0.3)`
  then `geom_point(data = \(d) filter(d, focus), fill = highlight, color = highlight_dark, alpha = 1)`.
- **Dark tone for text**: every direct label, legend mark, callout, or
  annotation tied to a series uses the series' dark tone (`gl$c_N_dark`),
  not the main tone — WCAG AA against paper.
- **Color scales**: default 6-color palette applies automatically; use
  `scale_color_gl("hs_sectors")` / `scale_fill_gl("hs_sectors")` for named
  external palettes; `scale_color_gl_gradient("sequential_1")` for
  continuous (choropleth) data.
- **Figure sizes**: use `save_fig("full", "filename.png")` with named sizes:
  `full`, `full_tall`, `full_square`, `major`, `half`, `half_tall`, `slide`
  (sizes defined in [`recipes/report.md`](recipes/report.md)).
- **Log scale**: use `scale_x_log10()` when GDP per capita is on the x-axis.
- **Mode**: `gl_setup()` defaults to report mode (suppresses title / subtitle
  / caption). Use `gl_setup(mode = "slide")` for standalone charts.
- **Legend**: report mode defaults to bottom-left. Override to
  `legend.position = "right"` only for charts with >6 categories. Use
  `guide_legend(nrow = 2)` if bottom labels clip.
- **Chart audit**: after generating charts, run the
  [`skills/chart-audit/`](skills/chart-audit/) checklist.

## Converting markdown

Four pipelines, all sharing the same design tokens and cover assets:

```bash
skills/md2docx/scripts/md2docx --theme gl input.md output.docx   # Word
skills/md2pdf/scripts/md2pdf input.md output.pdf                  # PDF (print)
skills/md2html/scripts/md2html input.md output.html               # self-contained HTML
skills/md2slides/scripts/md2slides input.md output.pdf            # 16:9 slide deck (Marp)
```

The docx, pdf, and html paths use pandoc; md2slides uses Marp. All require
`pandoc` + `pandoc-crossref` (except md2slides, which needs Node + the Marp
CLI). See each skill's `SKILL.md` for full usage.

## Regenerating charts

From the `pakistan-explore` working directory:

```bash
cd ~/dev/pakistan-explore
Rscript ~/dev/gl-design/playground/render_report_charts.R
```

This reads the macro parquet data and writes all PNGs to
`playground/imgs/fm_meeting/`.
