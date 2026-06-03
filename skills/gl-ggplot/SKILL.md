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
| `highlight` | `gl$c_1` (`#2F87C8`) — main blue, the default data focus: bar/area/point **fills** and highlighted **lines** |
| `highlight_dark` | `gl$c_1_dark` (`#1A5A8E`) — the **stroke** on a highlighted point and the **text/label** tied to the highlight (WCAG AA) |
| `lead_finding` | `gl$c_2` (`#CC4948`) — main red, for stark / lead-finding emphasis (sparingly) |
| `lead_finding_dark` | `gl$c_2_dark` (`#8A2C2B`) — stroke/label for the lead-finding mark |
| `accent` | `gl$accent` (`#1A5A8E`) — **non-data UI chrome only** (eyebrows, figure labels, links). Do **not** use as a data-mark fill — that is the typography↔data-viz mix-up to avoid |
| `c_muted` | `gl$c_muted` (`#999FA8`) — "everyone-else" gray for de-emphasis |
| `highlight_sz` | `linewidth` for the highlighted focus line (`0.65`, ~2.4px). Standard/muted lines default to `0.5` (~2px) — the focus is only ~1.3× thicker, per spec §5 (not a 2× jump) |
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
    geom_point(data = \(d) filter(d, !focus), alpha = 0.3) + # 1. muted backdrop, focus EXCLUDED
    geom_smooth() +                                        # 2. trend
    geom_point(data = \(d) filter(d, focus),               # 3. highlight, painted ONCE —
               fill = highlight, color = highlight_dark,   #    main fill + dark stroke
               alpha = 1, size = 3) +                       #    alpha = 1, no grey underneath
    geom_text_repel(data = \(d) filter(d, focus),          # 4. label uses the dark tone
                    aes(label = name), color = highlight_dark)
```

**Why exclude the focus from the backdrop?** The `geom_point` default carries
`alpha = 0.8` so dense clouds darken on overlap instead of washing out. But that
opacity is poison for a highlight: if you leave the focus row in the muted
backdrop *and* overpaint it, the highlight dot (a) shows the panel through its own
0.8 alpha and (b) sits on top of a grey dot — the blue comes out muddy and
desaturated. So a highlighted point is **painted once**: filter the focus *out* of
the backdrop layer, then draw it a single time at `alpha = 1`. (Lines and bars are
opaque, so they can stay one-line overpaints — this only bites `geom_point`.)

Use `highlight` (main blue `#2F87C8` = `c_1`) for the default focus — the
institutional voice. Use `lead_finding` (main red `#CC4948` = `c_2`) when the
finding is stark — gains vs. losses, alarm, exception. Use sparingly. For a
highlighted **point**, the fill is `highlight`, the **stroke** is
`highlight_dark` (`#1A5A8E`), and it is drawn **once at `alpha = 1`** (focus rows
excluded from the muted backdrop — see above); any **label** tied to the focus
also uses `highlight_dark`. Don't confuse this with `accent` (`#1A5A8E`), which is
for non-data UI chrome only.

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
             fill = highlight)                    # focus bar main blue (#2F87C8)
```

After `gl_setup()` the relevant defaults are:

| Geom | Default |
|------|---------|
| `geom_line` / `geom_path` / `geom_step` | colour = `c_muted_dark` |
| `geom_point` | **shape 21**, fill = `c_muted`, colour (stroke) = `c_muted_dark`, 0.8 alpha — every point has a fill + a 1px darker stroke |
| `geom_col` / `geom_bar` | fill = `c_muted`, **1px `paper` stroke** (gives the stacked-segment separation; invisible on a single bar) |
| `geom_area` | fill = `c_muted`, no stroke (stacked areas stay gapless) |
| `geom_smooth` | line `c_muted_dark`, ribbon `c_muted_light` |
| `geom_ribbon` | fill = `c_muted_light`, alpha 0.5 |
| `geom_boxplot` | **recedes**: `c_muted_light` fill, `c_muted` outline (background distribution) |
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
| `"categorical"` | 6 | Default. General purpose. Used automatically. Main (fill) tones. |
| `"categorical_dark"` | 6 | Dark tones, same order — strokes + all text tied to a series (WCAG AA). |
| `"categorical_light"` | 6 | Light tones, same order — backgrounds, faded states, two/three-tone fills. |
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

### 7. Prefer tones of one hue; three tones, three jobs

**Whenever possible, limit the number of different colors and use different
tones of the same hue instead** (spec §7). When two or three categories share
a parent — goods vs. services, low/medium/high, primary/intermediate/final —
encode them with one hue's light/main(/dark) tones rather than reaching for
unrelated colors. The shared hue keeps the chart reading as one total; the
lightness step carries the split. Reach for the categorical palette only when
the categories are genuinely unrelated.

```r
# Two-tone stacked bars: one hue, main + light
ggplot(data, aes(x = year, y = share, fill = tier)) +
    geom_col() +
    scale_fill_manual(values = c(Goods = gl$c_1, Services = gl$c_1_light))
```

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

The stroke must be the **dark** tone of the hue, the fill the **main** tone
(Decision Rule 2). With `shape = 21`, `fill` is the circle body and `color` is
the stroke — so pair a dark color scale with a main fill scale:

```r
ggplot(data, aes(x, y, color = group, fill = group)) +
    geom_point(shape = 21, size = 3, alpha = 0.8, stroke = 0.6) +
    scale_fill_gl("categorical") +        # main tone — circle body
    scale_color_gl("categorical_dark")    # dark tone — stroke
```

For a single-focus scatter, draw the focus point **once at `alpha = 1`** (and keep
it out of the muted backdrop layer):
`geom_point(shape = 21, fill = gl$c_1, color = gl$c_1_dark, alpha = 1, stroke = 0.6)`.
The 0.8 default opacity is for the overlapping *backdrop* cloud, not the highlight.

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

### 10. Stacked bars: 1px gap between segments

Spec §6 requires a **1px gap** separating each stacked-bar segment from the one
above — a clean boundary that also helps readers with low color discrimination.
The `geom_col`/`geom_bar` default now carries a 1px `paper` stroke, so plain
`geom_col()` already gives the gap; you don't add anything. Order categories
**largest mean share at the bottom**, upward.

Stacked **areas** are the exception — they sit edge-to-edge with no gap; the
color (or lightness, for the three-tone option) carries the separation.

**A marker on top of a stacked bar** (e.g. a net-total dot over saturated
segments) takes the **lightest muted tone with a white stroke** — the bar tones
are built to contrast strongly with white, so a pale dot ringed in `paper` reads
cleanly on top of them (a dark stroke would disappear into the dark segments).

```r
geom_point(aes(x = total), fill = gl$c_muted_light, color = gl$paper,
           size = 2.2, stroke = 0.7)
```

### 11. Axis & title conventions

- **Year axis:** when the X axis is just years, **omit the axis label** — the
  tick labels already name the dimension. Use `labs(x = NULL)`.
- **Chart title ends in a period** (slide mode, or the document in report mode)
  — it reads as a finding statement. The subtitle does **not** end in a period.
- **Gridlines default to horizontal (Y) only.** For horizontal-bar charts, flip
  to vertical so the reader can estimate bar lengths:
  `theme(panel.grid.major.x = element_line(color = gl$gridline, linewidth = 0.4), panel.grid.major.y = element_blank())`.
- **Tabular figures — known limitation.** The spec asks for
  `font-variant-numeric: tabular-nums` on all numerals, but Inter's tabular
  feature can't be enabled through `showtext` / `font_add_google()`, so tick
  digits render proportionally. Right-aligned y-axis ticks still align
  acceptably; avoid relying on column alignment of in-chart numbers.

### 12. Background distribution + highlighted country

When box plots (or violins) show the **background distribution** of a peer set
and a line shows one country relative to it, the box plots must **recede** —
they are context, not the subject. The `geom_boxplot` default does this for you
(soft `c_muted_light` fill, `c_muted` outline); draw the country as a
`highlight` line with a `fill = highlight, color = highlight_dark` point on top.

```r
data |>
    ggplot(aes(x = year, y = value, group = year)) +
    geom_boxplot(data = \(d) filter(d, iso %in% peers),     # muted grey, background
                 outlier.shape = NA) +
    geom_line(data = \(d) filter(d, iso == focus),          # main-blue line, pops
              aes(group = NA), color = highlight, linewidth = highlight_sz) +
    geom_point(data = \(d) filter(d, iso == focus),         # marker painted once, opaque
               aes(group = NA), fill = highlight, color = highlight_dark,
               alpha = 1, size = 2)
```

## Complete example

```r
source("~/dev/gl-design/skills/gl-ggplot/assets/theme_gl.R")
gl_setup()

library(dplyr)

focus_country <- "Mongolia"

trade_data |>
    ggplot(aes(x = year, y = export_value, group = country)) +
    geom_line(color = c_muted, linewidth = 0.5) +
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
gl$accent                        # "#1A5A8E"  (= gl$c_1_dark; UI chrome only)
gl$c_muted                       # "#999FA8"  (muted bars / "everyone else")
gl$c_muted_dark                  # "#5F6773"  (line/point strokes)
gl$c_1                           # "#2F87C8"  (main blue, = highlight)
gl$c_1_dark                      # "#1A5A8E"  (= highlight_dark — point strokes/labels)
gl$c_2                           # "#CC4948"  (main red, = lead_finding)
gl$ink                           # "#1A1714"
```

## Checklist before finalizing charts

- [ ] `gl_setup()` called at top of script
- [ ] No per-chart theme overrides (except legend position)
- [ ] No monospace anywhere (no JetBrains Mono, no `font.family = "mono"`)
- [ ] Highlights use `highlight` (main blue) or `lead_finding` (main red), not `"red"`, `accent`, or arbitrary hex — fills/lines use the **main** tone
- [ ] Highlighted points use `fill = highlight` + `color = highlight_dark` (main fill, dark 1px stroke); their labels use `highlight_dark`
- [ ] Highlighted points are painted **once** at `alpha = 1` — focus rows excluded from the muted backdrop layer, never overpainted on top of a grey dot
- [ ] Points are shape-21 filled circles with a darker 1px stroke (the geom default)
- [ ] Highlights use mute-then-paint — supporting data is `c_muted`
- [ ] Most charts have 2–4 colors; bigger palettes use the muted base
- [ ] Series labels / direct annotations / scatter strokes use the **dark tone**
      (`c_N_dark` / `categorical_dark`), not the main tone — WCAG AA contrast
- [ ] Overlapping marks (scatter, radar) use 0.8 fill+stroke opacity
- [ ] Related categories use one hue's tones (two/three-tone) before reaching
      for multiple colors
- [ ] Stacked bars have a 1px paper gap (`geom_col(color = gl$paper, linewidth = 0.5)`),
      ordered largest-share-at-bottom; stacked areas stay edge-to-edge
- [ ] Highlighted focus line is only ~1.3× the muted line (`highlight_sz`), not a 2× jump
- [ ] Sequential ramp for ordered values; diverging only with a real midpoint
- [ ] Year-only X axis omits its axis label (`labs(x = NULL)`)
- [ ] Chart title (slide mode) ends in a period; subtitle does not
- [ ] Horizontal-bar charts flip gridlines to vertical (X)
- [ ] Figures saved with `save_fig()` at named sizes
- [ ] GDP per capita axes use `scale_x_log10()`
- [ ] Legend fits without clipping (use `nrow = 2` or `position = "right"` if needed)
