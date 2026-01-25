update-manual:
  sed -i -ne '/```help/ {p; r'<(python p.py -h) \
    -e ':a; n; /```/ {p; b}; ba}; p' readme.md

test:
  python -mpytest --doctest-modules p.py --cov . \
    --cov-report term-missing
