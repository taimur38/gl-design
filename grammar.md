# Growth Lab Visual Grammar

The grammar is the medium-agnostic foundation of the Growth Lab design system:
the color, type, and chart conventions that hold true whether an output is a
50-page report, a presentation slide, a one-page brief, a standalone chart, or
a web page. Specific outputs ("recipes") apply the grammar to a medium —
picking page geometry, anchor sizes, and density to suit the artifact. See
[`recipes/`](recipes/) for those applications.

The system is small on purpose. Before introducing a new style, work through
the rules in §4.

## 1. Color

### Ink — a four-layer warm ramp

Text is layered. Black for emphasis, near-black for body, warm grey for
secondary copy, paler grey for hairlines. The ramp is **warm** (browns,
not neutral greys) — it sits on paper, not on a screen.

| Token   | Hex       | Use                                                              |
|---------|-----------|------------------------------------------------------------------|
| `ink`   | `#1A1714` | Cover title, all headings, strong emphasis, table emphasis cells |
| `ink-2` | `#2C2823` | Body copy, axis text, table cells                                |
| `ink-3` | `#6B645A` | Captions, eyebrows, page chrome, secondary copy                  |
| `ink-4` | `#9A9389` | Hairline rules, trendlines, deep-background markers              |

### Accent

| Token         | Hex       | Use                                                                |
|---------------|-----------|--------------------------------------------------------------------|
| `accent`      | `#015C9C` | Cover date, eyebrows, figure labels, primary chart series         |
| `accent-deep` | `#003E6B` | Reserved — strong emphasis variant                                 |
| `accent-soft` | `#3A85B8` | Reserved — softer variant                                          |
| `accent-tint` | `#E1F0FA` | Background tint for accent panels                                  |

### Paper

| Token        | Hex       | Use                                              |
|--------------|-----------|--------------------------------------------------|
| `paper`      | `#FAF8F4` | Page paper (warm white)                          |
| `paper-warm` | `#F4F1EA` | Warmer surface                                   |
| `cover-bg`   | `#F3F2EA` | Cover page paper — do not use on content pages   |
| `rule`       | `#DDDDDD` | Hairline borders between content blocks          |

### Categorical chart palette (6 colors)

```
#015C9C  #C77A20  #CEC96B  #51B196  #A8352C  #918BED
```

| Token | Hex       | Role                                              |
|-------|-----------|---------------------------------------------------|
| `c-1` | `#015C9C` | Primary — single-series default; also `accent`    |
| `c-2` | `#C77A20` | Contrast / lead-finding amber                     |
| `c-3` | `#CEC96B` | Third series                                      |
| `c-4` | `#51B196` | Fourth series                                     |
| `c-5` | `#A8352C` | Fifth series                                      |
| `c-6` | `#918BED` | Sixth series                                      |

Use in order. The palette is deliberately small and muted — calmer than a
saturated rainbow.

### Muted — for de-emphasis

| Token     | Hex       | Use                                                   |
|-----------|-----------|-------------------------------------------------------|
| `c-muted` | `#7E8A99` | "Everyone-else" series when one is highlighted        |

Used in the highlight pattern below — a cool grey that visually recedes
behind the warm ink and accent palette.

### Sector-specific palettes

For trade/product data, use the official Atlas HS sector colors defined in
[`assets/design-library/visualization_colors/atlas/hs_product_sectors.csv`](assets/design-library/visualization_colors/atlas/hs_product_sectors.csv).
These are an external standard and override the categorical palette when
charting product data.

## 2. Typography

### Two families, two jobs

Every text element uses one of two families. Which one is a function of what
the text *does* — serif for voice, sans for function.

**Source Serif 4** — long-form and display. Variable font (uses the `opsz`
optical-size axis). Carries the lab's voice. Weights used: 300, 400, 500, 600.

> Cover title, all section and subsection headings, the lead paragraph,
> chart titles, chart sources (italic), colophon body text, footnote markers.

**Inter** — UI, labels, and reading body. Variable font. Carries information
without inflection. Weights used: 400, 500, 600, 700.

> Body copy, chart labels, axis text and ticks, annotations, table headers
> and cells, TOC sub-entries, page chrome (running head, folio, footnotes),
> eyebrows, figure labels, any small uppercase label.

Both ship locally in [`assets/fonts/`](assets/fonts/); the in-chart theme
also pulls them from Google Fonts at runtime.

### Optical sizing (Source Serif 4)

Source Serif 4 carries a true optical-size axis. The same family rendered at
`opsz 60` and `opsz 14` produces different shapes — the display cut has finer
strokes and tighter spacing; the text cut has more ink and looser metrics.
Honor the axis when picking a face:

| Use            | opsz | Why                                       |
|----------------|------|-------------------------------------------|
| Cover display  | 60   | Maximum contrast, tight spacing, refined  |
| Section heads  | 36   | Display-leaning but readable              |
| Subsection     | 22   | Mid-range                                 |
| Lead paragraph | 18   | Slightly display, opens the section       |
| Body / caption | 14   | Maximum legibility at small sizes         |

Tools render this differently — CSS via `font-variation-settings`, LaTeX via
fontspec axis options, ggplot via the registered face name. Tooling stubs
where opsz isn't reachable should default to opsz 14 (text optical size).

### Role hierarchy

Every recipe assigns sizes to a common set of text roles. The roles
themselves are part of the grammar.

**Display tier — large, serif:**

| Role           | Family          | Weight | Color | Case      | Notes                       |
|----------------|-----------------|--------|-------|-----------|-----------------------------|
| Display        | Source Serif 4  | 400    | `ink` | Sentence  | Cover title only            |
| H1 (section)   | Source Serif 4  | 500    | `ink` | Sentence  | No trailing period          |
| H2 (subsection)| Source Serif 4  | 500    | `ink` | Sentence  | No trailing period          |

**Body tier:**

| Role              | Family         | Weight  | Color   | Notes                          |
|-------------------|----------------|---------|---------|--------------------------------|
| Lead paragraph    | Source Serif 4 | 300     | `ink-2` | One per section; opens it      |
| Body              | Inter          | 400     | `ink-2` | Default narrative              |
| Body emphasis     | Inter          | 600     | `ink`   | `<strong>`                     |
| Colophon body     | Source Serif 4 | 400     | `ink-2` | Imprint page only              |
| Footnote          | Inter          | 400     | `ink-3` | Bottom of page                 |
| Footnote anchor   | Source Serif 4 italic | 400 | `accent` | Superscripted marker     |

**Chart-adjacent tier (figure block elements that sit outside the plot panel):**

| Role           | Family                | Weight | Color    | Case      | Notes                              |
|----------------|-----------------------|--------|----------|-----------|------------------------------------|
| Eyebrow        | Inter                 | 600    | `accent` | UPPERCASE | Tracking 0.14em                    |
| Figure label   | Inter                 | 600    | `accent` | UPPERCASE | "Figure 4". Tracking 0.14em        |
| Chart title    | Source Serif 4        | 500    | `ink`    | Sentence  | Ends with period (finding)         |
| Chart subtitle | Inter                 | 400    | `ink-3`  | Sentence  | Optional; units / period / unit    |
| Chart source   | Source Serif 4 italic | 400    | `ink-2`  | Sentence  | Required; italic distinguishes provenance |

**Inside the chart panel (theme_gl handles):**

| Role          | Family        | Weight       | Color   | Notes               |
|---------------|---------------|--------------|---------|---------------------|
| Axis label    | Inter         | 500          | `ink-2` |                     |
| Axis tick     | Inter         | 400          | `ink-2` | tabular-nums        |
| Legend / series label | Inter | 600          | series  | Color matches geom  |
| Annotation    | Inter         | 400          | `ink-2` | Sparingly           |

**Tables:**

| Role            | Family | Weight | Color   | Notes                       |
|-----------------|--------|--------|---------|------------------------------|
| Table header    | Inter  | 600    | `ink`   | Sentence case (never caps)   |
| Table cell      | Inter  | 400    | `ink-2` | Numeric cols: tabular-nums   |
| Table emphasis  | Inter  | 600    | `ink`   | First-column key, etc.       |
| Table note      | Source Serif 4 italic | 400 | `ink-2` | Same style as chart source |

**Table of contents:**

| Role          | Family        | Weight | Color   | Notes                  |
|---------------|---------------|--------|---------|------------------------|
| TOC major     | Source Serif 4| 600    | `ink`   | Top-level entry        |
| TOC sub       | Inter         | 400    | `ink-2` | Nested, indented       |
| TOC sub-sub   | Inter italic  | 400    | `ink-3` | Deeper nesting         |

**Page chrome:**

| Role         | Family                 | Weight | Color   | Notes                            |
|--------------|------------------------|--------|---------|----------------------------------|
| Running head | Inter                  | 500    | `ink-3` | UPPERCASE, 0.16em tracking       |
| Folio (page #)| Inter                 | 500    | `ink-3` | tabular-nums                     |
| Folio note   | Source Serif 4 italic  | 400    | `ink-3` | Optional, beside the folio       |

Recipes pin the absolute size of each role.

## 3. Charts

### Highlight by muting

When one series carries the story, paint everything else in `c-muted` first,
then re-paint the focus series on top in an accent (typically `c-1` or `c-2`).
The muted layer carries the general trend; the highlight carries the finding.

In ggplot:

```r
data |>
    ggplot(aes(x = x, y = y, group = country)) +
    geom_line(color = c_muted, linewidth = 0.6) +
    geom_line(data = \(d) filter(d, country == "Mongolia"),
              color = c_2, linewidth = 1.8)
```

The `theme_gl()` helper provides `c_muted`, `c_1`, ... `c_6`, and `accent`
as named values; do not hard-code hex.

### Most charts: two to four colors

A reader can hold only a few categories in working memory. When a chart
truly needs more series, use the muted layer for the rest and let one or
two focus series carry the story.

### Tabular numerals everywhere numeric

Always set `font-variant-numeric: tabular-nums` (CSS), `\addfontfeatures{Numbers=Monospaced}`
(LaTeX), or the equivalent on:

- Numeric table columns
- Axis tick labels
- Page numbers / folios
- TOC page numbers
- Any column-aligned numeric content

Without tabular figures the numbers visually slide; with them, columns line
up and scanning is faster.

## 4. Rules

The system is small on purpose. Before introducing a new style, work through
this list.

1. **Serif or sans?** Serif for the cover, all headings, the lead, the
   colophon, chart titles, and chart sources. Sans for everything else.

2. **No monospace.** Numerals use Inter with tabular figures. Avoid mono
   fonts in body, charts, and tables.

3. **Color encodes meaning, not decoration.** Every color in a chart must
   carry a specific function — a category, a series, a threshold, a
   highlight. If a color is not earning its keep, remove it.

4. **Use color to highlight; mute the rest.** Paint the focus series in an
   accent and the supporting data in `c-muted`. The muted layer carries the
   trend; the highlight carries the finding.

5. **Keep most charts to two to four colors.** When a chart truly needs more
   series, use the muted color for the rest and let the focus series carry
   the story.

6. **Tabular numerals on all numeric content.** Tables, axis ticks, page
   numbers, TOC page numbers.

7. **No all-caps body or headings.** Uppercase is reserved for eyebrows,
   figure labels, running heads, and similar 9–11pt chrome.

8. **No trailing periods on headings.** Section headings, subsection
   headings, and TOC entries end without a period. Chart titles **do** end
   with a period — they read as findings, not labels.

Recipe-specific size and layout rules live in each recipe.
