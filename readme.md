# print images to terminal

```help
usage: p.py [-h] [-m MODE] [-o FILE] [-y] [-x | -z FACTOR] [-v] [-a]
            [-b LEVEL] [-f] [-t NUM]
            FILE

rasterize an image into the terminal.

positional arguments:
  FILE                  path to input image file.

options:
  -h, --help            show this help message and exit
  -m, --threshold MODE  threshold mode, allowed values:
                        [extremes|median|percentile|const|local] (default:
                        local)
  -o, --output FILE     output file (default: /dev/stdout).
  -y, --crop-y          crop image to terminal height.
  -v, --invert          use the input image's negative.
  -a, --smooth          smooth input image a little bit based on the sample
                        rate. might be a good idea for images with a lot
                        highly contrasted detail but is slow. Can be repeated
                        (default: 0).
  -b, --brightness LEVEL
                        adjust brightness in percent (default: 100).
  -f, --force           overwrite existing output file (default: True for
                        /dev/stdout).
  -t, --threshold-arg NUM
                        value to be passed to the threshold function (see the
                        --threshold option). required if selected threshold
                        mode is "percentile" or "const". threshold mode
                        "local" allows values between 0 and 9999.

resizing options:
  -x, --fit-x           scale image so it fits into the terminal window
                        horizontally (default: False).
  -z, --zoom FACTOR     factor by which input image should be scaled in size.
```


## examples

example image:

![](./eppels.png)


basic usage:

```bash
python p.py eppels.png
```

```output
⣶⣷⣶⣶⣶⣶⣶⠖⠶⠶⢾⣿⣿⣶⣶⣶⣶⣶⣶⣶
⣺⣿⣿⣿⣿⡟⠀⣌⣄⣠⡄⢹⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⠿⠛⠃⠀⠈⠾⠛⢃⠜⣛⣛⠻⢿⣿⣿⣿⣵
⣿⣿⣧⣀⢀⠀⠀⠁⣀⡴⠀⠸⣿⣦⣄⣄⡎⢿⣿⣿
⢿⣿⣿⣿⣿⣿⠛⠉⠁⠁⠀⡀⠈⠙⠛⠋⠁⣸⣿⣿
⣲⣿⣿⣿⣿⣿⣆⣀⠀⠀⠀⠀⠀⠀⣀⣀⣴⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣿⣿⣿⣿⣿⢿⣿
```

scale input image by factor `2` first:

```bash
python p.py eppels.png -z 2
```

```output
⣶⣾⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⠶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶
⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠋⡈⠉⠉⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⢀⣀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢽⣶⣿⣾⣶⣿⡿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠀⠀⠀⠀⢙⣿⣿⣿⡿⠮⠀⣸⣿⡿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣉⣌
⣿⣿⣿⣿⣿⠟⠉⠀⠀⠀⠀⠀⠀⣄⡀⠊⠙⠉⠀⠀⡠⠐⠉⢠⣤⡤⡄⠄⠈⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⢀⣀⡔⠀⠀⢨⣿⣿⣿⡞⠀⠀⠀⠀⣠⣬⠻⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣷⣤⣴⣤⣄⣀⣀⣀⣀⣀⣀⣴⣾⣿⠃⠀⠀⠀⠹⣿⣿⣿⣿⣷⣶⣿⣾⣿⠀⢹⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠉⠀⠈⠙⠈⠀⠀⠀⠀⠈⠁⠉⠿⠿⣿⡿⠋⠋⠀⢸⣿⣿⣿⣿⣿
⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠉⠀⠀⠀⠀⠀⠀⠀⠈⠠⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿
⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿
⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣜⡦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣤⣤⣤⣤⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿
⣿⣿⣿⡿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⣿⣿⣿
```


the default mode of threshold computation is some kind of localized brightness
adjustment by applying gaussian blur with a radius proportional to the image's
dimensions. A smaller radius value can bring out more detail:

```bash
python p.py eppels.png -t 5
```

```output
⢲⣶⣶⢶⣶⣶⣶⠖⠶⠶⢶⣶⣶⣶⣶⢶⢶⣶⣶⣶
⢚⣳⣗⢿⣿⡟⢠⣝⢦⣠⡦⢹⣿⣟⣿⣯⣽⣭⣿⡽
⣴⣿⣿⠿⠛⠃⣤⣬⠴⠛⣢⠜⣛⣛⣻⢾⣦⡨⡿⣕
⣿⣿⣭⣄⣀⠀⠈⠛⢀⡴⠀⢺⣿⢦⣄⣔⡎⢿⣾⣽
⢻⢿⡻⣿⣛⣿⠛⠉⠀⢴⠣⡈⠛⠘⣏⢯⠃⣸⣷⣾
⣳⣫⢷⣳⣽⣷⣧⣀⠀⠺⠇⠙⠶⠄⣁⣀⣴⣿⢽⣻
⣾⣧⣽⣯⣿⣿⣿⣷⣿⣶⣶⣶⣶⢿⣿⣿⣻⣿⢯⣵
```

the more often the `-a`/`--smooth` option gets repeated the more noise gets
removed by repeatedly applying a median filter.

```bash
python p.py eppels.png -t 5 -aaa
```

```output
⣶⣶⡷⢶⣶⣶⣶⠶⠶⠶⢿⣿⣶⣷⣶⣶⣶⣶⣶⣶
⣻⣳⣿⢿⣿⡟⢠⣼⢦⣤⡆⢹⣿⣿⣿⣯⣿⣭⣾⣿
⣾⣿⣿⠿⠛⠃⣤⡌⠾⠛⣡⠘⣛⣛⡻⢿⣯⡫⡿⣏
⣿⣿⣽⣄⣀⠀⠈⠛⣀⡴⠀⢺⣿⣧⣤⣴⡎⢿⣿⣿
⡻⢿⣿⣟⣻⣿⠛⠉⠀⢴⡣⡌⠙⠘⣏⢯⠁⣸⣿⣿
⣿⣻⣿⣿⣿⣷⣧⣀⠀⠸⠇⠙⠷⠄⣀⣀⣴⣿⢿⣯
⣿⣯⣽⣿⣿⣿⣿⣷⣿⣶⣶⣶⣶⣿⣿⣿⣻⣿⣯⣾
```

<!--- vim: set ts=2 sw=2 tw=80 et ft=markdown : -->
