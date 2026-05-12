# Recipe: Long-Form Report

Applies the Growth Lab visual [grammar](../grammar.md) to long-form research
publications: prose, data visualizations, tables, footnotes, references. The
authoring pipeline is Markdown → Word via pandoc (see
[`skills/md2docx/`](../skills/md2docx/)); the final deliverable is a PDF.

## 1. Page setup

| Property       | US Letter (default) | A4 (international) |
|----------------|---------------------|---------------------|
| Page size      | 8.5 × 11 in         | 8.27 × 11.69 in     |
| Top margin     | 1.0 in              | 1.0 in              |
| Bottom margin  | 1.25 in             | 1.25 in             |
| Left margin    | 1.0 in              | 1.0 in              |
| Right margin   | 1.0 in              | 1.0 in              |
| **Live area**  | **6.5 × 8.75 in**   | **6.27 × 9.44 in**  |

Horizontal margins are symmetric at 1.0". The bottom margin is 1.25" — slightly
larger than the top — for three converging reasons: (1) it hosts page numbers
and footnotes without crowding the body, (2) it optically centers the text
block on the page (a text block with equal vertical margins looks like it's
sinking), and (3) it makes the live height resolve cleanly into **exactly 7
vertical modules** (8.75" / 1.25" = 7), rather than 7.2 with a residual.

The default target is **US Letter**; all figure sizes below are specified for
the 6.5" live width.

## 2. Grid

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

| Span    | Columns | Width   | Use                                    |
|---------|---------|---------|----------------------------------------|
| Full    | 6       | 6.500"  | Hero figures, full-width tables        |
| Major   | 4       | 4.278"  | Primary figures with text wrap         |
| Half    | 3       | 3.167"  | Side-by-side figure pairs              |
| Minor   | 2       | 2.056"  | Small inset charts, margin figures     |

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

## 3. Type at report sizes

This recipe anchors the [grammar's ×1.25 scale](../grammar.md#type-scale-the-system)
at **11pt body / 15pt leading** (1.36 line-height). The full scale unwraps to:

| Step | Size    | Role                          |
|------|---------|-------------------------------|
| +3   | 21.5pt  | H1 (title), one per doc       |
| +3   | 21.5pt  | H2 (section)                  |
| +2   | 17pt    | (unused)                      |
| +1   | 14pt    | H3 (subsection)               |
| 0    | 11pt    | H4, Body, Body emphasis       |
| 0    | 11pt    | Figure title                  |
| −0.5 | 10pt    | Table header, Table body      |
| −1   | 9pt     | Footnote                      |
| −1.5 | 8.5pt   | Figure caption, Table note    |
| −2   | 8pt     | Page header / footer          |

(Note: H1/H2 share the +3 step; H3 lands at +1, not +2, to keep the heading
ladder visually distinct without dramatic jumps. Sizes are rounded to the
nearest 0.5pt for clean rendering.)

### Spacing rules

- **Above H2:** 24pt (roughly 2 baselines of breathing room)
- **Above H3:** 18pt
- **Above H4:** 12pt
- **Below all headings:** 6pt
- **Paragraph spacing:** 6pt after each paragraph (no first-line indent); body
  text is **justified**
- **Figure/table spacing:** 12pt above, 6pt below caption

## 4. Named figure sizes

These are the canonical figure dimensions for ggplot output in a report. Each
snaps to the grid and has a short name for use in `save_fig()` (see
[`skills/gl-ggplot/`](../skills/gl-ggplot/)).

| Name          | Width   | Height  | Aspect   | Grid fit            | Use case                          |
|---------------|---------|---------|----------|---------------------|-----------------------------------|
| `full`        | 6.5"    | 4.0"    | ~1.63:1  | 6 col × 3.2 v-mod   | Standard full-width chart         |
| `full_tall`   | 6.5"    | 6.0"    | ~1.08:1  | 6 col × 4.8 v-mod   | Stacked panels, patchwork (2 rows)|
| `full_square` | 6.5"    | 6.5"    | 1:1      | 6 col × 5.2 v-mod   | Heatmaps, correlation matrices    |
| `major`       | 4.278"  | 4.0"    | ~1.07:1  | 4 col × 3.2 v-mod   | Primary chart with text beside it |
| `half`        | 3.167"  | 3.0"    | ~1.06:1  | 3 col × 2.4 v-mod   | Side-by-side pair                 |
| `half_tall`   | 3.167"  | 5.0"    | ~0.63:1  | 3 col × 4 v-mod     | Portrait figure, ranked bar chart |

(`slide` — 10 × 5.625", 16:9 — also lives in the gl-ggplot helper today, but
will move into a slide recipe once that exists.)

## 5. Element patterns

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
- Caption always sits full-width below the figure; body prose only resumes on
  a new row (never wraps beside a figure)

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

## 6. Quick reference

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
