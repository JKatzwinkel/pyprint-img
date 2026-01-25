[doc("update usage instructions code block in readme.md \
with the output of running cli --help again")]
update-manual:
  sed -i -ne '/```help/ {p; r'<(python p.py -h) \
    -e ':a; n; /```/ {p; b}; ba}; p' readme.md

# run pytest
test pytest_args='':
  python -mpytest --capture=sys --doctest-modules p.py --cov . \
    --cov-report term-missing {{pytest_args}}

# run flake8
lint flake8_args='':
  python -mflake8 p.py {{flake8_args}}
