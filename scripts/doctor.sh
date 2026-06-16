#!/usr/bin/env bash
# doctor.sh — check that the tooling the Growth Lab design kit needs is present.
# Reports per-pipeline status and prints exact fix commands for whatever is missing.
# Does NOT install anything. Exit code 0 if all REQUIRED-by-nothing… see end.

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# ---- platform-aware install hint -------------------------------------------
case "$(uname -s)" in
  Darwin) PM="brew install" ;;
  Linux)  if command -v apt-get >/dev/null 2>&1; then PM="sudo apt-get install"
          elif command -v pacman >/dev/null 2>&1; then PM="sudo pacman -S"
          elif command -v dnf >/dev/null 2>&1; then PM="sudo dnf install"
          else PM="<your package manager> install"; fi ;;
  *)      PM="<your package manager> install" ;;
esac

green=$'\033[32m'; red=$'\033[31m'; yellow=$'\033[33m'; dim=$'\033[2m'; rst=$'\033[0m'
missing=0

ok()   { printf '  %s✓%s %s\n' "$green" "$rst" "$1"; }
bad()  { printf '  %s✗%s %s\n      %s↳ %s%s\n' "$red" "$rst" "$1" "$dim" "$2" "$rst"; missing=$((missing+1)); }
warn() { printf '  %s•%s %s\n      %s↳ %s%s\n' "$yellow" "$rst" "$1" "$dim" "$2" "$rst"; }

have() { command -v "$1" >/dev/null 2>&1; }

printf '\n%sGrowth Lab design kit — environment check%s\n' "$rst" "$rst"
printf '%sroot: %s%s\n\n' "$dim" "$ROOT" "$rst"

# ---- markdown → docx / pdf / html (pandoc path) ----------------------------
printf 'Markdown → Word / PDF / HTML (pandoc pipelines)\n'
have pandoc          && ok "pandoc"          || bad "pandoc"          "$PM pandoc"
have pandoc-crossref && ok "pandoc-crossref" || bad "pandoc-crossref" "see https://github.com/lierdakil/pandoc-crossref/releases (or 'brew install pandoc-crossref')"
if have chromium || have chromium-browser || have google-chrome || have google-chrome-stable; then
  ok "headless Chromium (for PDF)"
else
  bad "Chromium / Chrome (PDF rendering)" "$PM chromium  (or install Google Chrome)"
fi

# ---- slides (Marp) ----------------------------------------------------------
printf '\nMarkdown → slides (Marp)\n'
if have node; then ok "node ($(node --version 2>/dev/null))"; else bad "node" "$PM node  (or use nvm)"; fi
if have marp || npx --no-install @marp-team/marp-cli --version >/dev/null 2>&1; then
  ok "Marp CLI"
else
  warn "Marp CLI not found" "npm install -g @marp-team/marp-cli  (md2slides will npx it on demand)"
fi

# ---- charts (R) -------------------------------------------------------------
printf '\nCharts (R / ggplot2)\n'
if have Rscript; then
  ok "Rscript ($(Rscript --version 2>&1 | head -1))"
  pkgs=$(Rscript -e 'cat(setdiff(c("ggplot2","systemfonts","ragg","textshaping"), rownames(installed.packages())), sep=" ")' 2>/dev/null)
  if [ -z "${pkgs// }" ]; then
    ok "R packages: ggplot2, systemfonts, ragg, textshaping"
  else
    bad "missing R packages:$pkgs" "Rscript -e 'install.packages(c($(echo $pkgs | sed "s/[^ ]*/\"&\"/g;s/ /,/g")))'"
  fi
else
  bad "Rscript" "$PM r-base  (or install R from CRAN)"
fi

# ---- fonts ------------------------------------------------------------------
printf '\nFonts (Source Serif 4 + Inter)\n'
if [ -f "$ROOT/assets/fonts/inter/ttf/InterVariable.ttf" ]; then
  ok "bundled fonts present in repo (R uses these directly)"
else
  bad "bundled fonts missing from repo" "re-clone the repo; assets/fonts must be intact"
fi
if fc-list 2>/dev/null | grep -qi "Inter" && fc-list 2>/dev/null | grep -qi "Source Serif 4"; then
  ok "fonts registered with the system (needed for the PDF/xelatex + Chromium paths)"
else
  warn "fonts not system-registered" "run scripts/install.sh to copy them into your font dir, then 'fc-cache -f' (Linux)"
fi

# ---- summary ----------------------------------------------------------------
printf '\n'
if [ "$missing" -eq 0 ]; then
  printf '%sAll required tooling present.%s\n\n' "$green" "$rst"
  exit 0
else
  printf '%s%d required tool(s) missing — install the items marked ✗ above.%s\n\n' "$red" "$missing" "$rst"
  exit 1
fi
