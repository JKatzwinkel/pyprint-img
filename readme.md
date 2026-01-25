# print images to terminal

```help
usage: p.py [-h] [-m mode] [-y] [-v] [-t NUM] filename

rasterize an image into the terminal.

positional arguments:
  filename              path to image file

options:
  -h, --help            show this help message and exit
  -m mode, --threshold mode
                        threshold mode, allowed values:
                        [extremes|median|percentile|const|local] (default:
                        local)
  -y, --crop-y          crop image to terminal height
  -v, --invert          rasterize a negative of the image
  -t NUM, --threshold-arg NUM
                        value to be passed to the threshold function (see the
                        --threshold option). required if selected threshold
                        mode is "percentile" or "const". threshold mode
                        "local" allows values between 0 and 9999.
```
