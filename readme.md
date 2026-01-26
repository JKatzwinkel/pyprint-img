# print images to terminal

```help
usage: p.py [-h] [-m MODE] [-o FILE] [-d] [-y] [-x | -z FACTOR] [-v] [-a]
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
  -d, --debug           preceed normal output with debug log printed to
                        /dev/stderr
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
⣾⣿⣶⣶⣶⣶⣶⠖⠶⠶⢾⣿⣿⣷⣶⣶⣶⣶⣶⣶
⣿⣿⣿⣿⣿⡟⠀⢀⢀⣠⡤⢻⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⠟⠛⠃⠀⠀⠸⠛⢃⠜⣛⣛⠻⢿⣿⣿⣿⣿
⣿⣿⣧⡀⠀⠀⠀⠀⢀⡴⠀⠐⢿⢆⣀⣄⡎⢿⣿⣿
⣿⣿⣿⣿⣿⣿⠛⠉⠀⠀⠀⠀⠀⠈⠉⠋⠁⣸⣿⣿
⣿⣿⣿⣿⣿⣿⣆⢀⠀⠀⠀⠀⠀⠀⣀⣀⣴⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣾⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿
```

scale input image by factor `2` first and raise threshold forgivingness by 1%:

```bash
python p.py eppels.png -z 2 -b 101
```

```output
⣶⣾⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⠶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⢋⡈⠉⠉⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠑⠀⠀⠀⢀⣀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢽⣶⣿⣾⣶⣿⡿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠀⠀⠀⠘⢙⣿⣿⣿⡿⠮⠀⣸⣿⡿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠟⠋⠁⠀⠀⠀⠀⢴⣾⡁⠋⠙⠋⠀⠀⡠⠐⠉⢠⣤⡤⡄⠄⠈⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡃⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠀⠀⢀⣠⡜⠀⠀⢸⣿⣿⣿⡞⠀⠀⠀⢀⣠⣬⠻⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣷⣤⣴⣤⣄⣀⣀⣀⣀⣀⣀⣴⣾⣿⠇⠀⠀⠀⠹⣿⣿⣿⣿⣷⣾⣿⣾⣿⠀⢹⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠉⠀⠈⠙⡜⠀⠀⠀⠀⠈⠁⠉⢿⠿⣿⣿⠛⠋⠀⢸⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠈⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄⡀⠀⠀⠀⠀⠈⠀⠁⠀⠀⠀⣼⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣜⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣤⣤⣤⣤⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⡿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
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


### threshold modes

option `-m`/`--threshold` allows for switching between different threshold value
functions. some of those can be parametrized with the option
`-t`/`--threshold-arg`.

the default mode is `local` and takes the average brightness within some radius
into account when sampling a pixel and deciding whether its value exceeds the
required threshold.

```bash
python p.py eppels.png -z 2
```

> the option `--threshold local` is implied when omitted

```output
⣶⣾⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⠶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶
⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⢋⡈⠉⠉⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠚⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠑⠀⠀⠀⢀⣀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢽⣶⣿⣾⣶⣿⡿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⢻
⢸⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠀⠀⠀⠘⢙⣿⣿⣿⡿⠮⠀⣸⣿⡿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣉⣜
⣿⣿⣿⣿⣿⠟⠋⠁⠀⠀⠀⠀⢴⣾⡁⠋⠙⠋⠀⠀⡠⠐⠉⢠⣤⡤⡄⠄⠈⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡃⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠀⠀⢀⣠⡜⠀⠀⢸⣿⣿⣿⡞⠀⠀⠀⠀⣠⣬⠻⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣷⣤⣴⣤⣄⣀⣀⣀⣀⣀⣀⣴⣾⣿⠇⠀⠀⠀⠹⣿⣿⣿⣿⣷⣶⣿⣾⣿⠀⢹⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠉⠀⠈⠙⡜⠀⠀⠀⠀⠈⠁⠉⢿⠿⣿⡿⠋⠃⠀⢸⣿⣿⣿⣿⣿
⢰⡟⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠈⠀⠀⠀⠀⠀⠀⠀⠈⠳⣄⡀⠀⠀⠀⠀⠈⠀⠁⠀⠀⠀⣼⣿⣿⣿⣿⣿
⣖⣾⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⡧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿
⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣜⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⣴⣾⣿⣿⣿⣿⣿⣿⡿⣹
⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣤⣤⣤⣤⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡻⣾
⣿⣿⣿⡿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⣿⣿⣿
```

the radius affecting the brightness threshold used at any given pixel can be
overwritten with the `-t`/`--threshold-arg` option.

```bash
python p.py eppels.png -z 2 -m local -t 14
```

```output
⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⠶⣶⣶⣶⣶⣶⣶⣶⣶⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶
⢻⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⡿⠛⢋⡈⠉⠉⠉⠙⠻⣿⣿⣿⣿⣿⡟⣿⣿⣿⣿⣿⣿⡿⢿⡿⣿⣿⣿⣿
⠚⣿⣿⣿⣏⢶⠿⣿⣿⣿⣿⠏⠀⠀⠈⡟⠄⠀⠀⢠⣤⠈⢿⣿⣿⣿⠷⣷⢿⣿⣟⣛⣻⡭⢲⡿⣷⢿⣋⣿
⢸⣾⡟⣿⣽⣾⣿⣿⣿⣿⣿⠀⠀⠼⣿⣷⠿⣿⣶⣿⡿⠀⢸⣿⣿⣿⣿⣾⣿⣷⣿⣿⣿⣿⣽⣿⡽⡭⣯⢻
⠸⡾⣿⣿⣿⣿⣿⣿⣿⡿⠿⠀⢀⡀⠘⢙⣦⣾⣿⡿⠦⠀⣸⣿⡿⠿⠿⢿⣿⣿⣿⣿⣾⡄⣪⡛⣷⣵⣁⣜
⢼⣿⣿⣿⣿⠟⠋⠁⠀⠀⠀⠘⣿⣿⣅⠋⠹⠋⠀⠸⡴⠟⠉⢠⣤⡤⡄⠦⠊⠍⢛⠿⣿⣿⣧⣽⣿⡿⣿⣾
⠿⣼⣿⣿⡃⢀⠀⠀⠀⠀⠀⠀⠈⠙⠿⠇⠀⢀⣀⡞⠀⠀⢼⣿⣿⣿⣾⠀⠀⠀⢀⣠⣬⠻⣿⣿⣿⣿⣿⣿
⣯⣻⣿⣿⣿⣷⣯⣶⣦⣄⣀⣀⣀⣀⣀⣀⣴⣾⣿⠃⠀⠀⠈⠽⣿⣿⣿⣿⣷⣾⣿⣾⣿⠀⢹⣿⣿⣿⣿⣿
⣽⣽⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠉⠀⠀⠀⡜⢧⠀⠀⠑⠚⠁⠈⢿⠿⣛⡿⠋⠃⠀⢸⣿⣿⢯⣄⣿
⣰⡟⡱⣻⢶⣫⣟⣝⢿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⣳⡈⢻⣦⡂⠀⠀⠀⠀⢙⠀⠣⡦⠀⠀⣼⣿⣿⢽⢽⣿
⣷⣼⣶⡳⣿⣾⣟⣶⣿⣿⣿⣾⣧⡀⠀⠀⠀⠀⠐⠾⡷⠀⠉⢿⣶⡀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⡿⢟⣼⣭
⡾⣿⢿⣷⣟⣿⢾⢿⣿⣿⣿⣿⣿⣝⠦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠀⣠⣤⣤⣴⣾⣿⣿⣿⣟⣻⣏⡾⣿
⡮⣍⣦⣼⣿⣿⣿⣤⣿⣹⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣤⣤⣤⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣟⡋⢿⣿⠻⣾
⣿⣿⣿⡿⠿⠿⠿⣿⣿⣿⣿⡿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣟⣹⣿⣿⣾⡯⣿⡿⢛⣿⣿⣿
```


the `median` mode on the other hand uses the median brightness across the entire
image as its threshold, without adjusting for overall darker or lighter areas.

```bash
python p.py --threshold median -z 2 eppels.png
```

```output
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⠄⢴⣶⣾⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠀⠀⠈⠉⠉⠉⠈⠒⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠌⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠠⣀⣤⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⡀⠀⠄⢁⣀⠄⠟⠛⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⠿⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢠⣦⣖⣶⠎⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣴⡄⠀⢹⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⡖⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠁⠀⠀⢸⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
```

the `percentile` mode is a generalized version of this and accepts a parameter
specifying which percentile of the brightness distribution should be used as
threshold. So passing `-m percentile -t 50` would be equivalent to `-m median`.

```bash
python p.py --threshold percentile -t 35 -z 2 eppels.png
```

```output
⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⠶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠋⠈⠉⠉⠉⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠘⠁⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠄⠄⠈⠉⠛⡿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣶⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣶⣾⣿⣧⢹⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⡶⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠋⠛⠀⢿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⣀⠀⠀⠀⠀⠀⣀⣀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
```

the `extremes` mode just calculates the threshold right between the darkest and
the lightest pixel values, without regard for their respective frequency.

```bash
python p.py -m extremes -z 2 eppels.png
```

```output
⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⠶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⡈⠉⠉⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⢠⣮⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠐⡆⠠⣶⣶⣿⣿⡟⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠀⠀⠀⠀⠀⠀⠾⠿⠟⠯⠀⣸⣿⣿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠉⢠⣦⡶⡌⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡔⠀⠀⠀⢾⣿⣿⡾⠀⠀⢀⣽⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣶⣤⣄⣀⣀⣀⣀⠀⣀⣠⣶⠿⠁⠀⠀⠀⠀⠉⠿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠫⡿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣺⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣤⣤⣤⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
```

finally, it is possible to just pass the literal threshold value straight up
into the thing using `-t`/`--threshold-arg` in the `const` mode:

```bash
python p.py -m const -z 2 -t 160 eppels.png
```

```output
⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⠶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠋⠈⠉⠉⠉⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠓⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠄⠄⠈⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⣾⣿⣧⢹⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⡖⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠉⠋⠀⢻⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⢀⣀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
```


<!--- vim: set ts=2 sw=2 tw=80 et ft=markdown : -->
