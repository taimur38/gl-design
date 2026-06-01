---
name: md2html
description: Convert markdown files to a self-contained, GL-styled HTML document. Same pipeline as md2pdf but stops at HTML and embeds all assets as data URIs so the file is portable. Use this skill when the user wants to render markdown to HTML, share for review, or inspect what the PDF will look like before printing.
compatibility: Requires pandoc and pandoc-crossref. Shares the template and stylesheet with the md2pdf skill.
metadata:
  author: taimur-shah
  version: "1.0"
---

# GL md2html

Render a markdown source to a **single, self-contained HTML file** that
follows the [Growth Lab visual grammar](../../grammar.md) and the
[report recipe](../../recipes/report.md). The pipeline is identical to
[`md2pdf`](../md2pdf/SKILL.md) except for the final step:

```
                       pandoc-crossref
                       --citeproc            ┌─→ html writer + --embed-resources → output.html   (md2html)
input.md → pandoc ─────template.html5 ───────┤
references.bib                               └─→ html writer ──→ headless Chromium ──→ output.pdf  (md2pdf)
```

The `--embed-resources` flag inlines every referenced image, stylesheet,
and font into the output HTML as base64 data URIs, so the file opens in
any browser without needing the source repo on disk.

## Usage

```bash
md2html input.md             # outputs input.html alongside the source
md2html input.md output.html # outputs to a specific path
```

## When to use it vs. md2pdf

- **md2html** — sharing for design review, on-screen reading, embedding in
  email or a web preview, getting an inspectable artifact that someone can
  open Chrome devtools on and tweak CSS in directly.
- **md2pdf** — the final printable deliverable.

The two produce the **same visual output** modulo Chromium's print rendering
(paged media, page numbers via `@page { @bottom-right { content: counter(page) } }`,
forced page breaks, etc.). The PDF has explicit pagination; the HTML
naturally flows as a single long page.

## Markdown features supported

Same as md2pdf — see [`../md2pdf/SKILL.md`](../md2pdf/SKILL.md) for the full
list. Quick recap:

| Markdown                       | Renders as                                |
|--------------------------------|-------------------------------------------|
| YAML frontmatter (title, subtitle, author, date, series) | cover page |
| `::: {.box title="..."}`       | callout with eyebrow + accent left border |
| `![cap](path){#fig:label}`     | numbered figure                           |
| `@fig:label`                   | cross-reference                           |
| `[@key]` + `references.bib`    | citation + bibliography                   |

## Cover assets

The cover renders with two image assets by default, both embedded:

- `cover-pattern`: `assets/design-library/cover-patterns/rect-pattern.svg`
- `cover-logo`: `assets/design-library/logos/GL_logo_black.png`

Override per-document via YAML frontmatter:

```yaml
---
title: "..."
cover-pattern: "path/to/your-pattern.svg"
cover-logo: "path/to/your-logo.png"
---
```

## Asset sharing with md2pdf

The script reads `template.html5` and `md2pdf-style.css` directly from the
sibling `../md2pdf/assets/` directory. There is no copy. If you tweak the
CSS or template for the PDF, the HTML follows automatically (and vice
versa).
