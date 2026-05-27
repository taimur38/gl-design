# theme_gl.R — Growth Lab design system for ggplot2
#
# Usage:
#   source("~/dev/gl-design/skills/gl-ggplot/assets/theme_gl.R")
#   gl_setup()                          # loads fonts, sets theme + defaults
#   gl_setup(mode = "slide")            # slide mode (keeps title/subtitle)
#
# Requires: ggplot2, ggthemes, sysfonts, showtext

library(ggplot2)
library(ggthemes)
library(sysfonts)
library(showtext)

# ---- Design tokens (nil-design grammar) -------------------------------------
#
# Ink ramp — warm, four layers (browns, not neutral greys).
# Accent — primary blue + variants.
# Categorical chart palette — 6 curated colors.
# c_muted — cool grey for "everyone else" in the highlight-by-muting pattern.

gl <- list(
    # Ink ramp
    ink         = "#1A1714",  # Cover title, all headings, strong, table emphasis
    ink_2       = "#2C2823",  # Body, axis text, table cells
    ink_3       = "#6B645A",  # Captions, eyebrows, chrome
    ink_4       = "#9A9389",  # Hairlines, deep-background markers

    # Accent
    accent      = "#015C9C",  # Cover date, eyebrows, figure labels, primary series
    accent_deep = "#003E6B",
    accent_soft = "#3A85B8",
    accent_tint = "#E1F0FA",

    # Paper
    paper       = "#FAF8F4",  # Content pages
    paper_warm  = "#F4F1EA",
    cover_bg    = "#F3F2EA",  # Cover only
    rule        = "#DDDDDD",  # Hairline borders

    # Categorical (6) — use in order
    c_1 = "#015C9C",  # Primary blue
    c_2 = "#C77A20",  # Contrast / lead-finding amber
    c_3 = "#CEC96B",
    c_4 = "#51B196",
    c_5 = "#A8352C",
    c_6 = "#918BED",

    # Muted gray — paint "everyone else" with this
    c_muted = "#7E8A99",

    # Full palette as a vector for ggplot defaults
    palette = c("#015C9C", "#C77A20", "#CEC96B", "#51B196", "#A8352C", "#918BED")
)

# Highlight pattern constants — expose at top level so user code reads naturally
highlight    <- gl$c_2       # amber, the lead-finding accent
c_muted      <- gl$c_muted   # cool grey, "everyone else"
accent       <- gl$accent
highlight_sz <- 1.8          # line width for highlighted series (vs 0.6 for muted)

# ---- Named palettes ---------------------------------------------------------
#
# `categorical` is the nil-design 6-color palette. The sector/cluster palettes
# below are external standards (Atlas / Metroverse / Greenplexity) and remain
# the right choice for trade and product-space charts — see followups.md #7.

gl_palettes <- list(
    # Default nil-design categorical (6 colors)
    categorical = gl$palette,

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
# Tooling note: font_add_google() reaches the weight axis but not the opsz axis.
# Charts default to the text-cut shapes (opsz 14) — see followups.md #3.

theme_gl <- function(base_size = 12, mode = "report") {
    t <- theme_few(base_size = base_size) %+replace%
        theme(
            text = element_text(family = "gl_sans", color = gl$ink_2),

            # Chart title — Source Serif 4 14pt weight 500, ink. Rendered
            # inside the chart in slide mode; suppressed in report mode.
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

            # Chart source — Source Serif 4 italic 10pt ink-2.
            plot.caption = element_text(
                family = "gl_serif", face = "italic",
                size = rel(10 / 12), hjust = 0,
                color = gl$ink_2,
                margin = margin(t = 8)
            ),

            # Axes — Inter 12pt ink-2.
            axis.title   = element_text(family = "gl_sans", color = gl$ink_2,
                                        size = rel(1.0)),
            axis.title.x = element_text(margin = margin(t = 6)),
            axis.title.y = element_text(margin = margin(r = 6), angle = 90),
            axis.text    = element_text(family = "gl_sans", color = gl$ink_2,
                                        size = rel(1.0)),

            # Legend — Inter 12pt ink-2.
            legend.title = element_text(family = "gl_sans", color = gl$ink_2,
                                        size = rel(1.0)),
            legend.text  = element_text(family = "gl_sans", color = gl$ink_2,
                                        size = rel(1.0)),

            # Facet strip — Inter 12pt ink-2.
            strip.text   = element_text(family = "gl_sans", color = gl$ink_2,
                                        size = rel(1.0))
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

# ---- Highlight-by-muting pattern --------------------------------------------
#
# Nil's canonical chart move: paint every series in c_muted first, then
# re-paint the focus series in c_2 (or another accent) on top. The muted
# layer carries the trend; the highlight carries the finding.
#
# Pattern (for a line chart, similar for points / bars):
#
#   data |>
#       ggplot(aes(x = x, y = y, group = country)) +
#       geom_line(color = c_muted, linewidth = 0.6) +
#       geom_line(data = \(d) filter(d, country == "Mongolia"),
#                 color = highlight, linewidth = highlight_sz)
#
# `highlight` is the amber c_2. Swap to `accent` for the primary blue if the
# story wants a different emphasis tone.

# ---- Scale functions ---------------------------------------------------------

#' Discrete color scale using GL palettes
#'
#' @param palette Name of palette: "categorical" (default), "hs_sectors",
#'   "sitc_sectors", "product_space"
#' @param ... Passed to scale_color_manual
scale_color_gl <- function(palette = "categorical", ...) {
    pal <- gl_palettes[[palette]]
    if (is.null(pal)) stop("Unknown palette: ", palette)
    scale_color_manual(values = pal, ...)
}

#' Discrete fill scale using GL palettes
#'
#' @param palette Name of palette: "categorical" (default), "hs_sectors",
#'   "sitc_sectors", "product_space"
#' @param ... Passed to scale_fill_manual
scale_fill_gl <- function(palette = "categorical", ...) {
    pal <- gl_palettes[[palette]]
    if (is.null(pal)) stop("Unknown palette: ", palette)
    scale_fill_manual(values = pal, ...)
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
#' Registers Source Serif 4 (gl_serif) and Inter (gl_sans) from Google Fonts.
#' Source Serif 4's bold weight maps to 500 (chart title weight in nil's spec);
#' Inter's bold weight maps to 600 (axis title / table header / emphasis weight).
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
#' @param base_size Base font size (default 12 — matches nil's 12pt body)
gl_setup <- function(mode = "report", base_size = 12) {
    font_add_google("Source Serif 4", "gl_serif",
                    regular.wt = 400, bold.wt = 500)
    font_add_google("Inter", "gl_sans",
                    regular.wt = 400, bold.wt = 600)
    showtext_auto()
    showtext_opts(dpi = 300)

    apply_gl_defaults <- function() {
        theme_set(theme_gl(base_size = base_size, mode = mode))
        options(
            ggplot2.discrete.colour = gl$palette,
            ggplot2.discrete.fill   = gl$palette
        )
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
