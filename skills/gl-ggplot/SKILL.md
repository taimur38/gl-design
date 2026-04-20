---
name: gl-ggplot
description: Apply the Growth Lab design system to ggplot2 charts. Use this skill when creating R/ggplot visualizations in any project to ensure they follow GL visual standards — colors, typography, sizing, and save conventions.
compatibility: Requires R with ggplot2, ggthemes, sysfonts, showtext.
metadata:
  author: taimur-shah
  version: "1.0"
---

# GL ggplot Design System

This skill tells you how to produce ggplot2 charts that follow the Growth Lab design framework.

## Setup

At the top of every R script or Rmd file that produces charts, add:

```r
source("~/dev/gl-design/skills/gl-ggplot/assets/theme_gl.R")
gl_setup()                          # report mode (default) — no title/subtitle/caption
gl_setup(mode = "slide")            # slide mode — keeps title/subtitle/caption
```

This loads fonts (Source Sans 3 + JetBrains Mono), sets the theme globally, and configures the default discrete color/fill palette. You do **not** need to call `theme_set()` or set `ggplot2.discrete.colour` yourself — `gl_setup()` handles it.

## What `gl_setup()` provides

After calling `gl_setup()`, the following are available:

| Object | What it is |
|--------|-----------|
| `gl` | List of design tokens: `gl$text_dark`, `gl$text_muted`, `gl$border`, `gl$background`, `gl$brand_blue`, `gl$highlight`, `gl$palette` |
| `highlight` | Shortcut for `gl$highlight` (`#C64646`) — the standard emphasis color |
| `highlight_sz` | Standard larger size for highlighted elements (`1.1`) |
| `theme_gl()` | The theme function (already applied via `theme_set`) |
| `scale_color_gl()` | Discrete color scale using GL palettes |
| `scale_fill_gl()` | Discrete fill scale using GL palettes |
| `gl_palettes` | Named list of all available palettes |
| `gl_fig` | Named figure sizes for `save_fig()` |
| `save_fig()` | Save at a named size to `imgs/` at 300 DPI |

## Core rules

### 1. Do not override the theme per chart

The theme is set globally. Do **not** add `+ theme_gl()` or `+ theme_minimal()` to individual plots. The only per-chart theme adjustments allowed are:

- `legend.position = "right"` (when >8 categories)
- `guides(color = guide_legend(nrow = 2))` (when bottom legend clips)

### 2. Highlight with the double-paint technique

Never use `"red"` or arbitrary colors for emphasis. Always use the `highlight` variable and paint the geom twice:

```r
data |>
    ggplot(aes(x = year, y = value, group = country)) +
    geom_line() +
    geom_line(data = \(d) filter(d, country == focus),
              color = highlight, linewidth = highlight_sz)
```

This works with any geom: `geom_point`, `geom_col`, `geom_bar`, `geom_text`, etc.

### 3. Use the default palette by doing nothing

`gl_setup()` sets the default discrete colour and fill scales to the GL 9-color palette. For most charts, you don't need any scale call at all — just map to `color` or `fill` and the palette applies automatically.

```r
# This just works — no scale_color_* needed
data |>
    ggplot(aes(x = year, y = exports, color = sector)) +
    geom_line()
```

### 4. Use `scale_color_gl()` / `scale_fill_gl()` for named palettes

When you need a specific named palette (e.g., Atlas HS sector colors), use the scale functions:

```r
# HS product sector colors (named, so legend order doesn't matter)
data |>
    ggplot(aes(x = year, y = rca, fill = sector)) +
    geom_col() +
    scale_fill_gl("hs_sectors")
```

Available palettes:

| Name | Colors | Use case |
|------|--------|----------|
| `"categorical"` | 9 | Default. General purpose. Used automatically. |
| `"hs_sectors"` | 11 | Atlas HS product sectors (named) |
| `"sitc_sectors"` | 11 | Atlas SITC product sectors (named) |
| `"product_space"` | 8 | Product space clusters (named) |
| `"brand"` | 4 | Growth Lab brand colors |

For named palettes, the values are matched by name, so your data's factor levels must match the palette names (e.g., "Agriculture", "Metals", "Electronics").

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

- **Report mode** (`gl_setup()` or `gl_setup(mode = "report")`): title, subtitle, and caption are suppressed (the Word/PDF document provides them). Legend defaults to bottom-left.
- **Slide mode** (`gl_setup(mode = "slide")`): title, subtitle, and caption render normally. Use for standalone charts or presentations.

## Complete example

```r
source("~/dev/gl-design/skills/gl-ggplot/assets/theme_gl.R")
gl_setup()

library(dplyr)

focus_country <- "Pakistan"

trade_data |>
    ggplot(aes(x = year, y = export_value, color = sector)) +
    geom_line() +
    geom_line(data = \(d) filter(d, sector == "Textiles"),
              color = highlight, linewidth = highlight_sz) +
    scale_color_gl("hs_sectors") +
    scale_y_continuous(labels = scales::dollar) +
    labs(x = NULL, y = "Export value")

save_fig("full", "pakistan-exports-by-sector.png")
```

## Accessing raw palette vectors

If you need the color vectors directly (e.g., for non-ggplot use or custom scales):

```r
gl_palettes$categorical      # unnamed character vector of 9 colors
gl_palettes$hs_sectors       # named vector: "Agriculture" = "#e5c21a", ...
gl$highlight                 # "#C64646"
gl$brand_blue                # "#266798"
```

## Checklist before finalizing charts

- [ ] `gl_setup()` called at top of script
- [ ] No per-chart theme overrides (except legend position)
- [ ] Highlights use `highlight` variable, not `"red"`
- [ ] Highlights use double-paint technique
- [ ] Figures saved with `save_fig()` at named sizes
- [ ] GDP per capita axes use `scale_x_log10()`
- [ ] Legend fits without clipping (use `nrow = 2` or `position = "right"` if needed)
