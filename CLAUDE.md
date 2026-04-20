# Growth Lab Report Design Framework

A design system for Growth Lab research publications: grid, typography, figure sizing, color, and spacing — all derived from a small set of root decisions.

## Repo structure

```
framework.md          # Complete design specification (the source of truth)
intention.md          # Goals, constraints, and design inspirations
build_gl_template.py  # Builds the Word reference doc (gl-report.docx) from spec
gl-report.docx        # Word template for pandoc (built by script above)

design-library/       # Brand assets: logos, flags, color palettes (CSV)
playground/           # Working example: Pakistan FM brief
  demo-report.md      # Sample report in markdown
  report.Rmd          # R Markdown version with embedded chart code
  render_report_charts.R  # Standalone R script to regenerate all charts
  imgs/fm_meeting/    # Chart PNGs at framework dimensions (300 DPI)

skills/
  md2docx/            # Markdown → Word conversion skill (pandoc + Lua filters)
  chart-audit/        # Visual audit checklist for ggplot charts against framework
  gl-ggplot/          # Skill: GL design system for R/ggplot2 (theme, scales, sizes)
    assets/theme_gl.R  # Sourceable R file — the portable runtime

# Visual explainers (open in browser)
framework-visual.html           # Interactive walkthrough of the design system
framework-visual-a-serif.html   # Typography variant: Source Serif 4
framework-visual-b-editorial.html # Typography variant: Crimson Pro headings
framework-visual-c-hybrid.html  # Typography variant: Literata + IBM Plex Mono
font-comparison.html            # Side-by-side font switcher on the sample report
framework-deck.md               # Slide deck version (Marp markdown)
```

## Key design tokens

All values are defined in `framework.md`. Quick reference:

- **Page**: US Letter, 1.0" margins all sides, 6.5 × 9.0" live area
- **Grid**: 6 columns × 0.944" + 5 gutters × 0.167"
- **Fonts**: Source Sans 3 (body/headings) + JetBrains Mono (captions/data)
- **Body**: 11pt / 15pt leading (1.36 line height)
- **Type scale**: ×1.25 major third → 11 → 14 → 17 → 21.5pt
- **Colors**: text `#333333`, muted `#7c7c7c`, border `#dcdcdc`, bg `#f3f3f3`, brand `#266798`, highlight `#C64646`
- **Categorical palette**: `#266798 #C64646 #36B250 #EAC218 #D1852A #52E2DE #A42DE2 #7C6760 #757777`

## ggplot conventions

Every R script that produces charts should start with:

```r
source("~/dev/gl-design/skills/gl-ggplot/assets/theme_gl.R")
gl_setup()
```

This loads fonts, sets `theme_gl(mode = "report")`, and configures default color/fill palettes. See `skills/gl-ggplot/SKILL.md` for full usage guide.

Key rules (the skill has the complete reference):

- **Do not override the theme per chart** — only adjust `legend.position` or `guides()` when needed
- **Highlight color**: always use `highlight` variable (`#C64646`), never `"red"`
- **Highlighted elements**: paint the geom twice — once for all data, once filtered with `color = highlight` and larger `size`
- **Color scales**: default palette applies automatically; use `scale_color_gl("hs_sectors")` / `scale_fill_gl("hs_sectors")` for named palettes
- **Figure sizes**: use `save_fig("full", "filename.png")` with named sizes: `full`, `full_tall`, `full_square`, `major`, `half`, `half_tall`, `slide`
- **Log scale**: use `scale_x_log10()` when GDP per capita is on the x-axis
- **Mode**: `gl_setup()` defaults to report mode (suppresses title/subtitle/caption). Use `gl_setup(mode = "slide")` for standalone charts.
- **Legend**: report mode defaults to bottom-left. Override to `legend.position = "right"` only for charts with >8 categories. Use `guide_legend(nrow = 2)` if bottom labels clip.
- **Chart audit**: after generating charts, run the `skills/chart-audit/` checklist to catch visual issues

## Converting markdown to Word

Use the bundled md2docx skill:

```bash
skills/md2docx/scripts/md2docx --theme gl input.md output.docx
```

Requires `pandoc` and `pandoc-crossref`. See `skills/md2docx/SKILL.md` for full usage.

## Building the slide deck

Requires the `md2slides` tool (Marp-based):

```bash
md2slides framework-deck.md framework-deck.pdf
```

## Regenerating charts

From the `pakistan-explore` working directory:

```bash
cd ~/dev/pakistan-explore
Rscript ~/dev/gl-design/playground/render_report_charts.R
```

This reads the macro parquet data and writes all PNGs to `playground/imgs/fm_meeting/`.
