# print images to terminal

```help
usage: p.py [-h] [-m MODE] [-o FILE] [-y] [-v] [-f] [-t NUM] FILE

rasterize an image into the terminal.

positional arguments:
  FILE                  path to input image file.

options:
  -h, --help            show this help message and exit
  -m MODE, --threshold MODE
                        threshold mode, allowed values:
                        [extremes|median|percentile|const|local] (default:
                        local)
  -o FILE, --output FILE
                        output file (default: /dev/stdout).
  -y, --crop-y          crop image to terminal height
  -v, --invert          rasterize a negative of the image
  -f, --force           overwrite existing output file (default: True for
                        /dev/stdout).
  -t NUM, --threshold-arg NUM
                        value to be passed to the threshold function (see the
                        --threshold option). required if selected threshold
                        mode is "percentile" or "const". threshold mode
                        "local" allows values between 0 and 9999.
```
