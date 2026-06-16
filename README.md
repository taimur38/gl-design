# Growth Lab Design System

A visual grammar for all Growth Lab outputs — reports, slides, briefs, charts — codified
as a **source-of-truth grammar**, per-medium **recipes**, and the **runnable tools** that
apply them (an R/ggplot theme, markdown→Word/PDF/HTML/slide pipelines, and audit
checklists). The goal: you absorb the system by *using* it, not by reading a spec.

> Designing or changing the system itself? See **[CONTRIBUTING.md](CONTRIBUTING.md)** for
> the source-of-truth flow (`grammar.md` → recipes → encodings). This README is for
> *using* the kit.

## What you get

Run `/design-kit` in any project and the rest of your session inherits the grammar: charts
use the GL theme, documents render through the GL pipelines, no restating required. The kit
ships these skills:

| Skill | Does |
|---|---|
| **gl-ggplot** | GL theme, palettes, and `save_fig` sizes for R/ggplot2 charts |
| **chart-audit** | Visual audit checklist to run after generating charts |
| **md2docx** | Markdown → Word (.docx) with citations + cross-references |
| **md2pdf** | Markdown → styled PDF |
| **md2html** | Markdown → self-contained, portable HTML |
| **md2slides** | Markdown → 16:9 PDF slide deck (Marp) |
| **md2pdf-minimal** | Node-only fallback for PDF when the pandoc path is unavailable |
| **gl-docx-retheme** | Restyle an existing Word doc to the GL theme |

> **These skills ship together as the `gl-design` plugin — they are not standalone.**
> They share one source of truth: `grammar.md` and `recipes/` at the plugin root. The
> skills reference those shared files (and the bundled fonts), so copying a single skill
> directory out on its own will break it. Install the whole kit, not one skill.

## Install

### 1. Clone

```bash
git clone https://github.com/taimur38/gl-design.git
cd gl-design
```

### 2. Check / install dependencies

The kit leans on a few external tools (pandoc + pandoc-crossref, headless Chromium, Node +
Marp, R with ggplot2/systemfonts/ragg). Run the doctor to see what's present and get the
exact install command for anything missing:

```bash
bash scripts/doctor.sh
```

It does **not** install anything — it tells you what to run. Install the items it marks `✗`.

### 3. Install the skills

**Preferred — Claude Code plugin** (auto-updates from git, no symlinks):

```bash
claude plugin marketplace add ./           # or: taimur38/gl-design once pushed
claude plugin install gl-design
bash scripts/install-fonts.sh              # one-time: register fonts system-wide
```

The plugin install gives you the skills and `/design-kit`. It does **not** register the
fonts — and the PDF, slides, and xelatex paths resolve fonts by name from the OS (the
R/ggplot path reads the bundled fonts directly and needs nothing). So run
`scripts/install-fonts.sh` once after installing.

**Fallback — symlink script** (if you're not on the plugin system):

```bash
bash scripts/install.sh
```

This symlinks the eight skills into `~/.claude/skills/`, installs the fonts (via
`install-fonts.sh`), and re-runs the doctor.

## Use

In any project:

```
/design-kit
```

This verifies tooling, loads `grammar.md` + the report recipe, and adopts GL conventions
for the session. From there, just ask for charts or documents as normal — they'll follow
the grammar. You can also invoke any sub-skill directly (e.g. "convert this to a Word doc"
triggers `md2docx`).

Charts, by hand, start with:

```r
source(paste0(Sys.getenv("CLAUDE_PLUGIN_ROOT"), "/skills/gl-ggplot/assets/theme_gl.R"))
gl_setup()
```

The repo root is auto-detected, so the legacy `source("~/dev/gl-design/...")` form keeps
working too. Set `GL_DESIGN_ROOT` to override.

## Layout

```
grammar.md          SOURCE OF TRUTH — color, type, chart conventions
recipes/            Per-medium applications (report.md, slide.md)
intention.md        Why the system exists
skills/             The eight runnable skills (theme, pipelines, audits)
assets/             Fonts + brand library that the skills consume
commands/           /design-kit session primer
scripts/            doctor.sh (check deps) · install-fonts.sh (register fonts) · install.sh (symlink fallback)
playground/         Dogfood report that exercises the whole kit end-to-end
showcase/           Interactive walkthrough of the system (open in a browser)
nil/                Upstream design inspiration (read-only)
```
