---
marp: true
theme: growth-lab
size: 16:9
paginate: true
---

<!-- _class: title -->

# The Growth Lab Report Design Framework

### A considered system for research publications

---

## Why a design framework?

Growth Lab reports combine **prose, data visualizations, tables, and references** into long-form research documents read by policymakers.

Without a system:
- Figure sizes are ad-hoc, breaking visual rhythm
- Typography varies across documents
- Color usage is inconsistent
- Charts and text compete rather than complement

The framework gives every element **a clear home on the page** — so researchers can focus on the work, not the layout.

---

<!-- _class: break -->

# The Grid

---

## Page setup

### Asymmetric margins for binding

The page uses **asymmetric margins** — wider on the inside for binding, narrower outside to maximize reading space.

| Property | Value |
|----------|-------|
| Page size | US Letter (8.5 x 11 in) |
| Top / Bottom | 1.0 in each |
| Inside (binding) | 1.25 in |
| Outside | 0.75 in |
| **Live area** | **6.5 x 9.0 in** |

This mirrors the layouts of Foreign Affairs, World Bank flagships, and academic journals — generous margins that let the content breathe.

---

## The 6-column modular grid

### Horizontal structure

Every element on the page is placed on a **6-column grid** with consistent gutters.

```
  1.25"  │  col  │ g │  col  │ g │  col  │ g │  col  │ g │  col  │ g │  col  │  0.75"
 margin  │0.944" │   │0.944" │   │0.944" │   │0.944" │   │0.944" │   │0.944" │ margin
          ─────── gutter = 0.167"  ×  5 gutters = 0.833" ────────
          ─────── 6 columns × 0.944" = 5.667" ───────────────────
                                Total live width: 6.5"
```

Six columns allows **full-width, two-thirds, half, and one-third** layouts — more flexible than 3, simpler than 12.

---

## Column spans in practice

### How content maps to the grid

| Span | Columns | Width | Use case |
|------|---------|-------|----------|
| **Full** | 6 | 6.500" | Hero figures, full-width tables |
| **Major** | 4 | 4.278" | Primary figure with text beside |
| **Half** | 3 | 3.167" | Side-by-side figure pairs |
| **Minor** | 2 | 2.056" | Inset charts, margin figures |

This means a chart is never arbitrarily sized. It locks to 6.5", 4.278", or 3.167" wide — producing **visual consistency across every page**.

---

## Vertical rhythm

### Baseline-driven vertical modules

Vertical spacing is derived from the body text: **11pt on 15pt leading** = 0.208" per baseline.

A vertical module is **6 baselines = 1.250"** — the building block for figure heights.

| V-modules | Height | Use |
|-----------|--------|-----|
| 3 | 3.750" | Compact landscape figure |
| 4 | 5.000" | Standard figure height |
| 5 | 6.250" | Tall / stacked panel |
| 6 | 7.500" | Near-full-page figure |

Figures don't just fit the width — they **snap to the vertical rhythm** too, keeping text flow predictable.

---

<!-- _class: break -->

# Typography

---

## Two-font system

### Each font has a clear role

<div class="cols">
<div>

**Source Sans 3**
*Body & headings*

A humanist sans-serif with high x-height, excellent from 8pt to 22pt. Professional yet warm — widely used in academic publishing.

Used for: headings, body text, axis labels, legend text, table content

</div>
<div>

**JetBrains Mono**
*Captions & data*

Monospace for clear number alignment and visual separation from prose. Signals "this is metadata, not narrative."

Used for: figure captions, axis titles, strip text, page headers/footers, table notes

</div>
</div>

---

## The type scale

### Built on a 1.25 major third ratio

Starting from **11pt body**, each step multiplies by 1.25 (a musical interval), rounded to 0.5pt:

```
  11pt  ──×1.25──▶  14pt  ──×1.25──▶  17pt  ──×1.25──▶  21.5pt
  Body      H3          H2           H1
```

| Role | Size | Weight | Notes |
|------|------|--------|-------|
| H1 (title) | 21.5pt | SemiBold | One per document |
| H2 (section) | 17pt | SemiBold | Major sections |
| H3 (subsection) | 14pt | SemiBold | Subsections |
| H4 / Body | 11pt | SemiBold / Regular | Paragraph headings / prose |

A mathematical ratio creates **inherent visual harmony** — sizes relate to each other, not chosen arbitrarily.

---

## Typography roles at a glance

### Every text element has a defined style

| Element | Font | Size | Color |
|---------|------|------|-------|
| Body prose | Source Sans 3 | 11pt Regular | `#333333` |
| Block quote | Source Sans 3 | 11pt Italic | `#7c7c7c` |
| Figure title | Source Sans 3 | 11pt SemiBold | `#333333` |
| Figure caption | JetBrains Mono | 8.5pt | `#7c7c7c` |
| Table header | Source Sans 3 | 10pt SemiBold | `#333333` |
| Footnote | Source Sans 3 | 9pt | `#7c7c7c` |
| Page header/footer | JetBrains Mono | 8pt | `#7c7c7c` |

The two fonts create a **clear visual layer**: Source Sans = content to read. JetBrains Mono = metadata to reference.

---

<!-- _class: break -->

# Spacing

---

## Spacing methodology

### Tight coupling, generous separation

The spacing system follows one principle: **elements that belong together are close; elements that don't are far apart.**

| Element | Space before | Space after |
|---------|-------------|-------------|
| H2 (section) | **24pt** | 6pt |
| H3 (subsection) | **18pt** | 6pt |
| H4 (paragraph heading) | **12pt** | 6pt |
| Body paragraph | 0pt | 6pt |
| Figure title | 12pt | 0pt |
| Figure caption | 0pt | 6pt |
| Pull quote box | 12pt | 12pt |

Headings have **large space above** (breathing room) and **small space below** (coupling to content). Paragraphs use space-after instead of first-line indents.

---

## Line height

### Optimized for academic reading

**11pt text on 15pt leading** = 1.36 line height

- More generous than 1.15 (too tight for long-form)
- Less than 1.5 (too airy, wastes space)
- Matches the reading density of academic journals like QJE

The **0.208" baseline unit** — derived from this leading — cascades into the vertical grid modules, figure heights, and spacing values. One decision governs the entire vertical system.

---

<!-- _class: break -->

# Figure Sizes

---

## Named figure sizes

### Six canonical dimensions that snap to the grid

Every chart is saved at one of six sizes. No guessing dimensions — pick a name.

| Name | Width | Height | Use case |
|------|-------|--------|----------|
| `full` | 6.5" | 4.0" | Standard full-width chart |
| `full_tall` | 6.5" | 6.0" | Stacked panels / patchwork |
| `full_square` | 6.5" | 6.5" | Heatmaps, matrices |
| `major` | 4.278" | 4.0" | Chart + text beside it |
| `half` | 3.167" | 3.0" | Side-by-side pair |
| `half_tall` | 3.167" | 5.0" | Portrait / ranked bars |

All rendered at **300 DPI** for print-quality output.

---

## How figure sizes map to the grid

### Width from columns, height from vertical modules

```
  ┌──────────────────────────────────────────────────┐
  │                  full (6.5 × 4.0)                │   ← 6 columns
  │                                                  │
  └──────────────────────────────────────────────────┘

  ┌──────────────────────────────┐ ┌────────────────┐
  │                              │ │                │
  │     major (4.278 × 4.0)     │ │   (text area)  │   ← 4 + 2 columns
  │                              │ │                │
  └──────────────────────────────┘ └────────────────┘

  ┌───────────────────┐ ┌───────────────────┐
  │                   │ │                   │
  │  half (3.167×3.0) │ │  half (3.167×3.0) │         ← 3 + 3 columns
  │                   │ │                   │
  └───────────────────┘ └───────────────────┘
```

Figures are **first-class grid citizens**, not floating objects dropped onto a page.

---

## Slide vs. report mode

### Same code, two contexts

The `theme_gl()` ggplot theme accepts a `mode` parameter:

<div class="cols">
<div>

**Slide mode** *(default)*

Title, subtitle, and caption render **inside** the chart. For standalone presentations.

```r
theme_set(theme_gl(
  mode = "slide"
))
```

</div>
<div>

**Report mode**

Title, subtitle, and caption are **suppressed**. The document handles them via styled text above and below the figure.

```r
theme_set(theme_gl(
  mode = "report"
))
```

</div>
</div>

The same `labs(title=..., caption=...)` calls work in both — the theme controls visibility.

---

<!-- _class: break -->

# Color

---

## Color system

### Layered from UI to data

<div class="cols">
<div>

**Text & UI colors**

| Token | Hex | Role |
|-------|-----|------|
| Text dark | `#333333` | Primary text |
| Text muted | `#7c7c7c` | Captions, secondary |
| Border | `#dcdcdc` | Rules, dividers |
| Background | `#f3f3f3` | Shaded areas |
| Brand blue | `#266798` | Institutional color |
| Highlight | `#C64646` | Emphasis |

</div>
<div>

**Brand palette**

| | Color | Hex |
|-|-------|-----|
| ■ | Blue | `#6db5db` |
| ■ | Green | `#48c0a2` |
| ■ | Yellow | `#e5bd4f` |
| ■ | Red | `#ee3e4c` |

Text is `#333` not black — softer on the eye. Muted elements at `#7c7c7c` create a **clear information hierarchy** without competing with the data.

</div>
</div>

---

## Categorical data palette

### 9 colors, used in order

```
  #266798   #C64646   #36B250   #EAC218   #D1852A   #52E2DE   #A42DE2   #7C6760   #757777
```

- For fewer categories, take the **first N**
- For highlighting one series: `#C64646` (red) against a muted base
- First color is **brand blue** — institutional coherence even in data

The framework also includes **sector-specific palettes** for Atlas product sectors, geographic regions, Metroverse industries, and Greenplexity technologies — each with predefined, research-ready color mappings.

---

<!-- _class: break -->

# Element Patterns

---

## Figures, tables, and callouts

### Consistent patterns for every content type

<div class="cols">
<div>

**Figures**
```
Figure 1. GDP growth, 2000–2023
[chart image]
Source: World Bank WDI.
```
Bold title above. Mono caption below. 12pt above, 6pt below.

**Tables**
- Horizontal rules only (no vertical)
- SemiBold header with heavier bottom rule
- Optional alternating row shading (`#f3f3f3`)
- Mono notes below

</div>
<div>

**Call-out boxes**
- Background: `#f3f3f3`
- Left border: 3pt solid `#266798`
- Padding: 12pt all sides
- Visually isolated from body flow

**Horizontal rules**
- Color: `#dcdcdc`, weight: 0.5pt
- 12pt above and below
- Full live width

Every element follows the same spacing logic: **tight to its group, generous between groups.**

</div>
</div>

---

## In-chart typography

### The ggplot theme mirrors the document

`theme_gl()` maps the document's two-font system into chart space:

| Element | Font | Size (base 12) |
|---------|------|-----------------|
| Plot title | Source Sans 3 | 16.2pt |
| Axis title | JetBrains Mono | 10.2pt |
| Axis text | Source Sans 3 | 10.2pt |
| Legend title | JetBrains Mono | 9.6pt |
| Legend text | Source Sans 3 | 10.2pt |
| Strip text | JetBrains Mono | 10.2pt |
| Caption | JetBrains Mono | 9pt |

Charts are **typographically native** to the document — not foreign objects pasted onto the page.

---

<!-- _class: break -->

# Design Principles

---

## What makes this a considered framework

### Not a style guide — a system

<div class="cols">
<div>

**Everything derives from something**
- Type scale from a 1.25 ratio
- Vertical modules from line height
- Figure heights from vertical modules
- Spacing from baseline units
- Column widths from live area

Change one root value and the system adapts coherently.

</div>
<div>

**Researchers don't need design training**
- Pick a figure name, not a pixel size
- The theme handles typography
- Colors are predefined by sector
- Markdown in, styled PDF out

The framework absorbs complexity so the author doesn't have to.

</div>
</div>

---

## Design lineage

### Informed by authoritative publications

| Inspiration | What we took |
|-------------|-------------|
| **Foreign Affairs** | Generous margins, authoritative layout, strong hierarchy |
| **World Bank flagships** | Professional data presentation, structured figure placement |
| **The Economist** | Disciplined color, data-dense but readable, chart typography |
| **QJE** | Academic rigor, clean typesetting, well-integrated figures |

The framework synthesizes these influences into a system purpose-built for **data-rich policy research**.

---

<!-- _class: break -->

# Quick Reference

---

## The system at a glance

<div class="cols">
<div>

**Page & Grid**
- US Letter, 6.5 x 9.0" live area
- 6 columns at 0.944" + 0.167" gutters
- Vertical module: 6 baselines = 1.250"

**Typography**
- Source Sans 3 (body) + JetBrains Mono (data)
- 11pt / 15pt leading (1.36)
- Scale: 11 → 14 → 17 → 21.5pt

**Spacing**
- H2: 24pt before / 6pt after
- H3: 18pt / 6pt
- Paragraphs: 6pt after, no indent
- Figures: 12pt above, 6pt below caption

</div>
<div>

**Figure sizes**
- `full` — 6.5 x 4.0"
- `full_tall` — 6.5 x 6.0"
- `full_square` — 6.5 x 6.5"
- `major` — 4.278 x 4.0"
- `half` — 3.167 x 3.0"
- `half_tall` — 3.167 x 5.0"

**Colors**
- Text: `#333333` / `#7c7c7c`
- Border: `#dcdcdc` / BG: `#f3f3f3`
- Brand: `#266798` / Highlight: `#C64646`
- 9-color categorical palette
- Sector-specific palettes for Atlas, Metroverse, Greenplexity

</div>
</div>

---

<!-- _class: closing -->

# Growth Lab Design Framework

### A spatial, typographic, and chromatic system where every decision traces back to a root principle — so the design stays coherent even as the content changes.
