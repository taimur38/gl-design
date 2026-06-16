# Contributing to the Growth Lab Design System

This document is for people **changing the design system itself**. If you just want to
*use* the kit, see [README.md](README.md).

## The one rule: values flow downward, never back up

There is no generated tokens file. Consistency is maintained by convention, so the
authority order must be explicit. A design value (a color hex, a font family, a type size,
a figure dimension) has exactly one home, and every other place that carries it is a
**downstream copy that must match**.

```
nil/            UPSTREAM INSPIRATION — Nil's original deliverables.
                Read-only. We distill from it; we never edit it, and it is not
                authoritative once distilled.
  ↓ distilled into
grammar.md      SOURCE OF TRUTH — canonical, medium-agnostic values: color ramps +
                palettes, type stack, weights, type scale, in-chart conventions.
                If a value disagrees anywhere, grammar.md wins. CHANGE TOKENS HERE FIRST.
  ↓ applied per medium
recipes/        Medium APPLICATIONS — page geometry, grid, figure sizes, per-medium type
                sizes (report.md, slide.md). May ADD medium-only values but must never
                CONTRADICT grammar.md.
  ↓ encoded as runnable form
DOWNSTREAM      Must MATCH grammar.md + the relevant recipe. Never a source of truth.
ENCODINGS       When a grammar/recipe value changes, update every file below that carries
                it, then re-render the playground to verify.
```

## Where each value lives downstream

When you change a token in `grammar.md`, grep these and update every copy that carries it:

| File | Carries |
|---|---|
| `skills/gl-ggplot/assets/theme_gl.R` | R: the `gl` token list, palettes, `save_fig` sizes, geom defaults |
| `skills/gl-ggplot/assets/gl_pdf.tex` | xelatex: font families + the color palette (R Markdown PDF route) |
| `skills/md2docx/assets/build_gl_template.py` | Python constants → `gl.docx` / `gl.dotx`. **Deliberate** px→pt and boolean-bold compromises live here, documented in-file |
| `skills/md2pdf/assets/md2pdf-style.css` | CSS `:root` vars (shared by md2html) |
| `skills/md2pdf-minimal/assets/md2pdf-style.css` | CSS `:root` vars (minimal fallback) |
| `skills/md2slides/assets/themes/gl.css` | Marp theme CSS |
| `showcase/framework-visual.html` | Illustrative walkthrough — must look current |

`nil/` and `playground/` are **out of scope** for drift checks: the former is upstream, the
latter is derived output.

## Auditing for drift (and for LLMs)

Treat `grammar.md` as ground truth. For each color hex / font family / type size it
defines, grep the downstream encodings above and flag any that differ. **A mismatch is a
bug in the downstream file, not in grammar.md** — unless the downstream file documents a
deliberate per-medium compromise (as `build_gl_template.py` does for Word).

## After any change: re-render the playground

The playground is the dogfood verifier. From the `pakistan-explore` working directory:

```bash
cd ~/dev/pakistan-explore
Rscript ~/dev/gl-design/playground/render_report_charts.R   # regenerate chart PNGs
```

Then render the demo report through the pipeline(s) you touched and eyeball the result:

```bash
skills/md2pdf/scripts/md2pdf   playground/demo-report.md /tmp/demo.pdf
skills/md2docx/scripts/md2docx --theme gl playground/demo-report.md /tmp/demo.docx
```

A change isn't done until the playground reflects it.

## Portability note

Skills must not hardcode absolute paths. `theme_gl.R` resolves the repo root in this order:
`GL_DESIGN_ROOT` → `CLAUDE_PLUGIN_ROOT` → the script's own location → `~/dev/gl-design`
(legacy fallback). New scripts should follow the same pattern — derive paths from
`${CLAUDE_PLUGIN_ROOT}` (commands/hooks) or the script's own location, never from a fixed
`/home/...` path.

## Packaging

The repo root is itself the Claude Code plugin: `.claude-plugin/plugin.json` +
`.claude-plugin/marketplace.json` declare it, and `skills/`, `commands/` auto-discover.
Adding a skill = drop it under `skills/` and add it to the `skills` array in
`marketplace.json`. Adding a command = drop a `.md` under `commands/` (do **not** list it
in `marketplace.json` — the `commands`/`skills`/`agents` fields there are directory-path
*overrides*, not file lists).

**The skills are plugin members, not standalone.** They deliberately share one source of
truth — `grammar.md`, `recipes/`, and `assets/fonts` at the plugin root — and reference it
via `../../grammar.md`-style links and `${CLAUDE_PLUGIN_ROOT}`. That resolves only because
the whole repo is the plugin root; a skill copied out on its own will break. This is why
the repo is packaged as one plugin rather than eight per-skill plugins, and why new skills
should keep referencing the shared files at the root rather than vendoring copies.

**Fonts on the plugin path.** `claude plugin install` does not run any script, so plugin
users must run `scripts/install-fonts.sh` once to register the fonts system-wide. Only the
R/ggplot path reads the bundled fonts directly; the PDF / slides / xelatex paths resolve
fonts by name from the OS. `scripts/install.sh` (the symlink fallback) calls
`install-fonts.sh` for you. Keep font logic in `install-fonts.sh`, not duplicated.
