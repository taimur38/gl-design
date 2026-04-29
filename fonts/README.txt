Growth Lab brand fonts
======================

Standard set
------------

Body / headings : Source Sans 3   (https://github.com/adobe-fonts/source-sans, v3.052R)
Captions / data : JetBrains Mono  (https://github.com/JetBrains/JetBrainsMono, v2.304)

Editorial variant
-----------------

Headings        : Crimson Pro     (https://github.com/Fonthausen/CrimsonPro)
Body            : Source Sans 3   (same as above)
Captions / data : JetBrains Mono  (same as above)

The editorial variant swaps in a serif (Crimson Pro) for headings while
keeping Source Sans 3 for body text. See framework-visual-b-editorial.html
in the gl-design repo for the full visual specimen.

License
-------

All three families are licensed under the SIL Open Font License v1.1 —
see the LICENSE-*.txt files alongside this README. The OFL permits free
use, embedding, modification and redistribution, including bundling the
font files in a website.

Files included
--------------

source-sans-3/
  woff2/    Light, Regular, Semibold, Bold (+ italics)
  ttf/      Same eight weights/styles as TrueType

jetbrains-mono/
  woff2/    Regular, Medium, Bold (+ italics)
  ttf/      Same six weights/styles as TrueType

crimson-pro/
  woff2/    Regular, Semibold, Bold (+ italics)  — for editorial variant
  ttf/      Same six weights/styles as TrueType

Recommended use on the web
--------------------------

Serve the woff2 files (smallest, supported in every current browser).
Keep the ttf files only if you need to support very old user agents.

A ready-to-paste @font-face block is in fonts.css. Adjust the `url()`
paths to wherever you put the files on the server. The Crimson Pro
declarations are at the bottom — drop them if you're not using the
editorial variant.
