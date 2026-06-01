# theme_gl.R — Growth Lab design system for ggplot2
#
# Usage:
#   source("~/dev/gl-design/skills/gl-ggplot/assets/theme_gl.R")
#   gl_setup()                          # loads fonts, sets theme + defaults
#   gl_setup(mode = "slide")            # slide mode (keeps title/subtitle)
#
# Requires: ggplot2, ggthemes, sysfonts, showtext

library(ggplot2)
library(sysfonts)
library(showtext)

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
    paper_warm  = "#F4F1EA",  # Accent panels, cover medallion bg
    cover_bg    = "#F3F2EA",  # Cover only
    rule        = "#DDDDDD",  # Hairline borders
    gridline    = "#ECE9E2",  # In-chart gridlines

    # Categorical — three tones per hue
    c_1_light = "#B5D5EA", c_1 = "#2F87C8", c_1_dark = "#1A5A8E",   # Blue
    c_2_light = "#E89C9C", c_2 = "#CC4948", c_2_dark = "#8A2C2B",   # Red
    c_3_light = "#92D6BF", c_3 = "#2AA584", c_3_dark = "#1A6B53",   # Teal
    c_4_light = "#B5A0CC", c_4 = "#7554A3", c_4_dark = "#4A3470",   # Purple
    c_5_light = "#F4BC8A", c_5 = "#EA822D", c_5_dark = "#A8580F",   # Orange
    c_6_light = "#E6E2A8", c_6 = "#CDC86B", c_6_dark = "#8A8638",   # Yellow

    # Muted gray — "everyone else"
    c_muted_light = "#CDD2D9",
    c_muted       = "#999FA8",
    c_muted_dark  = "#5F6773",

    # Full categorical palette (main tones, in order)
    palette = c("#2F87C8", "#CC4948", "#2AA584",
                "#7554A3", "#EA822D", "#CDC86B")
)

# Top-level aliases so user code reads naturally
highlight    <- gl$accent     # blue popout (= c_1_dark) — the default focus color.
                              # Per Nil: "Reserve saturated hue (usually c-1) for
                              # one or two focus series."
lead_finding <- gl$c_2        # red, for stark / lead-finding emphasis (gains vs.
                              # losses, alarm, exception). Use sparingly.
c_muted      <- gl$c_muted    # cool grey, "everyone else"
accent       <- gl$accent     # primary blue — same hex as highlight; this name
                              # is for non-data UI (eyebrows, figure labels, links)
highlight_sz <- 1.8           # line width for highlighted series (vs 0.6 muted)

# ---- Named palettes ---------------------------------------------------------
#
# `categorical` is the default 6-color discrete palette.
# `sequential_*` and `diverging_*` are ordered ramps for choropleths /
# heatmaps / continuous encodings — pair with scale_*_gl_gradient() for
# continuous data, or scale_*_gl() for discrete (binned) data.
# The sector palettes are external Growth Lab standards.

gl_palettes <- list(
    # Default categorical (6 colors)
    categorical = gl$palette,

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
#   gridline    — 1px gl$gridline (#ECE9E2), horizontal only by default
#                 (Nil's rule: never both X and Y unless the chart is dense).
#                 Override with theme(panel.grid.major.x = element_line(...))
#                 when the chart genuinely needs vertical gridlines.
#   strip       — no background fill, bold sans label.
#
# Base is theme_minimal — gives no panel border / no frame by default, then
# we add the bottom+left axis lines explicitly. (theme_few would add a frame.)
#
# Tooling note: font_add_google() reaches the weight axis but not the opsz
# axis. Charts default to the text-cut shapes (opsz 14) — see followups.md #3.

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
            axis.title   = element_text(family = "gl_sans", color = gl$ink_2,
                                        size = rel(1.0), face = "bold"),
            axis.title.x = element_text(margin = margin(t = 6)),
            axis.title.y = element_text(margin = margin(r = 6), angle = 90),
            axis.text    = element_text(family = "gl_sans", color = gl$ink_2,
                                        size = rel(1.0)),

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

            # Legend — Inter 12pt ink-2.
            legend.title = element_text(family = "gl_sans", color = gl$ink_2,
                                        size = rel(1.0)),
            legend.text  = element_text(family = "gl_sans", color = gl$ink_2,
                                        size = rel(1.0)),

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
#   geom_col / bar / area / point / line / path  → c_muted family
#   geom_smooth                                  → c_muted_dark line + light ribbon
#   geom_boxplot                                 → neutral (white fill, ink stroke)
#   geom_hline / vline                           → dashed ink_3 (reference line)
#   geom_text / label                            → ink_2 (body color)
#
# Called from gl_setup() — these mutate global ggplot2 state.

gl_set_geom_defaults <- function() {
    # Lines + points read as "data" — darker grey (c_muted_dark, same as
    # geom_smooth) so a single-series chart looks substantive.
    update_geom_defaults("point",   list(colour = gl$c_muted_dark, fill = gl$c_muted_dark))
    update_geom_defaults("line",    list(colour = gl$c_muted_dark, linewidth = 0.8))
    update_geom_defaults("path",    list(colour = gl$c_muted_dark, linewidth = 0.8))
    update_geom_defaults("step",    list(colour = gl$c_muted_dark, linewidth = 0.8))

    # Bars and areas read as "backdrop" — softer grey (c_muted) since they're
    # usually a row of comparators with one highlighted.
    update_geom_defaults("col",     list(fill = gl$c_muted, colour = NA))
    update_geom_defaults("bar",     list(fill = gl$c_muted, colour = NA))
    update_geom_defaults("area",    list(fill = gl$c_muted, colour = NA))
    update_geom_defaults("ribbon",  list(fill = gl$c_muted_light, colour = NA, alpha = 0.5))

    update_geom_defaults("smooth",  list(colour = gl$c_muted_dark,
                                         fill = gl$c_muted_light, alpha = 0.5))

    # Boxplots: c_muted_dark stroke (not near-black ink) so they recede.
    update_geom_defaults("boxplot", list(fill = "white", colour = gl$c_muted_dark))
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
# `highlight` is blue (c_1_dark, = accent) — the default focus per Nil:
# "Reserve saturated hue (usually c-1) for one or two focus series."
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
    ggsave(file.path("imgs", filename), plot = plot,
           width = sz$w, height = sz$h, dpi = dpi)
}

# ---- Setup -------------------------------------------------------------------

#' Initialize the GL design system: load fonts, set theme and palette defaults
#'
#' Registers Source Serif 4 and Inter at every weight the grammar uses.
#' `font_add_google()` (this sysfonts version) only carries regular + bold
#' per family, so each "weight bucket" we need beyond 400/bold is a separate
#' family registration. The aliases below mirror the grammar's role hierarchy:
#'
#'   Family              regular   bold    Used for
#'   ──────────────────  ─────── ──────  ────────────────────────────────────
#'   gl_serif_light       300     —       Lead paragraph
#'   gl_serif             400    500      Body serif, chart title (bold),
#'                                         chart source (italic — slanted)
#'   gl_serif_semibold    600     —       TOC major, reference titles
#'   gl_sans              400    600      Body sans, axis title (bold),
#'                                         table header (bold)
#'   gl_sans_heavy        700     —       Cover date, TOC page numbers
#'
#' Italic is rendered as artificial slant — sysfonts on this system doesn't
#' carry a true italic weight axis through font_add_google().
#'
#' Charts use `gl_serif` (regular + bold for chart title) and `gl_sans`
#' (regular + bold for axis title). Document-level weights (light, semibold,
#' heavy) are also registered so slide-mode charts and inline annotations
#' can reach them.
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
    # Source Serif 4
    font_add_google("Source Serif 4", "gl_serif",
                    regular.wt = 400, bold.wt = 500)
    font_add_google("Source Serif 4", "gl_serif_light",
                    regular.wt = 300)
    font_add_google("Source Serif 4", "gl_serif_semibold",
                    regular.wt = 600)

    # Inter
    font_add_google("Inter", "gl_sans",
                    regular.wt = 400, bold.wt = 600)
    font_add_google("Inter", "gl_sans_heavy",
                    regular.wt = 700)

    showtext_auto()
    showtext_opts(dpi = 300)

    apply_gl_defaults <- function() {
        theme_set(theme_gl(base_size = base_size, mode = mode))
        options(
            ggplot2.discrete.colour = gl$palette,
            ggplot2.discrete.fill   = gl$palette
        )
        gl_set_geom_defaults()
    }

    apply_gl_defaults()

    # Self-installing knitr hook: re-apply defaults before every chunk so that
    # knitr's caching cannot leave a chunk rendering against default ggplot2.
    if (isTRUE(getOption("knitr.in.progress")) &&
        requireNamespace("knitr", quietly = TRUE)) {
        knitr::knit_hooks$set(gl_theme = function(before, options, envir) {
            if (before) apply_gl_defaults()
        })
        knitr::opts_chunk$set(gl_theme = TRUE)
    }

    invisible(NULL)
}
