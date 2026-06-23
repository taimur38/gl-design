# theme_gl.R — Growth Lab design system for ggplot2
#
# Usage (source by whatever path the kit lives at — the root is auto-detected):
#   source(".../skills/gl-ggplot/assets/theme_gl.R")
#   gl_setup()                          # loads fonts, sets theme + defaults
#   gl_setup(mode = "slide")            # slide mode (keeps title/subtitle)
#
# Requires: ggplot2, systemfonts, ragg (ragg pulls in textshaping)

library(ggplot2)
library(systemfonts)

# ---- Design tokens (grammar.md) ---------------------------------------------
#
# Ink ramp — warm, four layers (browns, not neutral greys).
# Accent — primary blue + variants. Same hex as c_1_dark by design.
# Categorical palette — six hues, three tones each (light / main / dark).
#   - Main = fills (bars, lines, treemap, scatter circles).
#   - Dark = strokes on overlapping marks + every label/legend/annotation
#            tied to the series (WCAG AA contrast against paper).
#   - Light = backgrounds, faded states, sequential ramp tail.
# c_muted (also light/main/dark) — cool grey for "everyone else".

gl <- list(
    # Ink ramp
    ink         = "#1A1714",
    ink_2       = "#2C2823",
    ink_3       = "#4F4A42",
    ink_4       = "#9A9389",

    # Accent (= c_1_dark)
    accent      = "#1A5A8E",
    accent_deep = "#003E6B",
    accent_soft = "#3A85B8",
    accent_tint = "#E1F0FA",

    # Paper & chrome
    paper       = "#FFFFFF",  # Content pages — pure white
    paper_warm  = "#F4F1EA",  # Accent panels, code / quote tint
    cover_bg    = "#F3F2EA",  # Cover only
    cover_disk  = "#ECEBE0",  # Report-cover medallion disk (one tone darker than cover_bg)
    rule        = "#DDDDDD",  # Hairline borders
    gridline    = "#D8D4CC",  # In-chart gridlines

    # Categorical — three tones per hue
    c_1_light = "#B5D5EA", c_1 = "#2F87C8", c_1_dark = "#1A5A8E",   # Blue
    c_2_light = "#E89C9C", c_2 = "#CC4948", c_2_dark = "#8A2C2B",   # Red
    c_3_light = "#92D6BF", c_3 = "#2AA584", c_3_dark = "#1A6B53",   # Teal
    c_4_light = "#B5A0CC", c_4 = "#7554A3", c_4_dark = "#4A3470",   # Purple
    c_5_light = "#F4BC8A", c_5 = "#EA822D", c_5_dark = "#A8580F",   # Orange
    c_6_light = "#E6E2A8", c_6 = "#CDC86B", c_6_dark = "#8A8638",   # Yellow

    # Muted gray — "everyone else"
    c_muted_light = "#CDD2D9",
    c_muted       = "#AFB5BE",
    c_muted_dark  = "#5F6773",

    # Full categorical palette (main tones, in order)
    palette = c("#2F87C8", "#CC4948", "#2AA584",
                "#7554A3", "#EA822D", "#CDC86B")
)

# Top-level aliases so user code reads naturally
# Data-mark focus colors are the MAIN tone — fills (bars, areas, point
# interiors) and highlighted lines all use the main tone (spec §5). Their
# *_dark partners are ONLY for strokes on those marks and for any text/label
# tied to them (Decision Rule 2). Both focus colors are main tones so they are
# consistent: highlight = c_1 (blue), lead_finding = c_2 (red).
#
# `accent` is a SEPARATE thing: non-data UI chrome (eyebrows, figure labels,
# links) and is the dark tone by design. Do NOT use `accent` as a data fill —
# that is the typography↔data-viz mix-up to avoid.
highlight         <- gl$c_1       # main blue (#2F87C8) — default data focus:
                                  # bar/area/point fills + highlighted lines.
highlight_dark    <- gl$c_1_dark  # #1A5A8E — stroke on a highlighted point and
                                  # the label/text tied to the highlight.
lead_finding      <- gl$c_2       # main red (#CC4948) — stark lead-finding
                                  # emphasis (gains vs. losses, alarm). Sparingly.
lead_finding_dark <- gl$c_2_dark  # #8A2C2B — stroke/label for the lead finding.
c_muted      <- gl$c_muted    # cool grey, "everyone else"
accent       <- gl$accent     # #1A5A8E — non-data UI chrome only (eyebrows,
                              # figure labels, links). NOT a data-mark fill.
highlight_sz <- 0.65          # linewidth for the highlighted focus line (~2.4px).
                              # Standard/muted lines default to 0.5 (~2px); the
                              # focus is only ~1.3x thicker, per spec §5
                              # (2px standard / 2.4px highlight) — not a 2x jump.

# ---- Named palettes ---------------------------------------------------------
#
# `categorical` is the default 6-color discrete palette.
# `sequential_*` and `diverging_*` are ordered ramps for choropleths /
# heatmaps / continuous encodings — pair with scale_*_gl_gradient() for
# continuous data, or scale_*_gl() for discrete (binned) data.
# The sector palettes are external Growth Lab standards.

gl_palettes <- list(
    # Default categorical (6 colors) — main tones, all fill work.
    categorical = gl$palette,

    # Dark tones, same order — strokes on overlapping marks + EVERY text
    # element tied to a series (direct labels, legend, callouts, annotations).
    # Required for WCAG AA against paper (Decision Rule 2). Pair a dark color
    # scale with a main fill scale: scale_color_gl("categorical_dark") +
    # scale_fill_gl("categorical").
    categorical_dark = c("#1A5A8E", "#8A2C2B", "#1A6B53",
                         "#4A3470", "#A8580F", "#8A8638"),

    # Light tones, same order — backgrounds, faded states, and the fills for
    # the two/three-tone single-hue option.
    categorical_light = c("#B5D5EA", "#E89C9C", "#92D6BF",
                          "#B5A0CC", "#F4BC8A", "#E6E2A8"),

    # Sequential 5-step ramps (low → high)
    sequential_1 = c("#E5F0F9", "#B5D5EA", "#6FA5CE", "#2F87C8", "#1A5A8E"),  # Blue
    sequential_2 = c("#F4D5D5", "#E89C9C", "#DC6F6E", "#CC4948", "#8A2C2B"),  # Red
    sequential_3 = c("#D5EFE7", "#92D6BF", "#5BC0A0", "#2AA584", "#1A6B53"),  # Teal
    sequential_4 = c("#E5DDF0", "#B5A0CC", "#9276BA", "#7554A3", "#4A3470"),  # Purple
    sequential_5 = c("#FBE5D5", "#F4BC8A", "#EE9A52", "#EA822D", "#A8580F"),  # Orange
    sequential_6 = c("#FBF8DC", "#E6E2A8", "#DCD68E", "#CDC86B", "#8A8638"),  # Yellow

    # Diverging 6-step palettes (negative tail → midpoint → positive tail)
    diverging_2_1 = c("#8A2C2B", "#DC6F6E", "#EFC7C0",
                     "#C5DCEC", "#6FA5CE", "#1A5A8E"),  # Red ↔ Blue (default)
    diverging_3_1 = c("#1A6B53", "#5BC0A0", "#BDE5D8",
                     "#C5DCEC", "#6FA5CE", "#1A5A8E"),  # Teal ↔ Blue
    diverging_5_1 = c("#A8580F", "#EE9A52", "#F4BC8A",
                     "#C5DCEC", "#6FA5CE", "#1A5A8E"),  # Orange ↔ Blue
    diverging_6_1 = c("#8A8638", "#DCD68E", "#E6E2A8",
                     "#C5DCEC", "#6FA5CE", "#1A5A8E"),  # Yellow ↔ Blue

    # Atlas HS product sectors — external standard, unchanged
    hs_sectors = c(
        "Services"    = "#b23c6f",
        "Textiles"    = "#7bc8a4",
        "Agriculture" = "#e5c21a",
        "Stone"       = "#caa46b",
        "Minerals"    = "#a88b7d",
        "Metals"      = "#c9656b",
        "Chemicals"   = "#b07ac9",
        "Vehicles"    = "#7a6cc3",
        "Machinery"   = "#6e8fc3",
        "Electronics" = "#74c5c6",
        "Other"       = "#2f5d74"
    ),

    # Atlas SITC product sectors — external standard, unchanged
    sitc_sectors = c(
        "Services"                = "#b23c6f",
        "Food"                    = "#e5c21a",
        "Beverages"               = "#e76f8f",
        "Crude Materials"         = "#cf6f6f",
        "Fuels"                   = "#b39183",
        "Vegetable Oils"          = "#f39c12",
        "Chemicals"               = "#b07ac9",
        "Material Manufacturers"  = "#d73027",
        "Machinery & Vehicles"    = "#6e8fc3",
        "Other Manufacturers"     = "#1f9d9a",
        "Unspecified"             = "#355f73"
    ),

    # Product space clusters — external standard, unchanged
    product_space = c(
        "Agricultural Goods"        = "#e0b614",
        "Construction Goods"        = "#c77c2b",
        "Electronics"               = "#5cc7c6",
        "Chemicals & Basic Metals"  = "#9c3bd6",
        "Metalworking Machinery"    = "#c43d3d",
        "Minerals"                  = "#7a6a63",
        "Textile & Home Goods"      = "#8a8a8a",
        "Apparel"                   = "#2fa84f"
    )
)

# ---- Theme -------------------------------------------------------------------
#
# Family conventions (from grammar.md):
#   gl_serif  — Source Serif 4, for chart title (mode = "slide" only).
#   gl_sans   — Inter, for axis, legend, strip, subtitle, body of chart.
#   Italic serif — used for plot.caption (chart source).
#
# In-chart chrome (grammar.md §3.5):
#   axis line   — 1px ink-2, bottom + left only (no panel border)
#   tick mark   — 1px ink-2, 4pt outward
#   gridline    — 1px gl$gridline (#D8D4CC), horizontal only by default
#                 (Nil's rule: never both X and Y unless the chart is dense).
#                 Override with theme(panel.grid.major.x = element_line(...))
#                 when the chart genuinely needs vertical gridlines.
#   strip       — no background fill, bold sans label.
#
# Base is theme_minimal — gives no panel border / no frame by default, then
# we add the bottom+left axis lines explicitly. (theme_few would add a frame.)
#
# Tooling note: fonts are registered via systemfonts (see gl_register_fonts),
# NOT showtext — so OpenType features reach the render path. In particular,
# every Inter family carries tabular figures (`tnum`), which showtext could not
# enable. The variable-font optical-size (opsz) axis is still NOT applied at
# render time, so glyphs render at the font's default optical size.

theme_gl <- function(base_size = 12, mode = "report") {
    t <- theme_minimal(base_size = base_size) %+replace%
        theme(
            text = element_text(family = "gl_sans", color = gl$ink_2),

            # Chart title — Source Serif 4 14pt weight 500, ink.
            plot.title = element_text(
                family = "gl_serif", face = "bold",
                size = rel(14 / 12), hjust = 0,
                color = gl$ink,
                margin = margin(b = 4)
            ),

            # Chart subtitle — Inter 12pt ink-3.
            plot.subtitle = element_text(
                family = "gl_sans",
                size = rel(1.0), hjust = 0,
                color = gl$ink_3,
                margin = margin(b = 10)
            ),

            # Chart source — Source Serif 4 italic 12pt ink-2.
            plot.caption = element_text(
                family = "gl_serif", face = "italic",
                size = rel(1.0), hjust = 0,
                color = gl$ink_2,
                margin = margin(t = 8)
            ),

            # Axes — Inter, ink-2. Label weight 500, tick weight 400.
            # Axis label is Inter 500 (gl_sans_medium), NOT 600 — the spec
            # reserves 600 for figure labels and series labels.
            # Axis label sits ~20px (≈15pt) off the tick labels — far enough that
            # a wide tick like "250" can't collide with the rotated Y title
            # (Nil data-vis §4 / Decision rule). Was 6pt — too tight.
            axis.title   = element_text(family = "gl_sans_medium", color = gl$ink_2,
                                        size = rel(1.0)),
            axis.title.x = element_text(margin = margin(t = 15)),
            axis.title.y = element_text(margin = margin(r = 15), angle = 90),
            # Tick label sits 6px outside the axis = 4pt tick + 2pt gap.
            axis.text    = element_text(family = "gl_sans", color = gl$ink_2,
                                        size = rel(1.0)),
            axis.text.x  = element_text(margin = margin(t = 2)),
            axis.text.y  = element_text(margin = margin(r = 2)),

            # Axis line + ticks: 1px ink-2, 4pt outward. Bottom + left only.
            axis.line          = element_line(color = gl$ink_2, linewidth = 0.4),
            axis.ticks         = element_line(color = gl$ink_2, linewidth = 0.4),
            axis.ticks.length  = unit(4, "pt"),

            # No panel border, paper background.
            panel.background   = element_rect(fill = gl$paper, color = NA),
            plot.background    = element_rect(fill = gl$paper, color = NA),
            panel.border       = element_blank(),

            # Gridlines: horizontal only by default; no vertical, no minor.
            panel.grid.major.y = element_line(color = gl$gridline, linewidth = 0.4),
            panel.grid.major.x = element_blank(),
            panel.grid.minor   = element_blank(),

            # Legend — Inter 12pt ink-2. Legend entries ARE series labels, so
            # they take series-label weight 600 (spec §3): face="bold" maps
            # gl_sans to its semibold (600) face. The legend title stays 400.
            legend.title = element_text(family = "gl_sans", color = gl$ink_2,
                                        size = rel(1.0)),
            legend.text  = element_text(family = "gl_sans", color = gl$ink_2,
                                        face = "bold", size = rel(1.0)),

            # Facet strip — Inter bold, ink-2, no background.
            strip.background = element_blank(),
            strip.text       = element_text(family = "gl_sans", color = gl$ink_2,
                                            size = rel(1.0), face = "bold",
                                            margin = margin(b = 6))
        )

    if (mode == "report") {
        # In report mode, the document handles figure label / chart title /
        # subtitle / source — the chart itself only contains axes and legend.
        t <- t + theme(
            plot.title           = element_blank(),
            plot.subtitle        = element_blank(),
            plot.caption         = element_blank(),
            legend.position      = "bottom",
            legend.justification = "left",
            legend.margin        = margin(t = 4),
            legend.key.size      = unit(0.4, "cm")
        )
    }

    t
}

# ---- Geom defaults -----------------------------------------------------------
#
# The GL chart pattern is: paint everyone in muted grey first, then re-paint
# the focus series in `highlight` (red) or `accent` (blue) on top.
#
#   geom_col() +                                  # all bars muted (default)
#   geom_col(data = \(d) filter(d, focus),
#            fill = highlight)                    # focus bar red
#
# For this to work, an untyped geom must default to *muted*, not c-1. The
# author opts *in* to color explicitly — that's the "color only when
# necessary" principle (Nil §IX rule 1). Setting the default to c-1 would
# force authors to manually mute every supporting layer.
#
# So:
#   geom_line / path / step                      → c_muted_dark line
#   geom_point                                   → shape 21, c_muted fill +
#                                                  c_muted_dark stroke, 0.8 alpha
#   geom_col / bar                               → c_muted fill + 1px paper stroke
#   geom_area / ribbon                           → c_muted fill, no stroke
#   geom_smooth                                  → c_muted_dark line + light ribbon
#   geom_boxplot                                 → recedes: c_muted_light fill,
#                                                  c_muted outline (background dist.)
#   geom_hline / vline                           → dashed ink_3 (reference line)
#   geom_text / label                            → ink_2 (body color)
#
# Called from gl_setup() — these mutate global ggplot2 state.

gl_set_geom_defaults <- function() {
    # Lines read as "data" — darker grey (c_muted_dark) so a single-series
    # chart looks substantive.
    update_geom_defaults("line",    list(colour = gl$c_muted_dark, linewidth = 0.5))
    update_geom_defaults("path",    list(colour = gl$c_muted_dark, linewidth = 0.5))
    update_geom_defaults("step",    list(colour = gl$c_muted_dark, linewidth = 0.5))

    # Points: a filled circle (shape 21) so EVERY point has a fill (a tone) AND
    # a 1px stroke in the darker version of that tone (spec §5). Default to the
    # muted pair; overlap-friendly at 0.8 opacity. The 0.8 alpha is for the
    # *backdrop* cloud only — a highlighted point must be drawn ONCE at alpha = 1
    # (focus rows excluded from this muted layer), else its blue is diluted by the
    # panel and muddied by the grey dot underneath. See the highlight block below.
    update_geom_defaults("point",   list(shape = 21, fill = gl$c_muted,
                                         colour = gl$c_muted_dark, stroke = 0.6,
                                         alpha = 0.8))

    # Bars read as "backdrop" — softer grey. A 1px paper-colored stroke gives
    # the spec's separation between stacked segments (§6); on a single bar it is
    # invisible against the white panel. Areas stay edge-to-edge (no stroke) —
    # the spec keeps stacked areas gapless.
    update_geom_defaults("col",     list(fill = gl$c_muted, colour = gl$paper, linewidth = 0.5))
    update_geom_defaults("bar",     list(fill = gl$c_muted, colour = gl$paper, linewidth = 0.5))
    update_geom_defaults("area",    list(fill = gl$c_muted, colour = NA))
    update_geom_defaults("ribbon",  list(fill = gl$c_muted_light, colour = NA, alpha = 0.5))

    update_geom_defaults("smooth",  list(colour = gl$c_muted_dark,
                                         fill = gl$c_muted_light, alpha = 0.5))

    # Boxplots most often show the BACKGROUND distribution (peers) behind a
    # highlighted country line — so they recede: soft grey fill + medium-grey
    # outline (the muted main tone, not the darker tone). The highlight line
    # drawn on top carries the eye.
    update_geom_defaults("boxplot", list(fill = gl$c_muted_light, colour = gl$c_muted))
    update_geom_defaults("violin",  list(fill = gl$c_muted_light, colour = gl$c_muted_dark,
                                         alpha = 0.6))
    update_geom_defaults("density", list(fill = gl$c_muted_light, colour = gl$c_muted_dark,
                                         alpha = 0.6))

    update_geom_defaults("hline",   list(colour = gl$ink_3, linetype = "dashed",
                                         linewidth = 0.4))
    update_geom_defaults("vline",   list(colour = gl$ink_3, linetype = "dashed",
                                         linewidth = 0.4))
    update_geom_defaults("text",    list(colour = gl$ink_2, family = "gl_sans"))
    update_geom_defaults("label",   list(colour = gl$ink_2, family = "gl_sans",
                                         fill = gl$paper))
    invisible(NULL)
}

# ---- Highlight-by-muting pattern --------------------------------------------
#
# The canonical chart move: untyped geoms are already muted (see
# gl_set_geom_defaults below), so the pattern collapses to overpainting
# the focus with `highlight` (blue, = accent):
#
#   data |>
#       ggplot(aes(x = x, y = y, group = country)) +
#       geom_line() +                                       # muted, default
#       geom_line(data = \(d) filter(d, country == "Mongolia"),
#                 color = highlight, linewidth = highlight_sz)
#
# `highlight` is blue (c_1, the main tone #2F87C8) — the default focus per Nil:
# "Reserve saturated hue (usually c-1) for one or two focus series." Its dark
# partner (c_1_dark = accent, #1A5A8E) is only for the point stroke and label.
#
# POINTS ARE THE EXCEPTION to the simple overpaint. Lines/bars are opaque, so
# drawing the muted layer then overpainting the focus works. But the point
# default carries alpha = 0.8, which dilutes a highlight dot two ways: through
# its own transparency, and by letting the grey dot beneath it show through. So a
# highlighted point is PAINTED ONCE — exclude the focus from the muted backdrop,
# then draw it a single time at alpha = 1:
#
#   geom_point(data = \(d) filter(d, !focus), alpha = 0.3) +   # backdrop, focus out
#   geom_point(data = \(d) filter(d, focus),                   # focus, painted once
#              fill = highlight, color = highlight_dark, alpha = 1, size = 3)
#
# For a stark "lead finding" emphasis (gains vs losses, alarm, exception)
# use `lead_finding` (c_2 red) instead. Use sparingly.

# ---- Scale functions ---------------------------------------------------------

#' Discrete color scale using GL palettes
#'
#' @param palette Name of palette: "categorical" (default),
#'   "sequential_1".."sequential_6", "diverging_2_1", "diverging_3_1",
#'   "diverging_5_1", "diverging_6_1", "hs_sectors", "sitc_sectors",
#'   "product_space"
#' @param ... Passed to scale_color_manual
scale_color_gl <- function(palette = "categorical", ...) {
    pal <- gl_palettes[[palette]]
    if (is.null(pal)) stop("Unknown palette: ", palette,
                           ". Available: ",
                           paste(names(gl_palettes), collapse = ", "))
    scale_color_manual(values = pal, ...)
}

#' Discrete fill scale using GL palettes
#'
#' @param palette Name of palette: same as scale_color_gl
#' @param ... Passed to scale_fill_manual
scale_fill_gl <- function(palette = "categorical", ...) {
    pal <- gl_palettes[[palette]]
    if (is.null(pal)) stop("Unknown palette: ", palette,
                           ". Available: ",
                           paste(names(gl_palettes), collapse = ", "))
    scale_fill_manual(values = pal, ...)
}

#' Continuous color scale using a GL sequential or diverging palette
#'
#' For continuous data (e.g., choropleth values). Interpolates between the
#' discrete steps of the chosen palette.
#'
#' @param palette Name of a sequential_* or diverging_* palette
#' @param ... Passed to scale_color_gradientn
scale_color_gl_gradient <- function(palette = "sequential_1", ...) {
    pal <- gl_palettes[[palette]]
    if (is.null(pal)) stop("Unknown palette: ", palette)
    scale_color_gradientn(colors = pal, ...)
}

#' Continuous fill scale using a GL sequential or diverging palette
#'
#' @param palette Name of a sequential_* or diverging_* palette
#' @param ... Passed to scale_fill_gradientn
scale_fill_gl_gradient <- function(palette = "sequential_1", ...) {
    pal <- gl_palettes[[palette]]
    if (is.null(pal)) stop("Unknown palette: ", palette)
    scale_fill_gradientn(colors = pal, ...)
}

# ---- Figure sizes ------------------------------------------------------------

gl_fig <- list(
    full        = list(w = 6.5,   h = 4.0),
    full_tall   = list(w = 6.5,   h = 6.0),
    full_square = list(w = 6.5,   h = 6.5),
    major       = list(w = 4.278, h = 4.0),
    half        = list(w = 3.167, h = 3.0),
    half_tall   = list(w = 3.167, h = 5.0),
    slide       = list(w = 10,    h = 5.625)
)

#' Save a plot at a named recipe size
#'
#' @param size_name One of: full, full_tall, full_square, major, half, half_tall
#' @param filename Output filename (saved to imgs/ subdirectory)
#' @param plot Plot object (defaults to last_plot())
#' @param dpi Resolution (default 300)
save_fig <- function(size_name, filename, plot = last_plot(), dpi = 300) {
    sz <- gl_fig[[size_name]]
    if (is.null(sz)) stop("Unknown size: ", size_name, ". Use: ",
                          paste(names(gl_fig), collapse = ", "))
    dir.create("imgs", showWarnings = FALSE, recursive = TRUE)
    # Render PNGs through ragg's agg_png so the systemfonts registrations and
    # tabular figures apply. (ggplot2 >= 3.3.4 picks agg by default when ragg is
    # present, but force it for PNG to be device-independent.) device = NULL lets
    # ggsave auto-detect for other extensions.
    dev <- if (grepl("\\.png$", filename, ignore.case = TRUE) &&
               requireNamespace("ragg", quietly = TRUE)) ragg::agg_png else NULL
    ggsave(file.path("imgs", filename), plot = plot,
           width = sz$w, height = sz$h, dpi = dpi, device = dev)
}

# ---- Font registration (systemfonts) ----------------------------------------
#
# Fonts are registered through systemfonts (NOT showtext) so OpenType features
# reach the render path. The critical one is tabular figures (`tnum`): showtext
# could not enable it, so tick numerals used to render proportionally — now
# every Inter family is tabular (spec Decision Rule 11).
#
# Each weight we need is its own registered family, built from the exact named
# instance of the bundled variable font. `register_variant(weight=)` does NOT
# honor the variable weight axis on this toolchain (it always resolves to the
# default instance), but `match_fonts(weight=)` returns the correct path+index,
# which we feed to `register_font()`. Serif families carry no `tnum` — the
# tabular rule is about Inter numerals, not serif.
#
#   Family             weight  tabular  Used for
#   ─────────────────  ──────  ───────  ──────────────────────────────────────
#   gl_sans            400/600   yes    Body sans + ticks (400); legend / series
#                                        labels + strips via face="bold" (600)
#   gl_sans_medium     500       yes    Axis title (Inter 500)
#   gl_sans_heavy      700       yes    Cover date, TOC page numbers
#   gl_serif           400/500    no    Body serif; chart title via face="bold"
#                                        (500); chart source via face="italic"
#   gl_serif_light     300        no    Lead paragraph
#   gl_serif_semibold  600        no    TOC major, reference titles
#
# Rendering must go through a systemfonts-aware device — ragg's agg_png (which
# save_fig / ggsave use by default when ragg is installed) or the default screen
# device on modern R. Old Cairo/X11 paths won't see these registrations.

# Resolve the gl-design repo root so bundled fonts/assets are found wherever the
# kit is installed (plugin, symlink, or git clone). Priority:
#   1. GL_DESIGN_ROOT          — explicit override
#   2. CLAUDE_PLUGIN_ROOT      — set when running inside the installed plugin
#   3. this script's location  — <root>/skills/gl-ggplot/assets/theme_gl.R
#   4. ~/dev/gl-design         — legacy fallback (original dev checkout)
gl_this_file <- function() {
    for (i in seq_len(sys.nframe())) {
        of <- sys.frame(i)$ofile
        if (!is.null(of)) return(normalizePath(of, mustWork = FALSE))
    }
    NA_character_
}

gl_design_root <- function() {
    has_fonts <- function(p) nzchar(p) && dir.exists(file.path(p, "assets", "fonts"))

    env <- Sys.getenv("GL_DESIGN_ROOT", "")
    if (has_fonts(env)) return(normalizePath(env))

    plugin <- Sys.getenv("CLAUDE_PLUGIN_ROOT", "")
    if (has_fonts(plugin)) return(normalizePath(plugin))

    self <- gl_this_file()
    if (!is.na(self)) {
        cand <- normalizePath(file.path(dirname(self), "..", "..", ".."),
                              mustWork = FALSE)
        if (has_fonts(cand)) return(cand)
    }

    path.expand("~/dev/gl-design")
}

gl_font_files <- function(root = gl_design_root()) {
    fd <- file.path(root, "assets", "fonts")
    c(file.path(fd, "inter", "ttf", "InterVariable.ttf"),
      file.path(fd, "inter", "ttf", "InterVariable-Italic.ttf"),
      file.path(fd, "source-serif-4", "ttf", "SourceSerif4Variable-Roman.ttf"),
      file.path(fd, "source-serif-4", "ttf", "SourceSerif4Variable-Italic.ttf"))
}

gl_register_fonts <- function() {
    files <- gl_font_files()
    if (all(file.exists(files))) {
        add_fonts(files)
        sans <- "Inter Variable"; serif <- "Source Serif 4 Variable"
    } else {
        warning("GL bundled fonts not found under the resolved gl-design root ",
                "(set GL_DESIGN_ROOT to override); ",
                "falling back to system-installed Inter / Source Serif 4.")
        sans <- "Inter"; serif <- "Source Serif 4"
    }

    tnum <- font_feature(numbers = "tabular")
    face <- function(family, weight, italic = FALSE) {
        m <- match_fonts(family, weight = weight, italic = italic)
        list(m$path, m$index)
    }

    # Inter — every family tabular (Decision Rule 11).
    register_font("gl_sans",
                  plain      = face(sans, "normal"),
                  bold       = face(sans, "semibold"),                 # ->600
                  italic     = face(sans, "normal",   italic = TRUE),
                  bolditalic = face(sans, "semibold", italic = TRUE),
                  features   = tnum)
    register_font("gl_sans_medium",
                  plain = face(sans, "medium"), features = tnum)       # 500
    register_font("gl_sans_heavy",
                  plain = face(sans, "bold"),   features = tnum)       # 700

    # Source Serif 4 — no tabular.
    register_font("gl_serif",
                  plain  = face(serif, "normal"),
                  bold   = face(serif, "medium"),                      # ->500
                  italic = face(serif, "normal", italic = TRUE))
    register_font("gl_serif_light",    plain = face(serif, "light"))     # 300
    register_font("gl_serif_semibold", plain = face(serif, "semibold"))  # 600

    invisible(NULL)
}

# ---- Setup -------------------------------------------------------------------

#' Initialize the GL design system: load fonts, set theme and palette defaults
#'
#' Registers Source Serif 4 and Inter at every weight the grammar uses via
#' systemfonts (see gl_register_fonts() for the family table and the reason we
#' use systemfonts rather than showtext — OpenType tabular figures).
#'
#' When called inside a knitr knit, also registers a chunk hook that re-applies
#' the theme and palette defaults before every chunk runs. This is necessary
#' because knitr's caching does not replay session-state side effects: if the
#' chunk that called `gl_setup()` is cached, the theme registration is not
#' restored on a re-knit, and any newly-rendered chunks would otherwise pick
#' up the default ggplot2 theme. The hook ensures every chunk starts with the
#' GL theme active. Note: it cannot re-style chunks whose plot output is
#' already cached — those need to be invalidated or rebuilt.
#'
#' @param mode "report" (suppresses title/subtitle/caption) or "slide"
#' @param base_size Base font size (default 12 — matches 12pt body)
gl_setup <- function(mode = "report", base_size = 12) {
    gl_register_fonts()

    # Non-interactive R (`Rscript foo.R`) defaults to the pdf() device, which
    # cannot resolve the systemfonts registry families — so a top-level ggplot
    # that auto-prints errors with "invalid font type". (Under showtext this
    # worked because showtext_auto() patched every device.) Route the default
    # device to ragg so auto-prints render harmlessly to a throwaway file.
    # save_fig() / ggsave() still open their own ragg device for output files.
    if (!interactive() && requireNamespace("ragg", quietly = TRUE)) {
        options(device = function(...)
            ragg::agg_png(filename = tempfile(fileext = ".png"), ...))
    }

    apply_gl_defaults <- function() {
        theme_set(theme_gl(base_size = base_size, mode = mode))
        options(
            ggplot2.discrete.colour = gl$palette,
            ggplot2.discrete.fill   = gl$palette
        )
        gl_set_geom_defaults()
    }

    apply_gl_defaults()

    # In a knit: render through ragg so the systemfonts registrations (and
    # tabular figures) apply, and re-apply defaults before every chunk so that
    # knitr's caching cannot leave a chunk rendering against default ggplot2.
    if (isTRUE(getOption("knitr.in.progress")) &&
        requireNamespace("knitr", quietly = TRUE)) {
        knitr::opts_chunk$set(dev = "ragg_png")
        knitr::knit_hooks$set(gl_theme = function(before, options, envir) {
            if (before) apply_gl_defaults()
        })
        knitr::opts_chunk$set(gl_theme = TRUE)
    }

    invisible(NULL)
}
