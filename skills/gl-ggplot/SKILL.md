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
visual grammar (Source Serif 4 + Inter; 4-layer warm ink ramp; categorical
palette with light/main/dark tones; mute-then-highlight).

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
| `highlight` | `gl$accent` (`#1A5A8E`) — blue popout, the default focus color |
| `accent` | `gl$accent` (`#1A5A8E`) — same hex as `highlight`; used for non-data UI (eyebrows, figure labels, links) |
| `lead_finding` | `gl$c_2` (`#CC4948`) — red, for stark / lead-finding emphasis (sparingly) |
| `c_muted` | `gl$c_muted` (`#999FA8`) — "everyone-else" gray for de-emphasis |
| `highlight_sz` | Standard line width for highlighted geoms (`1.8`) |
| `theme_gl()` | The theme function (already applied via `theme_set`) |
| `scale_color_gl()` | Discrete color scale using GL palettes |
| `scale_fill_gl()` | Discrete fill scale using GL palettes |
| `scale_color_gl_gradient()` | Continuous color scale (sequential / diverging) |
| `scale_fill_gl_gradient()` | Continuous fill scale (sequential / diverging) |
| `gl_palettes` | Named list of all available palettes |
| `gl_fig` | Named figure sizes for `save_fig()` |
| `save_fig()` | Save at a named size to `imgs/` at 300 DPI |

### Tokens in `gl`

| Token        | Hex       | Use                                                   |
|--------------|-----------|-------------------------------------------------------|
| `gl$ink`     | `#1A1714` | Headings, strong emphasis                             |
| `gl$ink_2`   | `#2C2823` | Body, axis text, table cells, axis lines / ticks      |
| `gl$ink_3`   | `#4F4A42` | Captions, eyebrows, chrome, chart subtitles           |
| `gl$ink_4`   | `#9A9389` | In-chart faint markers, sparse trendlines             |
| `gl$accent`  | `#1A5A8E` | Eyebrows, figure labels, links — = `gl$c_1_dark`      |
| `gl$gridline`| `#ECE9E2` | In-chart major gridlines                              |
| `gl$c_1`..`gl$c_6` | (palette) | Categorical main tones (fills)                 |
| `gl$c_1_dark`..`gl$c_6_dark` | (palette) | Dark tones — strokes + labels         |
| `gl$c_1_light`..`gl$c_6_light` | (palette) | Light tones — backgrounds, faded    |
| `gl$c_muted` | `#999FA8` | "Everyone else" gray for the mute-then-highlight move |
| `gl$c_muted_dark` | `#5F6773` | Strokes / labels for muted series                |

## Core rules

### 1. Do not override the theme per chart

The theme is set globally. Do **not** add `+ theme_gl()` or `+ theme_minimal()`
to individual plots. The only per-chart theme adjustments allowed are:

- `legend.position = "right"` (when >6 categories — more than the default palette)
- `guides(color = guide_legend(nrow = 2))` (when bottom legend clips)

### 2. Highlight with the mute-then-paint technique

The canonical Growth Lab chart move: untyped geoms are already muted (see
rule 3), so the pattern collapses to *overpainting the focus*. The muted
layer carries the trend; the highlight carries the finding. Never use
`"red"` or arbitrary hex for emphasis.

```r
data |>
    ggplot(aes(x = year, y = value, group = country)) +
    geom_line() +                                          # muted, default
    geom_line(data = \(d) filter(d, country == focus),
              color = highlight, linewidth = highlight_sz)
```

This works with any geom: `geom_point`, `geom_col`, `geom_bar`, `geom_text`, etc.

**Layer order matters: highlights go LAST.** ggplot draws geoms in the
order you add them, so the last layer sits on top. If you mix a muted
backdrop, a trend line, and a highlighted point, the highlight call must
come *after* `geom_smooth`/`stat_smooth`, otherwise the smooth ribbon will
occlude the focus dot.

```r
ggplot(data, aes(x, y)) +
    geom_point(alpha = 0.3) +                              # 1. muted backdrop
    geom_smooth() +                                        # 2. trend
    geom_point(data = filter(., focus),                    # 3. highlight on top
               color = highlight, size = 3) +
    geom_text_repel(data = filter(., focus),               # 4. label on top of dot
                    aes(label = name), color = highlight)
```

Use `highlight` (blue `#1A5A8E` = `accent`) for the default focus — the
institutional voice. Use `lead_finding` (red `#CC4948` = `c_2`) when the
finding is stark — gains vs. losses, alarm, exception. Use sparingly.

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

**Untyped geoms default to muted, not a saturated color** — this is the
GL popout pattern: paint everyone in `c_muted` first (no aesthetic mapping
needed), then re-paint the focus series in `highlight` or `accent`.
Authors opt *in* to color, never out of it.

```r
data |>
    ggplot(aes(x = country, y = value)) +
    geom_col() +                                  # all bars c_muted grey
    geom_col(data = \(d) filter(d, focus),
             fill = highlight)                    # focus bar red
```

After `gl_setup()` the relevant defaults are:

| Geom | Default |
|------|---------|
| `geom_line` / `geom_path` / `geom_step` / `geom_point` | colour = `c_muted_dark` |
| `geom_col` / `geom_bar` / `geom_area` | fill = `c_muted` (lighter — "backdrop") |
| `geom_smooth` | line `c_muted_dark`, ribbon `c_muted_light` |
| `geom_ribbon` | fill = `c_muted_light`, alpha 0.5 |
| `geom_boxplot` | white fill, `c_muted_dark` stroke |
| `geom_hline` / `geom_vline` | dashed `ink_3` (reference line) |
| `geom_text` / `geom_label` | `ink_2`, sans family |

The line/point grey is *darker* than the bar grey because lines and points
read as "the data" — a single-series time series should feel substantive.
Bars are typically a row of comparators where one will be highlighted, so
they sit on a softer backdrop. For an institutional-voice single-series
chart where the line should be blue, override: `geom_line(color = accent)`.

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
| `"sequential_1"`..`"sequential_6"` | 5 each | Single-hue ramp low → high (one per c-N) |
| `"diverging_2_1"` | 6 | Red ↔ blue, midpoint-centered (default diverging) |
| `"diverging_3_1"` | 6 | Teal ↔ blue |
| `"diverging_5_1"` | 6 | Orange ↔ blue |
| `"diverging_6_1"` | 6 | Yellow ↔ blue |
| `"hs_sectors"` | 11 | Atlas HS product sectors (named) — external standard |
| `"sitc_sectors"` | 11 | Atlas SITC product sectors (named) — external standard |
| `"product_space"` | 8 | Product space clusters (named) — external standard |

The sector and product-space palettes are external Growth Lab standards
that coexist with the categorical grammar. Use them whenever the chart is
about that specific data taxonomy.

For named palettes, the values are matched by name — your data's factor
levels must match the palette names (e.g., "Agriculture", "Metals").

**Sequential vs. diverging:**

- Use **sequential** for any ordered encoding without a natural midpoint
  (population, GDP, complexity, count). Darker = higher.
- Use **diverging** *only* when the data has a real reference point — gains
  vs. losses, above vs. below baseline. Never on a purely positive scale.

For continuous data (e.g. choropleth fill), use `*_gl_gradient()`:

```r
states |>
    ggplot(aes(geometry = geom, fill = gdp_per_cap)) +
    geom_sf() +
    scale_fill_gl_gradient("sequential_1")
```

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

### 7. Three tones, three jobs

Each `c-N` hue has light / main / dark variants. They are not
interchangeable:

- **Main** (`gl$c_1`, `gl$c_2`, ...) — fills (bars, lines, treemap tiles,
  scatter circles, choropleth polygons).
- **Dark** (`gl$c_1_dark`, ...) — strokes on overlapping marks, and every
  text element tied to the series: direct labels, legend marks, callouts,
  annotations. Required for WCAG AA contrast against paper. **Do not use
  the main tone for text** — it fails contrast.
- **Light** (`gl$c_1_light`, ...) — backgrounds, faded states, the lighter
  end of a sequential ramp.

The only place dark is used as a *fill* is the three-tone stacked area
(light / main / dark of one hue, when three bands belong to the same parent
variable).

### 8. Opacity on overlapping marks

When marks can overlap, set both fill and stroke opacity to 0.8 — overlapping
points then darken together rather than washing out.

```r
ggplot(data, aes(x, y, color = group, fill = group)) +
    geom_point(shape = 21, size = 3, alpha = 0.8, stroke = 0.6)
```

Single-layer marks (bars, treemap tiles, choropleths) stay at full opacity —
overlap isn't a risk and lowering opacity just dilutes the color.

Radar polygons are the exception: fill at 0.25 so gridlines and labels read
through the polygon.

### 9. Report vs slide mode

- **Report mode** (`gl_setup()` or `gl_setup(mode = "report")`): the chart's
  plot.title, plot.subtitle, and plot.caption are suppressed — the
  document handles the figure label, chart title, subtitle, and source via
  Word styles. Legend defaults to bottom-left.
- **Slide mode** (`gl_setup(mode = "slide")`): plot.title (Source Serif 4
  14pt), plot.subtitle (Inter 12pt), and plot.caption (Source Serif 4
  italic 12pt) all render inside the chart. Use for standalone charts or
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
gl_palettes$categorical          # 6-color unnamed vector
gl_palettes$sequential_1         # 5-color blue ramp, low → high
gl_palettes$diverging_2_1        # 6-color red ↔ blue
gl_palettes$hs_sectors           # named: "Agriculture" = "#e5c21a", ...
gl$accent                        # "#1A5A8E"  (= gl$c_1_dark, = highlight)
gl$c_muted                       # "#999FA8"  (muted bars / "everyone else")
gl$c_muted_dark                  # "#5F6773"  (lines, points, boxplot strokes)
gl$c_1                           # "#2F87C8"  (main tone)
gl$c_2                           # "#CC4948"  (= lead_finding red)
gl$ink                           # "#1A1714"
```

## Checklist before finalizing charts

- [ ] `gl_setup()` called at top of script
- [ ] No per-chart theme overrides (except legend position)
- [ ] No monospace anywhere (no JetBrains Mono, no `font.family = "mono"`)
- [ ] Highlights use `highlight` (blue) or `lead_finding` (red), not `"red"` or arbitrary hex
- [ ] Highlights use mute-then-paint — supporting data is `c_muted`
- [ ] Most charts have 2–4 colors; bigger palettes use the muted base
- [ ] Series labels / direct annotations use the **dark tone** (`c_N_dark`),
      not the main tone — WCAG AA contrast
- [ ] Overlapping marks (scatter, radar) use 0.8 fill+stroke opacity
- [ ] Sequential ramp for ordered values; diverging only with a real midpoint
- [ ] Figures saved with `save_fig()` at named sizes
- [ ] GDP per capita axes use `scale_x_log10()`
- [ ] Legend fits without clipping (use `nrow = 2` or `position = "right"` if needed)
