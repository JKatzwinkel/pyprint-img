default: test

[doc("update usage instructions code block in readme.md \
with the output of running cli --help again")]
update-manual:
  #!/usr/bin/env bash
  set -euo pipefail
  sed -i -ne '/```help/ {p; r'<(python p.py -h) \
    -e ':a; n; /```/ {p; b}; ba}; p' readme.md
  readarray examples < <(
    sed -ne '/```bash/ {:a;n;p;n; /```$/ {=;b}; ba}; ' readme.md | \
    sed 'N;s/\n/:::/'
  )
  for example in "${examples[@]}"; do
    cmd="${example%:::*}"
    lineno=$(echo -n "${example#*:::}" | tr -d '\n')
    echo "${cmd}"
    sed -i -ne $((lineno+2))',/```$/ {/```output/ {p; r'<($cmd) \
      -e ':a; n; /```$/ {p; b}; ba}}; p' readme.md
  done


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


# run pytest
test pytest_args='':
  python -mpytest --capture=sys --doctest-modules p.py --cov . \
    --cov-report term-missing {{pytest_args}} tests.py

# run flake8
lint flake8_args='':
  python -mflake8 p.py {{flake8_args}}

# run mypy
type mypy_args='':
  python -mmypy --strict {{mypy_args}} tests.py
