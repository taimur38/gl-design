---
name: chart-audit
description: Audit ggplot2 charts against the Growth Lab design framework. Use this skill after generating or modifying charts to flag visual issues — legend sizing, color misuse, dimension mismatches, highlight consistency, and readability problems.
compatibility: Requires R script with ggplot2 charts and the GL design framework (framework.md).
metadata:
  author: taimur-shah
  version: "1.0"
---

# Chart Audit

Audit ggplot2 charts against the Growth Lab design framework. Run this after generating or modifying charts to catch visual problems before they reach a report.

## When to use

- After creating or editing charts in an R script
- Before converting a report to Word/PDF
- When reviewing an existing set of chart PNGs

## How to run

This is a manual audit skill — Claude reads the R source and/or rendered PNGs and checks each chart against the rules below. To invoke:

1. Read the R script that produces the charts
2. Read the rendered PNG images
3. Walk through every check below for each chart
4. Report a summary table: chart name, pass/flag, issue

## Audit checks

### 1. Legend placement

| Condition | Expected | Flag if |
|-----------|----------|---------|
| Report mode, ≤8 legend items | `legend.position = "bottom"` (theme default) | Legend is on the right, consuming plot width |
| Report mode, >8 legend items | `legend.position = "right"` (explicit override) | Bottom legend wrapping to 3+ rows |
| Bottom legend with 4+ items | Items fit in 1–2 rows without clipping | Any label is truncated or runs off-edge |
| Any legend | Title is either `NULL`/`""` or a short mono label | Long prose legend titles |
| Slide mode | Default ggplot position (right) is acceptable | — |

### 2. Highlight color

| Condition | Expected | Flag if |
|-----------|----------|---------|
| Highlighted data points | Uses the `highlight` variable (`#C64646`) | Uses `"red"`, `"#FF0000"`, or any other red |
| Highlighted geoms | Painted twice — full data at default, then filtered subset at `color = highlight` with larger `size` | Single geom with conditional color |
| Non-highlighted geoms | Default palette colors or theme defaults | Gratuitous color on geoms that don't need it |

### 3. Figure dimensions

| Condition | Expected | Flag if |
|-----------|----------|---------|
| `save_fig()` call present | Uses a named size from `gl_fig` | Raw `ggsave()` with arbitrary dimensions |
| Named size matches content | `full` (6.5×4.0) for standard charts, `full_tall` (6.5×6.0) for faceted/stacked, `half` (3.167×3.0) for side-by-side | Size doesn't match chart complexity |
| Faceted charts with ≥4 panels | `full_tall` or `full_square` | `full` — panels will be too compressed |

### 4. Color palette

| Condition | Expected | Flag if |
|-----------|----------|---------|
| Discrete color/fill scales | Uses `gl$palette` (set via `options()`) or `scale_*_manual()` with framework colors | Default ggplot rainbow, or colors outside the framework palette |
| Categorical palette | `#266798 #C64646 #36B250 #EAC218 #D1852A #52E2DE #A42DE2 #7C6760 #757777` | Unlisted hex values (except greys and `highlight`) |
| Manual color values | Framework tokens or standard greys | Arbitrary hex colors not in the palette |

### 5. Theme compliance

| Condition | Expected | Flag if |
|-----------|----------|---------|
| `theme_gl()` is set | `theme_set(theme_gl(mode = "report"))` at top of script | Missing, or using `theme_minimal()`, `theme_bw()`, etc. |
| Report mode | `plot.title`, `plot.subtitle`, `plot.caption` are blank | Title/subtitle/caption visible in rendered PNG |
| Per-chart theme overrides | Minimal — only `legend.position` or `strip.text` adjustments | Overriding fonts, font sizes, colors, or axis styling |

### 6. Axis and scale conventions

| Condition | Expected | Flag if |
|-----------|----------|---------|
| GDP per capita on x-axis | `scale_x_log10()` | Linear scale for GDP per capita |
| Percentage y-axis | `labels = percent` or `percent_format()` | Raw decimal values (0.05 instead of 5%) |
| Year axis | Reasonable breaks (not every year) | Overlapping year labels |

### 7. Text and labels

| Condition | Expected | Flag if |
|-----------|----------|---------|
| Axis titles | Short, in mono font (theme handles this) | Long prose axis titles |
| `labs()` in report mode | `title = "unused"`, `caption = "unused"` (or omitted) | Actual title/caption text that will be suppressed anyway |
| Direct labels (if used) | `geom_text_repel()` or `geom_label_repel()` | `geom_text()` with overlapping labels |

### 8. Visual weight and readability

This check requires reading the rendered PNG:

| Condition | Expected | Flag if |
|-----------|----------|---------|
| Data-ink ratio | Chart area dominates; legends, axes, whitespace are secondary | Legend or axis labels take >30% of figure area |
| Highlight visibility | Highlighted element is immediately identifiable | Highlight color lost among other saturated colors |
| Overplotting | Points/lines are distinguishable | Dense scatter with no alpha, or many overlapping lines |
| Grid lines | Minimal (theme_few base) | Heavy grid lines competing with data |

## Output format

After auditing, produce a summary:

```
## Chart Audit Results

| # | Chart | Status | Issues |
|---|-------|--------|--------|
| 1 | reserves-time-series | PASS | — |
| 2 | sbp-balance-sheet | FLAG | Legend clipped at right edge |
| 3 | exports-per-capita | PASS | — (right legend override OK for 15 categories) |
...

### Flagged items

**sbp-balance-sheet** — Legend clipped at right edge
- Current: 4 long labels in single-row bottom legend
- Fix: Add `guides(color = guide_legend(nrow = 2))`
```
