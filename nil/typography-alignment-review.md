# Typography — alignment review

> Compares Nil's typography spec (`typography-spec.html`, transcribed in
> [`typography-rules.md`](typography-rules.md)) against how the design system
> currently encodes type: [`grammar.md`](../grammar.md),
> [`recipes/report.md`](../recipes/report.md), and the runtime CSS in
> [`skills/md2pdf/assets/md2pdf-style.css`](../skills/md2pdf/assets/md2pdf-style.css).
>
> Severity is my read, not a verdict.

## Actions taken (2026-06-02)

Resolved A, B, and D below in favor of Nil's spec (which the runtime CSS already
matched for A1):

- **A1** — `grammar.md` + `report.md` cover authors changed `ink-2` → `ink`
  (matches Nil and the md2pdf CSS); removed the "ink-2, not ink-3" rationale.
- **A2** — added a `cover-disk` `#ECEBE0` token to `grammar.md` and
  `theme_gl.R`; corrected `paper-warm`'s role (it never was the medallion disk);
  `report.md` now points the medallion at `cover-disk`. *(Note: the disk is
  documentation-only — `circle-pattern.svg` renders no disk — so this is a token
  + prose correction, not a render change.)*
- **A3** — `report.md` reference title 10pt → 11pt (one step above the body).
- **B1 / B2** — added "References page" (closing nameplate footer) and "Colophon
  page" (address block + imprint paragraphs) element patterns to `report.md` §5.
- **B3** — `report.md` TOC page numbers split: major `ink`/700, sub `ink-2`/500.
- **D1** — added a note to `grammar.md`'s optical-sizing table that recipes
  rescale opsz to their rendered size.

**Still open — Section C (additions beyond Nil's spec).** Left unchanged; these
are working extensions that only Nil can bless: C1 the H3 heading level, C2 the
`ink-4` chart token, C3 the broadened `accent` scope. See §C for detail.

## How the system already diverges *on purpose* (context, not a problem)

Nil's spec is in **px** (it's an HTML mockup). The report recipe translates to
**print pt** — roughly px × 0.75, rounded to typographer-friendly values
(56px→44pt display, 34px→26pt H1, 20px→16pt H2), while body/footnote stay
anchored to print readability (12pt/9pt). This is documented in `report.md` §3
and `followups.md`. The md2pdf CSS goes further: it keeps the **cover** at
literal px (56/11/14 — "match Nil literally") but renders **content headings**
in pt. So conversions below are expected and *not* flagged. Only genuine
mismatches are.

---

## A. Substantive divergences (color / size / semantics)

### A1. Cover authors color — `ink` vs `ink-2` *(medium)*
- **Nil:** cover authors = `--ink` (#1A1714). The anatomy diagrams also label it "Authors (serif, 14px, --ink)."
- **grammar.md** (role table) and **report.md** (§5) say `ink-2`, and report.md explicitly argues *"ink-2, not ink-3 — the byline carries voice."*
- **But the runtime CSS** (`md2pdf-style.css` `.author`) uses `--ink` — i.e. it matches Nil, not the docs.
- → The two **docs disagree with both Nil and their own implementation.** Decide: authors in `ink` (align docs to Nil + CSS) or `ink-2` (a deliberate softening — then fix the CSS).

### A2. Report-cover / colophon medallion disk color — `#ECEBE0` vs `paper-warm #F4F1EA` *(medium)*
- **Nil:** the circular medallion sits in a `#ECEBE0` disk, defined as "one tone darker than the cover paper #F3F2EA."
- **grammar.md** (§Paper & chrome) and **report.md** (§5 + quick ref) both call this disk `paper-warm` (#F4F1EA).
- `#ECEBE0` ≠ `#F4F1EA` — close, but a different swatch.
- → Decide: add an `#ECEBE0` token (e.g. `medallion-disk`) and point the docs at it, or accept `paper-warm` as the approved substitute.

### A3. Reference title size — 11px vs 10px *(low)*
- **Nil:** reference body is 10px, but the italic serif **title** (`<em>`) is bumped to **11px** — one step larger.
- **report.md** sets reference title at 10pt, same as the body.
- → Decide whether to restore the one-step bump on reference titles.

---

## B. Gaps — in Nil's spec, missing from grammar / recipe

### B1. References closing footer (nameplate sign-off) *(low)*
- **Nil:** the references page closes with a 1px `--rule` hairline + an Inter 9px / 500 / uppercase / 0.16em / `--ink-3` eyebrow ("Growth Lab · Harvard Kennedy School").
- Not described in grammar.md or report.md. → Add to the report recipe?

### B2. Colophon address block *(low)*
- **Nil:** Inter 10px / 600 / uppercase / 0.18em / `--ink-2`, leading 1.7, five stacked lines — reads as a nameplate.
- report.md covers colophon body prose but not the address block. → Add?

### B3. TOC page-number differentiation by level *(low)*
- **Nil:** major folio = `ink` weight 700; sub folio = `ink-2` weight 500.
- **report.md** flattens TOC page numbers to a single 11pt / 500 (no color/weight split by level).
- → Decide whether the level distinction matters.

---

## C. Additions — in grammar / recipe, not in Nil's typography spec

These extend Nil; likely fine but worth confirming none contradict her intent.

### C1. H3 / sub-subsection *(confirm)*
- **report.md** + CSS define an H3 (Source Serif 4, 14pt, weight 600, opsz 16).
- **Nil's spec has only section (h1) and subsection (h2)** — no third heading level. → Confirm H3 is a sanctioned extension (reports often need it).

### C2. `ink-4` (#9A9389) *(confirm)*
- **grammar.md** adds a 4th ink layer. **Nil's typography palette is 3 inks + accent.**
- grammar scopes ink-4 to "inside the chart panel," justified by the data-vis spec — so it's a chart token, not a text token. Probably fine; noting for completeness.

### C3. Accent scope is broader than Nil's rule *(confirm)*
- **Nil decision-rule 5:** reach for `--accent` *"only for eyebrows and the cover date."*
- **grammar.md** also lists accent for "figure labels, footnote anchor, accent text."
- These extra uses are reconciled by the **data-vis spec** (figure label = accent #1A5A8E) and by Nil's own colophon footnote anchor (accent italic) — so they're consistent across the *two* specs, just broader than the typography doc's stand-alone rule. → Confirm the cross-spec reconciliation is intended.

---

## D. Internal inconsistency to resolve regardless of Nil

### D1. opsz values: grammar table vs recipe/CSS — *resolved via the px switch*
- Originally: grammar listed Nil's opsz (60/36/22/18) while report/CSS used rescaled values (48/28/18/16).
- Resolved by the **px-everywhere decision (see §E)**: the report now renders at Nil's exact px sizes, so it uses Nil's opsz as-is. grammar's note was updated to say recipes only rescale opsz when they render at a *different* scale (e.g. a pt-native docx).

---

## E. Unit decision — px everywhere (2026-06)

You chose to make the **HTML→PDF report the source of truth and author it in px**, 1:1 with Nil (CSS px is an absolute print unit — `96px = 72pt = 1in` — so it renders deterministically; and Nil designed at real 8.5×11in geometry, so her px *are* print sizes). Actioned:

- **md2pdf CSS** (`skills/md2pdf/assets/md2pdf-style.css`) and **md2pdf-minimal CSS** — all font sizes converted pt → Nil's px (body 12px, H1 34px, H2 20px, lead 17px, etc.); table paddings to Nil's px; leading/opsz aligned to Nil. Code blocks stay in pt (not a Nil element).
- **report.md** §3/§4/§5/§7 — type tables, spacing, ASCII diagrams, and quick-ref all rewritten in px; added an explanation of why px (not pt).
- **grammar.md** — opsz note revised (D1).
- **followups.md** §9 — history note updated to record the reversal; §1/§2 numbers updated to px.
- **build_gl_template.py** (docx) — left in pt with a new comment: it is now an explicit best-effort approximation (literal 1px→1pt, ~33% larger than the PDF).

**Consequence to be aware of:** body is now 12px = **9pt physical** — dense, editorial, and exactly Nil's reference (the recipe had previously bumped it to 12pt for comfort).

**Open:** whether to rescale the docx template ×0.75 so Word matches the PDF physically (body 9pt, footnotes 6.75pt), or keep Word print-readable but ~33% larger than the canonical PDF.

---

## Verdict

The system is **faithful to Nil overall** — families, weights, case rules, ink
layering, the two-line cover meta, "no trailing periods on headings,"
tabular-nums, and the no-monospace rule all match. The open items are A1
(authors color — the only place a doc contradicts both Nil and the running
code), A2 (disk swatch), and a handful of low-severity gaps/additions. Nothing
here blocks rendering; they're consistency calls for you.
