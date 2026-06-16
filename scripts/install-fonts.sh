#!/usr/bin/env bash
# install-fonts.sh — register the GL fonts (Source Serif 4 + Inter) with the system.
#
# Why this exists separately from install.sh: the R/ggplot path reads the bundled
# fonts directly and needs nothing. But the PDF (chrome-headless-shell), slides
# (Marp/Chromium), and xelatex (gl_pdf.tex) paths resolve fonts BY NAME via the OS
# font system. `claude plugin install` does NOT run install.sh, so plugin users
# should run this once to make those paths work.
#
#   bash scripts/install-fonts.sh
#   # under the installed plugin:  bash "$CLAUDE_PLUGIN_ROOT/scripts/install-fonts.sh"

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/assets/fonts"

case "$(uname -s)" in
  Darwin) FONT_DST="${HOME}/Library/Fonts" ;;
  *)      FONT_DST="${HOME}/.local/share/fonts/gl-design" ;;
esac

mkdir -p "$FONT_DST"
n=0
# Non-legacy faces only (Inter + Source Serif 4 are the live stack).
while IFS= read -r f; do
  cp -f "$f" "$FONT_DST/"
  n=$((n+1))
done < <(find "$SRC" -path '*/legacy/*' -prune -o \( -name '*.ttf' -o -name '*.otf' \) -print 2>/dev/null)

echo "Installed $n font file(s) → $FONT_DST"

if command -v fc-cache >/dev/null 2>&1; then
  fc-cache -f "$FONT_DST" >/dev/null 2>&1 && echo "Refreshed font cache (fc-cache)."
fi

# Quick verify (Linux / fontconfig).
if command -v fc-list >/dev/null 2>&1; then
  if fc-list 2>/dev/null | grep -qi "Inter" && fc-list 2>/dev/null | grep -qi "Source Serif 4"; then
    echo "Verified: Inter and Source Serif 4 are now visible to the system."
  else
    echo "Note: fonts copied but not yet visible to fontconfig — open a new shell or re-run 'fc-cache -f'."
  fi
fi
