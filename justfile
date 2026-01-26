unexport DISPLAY

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
    tmpfile=$(mktemp)
    echo "${cmd}"
    bash -c "${cmd} -fo ${tmpfile}"
    sed -i -ne $(( lineno+2 ))',/```$/ {/```output/ {p; r'"${tmpfile}" \
      -e ':a; n; /```$/ {p; b}; ba}}; p' readme.md
  done

# run pytest
test pytest_args='':
  python -mpytest --capture=sys --doctest-modules p.py --cov . \
    --cov-report term-missing {{pytest_args}}

# run flake8
lint flake8_args='':
  python -mflake8 p.py {{flake8_args}}

# run mypy
type mypy_args='':
  python -mmypy --strict {{mypy_args}} p.py
