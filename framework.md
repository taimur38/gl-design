# Growth Lab Report Design Framework

## 1. Page Setup

| Property       | US Letter         | A4 (international)  |
|----------------|-------------------|----------------------|
| Page size      | 8.5 × 11 in       | 8.27 × 11.69 in     |
| Top margin     | 1.0 in            | 1.0 in               |
| Bottom margin  | 1.25 in           | 1.25 in              |
| Left margin    | 1.0 in            | 1.0 in               |
| Right margin   | 1.0 in            | 1.0 in               |
| **Live area**  | **6.5 × 8.75 in** | **6.27 × 9.44 in**  |

Horizontal margins are symmetric at 1.0". The bottom margin is 1.25" — slightly
larger than the top — for three converging reasons: (1) it hosts page numbers
and footnotes without crowding the body, (2) it optically centers the text
block on the page (a text block with equal vertical margins looks like it's
sinking), and (3) it makes the live height resolve cleanly into **exactly 7 vertical
modules** (8.75" / 1.25" = 7), rather than 7.2 with a residual.

The default target is **US Letter**; all figure sizes below are specified for
the 6.5" live width.

## 2. Grid System

A **6-column modular grid** governs horizontal placement of all elements.

```
┌─────────────────────────────────────────────────────────┐
│ 1.0" │  col  │g│  col  │g│  col  │g│  col  │g│  col  │g│  col  │ 1.0" │
│margin│ 0.944"│ │ 0.944"│ │ 0.944"│ │ 0.944"│ │ 0.944"│ │ 0.944"│margin│
└─────────────────────────────────────────────────────────┘
       gutter (g) = 0.167"  ×  5 gutters = 0.833"
       columns: 6 × 0.944" = 5.667"
       total live width: 5.667" + 0.833" = 6.5"
```

| Span         | Columns | Width   | Use                                    |
|--------------|---------|---------|----------------------------------------|
| Full         | 6       | 6.500"  | Hero figures, full-width tables        |
| Major        | 4       | 4.278"  | Primary figures with text wrap         |
| Half         | 3       | 3.167"  | Side-by-side figure pairs              |
| Minor        | 2       | 2.056"  | Small inset charts, margin figures     |

### Vertical modules

The vertical grid is based on the body text baseline: **11pt text on 15pt
leading** = 0.208" per baseline unit. Vertical modules are **6 baselines =
1.250"**. The 8.75" live height is **exactly 7 modules** tall — so just as
6 columns address every horizontal position, 7 modules address every vertical
position, and any element on the page lives in a `(column-span × module-span)`
cell.

| V-modules | Height  | Use                                          |
|-----------|---------|----------------------------------------------|
| 3         | 3.750"  | Compact landscape figure                     |
| 4         | 5.000"  | Standard figure height                       |
| 5         | 6.250"  | Tall figure / stacked panel                  |
| 6         | 7.500"  | Near-full-page figure (leaves 1 mod chrome)  |
| 7         | 8.750"  | Full-bleed figure (rare — no chrome room)    |

## 3. Named Figure Sizes

These are the canonical figure dimensions for ggplot output. Each snaps to the
grid and has a short name for use in `ggsave()`.

| Name         | Width   | Height  | Aspect   | Grid fit                | Use case                                |
|--------------|---------|---------|----------|-------------------------|-----------------------------------------|
| `full`       | 6.5"    | 4.0"    | ~1.63:1  | 6 col × 3.2 v-mod      | Standard full-width chart               |
| `full_tall`  | 6.5"    | 6.0"    | ~1.08:1  | 6 col × 4.8 v-mod      | Stacked panels, patchwork (2 rows)      |
| `full_square`| 6.5"    | 6.5"    | 1:1      | 6 col × 5.2 v-mod      | Heatmaps, correlation matrices          |
| `major`      | 4.278"  | 4.0"    | ~1.07:1  | 4 col × 3.2 v-mod      | Primary chart with text beside it       |
| `half`       | 3.167"  | 3.0"    | ~1.06:1  | 3 col × 2.4 v-mod      | Side-by-side pair                       |
| `half_tall`  | 3.167"  | 5.0"    | ~0.63:1  | 3 col × 4 v-mod        | Portrait figure, ranked bar chart       |
| `slide`      | 10"     | 5.625"  | 16:9     | —                       | Full slide chart (Marp, PowerPoint)     |

### R helper

```r
# Place in your Rmd setup chunk or source from a shared utils file.
gl_fig <- list(
    full        = list(w = 6.5,  h = 4.0),
    full_tall   = list(w = 6.5,  h = 6.0),
    full_square = list(w = 6.5,  h = 6.5),
    major       = list(w = 4.278, h = 4.0),
    half        = list(w = 3.167, h = 3.0),
    half_tall   = list(w = 3.167, h = 5.0),
    slide       = list(w = 10,    h = 5.625)
)

save_fig <- function(name, filename, plot = last_plot(), dpi = 300) {
    sz <- gl_fig[[name]]
    ggsave(filename, plot = plot, width = sz$w, height = sz$h, dpi = dpi)
}

# Usage:
# save_fig("full", "imgs/gdp_growth.png")
# save_fig("half", "imgs/export_share.png")
```

## 4. Typography

All text uses the Growth Lab type stack: **Source Sans 3** for reading text and
**JetBrains Mono** for technical/data annotations.

### Type scale

The scale is based on a **1.25 major third** ratio from an 11pt body size.
Every size is rounded to the nearest 0.5pt for clean rendering.

| Role              | Font            | Size   | Weight     | Color     | Notes                         |
|-------------------|-----------------|--------|------------|-----------|-------------------------------|
| H1 (title)        | Source Sans 3   | 21.5pt | SemiBold   | #333333   | Report title, one per doc     |
| H2 (section)      | Source Sans 3   | 17pt   | SemiBold   | #333333   | Major sections                |
| H3 (subsection)   | Source Sans 3   | 14pt   | SemiBold   | #333333   | Subsections                   |
| H4 (sub-sub)      | Source Sans 3   | 11pt   | SemiBold   | #333333   | Paragraph-level headings      |
| Body              | Source Sans 3   | 11pt   | Regular    | #333333   | Main prose                    |
| Body emphasis      | Source Sans 3   | 11pt   | SemiBold   | #333333   | Bold text within prose        |
| Block quote       | Source Sans 3   | 11pt   | Regular Italic | #7c7c7c | Indented quotes             |
| Figure title      | Source Sans 3   | 11pt   | SemiBold   | #333333   | Above figure: "Figure 1."    |
| Figure caption    | JetBrains Mono  | 8.5pt  | Regular    | #7c7c7c   | Below figure: source/notes   |
| Table header      | Source Sans 3   | 10pt   | SemiBold   | #333333   | Column headers                |
| Table body        | Source Sans 3   | 10pt   | Regular    | #333333   | Cell contents                 |
| Table note        | JetBrains Mono  | 8.5pt  | Regular    | #7c7c7c   | Below table: source/notes    |
| Footnote          | Source Sans 3   | 9pt    | Regular    | #7c7c7c   | Page footnotes                |
| Page header       | JetBrains Mono  | 8pt    | Regular    | #7c7c7c   | Running head                  |
| Page footer       | JetBrains Mono  | 8pt    | Regular    | #7c7c7c   | Page number                   |

### Spacing rules

- **Above H2:** 24pt (roughly 2 baselines of breathing room)
- **Above H3:** 18pt
- **Above H4:** 12pt
- **Below all headings:** 6pt
- **Paragraph spacing:** 6pt after each paragraph (no first-line indent); body text is **justified**
- **Figure/table spacing:** 12pt above, 6pt below caption

### Slide vs. report mode

`theme_gl()` accepts a `mode` parameter:

- **`mode = "slide"`** (default) — title, subtitle, and caption are rendered
  inside the chart. Use for standalone slides and presentations.
- **`mode = "report"`** — title, subtitle, and caption are **suppressed**
  (set to `element_blank()`). The document handles these via Figure Title
  and Figure Source styles. Axis labels (`x`, `y`) are kept.
  Legend is placed **bottom-left** by default to preserve plot width.
  Charts with many categories (>8) may override to `legend.position = "right"`.

```r
theme_set(theme_gl(mode = "report"))
```

This means the same `labs(title = ..., subtitle = ..., caption = ...)` calls
work in both contexts — the theme controls whether they render.

### In-chart typography (ggplot `theme_gl`)

These sizes are set inside the ggplot theme and are **relative to the figure's
own coordinate space**, not the page. They are already defined in `theme_gl()`
(base_size = 12) and should not be overridden per-chart.

| Element       | Font           | Relative size | Absolute at base 12 |
|---------------|----------------|---------------|----------------------|
| Plot title    | Source Sans 3  | 1.35×         | 16.2pt               |
| Plot subtitle | Source Sans 3  | 1.0×          | 12pt                 |
| Axis title    | JetBrains Mono | 0.85×         | 10.2pt               |
| Axis text     | Source Sans 3  | 0.85×         | 10.2pt               |
| Legend title   | JetBrains Mono | 0.8×          | 9.6pt                |
| Legend text   | Source Sans 3  | 0.85×         | 10.2pt               |
| Strip text    | JetBrains Mono | 0.85×         | 10.2pt               |
| Caption       | JetBrains Mono | 0.75×         | 9pt                  |

## 5. Color System

### Brand palette

| Name   | Hex       | Use                                        |
|--------|-----------|--------------------------------------------|
| Blue   | `#6db5db` | Accent, links                              |
| Green  | `#48c0a2` | Secondary accent                           |
| Yellow | `#e5bd4f` | Tertiary accent                            |
| Red    | `#ee3e4c` | Alerts, highlights                         |

### Text and UI colors

| Token        | Hex       | Use                                       |
|--------------|-----------|-------------------------------------------|
| text_dark    | `#333333` | Primary text, headings                    |
| text_muted   | `#7c7c7c` | Captions, secondary text, axis labels     |
| border       | `#dcdcdc` | Rules, table borders, dividers            |
| background   | `#f3f3f3` | Shaded boxes, sidebars                    |
| brand_blue   | `#266798` | Chart primary color, institutional blue   |

### Categorical palette (9 colors, for data visualization)

```
#266798  #C64646  #36B250  #EAC218  #D1852A  #52E2DE  #A42DE2  #7C6760  #757777
```

Use in order. For fewer categories, take the first N. For highlighting a single
series, use `#C64646` (red) against a grey or muted base.

### Sector-specific palettes

For trade/product data, use the official Atlas HS sector colors defined in
`design-library/visualization_colors/atlas/hs_product_sectors.csv`.

## 6. Element Patterns

### Figures

```markdown
**Figure 1.** GDP per capita growth, 2000–2023

![](imgs/gdp_growth.png)

*Source: World Bank WDI. Authors' calculations.*
```

- Title above the image in **bold body text** (Source Sans 3, 11pt SemiBold)
- Caption below in *italic* monospace (JetBrains Mono, 8.5pt)
- Image saved at the appropriate named size (usually `full`)
- 12pt space above the figure title, 6pt below the caption

### Tables

- Light top and bottom rules (border color `#dcdcdc`)
- No vertical rules
- Header row in SemiBold with a heavier bottom rule
- Alternating row shading optional (use `#f3f3f3`)
- Table notes below in the same style as figure captions

### Pull quotes / call-out boxes

- Background: `#f3f3f3`
- Left border: 3pt solid `#266798` (brand blue)
- Text: Body style, optionally italic
- Padding: 12pt all sides

### Horizontal rules

- Color: `#dcdcdc`
- Weight: 0.5pt
- Full live width
- 12pt above and below

## 7. Quick Reference Card

```
PAGE:   US Letter, margins 1.0/1.0/1.0/1.25 (L/R/T/B) → live 6.5 × 8.75"
GRID:   6 columns × 0.944" + 5 gutters × 0.167" = 6.5" live width
        7 modules × 1.25" = 8.75" live height
FONTS:  Source Sans 3 (body/heads) + JetBrains Mono (captions/data)
BODY:   11pt / 15pt leading
SCALE:  × 1.25 major third → 11 → 14 → 17 → 21.5

FIGURE SIZES (width × height):
  full        6.5 × 4.0"     Standard chart
  full_tall   6.5 × 6.0"     Stacked / patchwork
  full_square 6.5 × 6.5"     Heatmaps
  major       4.278 × 4.0"   Chart + text wrap
  half        3.167 × 3.0"   Side-by-side pair
  half_tall   3.167 × 5.0"   Portrait chart

COLORS:
  Text:      #333333 / #7c7c7c (muted)
  Border:    #dcdcdc
  BG:        #f3f3f3
  Highlight: #C64646
  Brand:     #266798
```
