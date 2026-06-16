---
description: Prime this session onto the Growth Lab design grammar — verify tooling, load the grammar + report recipe, and adopt GL conventions for every chart and document produced from here on.
allowed-tools: Bash(bash:*), Bash(Rscript:*), Read, Glob
---

# Growth Lab design kit — session primer

You are activating the Growth Lab design system for this working session. After this
command, **everything you produce — charts, reports, slides, briefs — must follow the
grammar below**, without the user having to restate it.

## 1. Tooling check

Run the doctor and report what's available. If anything required for a task the user
later asks for is missing, surface the exact fix from the doctor output — do not fail
silently.

!`bash "${CLAUDE_PLUGIN_ROOT}/scripts/doctor.sh"`

## 2. Load the source of truth

Read these now and treat them as authoritative for the rest of the session:

- @${CLAUDE_PLUGIN_ROOT}/grammar.md — color ramps, type stack, type scale, in-chart conventions (THE source of truth)
- @${CLAUDE_PLUGIN_ROOT}/recipes/report.md — figure sizes, page geometry, layout patterns for long-form output

For the full ggplot API and examples, the `gl-ggplot` skill is available; for rendering
markdown, the `md2docx` / `md2pdf` / `md2html` / `md2slides` skills are available; after
producing charts, use `chart-audit`.

## 3. Working agreement for this session

**Charts (R / ggplot2).** Every chart script starts with:

```r
source(paste0(Sys.getenv("CLAUDE_PLUGIN_ROOT"), "/skills/gl-ggplot/assets/theme_gl.R"))
gl_setup()                  # report mode; use gl_setup(mode = "slide") for standalone charts
```

(If `CLAUDE_PLUGIN_ROOT` is unset because the kit was installed via the symlink path,
source the `theme_gl.R` under `~/.claude/skills/gl-ggplot/assets/` instead — the root is
auto-detected either way.)

Then:

- **Do not override the theme per chart.** Let `theme_gl()` do the work; don't hand-tune
  font sizes, weights, or geom colors.
- **Highlight by muting.** Untyped geoms default to muted grey; overpaint the focus series
  in `highlight` (main blue `#2F87C8`). Lines/fills use the main tone; a highlighted point
  is `fill = highlight, color = highlight_dark` drawn **once** at `alpha = 1` (exclude it
  from the muted backdrop). Labels use the series' dark tone. Reserve `lead_finding`
  (red `#CC4948`) for stark lead-finding emphasis. Never `"red"`, `accent`, or arbitrary hex.
- **Color scales** apply automatically; use `scale_color_gl("hs_sectors")` /
  `scale_fill_gl(...)` for named palettes, `scale_*_gl_gradient(...)` for continuous.
- **Save** with `save_fig("full", "name.png")` — named sizes only (`full`, `full_tall`,
  `full_square`, `major`, `half`, `half_tall`, `slide`).
- **Log scale** (`scale_x_log10()`) whenever GDP per capita is on the x-axis.
- After generating charts, run the **chart-audit** checklist.

**Documents.** Render markdown through the GL pipelines, not ad-hoc pandoc:

```bash
"${CLAUDE_PLUGIN_ROOT}/skills/md2docx/scripts/md2docx" --theme gl in.md out.docx   # Word
"${CLAUDE_PLUGIN_ROOT}/skills/md2pdf/scripts/md2pdf"   in.md out.pdf               # PDF
"${CLAUDE_PLUGIN_ROOT}/skills/md2html/scripts/md2html" in.md out.html              # HTML
"${CLAUDE_PLUGIN_ROOT}/skills/md2slides/scripts/md2slides" in.md out.pdf           # 16:9 deck
```

Confirm to the user, in one line, that the GL design kit is active and note anything the
doctor flagged as missing.
