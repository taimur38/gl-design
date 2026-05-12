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

## Repo structure

```
grammar.md            # Visual grammar — color, type, chart conventions
intention.md          # Purpose, problem, approach, inspirations
recipes/
  report.md           # Long-form report: page, grid, figure sizes, patterns

assets/               # Static embodiments of grammar + recipe
  fonts/              # Source Sans 3 + JetBrains Mono (local copies)
  design-library/     # GL brand assets: logos, flags, color palettes (CSV)
  gl-report.docx      # Word reference doc for pandoc
  build_gl_template.py  # Builds gl-report.docx from the md2docx base template

skills/               # Runnable, Claude-consumable tools
  gl-ggplot/          # GL design system for R/ggplot2 (theme, scales, sizes)
    assets/theme_gl.R   # Sourceable R file — the portable runtime
  md2docx/            # Markdown → Word conversion (pandoc + Lua filters)
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

- **Do not override the theme per chart** — only adjust `legend.position` or
  `guides()` when needed.
- **Highlight color**: always use `highlight` variable (`#C64646`), never
  `"red"`.
- **Highlighted elements**: paint the geom twice — once for all data, once
  filtered with `color = highlight` and larger `size`.
- **Color scales**: default palette applies automatically; use
  `scale_color_gl("hs_sectors")` / `scale_fill_gl("hs_sectors")` for named
  palettes.
- **Figure sizes**: use `save_fig("full", "filename.png")` with named sizes:
  `full`, `full_tall`, `full_square`, `major`, `half`, `half_tall`, `slide`
  (sizes defined in [`recipes/report.md`](recipes/report.md)).
- **Log scale**: use `scale_x_log10()` when GDP per capita is on the x-axis.
- **Mode**: `gl_setup()` defaults to report mode (suppresses title / subtitle
  / caption). Use `gl_setup(mode = "slide")` for standalone charts.
- **Legend**: report mode defaults to bottom-left. Override to
  `legend.position = "right"` only for charts with >8 categories. Use
  `guide_legend(nrow = 2)` if bottom labels clip.
- **Chart audit**: after generating charts, run the
  [`skills/chart-audit/`](skills/chart-audit/) checklist.

## Converting markdown to Word

Use the bundled md2docx skill:

```bash
skills/md2docx/scripts/md2docx --theme gl input.md output.docx
```

Requires `pandoc` and `pandoc-crossref`. See
[`skills/md2docx/SKILL.md`](skills/md2docx/SKILL.md) for full usage.

## Regenerating charts

From the `pakistan-explore` working directory:

```bash
cd ~/dev/pakistan-explore
Rscript ~/dev/gl-design/playground/render_report_charts.R
```

This reads the macro parquet data and writes all PNGs to
`playground/imgs/fm_meeting/`.
