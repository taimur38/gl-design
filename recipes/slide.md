# Recipe: 16:9 Slide Deck

Applies the Growth Lab visual [grammar](../grammar.md) to slide decks for
talks, meetings, and project briefings. The authoring pipeline is Markdown
→ Marp → headless Chromium → PDF (see [`skills/md2slides/`](../skills/md2slides/));
the deliverable is a 16:9 PDF.

Slides are not micro-reports. They are read from across a room, on a
projector, by someone whose attention is split between you and the deck.
The recipe scales the grammar's type roles up, drops density, and reserves
each slide for one idea.

## 1. Canvas

| Property       | Value                                |
|----------------|--------------------------------------|
| Aspect         | 16:9                                 |
| Pixel size     | 1280 × 720 (Marp default)            |
| Print analog   | ~13.33 × 7.50 inches at 96 DPI       |
| Paper color    | `paper` (#FFFFFF) on content slides  |
| Cover paper    | `cover-bg` (#F3F2EA)                 |
| Break paper    | `ink-2` (#2C2823) — warm near-black  |
| Closing paper  | `paper-warm` (#F4F1EA)               |

Padding inside the live area:

| Slide class    | Top  | Right | Bottom | Left | Rationale                          |
|----------------|------|-------|--------|------|------------------------------------|
| Content        | 64px | 80px  | 72px   | 80px | Anchor type at left, breathe       |
| Title          | 64px | 80px  | 64px   | 80px | Logo, date, display, pattern       |
| Chart          | 48px | 64px  | 56px   | 64px | Tighter — chart needs the real estate |
| Break          | 80px | 96px  | 80px   | 96px | Roomy — section dividers breathe   |
| `img-full`     | 40px | 56px  | 40px   | 56px | Image dominates                    |
| `map-slide`    | 28px | 40px  | 28px   | 40px | Maps want every pixel              |
| Closing        | 80px | 96px  | 80px   | 96px | Centered, generous                 |

Unlike the report recipe (which is built on a column grid), slides are
single-column. The horizontal padding plays the role of margins; layout
inside the live area is structural (flexbox), not grid.

## 2. Type sizes

Applies the [grammar's role hierarchy](../grammar.md#role-hierarchy) at
slide sizes. Anchor body at **24px / 1.55 leading**.

### Display tier

| Role               | Family         | Size  | Weight | Leading | opsz | Letter-spacing |
|--------------------|----------------|-------|--------|---------|------|----------------|
| Cover title        | Source Serif 4 | 64px  | 400    | 1.05    | 60   | -0.025em       |
| Break title        | Source Serif 4 | 56px  | 400    | 1.10    | 48   | -0.020em       |
| Closing title      | Source Serif 4 | 40px  | 400 italic | 1.25 | 36 | —              |
| H1 (slide head)    | Source Serif 4 | 40px  | 500    | 1.15    | 36   | -0.018em       |
| H2 (sub-head)      | Source Serif 4 | 26px  | 500    | 1.25    | 22   | -0.010em       |
| H3 (column head)   | Source Serif 4 | 20px  | 600    | 1.30    | 18   | -0.005em       |

Slide sizes are about **1.7× the report sizes** at each role — chosen for
projection legibility, not literal scaling. The grammar's role identity
(serif for voice, ink for text) is preserved.

### Body tier

| Role             | Family                | Size | Weight | Leading |
|------------------|-----------------------|------|--------|---------|
| Body             | Inter                 | 24px | 400    | 1.55    |
| Body emphasis    | Inter                 | 24px | 600    | 1.55    |
| Blockquote       | Inter                 | 22px | 400    | 1.50    |
| Code (inline)    | mono                  | 0.85em | 400  | —       |
| Code block       | mono                  | 18px | 400    | 1.5     |

### Chart-adjacent tier (chart slide)

| Role           | Family                | Size | Weight | Case      |
|----------------|------------------------|------|--------|-----------|
| Figure label   | Inter                  | 13px | 600    | UPPERCASE |
| Chart title    | Source Serif 4         | 26px | 500    | Sentence  |
| Chart source   | Source Serif 4 italic  | 16px | 400    | Sentence  |

Chart title ends with a period (it's a finding, not a label).

### Tables

| Role           | Family | Size  | Weight |
|----------------|--------|-------|--------|
| Table header   | Inter  | 20px  | 600    |
| Table cell     | Inter  | 20px  | 400    |

Slide tables fit ~6 rows × 4 cols comfortably. Past that, simplify or
split across two slides.

### Page chrome

| Role         | Family | Size | Weight | Case  | Color      |
|--------------|--------|------|--------|-------|------------|
| Folio        | Inter  | 11px | 500    | —     | `ink-3`    |
| Cover date   | Inter  | 14px | 700    | UPPER | `accent`   |
| Closing tag  | Inter  | 13px | 500    | UPPER | `ink-3`    |

Folios use tabular-nums. The cover date and any UPPER-case label gets
0.18em letter-spacing.

## 3. Spacing

- **Above an H1 on a content slide:** 0 (H1 anchors the top of the slide).
- **Below H1 → body:** 0.5em — but the body block is vertically
  centered in the remaining space via auto-margin, so this is a floor.
- **Paragraph:** 0.4em above and below.
- **List item:** 0.35em vertical.
- **Above the chart title (on a chart slide):** 6px below the eyebrow.
- **Below the chart:** 0.6em above the source line.
- **Between cover meta and display:** 96px (~1in) — the long drop is
  deliberate; it pulls the eye to the title.

## 4. Element patterns

### Cover slide

```
┌──────────────────────────────────────────────────────────────────────┐
│ MAY 2026                                                  [GL logo]  │  ← cover meta + logo
│                                                                      │
│                                                                      │
│  Pakistan's Path to Growth                                           │  ← display (Source Serif 4 64px)
│  Through Productive Diversification                                  │
│  ────────────────                                                    │  ← 3px accent rule, 50% width
│                                                                      │
│  Taimur Shah, Ricardo Hausmann, and Tim O'Brien                      │  ← byline (Source Serif 4 22px)
│                                                                      │
│  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │  ← rect-pattern-wide.svg, 0.65 opacity
└──────────────────────────────────────────────────────────────────────┘
```

**Rules:**

- Cover meta is **the date alone** — no series eyebrow. Authors who want a
  series tag can add an `#### Eyebrow` line above the date, but the default
  is date-only.
- Date: Inter 14px 700 UPPERCASE `accent`, 0.18em tracking.
- Logo top-right at **140px wide**, 56px from the top.
- Title rule is **3px solid `accent`, 50% width, left-anchored**. The
  theme inserts this automatically below the H1 — don't write a `---`.
- Authors: Source Serif 4 22px `ink-2`, comma-separated, "and" before
  the last name.
- Cover pattern is `rect-pattern-wide.svg` (mirror of the report's
  `rect-pattern.svg`, 1168 × 172 viewBox, baked-in 0.65 opacity) — sized
  to 100% slide width, anchored at the bottom edge.
- No folio on the cover.

### Content slide

```
┌──────────────────────────────────────────────────────────────────────┐
│ CHAPTER 01                                                           │  ← eyebrow (optional)
│ A macroeconomic recovery is underway.                                │  ← H1 (Source Serif 4 40px)
│                                                                      │
│                                                                      │
│  Inflation has fallen sharply, reserves have rebuilt, and the        │  ← body (Inter 24px), centered
│  current account is moving from a structural deficit toward          │     in the remaining space
│  balance — but the recovery rests on a narrow industrial base.       │
│                                                                      │
│                                                                      │
│                                                                  2   │  ← folio
└──────────────────────────────────────────────────────────────────────┘
```

H1 sits at the top; body block auto-centers in the remaining vertical
space. One idea per slide — the body is for the body of *that* idea,
not for a continued narrative.

### Chart slide

```
┌──────────────────────────────────────────────────────────────────────┐
│ FIGURE 1                                                             │
│ Reserves have rebuilt from the 2023 trough.                          │  ← chart title (Source Serif 4 26px)
│                                                                      │
│      [ chart fills the slide ]                                       │
│                                                                      │
│ Source: Growth Lab analysis of State Bank of Pakistan data.          │  ← source (Source Serif 4 italic 16px)
│                                                                  4   │
└──────────────────────────────────────────────────────────────────────┘
```

Compact eyebrow + title at the top, chart fills the rest, source line at
the bottom. Mirrors the report's figure-block role hierarchy at slide scale.

### Break slide

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│                                                                      │
│  PART TWO                                                            │  ← eyebrow in cover-bg tone
│  The growth question.                                                │  ← display (Source Serif 4 56px) in cover-bg
│  What would it take to translate macro stabilization into…?          │  ← italic subtitle, muted
│                                                                      │
│                                                                  7   │  ← folio in ink-4 tone
└──────────────────────────────────────────────────────────────────────┘
```

`ink-2` background (warm near-black). Type renders in `cover-bg` (warm
light) for contrast with the dark ground — the inversion of the content
slide.

### Closing slide

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│                                                                      │
│                                                                      │
│                       Thank you.                                     │  ← italic display, centered
│                                                                      │
│                CONTACT — name@host.edu                               │  ← UPPER tag + body link
│                                                                      │
│                                                                  9   │
└──────────────────────────────────────────────────────────────────────┘
```

`paper-warm` ground, italic Source Serif 4 display, eyebrow-style footer
in `ink-3`. Echoes the cover's warm tone — books-end the deck.

### Two-column (`.cols`)

```html
<div class="cols">
<div>

### Left column head

Body text in the left column.

</div>
<div>

### Right column head

Body text in the right column.

</div>
</div>
```

Equal columns with a 56px gutter. Use for parallel comparisons; not for
forcing two unrelated ideas onto one slide.

### Two-column with divider (`.cols.divided`)

```html
<div class="cols divided">
  <div>…</div>
  <div>…</div>
</div>
```

Adds a 1px `rule` hairline between the columns, with 32px padding on
each side. Use when the comparison **is** the slide — parallel arguments,
two interpretations of the same evidence, two options under consideration —
and the reader needs to *see* the division rather than infer it from
layout alone. Leave plain `.cols` for two-up chart layouts, where the
charts' own visual frames already mark the split.

## 5. Recipe-specific rules

These extend the [grammar's general rules](../grammar.md#4-rules) with
slide-specific values.

1. **Body size is 24px.** Don't push body text smaller — slides are read
   at distance.
2. **One idea per slide.** If a slide has two H1s' worth of content, it's
   two slides.
3. **Cover meta is the date alone.** No series eyebrow by default.
4. **Title rule is automatic.** Don't write `---` to make it appear; the
   theme inserts it under the cover H1.
5. **Chart titles end with a period.** Findings, not labels.
6. **Slide-page chrome is just the folio.** No running head, no series
   tag on every slide — the deck's identity sits on the cover.
7. **No body, no chart on a break slide.** It's a punctuation mark.

## 6. Quick reference

```
CANVAS: 1280 × 720 (16:9), Marp default
        Paper #FFFFFF (content); cover-bg #F3F2EA (cover);
        ink-2 #2C2823 (break); paper-warm #F4F1EA (closing)

PADDING: content 64 / 80 / 72 / 80 (T/R/B/L)
         chart   48 / 64 / 56 / 64
         break   80 / 96 / 80 / 96
         closing 80 / 96 / 80 / 96

FONTS:  Source Serif 4 (voice) + Inter (function)
BODY:   Inter 24px / 1.55 leading

TYPE SCALE (size / family / weight):
  Cover title    64 Serif 400, opsz 60, -0.025em
  Break title    56 Serif 400, opsz 48
  H1 slide head  40 Serif 500, opsz 36
  H2 sub-head    26 Serif 500, opsz 22
  H3 col head    20 Serif 600, opsz 18
  Chart title    26 Serif 500
  Closing        40 Serif 400 italic
  Body           24 Inter 400
  Cover date     14 Inter 700 UPPER accent, 0.18em
  Eyebrow / fig  13 Inter 600 UPPER accent, 0.14em
  Source line    16 Serif italic
  Folio          11 Inter 500 ink-3

COVER:  rect-pattern-wide.svg (1168 × 172, 0.65 opacity, bottom 100%)
        GL_logo_black.png at 140px wide, top-right
        Date alone in top-left; auto accent rule below H1

INK:    ink #1A1714 / ink-2 #2C2823 / ink-3 #4F4A42 / ink-4 #9A9389
ACCENT: #1A5A8E (= c-1-dark)
```
