# alias for `test`, `type`, && `lint` recipes
default: test type lint

# print tool's `--help` output
help:
  bra -h

alias update-manual := doc

# make sure readme.md is up-to-date
doc: doc-help doc-examples


[doc("update usage instructions code block in readme.md \
with the output of running cli --help again")]
doc-help $TERM_RCWH='44x174':
  #!/usr/bin/env bash
  set -euo pipefail
  sed -i -ne '/```help/ {p; r'<(bra -h) \
    -e ':a; n; /```/ {p; b}; ba}; p' readme.md


# run examples snippets in readme and update example outputs
doc-examples $TERM_RCWH='44x174':
  python util/doc_examples.py readme.md


# render preview for installed fonts supporting braille charset
font-preview:
  #!/usr/bin/env bash
  set -euo pipefail
  tmpfile=$(mktemp)
  echo "magick montage -geometry 420x120 -pointsize 72 \\" >> "${tmpfile}"
  for ff in $(fc-list ':charset=2800' | cut -d: -f1); do
    fn=$(fc-scan --format '%{fullname}' "${ff}")
    echo "-font ${ff} -label '${fn}' label:⠈⠈⠳⣝⠧⡇ \\" >> "${tmpfile}"
  done
  echo "-tile 4x8 \\" >> "${tmpfile}"
  echo "-font Arial -pointsize 24 -geometry +2+2 \\" >> "${tmpfile}"
  echo "-frame 5 -bordercolor SkyBlue fonts.png" >> "${tmpfile}"
  bash "${tmpfile}"


# take a screenshot && replace image file at screenshot.png
take-screenshot cmd='python p.py eppels.png -z4 -e.5' $TERM_RCWH='44x174':
  #!/usr/bin/env bash
  FONT_PS=$(fc-list ':mono' file | grep -im1 'dejavu')
  echo "prompt font: ${FONT_PS%:*}"
  FONT_OUT=$(fc-list ':charset=2800 :mono' file | grep -vim1 'freemono')
  FONT_OUT=${FONT_OUT:-$(fc-list :charset=2800 file | grep -m1 'DejaVuSerif-Bold')}
  echo "stdout font: ${FONT_OUT%:*}"
  {{cmd}} | \
    magick -background indigo -fill seashell3 -gravity south \
    -font "${FONT_OUT%:*}" -size 1200x -pointsize 17 caption:@- \
    -define png:exclude-chunks=date,time \
    screenshot.png
  magick screenshot.png -pointsize 21 \
    -font "${FONT_PS%:*}" -fill chartreuse \
    -annotate +41+25 '> {{cmd}}' \
    -define png:exclude-chunks=date,time \
    screenshot.png


# run pytest
test pytest_args='':
  python -mpytest --capture=sys --doctest-modules --cov bryle \
    --cov-report term-missing {{pytest_args}} tests/ util/* bryle/ \
    --durations 14

# run flake8
lint flake8_args='':
  python -mflake8 bryle/ tests/ util/ {{flake8_args}}

# run mypy
type mypy_args='':
  python -mmypy --strict {{mypy_args}} tests/ util/

# python profiler
profile:
  #!/usr/bin/env python
  import cProfile
  import bryle
  with cProfile.Profile() as pr:
      bryle.main('eppels.png -xe.5'.split())
      pr.print_stats(sort='cumulative')

# cython annotate code
cy:
  cython -va bryle/pxp.py

# cython compilation status
pxp:
  #!/usr/bin/env python
  import bryle.pxp
  print(f'cython module loaded: {bryle.pxp.__file__}')
