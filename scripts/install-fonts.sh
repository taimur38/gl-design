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
  MINGW*|MSYS*|CYGWIN*)
    # Native Windows can't reliably register fonts from bash (needs a registry
    # entry under HKCU, not just a file copy). Tell the operator what to do.
    cat <<'MSG'
Detected a Windows shell. Font registration on Windows isn't reliable from bash.
Install these four files for the current user (right-click -> Install, or use
PowerShell), then re-run the doctor:
  assets/fonts/inter/ttf/InterVariable.ttf
  assets/fonts/inter/ttf/InterVariable-Italic.ttf
  assets/fonts/source-serif-4/ttf/SourceSerif4Variable-Roman.ttf
  assets/fonts/source-serif-4/ttf/SourceSerif4Variable-Italic.ttf
(The R/ggplot chart path works without this; only PDF/slides/xelatex need it.)
MSG
    exit 0 ;;
  *)      FONT_DST="${HOME}/.local/share/fonts/gl-design" ;;
esac

mkdir -p "$FONT_DST"
n=0
# The live stack (Inter + Source Serif 4) plus JetBrains Mono, which the xelatex
# header (gl_pdf.tex) resolves by name. Other legacy/retired faces are skipped.
# Source dirs are listed explicitly — far simpler than pruning the legacy tree.
while IFS= read -r f; do
  cp -f "$f" "$FONT_DST/"
  n=$((n+1))
done < <(find "$SRC/inter" "$SRC/source-serif-4" "$SRC/legacy/jetbrains-mono" \
            \( -name '*.ttf' -o -name '*.otf' \) -print 2>/dev/null)

echo "Installed $n font file(s) → $FONT_DST"

if [ "$(uname -s)" = "Darwin" ]; then
  echo "macOS resolves these directly from ~/Library/Fonts — no cache step needed."
fi

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
