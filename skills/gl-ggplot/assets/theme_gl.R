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

# ---- Design tokens -----------------------------------------------------------

gl <- list(
    text_dark   = "#333333",
    text_muted  = "#7c7c7c",
    border      = "#dcdcdc",
    background  = "#f3f3f3",
    brand_blue  = "#266798",
    highlight   = "#C64646",
    palette     = c(
        "#266798", "#C64646", "#36B250", "#EAC218", "#D1852A",
        "#52E2DE", "#A42DE2", "#7C6760", "#757777"
    )
)

highlight    <- gl$highlight
highlight_sz <- 1.1

# ---- Named palettes ---------------------------------------------------------

gl_palettes <- list(
    # Default 9-color categorical
    categorical = gl$palette,

    # Atlas HS product sectors
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

    # Atlas SITC product sectors
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

    # Product space clusters
    product_space = c(
        "Agricultural Goods"        = "#e0b614",
        "Construction Goods"        = "#c77c2b",
        "Electronics"               = "#5cc7c6",
        "Chemicals & Basic Metals"  = "#9c3bd6",
        "Metalworking Machinery"    = "#c43d3d",
        "Minerals"                  = "#7a6a63",
        "Textile & Home Goods"      = "#8a8a8a",
        "Apparel"                   = "#2fa84f"
    ),

    # Growth Lab brand colors
    brand = c(
        "Blue"   = "#6db5db",
        "Green"  = "#48c0a2",
        "Yellow" = "#e5bd4f",
        "Red"    = "#ee3e4c"
    )
)

# ---- Theme -------------------------------------------------------------------

theme_gl <- function(base_size = 12, mode = "slide") {
    t <- theme_few(base_size = base_size) %+replace%
        theme(
            text          = element_text(family = "gl_sans", color = gl$text_dark),
            plot.title    = element_text(family = "gl_sans", face = "plain",
                                         size = rel(1.35), hjust = 0,
                                         margin = margin(b = 4)),
            plot.subtitle = element_text(family = "gl_sans", color = gl$text_muted,
                                         size = rel(1.0), hjust = 0,
                                         margin = margin(b = 10)),
            plot.caption  = element_text(family = "gl_mono", color = gl$text_muted,
                                         size = rel(0.75), hjust = 1,
                                         margin = margin(t = 8)),
            axis.title    = element_text(family = "gl_mono", color = gl$text_muted,
                                         size = rel(0.85)),
            axis.title.x  = element_text(margin = margin(t = 6)),
            axis.title.y  = element_text(margin = margin(r = 6), angle = 90),
            axis.text     = element_text(family = "gl_sans", color = gl$text_dark,
                                         size = rel(0.85)),
            legend.title  = element_text(family = "gl_mono", color = gl$text_muted,
                                         size = rel(0.8)),
            legend.text   = element_text(family = "gl_sans", size = rel(0.85)),
            strip.text    = element_text(family = "gl_mono", color = gl$text_dark,
                                         size = rel(0.85))
        )

    if (mode == "report") {
        t <- t + theme(
            plot.title         = element_blank(),
            plot.subtitle      = element_blank(),
            plot.caption       = element_blank(),
            legend.position    = "bottom",
            legend.justification = "left",
            legend.margin      = margin(t = 4),
            legend.key.size    = unit(0.4, "cm")
        )
    }

    t
}

# ---- Scale functions ---------------------------------------------------------

#' Discrete color scale using GL palettes
#'
#' @param palette Name of palette: "categorical" (default), "hs_sectors",
#'   "sitc_sectors", "product_space", "brand"
#' @param ... Passed to scale_color_manual
scale_color_gl <- function(palette = "categorical", ...) {
    pal <- gl_palettes[[palette]]
    if (is.null(pal)) stop("Unknown palette: ", palette)
    scale_color_manual(values = pal, ...)
}

#' Discrete fill scale using GL palettes
#'
#' @param palette Name of palette: "categorical" (default), "hs_sectors",
#'   "sitc_sectors", "product_space", "brand"
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

#' Save a plot at a named framework size
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
#' When called inside a knitr knit, also registers a chunk hook that re-applies
#' the theme and palette defaults before every chunk runs. This is necessary
#' because knitr's caching does not replay session-state side effects: if the
#' chunk that called `gl_setup()` is cached, the theme registration is not
#' restored on a re-knit, and any newly-rendered chunks would otherwise pick
#' up the default ggplot2 theme. The hook ensures every chunk starts with the
#' GL theme active. Note: it cannot re-style chunks whose plot output is
#' already cached — those need to be invalidated or rebuilt.
#'
#' @param mode "report" (suppresses title/subtitle/caption) or "slide" (default)
#' @param base_size Base font size (default 12)
gl_setup <- function(mode = "report", base_size = 12) {
    font_add_google("Source Sans 3", "gl_sans")
    font_add_google("JetBrains Mono", "gl_mono")
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
