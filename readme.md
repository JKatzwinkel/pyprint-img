# print images to terminal

![](./screenshot.png)

converts image files into monochrome unicode text utilizing the braille charset.


## usage

```help
usage: p.py [-h] [-m MODE] [-o FILE] [-f] [-H] [-d] [-y] [-z FACTOR | -x] [-v]
            [-a] [-A] [-b LEVEL] [-e [FACTOR]] [-D METH | --floyd] [-t NUM]
            FILE

rasterize an image into the terminal.

positional arguments:
  FILE                  path to input image file, or "-" to read from stdin.

options:
  -h, --help            show this help message and exit
  -m, --threshold MODE  threshold mode, allowed values:
                        [extrema|median|percentile|const|local] (default:
                        local)
  -o, --output FILE     output file (default: /dev/stdout).
  -f, --force           overwrite existing output file (default: True for
                        /dev/stdout).
  -y, --crop-y          crop image to terminal height.
  -v, --invert          invert 'pixel' values of output.
  -a, --sharpen         enhance input image by emphasizing edges a little (the
                        more often the option gets repeated, the more).
  -A, --aliasing        disable antialiasing.
  -b, --brightness LEVEL
                        adjust brightness in percent (default: 100).
  -t, --threshold-arg NUM
                        value to be passed to the threshold function (see the
                        --threshold option). required if selected threshold
                        mode is "percentile" or "const". threshold mode
                        "local" allows values between 0 and 9999.

debug options:
  -H, --histogram       plot image histogram to stdout.
  -d, --debug           preceed normal output with debug log printed to
                        /dev/stderr.

resizing options:
  -z, --zoom FACTOR     factor by which input image should be scaled in size.
  -x, --fit-x           scale image so it fits into the terminal window
                        horizontally.

dithering options:
  -e, --dither [FACTOR]
                        error preservation factor/dithering ratio. accepts an
                        optional float value and assumes 1.0 if omitted.
                        (default: 0.0).
  -D, --dmethod METH    dither method to use (one of atkinson|floyd-steinberg,
                        default: atkinson).
  --floyd               shortcut for -Dfloyd-steinberg

p.py reads the environment variable TERM_RCWH which when set bypasses any
attempt at determining actual terminal && xterm window sizes from tty and
ioctl and forces fixed terminal and optionally window size to be used for
image processing. TERM_RCWH accepts values in the forms `RxC` and `RxCxWxH`
where `RxC` is terminal size in rows and columns and `WxH` is window width and
hieght in pixels.
```


a font supporting the braille charset at codepoints `U+2800` through `U+28ff` is
required. here are some examples of fonts with braille glyphs and what they look
like:

![](./fonts.png)


## examples

example image:

![](./eppels.png)


basic usage:

```bash
python p.py eppels.png
```

```output
⢶⣷⣶⣶⣶⣶⣶⡶⠶⠶⠶⢶⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶
⢺⣿⣿⣿⣿⣿⠋⠀⣁⣀⣀⡄⢻⣿⣿⣿⣿⣿⣿⣿⡿⢿
⣽⣿⣿⣿⠿⠿⠀⡀⣻⣿⠿⠃⡸⠿⠿⠿⣿⣿⣿⣿⣿⣷
⣿⣿⣏⠀⠀⠀⠈⠛⠄⠀⣠⠁⢰⣿⣗⡀⢀⢩⠻⣿⣿⣿
⣻⣿⣿⣿⣾⣶⣶⡶⠒⠛⠃⠀⠀⠙⠛⠿⣿⠿⠀⣿⣿⣿
⣺⣻⣿⣿⣿⣿⣧⡀⠀⠀⠀⠈⠲⡀⠀⠀⠀⠀⣰⣿⣿⣿
⣺⣿⣿⣿⣿⣿⣿⣮⣦⣄⣀⣀⣀⣀⣠⣴⣶⣿⣿⣿⣿⣶
⡿⠿⠛⠛⠻⠿⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⢽⣿
```

read from stdin by passing `-` as the file argument:

```bash
paste <( \
echo eppels.png | python p.py - \
) <(\
cat eppels.png | python p.py - \
)
```

```output
⢶⣷⣶⣶⣶⣶⣶⡶⠶⠶⠶⢶⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶	⢶⣷⣶⣶⣶⣶⣶⡶⠶⠶⠶⢶⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶
⢺⣿⣿⣿⣿⣿⠋⠀⣁⣀⣀⡄⢻⣿⣿⣿⣿⣿⣿⣿⡿⢿	⢺⣿⣿⣿⣿⣿⠋⠀⣁⣀⣀⡄⢻⣿⣿⣿⣿⣿⣿⣿⡿⢿
⣽⣿⣿⣿⠿⠿⠀⡀⣻⣿⠿⠃⡸⠿⠿⠿⣿⣿⣿⣿⣿⣷	⣽⣿⣿⣿⠿⠿⠀⡀⣻⣿⠿⠃⡸⠿⠿⠿⣿⣿⣿⣿⣿⣷
⣿⣿⣏⠀⠀⠀⠈⠛⠄⠀⣠⠁⢰⣿⣗⡀⢀⢩⠻⣿⣿⣿	⣿⣿⣏⠀⠀⠀⠈⠛⠄⠀⣠⠁⢰⣿⣗⡀⢀⢩⠻⣿⣿⣿
⣻⣿⣿⣿⣾⣶⣶⡶⠒⠛⠃⠀⠀⠙⠛⠿⣿⠿⠀⣿⣿⣿	⣻⣿⣿⣿⣾⣶⣶⡶⠒⠛⠃⠀⠀⠙⠛⠿⣿⠿⠀⣿⣿⣿
⣺⣻⣿⣿⣿⣿⣧⡀⠀⠀⠀⠈⠲⡀⠀⠀⠀⠀⣰⣿⣿⣿	⣺⣻⣿⣿⣿⣿⣧⡀⠀⠀⠀⠈⠲⡀⠀⠀⠀⠀⣰⣿⣿⣿
⣺⣿⣿⣿⣿⣿⣿⣮⣦⣄⣀⣀⣀⣀⣠⣴⣶⣿⣿⣿⣿⣶	⣺⣿⣿⣿⣿⣿⣿⣮⣦⣄⣀⣀⣀⣀⣠⣴⣶⣿⣿⣿⣿⣶
⡿⠿⠛⠛⠻⠿⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⢽⣿	⡿⠿⠛⠛⠻⠿⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⢽⣿
```

this is useful for integrating with other command-line tools:

```bash
# enable 10% dithering && invert output
curl -s https://www.python.org/static/community_logos/python-logo-master-v3-TM.png \
  | python p.py - -ve.1
```

```output
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣉⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢲⣰⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣴⣶⣿⣿⣿⣿⣿⣿⠀⠰⣄⠀⠀⠀⢀⣤⠖⠒⢶⡄⠀⣶⠀⠀⠀⣶⠀⠒⣿⠒⠀⣿⡤⠶⠶⣤⠀⢀⡴⠖⠶⣤⠀⢠⡴⠒⠲⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡿⠿⠿⠿⠿⠋⠀⡰⣿⠀⠀⠀⢸⣿⠀⠀⠈⣿⠀⣿⠀⠀⠀⣿⠀⠀⣿⠀⠀⣿⠀⠀⠀⣿⠀⣿⠁⠀⠀⢸⡇⢸⡇⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⠀⠀⢀⡀⣄⡰⣦⣿⡿⠀⠀⠀⢸⣿⣀⢀⣰⡟⠀⢿⣄⡀⣀⣿⠀⠀⣿⡀⠀⣿⡀⠀⠀⣿⠀⠹⣆⡀⢀⡾⠃⢸⡇⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⣤⡸⣤⢳⠼⢿⠉⠉⠀⠀⠀⠀⢸⣿⠈⠉⠁⠀⠀⠀⠉⠉⠁⣿⠀⠀⠈⠉⠀⠉⠁⠀⠀⠉⠀⠀⠈⠉⠉⠀⠀⠈⠁⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠻⠟⠓⠋⠀⠀⠀⠀⠀⠀⠘⠻⠀⠀⠀⠀⠀⠀⠐⠖⠚⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠐⠂⠖⠢⠒⠄⠢⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⡀⣀⢀⡀⣀⢀⡀⣀⢀⡀⣀⢀⡀⣀⢀⡀⣀⢀⡀⣀⢀⡀⣀⢀⡀⣀⢀⡀⣀⢀⡀⣀⢀⡀⣀⢀⡀⣀⢀⡀⣀⢀⡀⣀⢀⡀⣀⢀⡀⣀⢀⡀⣀⢀⡀⣀⢀⡀⣀⢀⡀⣀⢀⡀⣀⢀
```


enable dithering but invert color values:

```bash
python p.py eppels.png -e.5 -v
```

```output
⠱⡈⢍⡉⡉⠉⠉⢉⣉⣉⣉⡁⠌⠠⢉⠉⡉⢉⠉⡉⢉⠉
⠱⡈⢆⠐⠡⠀⣼⡟⢮⠻⠟⡹⡄⠡⠈⠔⡐⠂⢌⠰⢀⠊
⡑⡈⠄⣈⣄⣠⡟⡿⣆⢧⣡⠻⢅⣀⣈⣐⠀⢁⠂⢂⠡⠌
⡐⠄⠒⡿⣿⣿⣿⣶⣹⡾⠏⣿⣏⠠⠜⡾⢟⠢⢌⠀⠂⠌
⠰⣈⠐⠠⢁⠉⠉⣉⣭⣴⢺⡽⣿⣎⡷⣠⠄⣄⠯⢀⠡⠌
⠡⢂⠩⡐⠂⠄⢚⢽⣿⣞⣯⢷⣭⢿⣿⣷⣿⡼⠋⢀⠂⠌
⡁⠎⡐⠤⢉⠐⡈⠐⡙⠻⠿⠿⠿⠿⠞⠉⠉⡀⠐⡠⢈⠂
⢄⡡⠔⣄⢂⡰⢠⣁⠐⠠⠁⠌⢠⠐⢠⠁⠆⡈⠔⣀⠂⠡
```

scale input image by factor `2` first and raise threshold forgivingness by 1%:

```bash
python p.py eppels.png -z 2 -b 101
```

```output
⣶⣶⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⡶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠁⠉⠉⠉⠉⠛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠈⠉⠀⠀⠀⠀⠀⣀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢲⣦⣴⣶⣶⣶⣾⣿⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠈⠿⣿⣿⣿⣿⣿⡇⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡿⠟⠛⠉⠉⠉⠀⣠⣤⠀⠴⠿⡿⠟⠋⠁⢀⡠⠞⠋⠉⠉⠉⠉⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠙⢿⣷⠀⠀⠀⠀⠀⣠⠋⠀⠀⣴⣿⣷⣝⡄⠀⠀⠀⠀⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣷⣄⡀⢀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⢀⣰⣾⠇⠀⠀⠘⣿⣿⣿⣿⣤⣤⣀⣠⣔⣺⣿⠀⢻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣷⣿⣷⣶⣦⣤⣤⣤⣤⣤⠶⠿⠿⣿⠀⠀⠀⠀⠈⠹⡿⠿⣿⣿⣿⣿⣿⣿⡿⠂⠈⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠀⠀⠀⠀⠈⠀⢀⡀⠀⠀⠀⠀⠀⠈⠻⠻⢿⡿⠁⠁⠀⢀⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣦⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣗⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⠦⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⡷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣤⣤⣤⣤⣤⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣷
⠿⠟⠋⠁⠀⠀⠀⠀⠈⠉⠉⠉⠁⠀⠉⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⡿⣿⣿⣿⡟⠿⣿⣿⣿⣿
```


the default mode of threshold computation is some kind of localized brightness
adjustment by applying gaussian blur with a radius proportional to the image's
dimensions. A smaller radius value can bring out more detail:

```bash
python p.py eppels.png -t 5
```

```output
⠶⣶⣶⣶⣶⣶⣶⡶⠶⠶⠶⢶⣶⣶⡶⣶⣶⣶⢶⠶⣶⣶
⢺⣷⢯⣿⣿⣿⠋⣠⣕⢤⣠⡆⢻⣯⣯⣾⣿⣿⣗⣟⡾⢽
⢹⣿⣿⣿⠿⠿⢀⣉⣻⣸⠾⢃⡸⠿⠿⠿⣿⣿⡋⢿⣾⣷
⣿⣿⣿⢀⠀⠀⠈⠛⠦⠁⣠⠁⢴⣿⣗⣁⣁⢭⠻⣿⣷⣻
⣺⣿⡿⣷⣿⣶⣶⡶⠒⠋⣁⢆⠘⠹⡙⠻⢻⠻⠀⣿⣟⣿
⢾⣫⣿⣶⡿⣿⣣⡀⠀⠀⣼⡎⢺⣄⠀⠸⠋⠋⣰⡿⣷⠺
⢺⣞⣺⡿⣟⣿⣿⣮⣦⣄⣀⣁⣀⣈⣩⣶⣶⣿⢿⡏⣦⢖
⡿⠾⠛⠛⠻⠿⠛⠻⢿⣿⣷⣾⣿⣿⣿⣹⢙⣷⣫⣗⣽⣾
```

the input image can be de-noised somewhat by emphasizing edges with the option
`-a`/`--sharpen`.

```bash
python p.py eppels.png -t 5 -aaa
```

```output
⢶⣶⣶⣶⣶⣶⣶⡶⠶⠶⠶⣶⣾⣶⣶⣶⣶⣶⣶⣶⣶⣶
⢺⣷⣯⣼⣿⣿⠋⢠⣕⣄⣠⡄⢻⣿⣧⣿⣿⣿⡝⣟⡿⢙
⢸⣿⣿⣿⠿⠿⢀⣈⣻⣽⠿⢃⡸⠿⠿⠿⣿⣿⣯⢿⣾⣡
⣼⣿⣟⢀⠀⠀⠈⠛⠆⠀⣠⠁⢴⣿⣗⡁⢀⢩⠻⣿⣿⣿
⢺⣿⣿⣿⣿⣶⣶⡶⠒⠋⠁⠄⠀⠙⠙⠿⣿⠿⠀⣿⣿⣿
⢈⣈⣽⣟⣿⣿⣣⡀⠀⠀⠀⠎⠺⣄⠀⠀⠈⠂⣰⣿⣿⠸
⢸⣟⣮⣿⣿⣿⣿⣮⣦⣄⣀⣀⣀⣈⣠⣴⣶⣿⣿⡿⣦⣖
⡿⠿⠛⠛⠻⠿⠛⠻⢿⣿⣿⣿⣿⣿⡿⡿⢿⣯⣏⣇⣽⣾
```

enable debug messages to `/dev/stderr` with the `-d`/`--debug` flag.

```bash
TERM_RCWH=5x20 python p.py eppels.png -dxy 2>&1
```

```output
image dimensions: 202×151
got fixed term size from TERM_RCWH env var: 5×20
resize image to 89.1%
gaussian blur radius for `local` mode: 12
got fixed term size from TERM_RCWH env var: 5×20
xterm window dimensions: 180×95 pixels, 20×5 characters
character size in pixels: 9.00×19.00
sample rate in pixels: 5.05 horizontal, 5.33 vertical
using 20 columns × 5 rows
⣶⣷⣶⣶⣶⣶⡶⠶⠶⠶⢾⣿⣷⣶⣶⣶⣶⣶⣶⣶
⣸⣿⣿⣿⣿⡏⠀⣌⣤⣤⠎⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣾⣿⡿⠛⠛⠃⣤⠘⠟⠋⠠⢛⡛⠛⠻⢿⣿⣿⣿⣿
⣿⣿⣦⣠⣀⣀⣈⣁⣰⡎⠀⠻⣿⣤⣤⣴⠘⣿⣿⣿
⠾⡿⣿⣿⣿⣿⠋⠁⠀⠁⠠⡀⠀⠙⠙⠉⢀⣿⣿⣿
```

the `TERM_RCWH` environment variable can be used to pass fixed terminal
dimensions and to bypass attempts to determine terminal and terminal window
sizes from `ioctl`. If neither `stdin` nor `stdout` are a terminal, actual sizes
cannot be determined and passing of a fixed terminal size might be necessary:

```bash
# set fixed terminal size in rows×cols
export TERM_RCWH=14x79
# run braillify with no tty at neither stdin nor stdout
cat shelly.jpg | python p.py - -dxye.3 2>&1 > >(cat)
```

```output
image dimensions: 720×1280
got fixed term size from TERM_RCWH env var: 14×79
resize image to 98.8%
gaussian blur radius for `local` mode: 45
got fixed term size from TERM_RCWH env var: 14×79
xterm window dimensions: 711×266 pixels, 79×14 characters
character size in pixels: 9.00×19.00
sample rate in pixels: 4.56 horizontal, 4.81 vertical
using 79 columns × 14 rows
⠀⠀⠀⠀⠐⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠌⣹⠀⠌⡂⠌⠠⢁⠂⠄⠡⠈⠄⡐⢀⠀⠁⠌⡐⠈⠐⠠⠁⠌⠠⠁⠌⠐⡀⠂⠄⠂⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⡐⢀⠠⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⡐⢈⠐⠠⠈⠀⠀⠂⠈⠀⠁⠐⠀⠀⠀⠀⠀⠀⢈⠀⠀⠄⠈⠠⠁⠈⠠⠀⠌⠠⠈⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠠⠈⠐⠀⠀⠂⠠⢀⠀⢂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠠⢄⠰⡂⠀⠀⠀⠀⠀⠀⠠⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡐⢈⠐⠄⠁⠊⠀⠁⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣤⣤⣤⣤⣄⣤⣠⣀⣤⣀⣄⣠⣀⣠⣀⣄⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⡀⢀⠀⠀⢀⣀⣀⣀⣀⣤⡤⢤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣦⣴⣤⣦⣤⣤⣤⣤⡀⣀⢀⡀⡀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣻⢭⣻⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⣝⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢛⢭⣺⣽⣿⣿⣿⣿⣿⣿⣿⣿⢟⡽⡲⢧⡾⣖⣳⠸⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣟⡾⣽⣞⣯⢿⣽⣻⡽⣯⢿⣽⣻⡽⣯⢿⡿⣿⣻⢿⡿⣿⣿⡿⣫⣼⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⡁⣘⡬⣫⠕⣪⡡⣡⣦⡘⣿⣿⣿⣿⣿⣿⣿⢿⣿⡿⣿⡿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢾⡹⣷⢻⣞⠿⣞⢷⣻⢽⣻⡞⣷⣻⡽⣯⣟⡷⣯⢿⣽⡳⢫⡾⢛⣶⣿⣿⢿⣿⣿⣿⣿⣿⣿⠃⠞⣰⢛⡱⠜⡼⢋⣵⣿⣿⡇⣽⣿⣿⢿⣿⡽⣞⣯⢿⣽⣳⢿⡽⣞⣯⣟⡾⣯⣟⡿⣽⣻⢯⣟⣿⣻⢿⡽⣟⣿⣻⢿
⣏⢷⡹⣏⣞⡻⣜⢯⡞⣧⢳⡽⣣⣏⢷⡻⣾⡽⣯⢿⡔⣻⡏⢱⡿⢝⡻⢡⣿⣡⣿⣿⠿⣻⠃⠀⠀⢤⡖⣉⠩⡾⠺⣿⣿⣿⡇⣿⣟⣿⢯⣷⣻⡽⣞⡿⣾⡽⣯⢿⡽⣾⣽⣻⢷⣯⣟⡷⣯⣟⣾⣳⢯⡿⣽⣻⢾⡽⣯
⠘⠧⣻⡜⣮⡝⣮⢳⡝⣮⢳⣝⡳⢮⣏⡷⣯⢿⡽⣯⡟⡾⠻⠌⡜⢣⠆⠋⠤⣺⢿⡿⡼⠣⣶⢆⢇⣿⣿⣾⡉⢌⡁⣲⣟⢁⣐⣻⢿⣞⡿⣞⣷⣻⣽⣻⢷⣻⡽⢯⣟⡷⣯⣟⡿⣾⣽⣻⣳⣟⡾⣽⢯⣟⡷⣯⢿⣽⣳
⡏⢡⢷⡹⣖⡻⣜⢧⡻⣜⡳⢮⣝⣻⢾⡽⣯⢿⣽⣷⣯⣃⣐⣒⣬⣭⣤⣔⡱⡥⠛⠟⡁⠿⢻⣿⣿⣿⣿⣿⣿⣿⣶⢿⣿⡄⢿⣽⣻⢾⣽⣻⣞⡷⣯⠷⣯⣳⢯⣟⡾⣽⣳⢯⣟⣷⣳⢯⣗⡯⣿⣽⢳⡾⣽⣫⢿⣜⣳
⡜⣯⢞⡵⣫⢷⡹⣎⠷⣭⣛⢷⣺⣭⢿⡽⣯⣟⣾⣷⣿⡿⠟⢋⠻⢟⡫⠍⠡⣀⣠⣆⠻⣷⢿⣿⣿⣿⣿⣿⣿⣯⣷⣘⠩⣙⣠⡿⣽⣻⣞⡷⣯⢿⡽⣯⢷⣏⣿⢺⡽⢶⣯⣻⢞⣧⣟⡿⡾⣽⣳⡞⣯⣽⣳⢏⣟⡾⣳
⢹⣎⠿⣜⢧⣏⠷⣭⣛⢶⣛⣮⢷⣯⢿⣽⣳⢯⣿⣿⣿⠁⠁⠈⣀⣁⣰⡬⣥⢤⣬⡽⡿⠶⠤⠉⢻⣿⣿⣿⣯⣍⠍⠁⣵⡿⣽⣻⢷⣻⢾⡽⣏⡿⣽⣳⠿⣼⣣⣟⡽⣻⣼⡳⣟⣾⣹⢿⣽⣳⢯⣟⣳⡟⣾⡝⣮⢟⡵
```

### threshold settings

option `-m`/`--threshold` allows for switching between different threshold value
functions. some of those can be parametrized with the option
`-t`/`--threshold-arg`.

the default setting is `local` and takes the average brightness within some
radius into account when sampling a pixel and deciding whether its value exceeds
the required threshold.

```bash
python p.py eppels.png -z 2
```

> the option `--threshold local` is implied when omitted

```output
⣶⣶⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⡶⢶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶
⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠁⠉⠉⠉⠉⠛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠉⠀⠀⠀⠀⠀⡀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⢲⣦⣴⣶⣶⣶⣾⣿⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣻⡹⢿⣿
⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠈⠿⣿⣿⣿⣿⣿⡇⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠾⢿
⣽⣿⣿⣿⣿⣿⡿⠟⠛⠉⠉⠉⠀⣠⣤⠀⠴⠿⡿⠟⠋⠁⢀⡠⠞⠋⠉⠉⠉⠉⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷
⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠙⢿⣷⠀⠀⠀⠀⠀⣠⠋⠀⠀⣴⣿⣷⣝⡄⠀⠀⠀⠀⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⡏
⣿⣿⣿⣿⣷⣄⠀⢀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⢀⣰⣾⠇⠀⠀⠘⣿⣿⣿⣿⣤⣤⣀⣠⣔⣨⣿⠀⢻⣿⣿⣿⣿⣿⣿⡗
⣿⣿⣿⣿⣿⣿⣿⣷⣾⣷⣶⣦⣤⣤⣤⣤⣤⠶⠿⠿⣿⠀⠀⠀⠀⠈⠹⡿⠿⣿⣿⣿⣿⣿⣿⡿⠀⠈⣿⣿⣿⣿⣿⣟⣇
⢾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠉⠀⠀⠀⠀⠈⠀⢀⡀⠀⠀⠀⠀⠀⠈⠻⠻⠿⡿⠁⠁⠀⢀⣿⣿⣿⣿⣿⣿⣷
⢼⠏⡟⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣦⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⡷
⣾⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣗⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⠦⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⡟⣿⠟
⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣮⡳⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣤⣶⣿⣿⣿⣿⣿⣿⣿⣟⣴⣾⡓
⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣤⣤⣤⣤⣤⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠏
⣿⣿⣿⣿⡿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢹⣿⢷⣿⡅
⠿⠛⠉⠁⠀⠀⠀⠀⠈⠉⠉⠉⠀⠀⠈⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⡿⠿⠿⢿⡆⠻⣿⣿⣿⡿
```

the radius affecting the brightness threshold used at any given pixel can be
overwritten with the `-t`/`--threshold-arg` option. Option `-b/--brightness`
allows to adjust the respective threshold values before sampling. Use the
`-H/--histogram` flag to show the effects.

```bash
python p.py eppels.png -z 2 -m local -t 16 -b 110
```

```output
⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⡶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠁⠉⠉⠉⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠈⠉⠀⠀⠀⠀⢀⣀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢲⣦⣴⣶⣶⣶⣿⣿⠆⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠈⠿⣿⣿⣿⣿⣿⣟⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡿⠟⠛⠉⠉⠉⠀⠀⠀⠀⢴⠿⡿⠿⠟⠉⣉⡦⠞⠛⣉⣉⡉⢉⡉⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠻⣧⠀⠀⠀⠀⠀⣰⠋⠀⢠⣴⣿⣷⣝⡄⠀⠀⠀⠐⢋⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣇⡀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣰⣾⠇⠀⠀⠸⣿⣿⣿⣿⣤⣤⣀⣤⣴⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣤⣤⣤⣤⣴⡾⠿⣿⣿⢠⠀⠀⠀⠘⢿⡿⢿⣿⣿⣿⣿⣿⣿⣿⡟⡎⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠀⠀⠀⠈⠛⠈⢀⠀⠀⠀⠀⠀⠀⠘⠻⢿⢿⣿⡟⠋⠀⢠⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⢦⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣤⣤⣤⣤⣤⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
```

```bash
python p.py eppels.png -z 2 -m local -t 16 -b 110 -H
```

```output
---------------------------[                  |  ]-------       
                                                 \              
                                                 \              
                                                 |\             
                                                 |\             
                                                /||             
                                             /\//||             
           /                                //\/|||\            
\/////\////|\\\\//\//\/\///\\///\\\\//\\/\//|||||||\\\  /       
<=============================================|=========>=======
              --------------[         |  ]----
```

---

the `median` setting on the other hand uses the median brightness across the entire
image as its threshold, without adjusting for overall darker or lighter areas.

```bash
python p.py --threshold median -z 2 eppels.png
```

```output
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡤⠄⢴⣶⣾⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠙⠰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⡀⢀⡀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠄⠂⠀⠀⣰⠼⠿⠿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⢀⡰⠀⣰⣤⠞⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠋⠉⠉⠀⠈⠉⠛⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣼⣷⣷⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣷⣤⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⠾⠃⠀⠀⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠟⠛⠉⠀⠀⠀⠀⠀⠈⠉⠉⠉⠁⠀⠈⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
```

<details><summary>median threshold histogram</summary>

```bash
python p.py -mmedian -H eppels.png
```

```output
---------------------------[                  |  ]-------       
                                                 \              
                                                 \              
                                                 |\             
                                                 |\             
                                                /||             
                                             /\//||             
           /                                //\/|||\            
\/////\////|\\\\//\//\/\///\\///\\\\//\\/\//|||||||\\\  /       
<=============================================|=========>=======
                                              |
```
</details>

---

the `percentile` setting is a generalized version of this and accepts a parameter
specifying which percentile of the brightness distribution should be used as
threshold. So passing `-m percentile -t 50` would be equivalent to `-m median`.

```bash
python p.py --threshold percentile -t 35 -z 2 eppels.png
```

```output
⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⡶⢶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠁⠉⠉⠉⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠂⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠟⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠜⠋⠉⠉⠉⠉⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣸⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣦⣤⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣾⣿⣿⡿⠟⡞⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠁⠀⢨⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⣀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
```

<details><summary>percentile threshold histogram</summary>

```bash
python p.py --threshold percentile -t 35 -H eppels.png
```

```output
---------------------------[                  |  ]-------       
                                                 \              
                                                 \              
                                                 |\             
                                                 |\             
                                                /||             
                                             /\//||             
           /                                //\/|||\            
\/////\////|\\\\//\//\/\///\\///\\\\//\\/\//|||||||\\\  /       
<=============================================|=========>=======
                                       |
```
</details>

---

the `extrema` setting just calculates the threshold right between the darkest and
the lightest pixel values, without regard for their respective frequency.

```bash
python p.py -m extrema -z 2 eppels.png
```

```output
⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⡶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠁⠉⠉⠉⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⢀⣬⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⣤⠀⣠⣤⣴⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠈⠀⢈⢿⣿⣿⡟⠁⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠟⠛⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠞⠛⣉⣉⡩⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣷⣝⡎⠉⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⠃⠀⠀⠀⠘⢿⣿⣯⣤⣤⣄⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣤⣤⣤⣀⡤⠴⠞⠛⠛⠀⠀⠀⠀⠀⠀⠈⠉⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠟⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣤⣤⣤⣤⣤⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
```

<details><summary>extrema threshold histogram</summary>

```bash
python p.py -mextrema -H eppels.png
```

```output
---------------------------[                  |  ]-------       
                                                 \              
                                                 \              
                                                 |\             
                                                 |\             
                                                /||             
                                             /\//||             
           /                                //\/|||\            
\/////\////|\\\\//\//\/\///\\///\\\\//\\/\//|||||||\\\  /       
<=============================================|=========>=======
                            |
```

</details>

---

finally, it is possible to just pass the literal threshold value straight up
into the thing using `-t`/`--threshold-arg` with the `const` setting:

```bash
python p.py -m const -z 2 -t 160 eppels.png
```

```output
⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⡶⢶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠁⠉⠉⠉⠉⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠜⠋⠉⠉⠉⠉⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣧⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣸⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣷⣦⣤⣀⣀⣀⣀⣀⡀⡀⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣾⣿⣿⡿⠛⠎⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠁⠀⢠⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⣀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
```

<details><summary>const threshold histogram</summary>

```bash
python p.py -mconst -H eppels.png -t160
```

```output
---------------------------[                  |  ]-------       
                                                 \              
                                                 \              
                                                 |\             
                                                 |\             
                                                /||             
                                             /\//||             
           /                                //\/|||\            
\/////\////|\\\\//\//\/\///\\///\\\\//\\/\//|||||||\\\  /       
<=============================================|=========>=======
                                        |
```

</details>




### dithering

the `-e`/`--dither` option turns on dithering or changes the degree to which the
result of the monochrome mapping error function is being distributed to
neighboring pixels.

```bash
python p.py eppels.png -z 2 --dither
```

```output
⡞⣵⢫⡞⣶⢳⠶⡶⢶⠶⣶⠶⣶⢶⡶⣶⠶⢶⣶⢶⡶⣞⣶⣛⣞⡷⣛⣾⢳⣞⡶⣶⢶⡶⣶⢶⡶⣶⢶⡶⣶⢶⡶⣶⢶
⣝⢮⣗⡻⣜⢯⡻⣝⢯⣛⡾⣽⣛⡾⠝⢋⡡⢉⠈⡉⢉⡙⠾⣽⣺⣽⣛⣾⣛⡾⣽⣫⢯⣟⣭⢿⣹⣽⣫⡽⢯⣻⡽⣏⡿
⢮⣳⢞⡽⣹⡞⣵⢯⢯⣽⣳⢯⠟⠀⠈⡄⠓⡄⡐⠀⠤⡘⡴⣈⢷⣳⣟⡶⣯⡽⣾⣹⡟⣮⢯⣟⣳⣞⢷⣻⢯⢷⣻⡽⣽
⡳⣝⡾⣹⢧⣻⢧⡟⣯⢶⣯⡟⠀⠠⡑⢌⢧⠰⣡⢏⠶⣹⢲⠩⡜⣷⣻⣞⡷⣻⣵⣻⢾⡽⣛⣾⢳⡯⣟⡾⣏⡿⣞⡵⣯
⣝⢧⣟⣳⢯⣳⢯⡿⣽⣻⢞⡧⠐⡠⠘⠨⢌⠓⣌⢎⡳⢥⡃⢇⠼⣷⣻⢾⣽⣳⢯⡷⣯⢿⡽⣞⣯⢿⣭⢷⡯⣟⡽⣯⢷
⢾⣹⢮⠷⣯⢏⡿⠘⠃⠡⠉⡀⠣⡐⢡⠃⡌⠚⠤⢃⠜⠤⣉⠦⠟⢋⡩⣉⠬⢩⣍⠻⡽⢯⡿⣽⣞⣯⣞⣯⡽⣯⢟⡾⢯
⣏⡾⣽⢻⡭⢇⠄⡁⠌⢀⠁⡀⠄⠑⠢⡑⡈⠄⡑⠈⢄⢣⠈⠠⡘⢦⠳⣥⠝⡂⠌⢁⠣⢓⡭⡳⢟⣮⢷⣯⡽⣯⢿⡽⣯
⣞⡵⣯⣻⡵⣋⠖⣄⡀⠂⠀⠄⠀⠄⢀⠀⠁⠒⢠⣱⣾⠃⠀⠠⠑⢎⠳⣬⠹⡔⣤⢂⣎⣳⢺⡝⣏⢾⣻⢾⡽⣽⢾⣽⣳
⢮⡽⡶⣏⡷⣯⣟⡶⣭⣓⣎⠶⣬⡴⣤⣊⡴⠹⠎⢓⠩⢐⠠⠁⠌⠢⠱⢌⠣⡝⢦⡻⣼⡽⢯⡻⡜⣎⡿⣯⡽⣯⣟⡾⣵
⣏⣷⢻⣭⢷⣳⠾⣝⣳⡟⣾⣻⢷⠛⡆⠡⠠⠡⠘⠠⡑⠈⢄⠡⢈⠀⠡⢈⠒⢌⠲⢡⠧⣙⢇⢳⡙⢦⣟⣷⣻⠷⣾⣽⣳
⢾⡼⣻⡼⣳⣏⡿⣝⣧⡟⡷⣯⢞⡡⠂⡁⢂⠡⢁⠡⢀⠉⠄⠒⡠⠌⠐⡀⠈⠄⠨⣁⠒⡡⢎⠣⡜⣿⣞⡷⣯⣟⡷⣞⡷
⣳⢯⣗⣻⣵⣛⡾⡽⣶⢻⣽⣻⡼⡱⣅⠐⡀⠂⠄⠂⠌⡐⢈⠐⢀⠘⠤⠐⠠⢈⠐⡀⢂⠡⢂⣳⡾⣟⡾⣽⣳⡟⣾⡽⣛
⡽⣞⣭⢷⣞⣭⢷⣛⣷⡻⢾⣵⣻⡵⣎⡳⢤⣁⠌⠐⠠⠐⠀⠌⠀⠠⠀⠉⠒⢄⣲⣤⢧⣾⣟⣯⢿⣽⣛⡷⣯⣻⡗⣿⡽
⣳⢟⣮⢟⣮⢯⣯⢟⣶⡻⣟⣮⢷⣻⢷⢯⣳⡜⣎⡳⢲⢤⢣⡔⡬⡔⣦⣓⣮⣟⣳⢯⣟⡾⣽⡞⣟⡾⣽⣻⡵⣯⣟⢷⣻
⡽⣾⣹⠾⣽⢳⢯⡟⣾⣽⢻⡼⣯⢟⡾⣯⢷⣻⣽⢻⣟⡾⣳⠿⣽⣻⣳⢟⡾⣭⢯⣟⡾⣽⣳⠿⣝⣯⢷⢯⣽⣳⣞⣯⢷
⡽⣖⢯⡻⣜⢯⡞⣽⢲⡭⣏⢷⡹⢮⡝⣞⢯⢷⣫⣟⢾⣝⣯⢟⣳⢷⣫⢿⣹⣭⣟⠾⣝⡷⢯⡿⣽⡞⣯⣟⢾⣳⡟⣾⢯
```

the default error preservation factor is `0` (no dithering), a value of `1`
means that all of the error gets distributed (i.e. 75% because it is atkinson
dithering).

```bash
python p.py eppels.png -z 2 -e .5
```

```output
⣎⢷⡹⣖⡳⢶⠶⣶⢶⡶⣶⣶⣶⣶⣶⣶⡶⢶⣶⣶⣶⣶⣾⣳⣟⣾⣳⣟⡾⣶⢶⡶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶
⣎⢷⡹⢮⡝⣯⣛⠾⣭⣟⣷⣻⣿⡿⠟⠛⣁⠉⠉⠉⠉⠙⠳⣿⣞⣷⣻⢾⣝⣯⢿⣽⣳⣟⣾⣳⣟⡾⣽⣳⢯⣟⣯⣟⡿
⣎⢷⡹⢧⣛⠶⣭⣛⣷⣻⣾⣿⠟⠀⠀⢉⠐⣂⠀⠀⠀⢌⡥⠘⢿⣾⣽⣻⣞⣮⢟⣞⡷⣻⣼⡳⣽⣛⡷⢯⣟⣞⣳⢯⣟
⣎⢷⡹⢧⣏⡿⣖⡿⣞⣷⣿⡟⠀⠀⣀⠓⣮⣐⡣⣾⡜⣾⢣⠋⠜⣿⣾⣳⣟⣾⣻⢾⣽⣳⢷⣻⡵⢯⣛⡿⣼⢫⡾⣝⡾
⢮⡳⢯⣗⣯⢷⣯⣿⣿⣿⣿⡧⠀⡀⠠⠉⠖⣡⢚⡵⣺⢥⡃⢅⢺⣿⣿⣿⣾⣷⣯⣟⣾⡽⣯⢷⣻⢯⡽⢾⣹⢯⢷⣫⡽
⡳⣽⣛⡾⣽⣟⠯⠓⠙⠀⠉⠈⠐⡄⢣⠘⡰⢁⠞⡰⠁⢆⡉⠦⠞⢋⣉⣉⡡⢩⣉⡛⠿⣿⣽⣯⢿⣽⣛⣯⢯⡿⣭⢷⣻
⣽⢲⣯⣟⡷⡉⠀⠀⠀⠀⠀⠀⠀⠈⢃⠎⡐⠀⠐⠀⡁⢢⠉⠀⠤⣳⠼⣦⡝⡄⠂⠈⠑⢢⣉⠟⣿⢾⡽⣞⡿⣾⣽⣳⢯
⢮⣗⣻⣞⣧⣝⠢⣄⠀⠀⠀⠀⠀⠀⠀⠈⠀⠁⢂⣰⣾⠃⠀⠀⠱⢩⣛⢦⡽⡤⢤⣠⢜⣦⢭⡻⣌⢿⡽⣯⣟⣾⣳⢯⣻
⣳⢞⡧⣟⡾⣽⢿⣶⣯⣳⣖⣦⣴⣤⣦⣲⡴⠾⠛⡛⢛⠠⢂⠀⠁⠢⡘⢎⠲⡹⢧⡿⣞⣿⢿⡻⠜⣌⣿⣳⣟⡾⣝⣯⢷
⡽⣺⡝⣾⣹⢯⣟⡾⣽⣻⢿⣿⣿⠟⡋⠁⢀⠂⠡⠘⠠⠌⢠⠈⠄⠀⠈⠠⠁⠜⣡⠙⡬⣋⠖⣉⠞⣤⣿⣳⢯⡿⡽⣞⡽
⡳⢧⣻⡜⣧⡟⣮⡽⣳⢯⣟⣯⢻⡄⠀⠀⠀⠈⠄⡁⠂⠌⡀⠉⢆⠡⠀⠀⠀⠐⠠⠑⠄⡑⠎⠤⣉⣾⡷⣯⢿⣽⢻⣭⣟
⡽⣳⢧⣻⢵⣫⢷⣹⣏⡿⣞⣿⡳⡖⣅⠀⠀⠀⠀⠀⡁⠂⠄⠁⠈⠢⢑⠠⠀⠀⠀⠈⠀⠀⢂⣴⣾⡿⣽⢯⣟⡾⣻⡼⣞
⣝⡧⢿⣱⢯⣳⣏⢷⢾⣹⣟⡾⣿⣝⣮⡓⢦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠂⢡⣄⣦⣴⣾⣿⡿⣯⢿⣽⣻⢾⣝⡷⣯⣛
⢮⣽⢻⡼⣏⡷⣞⣯⣞⡷⣯⣟⣷⣻⢷⣿⣳⢮⡝⣖⡲⣤⢆⡤⣤⠴⣴⣲⣾⣿⣿⢿⣻⣟⣷⣻⣽⣻⠾⣽⢯⡾⣽⡳⢯
⣻⡼⣯⠷⣯⢟⡽⢾⡽⣞⣷⣻⢾⣽⣻⣞⣿⣻⢿⡿⣷⢿⣾⢿⡿⣿⣟⡿⣽⢾⡽⣯⢷⣻⣞⡷⡽⣞⣿⡹⣾⢽⣳⡟⣯
⢳⡝⣣⡛⣴⢫⡜⣧⢹⣙⢎⡳⣭⢒⢧⡛⡾⣽⢯⡿⣽⣻⣞⣯⢟⡷⢯⠿⣝⣻⢾⡹⢷⢯⡾⡽⣝⣯⠾⣝⣳⢯⢷⣛⡷
```

floyd-steinberg dithering can be used as an alternative method.

```bash
python p.py eppels.png -z2 -e.5 --floyd
```

```output
⡺⣺⡺⣺⡪⣖⣗⣖⣖⣖⢶⣲⢶⡶⣶⣶⡶⢶⣶⣶⡶⣞⣞⣞⡮⡷⣽⣺⣺⣺⣖⡶⡶⡶⡶⡶⣶⢶⡶⣶⢶⡶⣶⢶⣶
⣝⢮⣺⡺⣺⡺⣺⣺⡺⣮⣻⣺⣽⣻⠝⢚⢁⠉⠉⠉⢉⠙⢞⡾⣽⢽⣺⣺⣺⣺⣺⢽⣝⡯⡿⡽⡽⡯⡯⡯⡯⡿⣽⣻⣞
⢮⣳⡳⣝⣞⣞⣞⢮⣻⣺⣺⣗⡏⠀⠀⢅⢑⢄⠈⠀⠠⢨⢢⢊⢿⣽⣺⣺⣺⡺⡮⣗⣗⢯⢯⢯⢯⢯⢯⢯⢯⣻⣺⣺⡺
⡳⡵⣝⣞⣞⣞⢮⣳⣳⣗⣿⡞⠀⠀⢌⢒⢦⢢⢣⢧⣣⡳⡣⡣⠪⣷⣳⣗⣗⣯⣻⣺⣺⢽⢽⢽⢽⢽⢽⣝⣗⣗⣗⢷⣝
⢽⢝⣞⣞⣞⡮⣟⣞⡷⣿⢿⡧⢀⢐⠠⠑⠕⡕⡕⡕⡮⡪⡪⠢⡱⣿⣷⣿⣺⣞⣾⣺⢾⡽⡽⡽⡽⣝⣗⣗⣗⢷⣝⣗⣗
⢽⣕⣗⣗⣗⡯⡟⠎⠋⠊⠁⠉⢐⠄⡅⠅⠕⠜⠜⢜⢘⢌⢪⠪⠞⡋⡍⡍⡌⢪⢹⢚⠯⣿⢽⡯⡯⣗⣗⢷⣝⣗⣗⣗⣗
⣳⣳⣳⣳⡳⡣⠁⠀⠀⠀⠀⠀⠀⠑⢌⠪⠨⠈⠌⠐⡐⡰⠁⢀⠱⡸⡼⣜⢜⠌⠊⠈⢊⢒⢍⢟⢽⣳⢽⣳⣳⣳⣳⣳⡳
⣺⣺⡺⡮⣗⣕⢕⢄⡀⠀⠀⠀⠀⠀⠀⠈⠈⢈⠠⣱⣾⠃⠀⢀⠱⡱⡹⣜⢜⢔⢄⢆⢆⣇⢯⡫⡎⡯⣟⣞⣞⣞⣞⡮⡯
⡺⡮⡯⡯⣗⣗⣯⢮⣮⣳⣲⣢⢦⣢⣆⣆⡵⠴⠻⡙⡛⠄⠅⡀⠂⢌⠪⡪⠪⡳⡕⡯⣗⣯⢿⢝⢎⢎⣷⣳⣳⣳⡳⡯⡯
⢽⢽⢽⣝⣞⣞⢾⢽⣺⣳⣻⣟⣿⢻⠪⠂⡂⠅⡑⡐⠌⠌⠢⡐⡈⠀⠨⠨⠨⡘⢜⢜⢜⢎⢇⢏⢎⢮⣞⣷⣳⡳⡯⡯⡯
⢽⢽⣕⣗⢷⢽⣝⣗⣗⣗⣗⣟⢞⠔⡁⠀⢂⠁⡂⠂⠅⡑⠄⢂⠢⠡⠐⠈⠀⠂⠂⠕⢌⢊⢎⠪⡪⣞⣷⣳⣗⡯⡯⡯⡯
⣝⣗⢷⢽⣝⣗⣗⣗⣗⣗⣗⣯⡳⡕⣔⢀⠀⠂⠠⠁⠅⠂⠅⢂⠈⠌⢌⢐⢀⠀⡁⠅⠐⡐⢠⣱⣾⣻⣞⣞⢾⢽⢽⢽⣝
⡺⡮⣯⣳⣳⣳⣳⣳⣳⣳⡳⡯⣯⣗⢵⡱⡢⣀⠀⠂⠈⠀⠁⠠⠀⠀⠀⠐⠐⢐⢔⣬⣴⡾⣿⢽⣞⣷⣳⢯⢯⢯⢯⣗⣗
⢽⣝⣞⣞⣞⣞⣞⣞⣞⡮⡯⡯⣗⣟⡷⣯⣺⣜⣝⢖⢆⣆⢦⢄⢦⡰⣔⣦⢷⣻⣟⣯⢷⣻⢽⣻⣺⣺⣺⢽⢽⣝⣗⣗⣗
⣳⣳⣳⣳⣳⣳⣳⣳⡳⡯⡯⡯⣗⢷⢯⣗⣟⡾⡽⣯⢷⢷⣻⢽⣻⣻⢽⣞⡯⣗⣗⣯⣻⣺⢽⣺⣺⣺⣺⣝⣗⣗⣗⣗⣗
⡺⡺⡪⡮⡪⡮⣪⡺⡪⣏⢯⡫⡮⣫⢳⢳⡳⡯⡯⡯⣯⣻⣺⢽⣺⡺⣽⡺⣝⣗⣗⣗⢷⢽⢽⣺⣺⣺⣺⣺⣺⣺⣺⡺⡮
```

<!--- vim: set ts=2 sw=2 tw=80 et ft=markdown : -->
