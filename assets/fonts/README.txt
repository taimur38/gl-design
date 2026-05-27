Growth Lab brand fonts
======================

Two families do all the work:

  Source Serif 4   — voice; long-form and display text. Variable font with
                     weight (100–900) and opsz (8–60) axes. Used for the
                     cover title, all headings, lead paragraphs, chart
                     titles, chart sources (italic), colophon body, and
                     footnote markers.
                     https://github.com/adobe-fonts/source-serif (v4.005R)

  Inter            — function; UI, labels, body text. Variable font with
                     weight (100–900) axis. Used for body copy, chart
                     labels and ticks, table headers and cells, eyebrows,
                     figure labels, page chrome, and any small uppercase
                     label.
                     https://github.com/rsms/inter (v4.0)

Layout
------

source-serif-4/
  ttf/    SourceSerif4Variable-Roman.ttf, SourceSerif4Variable-Italic.ttf
  woff2/  SourceSerif4Variable-Roman.woff2, SourceSerif4Variable-Italic.woff2

inter/
  ttf/    InterVariable.ttf, InterVariable-Italic.ttf
  woff2/  InterVariable.woff2, InterVariable-Italic.woff2

legacy/                    Older font families from the pre-nil-design
                           system (Source Sans 3, JetBrains Mono,
                           Crimson Pro). Kept for reference; not
                           referenced by current tooling.

License
-------

Both Source Serif 4 (LICENSE-Source-Serif-4.md) and Inter (LICENSE-Inter.txt)
are licensed under the SIL Open Font License v1.1. The OFL permits free use,
embedding, modification, and redistribution — including bundling the font
files in a website.

Recommended use on the web
--------------------------

Serve the woff2 variable files. A ready-to-paste @font-face block is in
fonts.css. Variable fonts let CSS animate the weight axis and (for Source
Serif 4) the optical-size axis via `font-variation-settings: 'opsz' 60`.

Optical sizing (Source Serif 4)
-------------------------------

When using Source Serif 4 at display sizes, set the opsz axis to match:
  - opsz 60 for cover-display sizes (~56pt+)
  - opsz 36 for section headings (~34pt)
  - opsz 22 for subsection headings (~20pt)
  - opsz 18 for the lead paragraph (~17pt)
  - opsz 14 for body, chart titles, and captions (~12–14pt)

Honoring the axis is what makes the display cut feel like display type and
the text cut feel like text type — the same family contains genuinely
different glyph shapes at each optical size.
