---
name: gl-ggplot
description: Apply the Growth Lab design system to ggplot2 charts. Use this skill when creating R/ggplot visualizations in any project to ensure they follow GL visual standards — colors, typography, sizing, and save conventions.
compatibility: Requires R with ggplot2, ggthemes, sysfonts, showtext.
metadata:
  author: taimur-shah
  version: "2.0"
---

# GL ggplot Design System

This skill tells you how to produce ggplot2 charts that follow the Growth Lab
visual grammar (Source Serif 4 + Inter; 4-layer warm ink ramp; mute-then-highlight).

## Setup

At the top of every R script or Rmd file that produces charts, add:

```r
source("~/dev/gl-design/skills/gl-ggplot/assets/theme_gl.R")
gl_setup()                          # report mode (default) — no title/subtitle/caption
gl_setup(mode = "slide")            # slide mode — keeps title/subtitle/caption
```

This loads fonts (**Source Serif 4** + **Inter** via Google Fonts), sets the
theme globally, and configures the default discrete color/fill palette. You
do **not** need to call `theme_set()` or set `ggplot2.discrete.colour`
yourself — `gl_setup()` handles it.

## What `gl_setup()` provides

After calling `gl_setup()`, the following are available:

| Object | What it is |
|--------|-----------|
| `gl` | Full list of design tokens — see below |
| `highlight` | `gl$c_2` (`#C77A20`) — the amber highlight / lead-finding accent |
| `c_muted` | `gl$c_muted` (`#7E8A99`) — "everyone-else" gray for de-emphasis |
| `accent` | `gl$accent` (`#015C9C`) — primary blue |
| `highlight_sz` | Standard line width for highlighted geoms (`1.8`) |
| `theme_gl()` | The theme function (already applied via `theme_set`) |
| `scale_color_gl()` | Discrete color scale using GL palettes |
| `scale_fill_gl()` | Discrete fill scale using GL palettes |
| `gl_palettes` | Named list of all available palettes |
| `gl_fig` | Named figure sizes for `save_fig()` |
| `save_fig()` | Save at a named size to `imgs/` at 300 DPI |

### Tokens in `gl`

| Token        | Hex       | Use                                                   |
|--------------|-----------|-------------------------------------------------------|
| `gl$ink`     | `#1A1714` | Headings, strong emphasis                             |
| `gl$ink_2`   | `#2C2823` | Body, axis text, table cells                          |
| `gl$ink_3`   | `#6B645A` | Captions, eyebrows, chrome                            |
| `gl$ink_4`   | `#9A9389` | Hairlines, secondary markers                          |
| `gl$accent`  | `#015C9C` | Primary chart series, eyebrows, links                 |
| `gl$c_1`..`gl$c_6` | (palette) | Individual categorical colors                  |
| `gl$c_muted` | `#7E8A99` | "Everyone else" gray for the mute-then-highlight move |

## Core rules

### 1. Do not override the theme per chart

The theme is set globally. Do **not** add `+ theme_gl()` or `+ theme_minimal()`
to individual plots. The only per-chart theme adjustments allowed are:

- `legend.position = "right"` (when >6 categories — more than the default palette)
- `guides(color = guide_legend(nrow = 2))` (when bottom legend clips)

### 2. Highlight with the mute-then-paint technique

The canonical Growth Lab chart move: paint **every** series in `c_muted`
first, then re-paint the focus series on top in `highlight` (amber) or
`accent` (blue). The muted layer carries the trend; the highlight carries
the finding. Never use `"red"` or arbitrary colors for emphasis.

```r
data |>
    ggplot(aes(x = year, y = value, group = country)) +
    geom_line(color = c_muted, linewidth = 0.6) +
    geom_line(data = \(d) filter(d, country == focus),
              color = highlight, linewidth = highlight_sz)
```

This works with any geom: `geom_point`, `geom_col`, `geom_bar`, `geom_text`, etc.

Use `highlight` (amber `#C77A20`) when the focus *is* the finding. Use
`accent` (blue `#015C9C`) when the focus is the lab's primary subject
(institutional voice).

### 3. Use the default palette by doing nothing

`gl_setup()` sets the default discrete colour and fill scales to the GL
6-color categorical palette. For most charts, you don't need any scale call
at all — just map to `color` or `fill`.

```r
# This just works — no scale_color_* needed
data |>
    ggplot(aes(x = year, y = exports, color = sector)) +
    geom_line()
```

The 6-color palette is deliberately small. If you have 7+ categories,
consider whether mute-then-highlight would tell the story better than seven
distinct colors.

### 4. Use `scale_color_gl()` / `scale_fill_gl()` for named palettes

When you need a specific named palette (e.g., Atlas HS sector colors), use:

```r
data |>
    ggplot(aes(x = year, y = rca, fill = sector)) +
    geom_col() +
    scale_fill_gl("hs_sectors")
```

Available palettes:

| Name | Colors | Use case |
|------|--------|----------|
| `"categorical"` | 6 | Default. General purpose. Used automatically. |
| `"hs_sectors"` | 11 | Atlas HS product sectors (named) — external standard |
| `"sitc_sectors"` | 11 | Atlas SITC product sectors (named) — external standard |
| `"product_space"` | 8 | Product space clusters (named) — external standard |

The sector and product-space palettes are external Growth Lab standards
that coexist with the categorical grammar. Use them whenever the chart is
about that specific data taxonomy.

For named palettes, the values are matched by name — your data's factor
levels must match the palette names (e.g., "Agriculture", "Metals").

### 5. Save figures at named sizes

Always use `save_fig()` with a named size:

```r
save_fig("full", "exports-timeseries.png")
save_fig("full_tall", "faceted-sectors.png")
save_fig("half", "small-sidebar-chart.png")
```

| Size | Dimensions | Use |
|------|-----------|-----|
| `full` | 6.5 × 4.0" | Standard full-width chart |
| `full_tall` | 6.5 × 6.0" | Faceted or vertically stacked |
| `full_square` | 6.5 × 6.5" | Square charts (scatter, network) |
| `major` | 4.278 × 4.0" | 4-column chart alongside text |
| `half` | 3.167 × 3.0" | Side-by-side pair |
| `half_tall` | 3.167 × 5.0" | Tall narrow chart |
| `slide` | 10 × 5.625" | 16:9 slide deck (Marp, PowerPoint) |

### 6. Log scale for GDP per capita

When GDP per capita is on the x-axis, always use `scale_x_log10()`.

### 7. Report vs slide mode

- **Report mode** (`gl_setup()` or `gl_setup(mode = "report")`): the chart's
  plot.title, plot.subtitle, and plot.caption are suppressed — the
  document handles the figure label, chart title, subtitle, and source via
  Word styles. Legend defaults to bottom-left.
- **Slide mode** (`gl_setup(mode = "slide")`): plot.title (Source Serif 4
  14pt), plot.subtitle (Inter 12pt), and plot.caption (Source Serif 4
  italic 10pt) all render inside the chart. Use for standalone charts or
  presentations.

## Complete example

```r
source("~/dev/gl-design/skills/gl-ggplot/assets/theme_gl.R")
gl_setup()

library(dplyr)

focus_country <- "Mongolia"

trade_data |>
    ggplot(aes(x = year, y = export_value, group = country)) +
    geom_line(color = c_muted, linewidth = 0.6) +
    geom_line(data = \(d) filter(d, country == focus_country),
              color = highlight, linewidth = highlight_sz) +
    scale_y_continuous(labels = scales::dollar) +
    labs(x = NULL, y = "Export value")

save_fig("full", "mongolia-exports-vs-peers.png")
```

## Accessing raw palette vectors

If you need the color vectors directly:

```r
gl_palettes$categorical      # 6-color unnamed vector
gl_palettes$hs_sectors       # named vector: "Agriculture" = "#e5c21a", ...
gl$accent                    # "#015C9C"
gl$c_muted                   # "#7E8A99"
gl$ink                       # "#1A1714"
```

## Checklist before finalizing charts

- [ ] `gl_setup()` called at top of script
- [ ] No per-chart theme overrides (except legend position)
- [ ] No monospace anywhere (no JetBrains Mono, no `font.family = "mono"`)
- [ ] Highlights use `highlight` (amber) or `accent` (blue), not `"red"`
- [ ] Highlights use mute-then-paint — supporting data is `c_muted`
- [ ] Most charts have 2–4 colors; bigger palettes use the muted base
- [ ] Figures saved with `save_fig()` at named sizes
- [ ] GDP per capita axes use `scale_x_log10()`
- [ ] Legend fits without clipping (use `nrow = 2` or `position = "right"` if needed)
