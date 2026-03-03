import argparse
import array
import struct
from collections import defaultdict
from typing import Callable, Iterable
import sys

import pyvips

from .chars import PairCharset
from .util import Debug
from .stat import BoxplotCharset, boxplot, percentile, plot


def _to_grey(image: pyvips.Image) -> pyvips.Image:
    if image.bands > 1:
        if image.hasalpha():
            image = image.flatten()
        return image.colourspace(pyvips.Interpretation.B_W)
    return image


def histogram(image: pyvips.Image) -> list[int]:
    data = bytes(_to_grey(image).hist_find().write_to_memory())
    return list(struct.unpack(f'{len(data) // 4}I', data))


class ImgData:
    def __init__(self, image: pyvips.Image):
        self.pixels = array.array(  # type: ignore[type-var]
            'B', bytes(image.write_to_memory())
        )
        self.width, self.height = image.width, image.height


type ThresholdFunc = Callable[[tuple[float, float]], float]
type ThresholdFuncFactory = Callable[[pyvips.Image, int], ThresholdFunc]


def thr_percentile_factory(
    image: pyvips.Image, percent: int = 50,
) -> ThresholdFunc:
    threshold = percentile(histogram(image), percent)
    Debug.log(f'{percent}th percentile at brightness level {threshold}')
    return lambda pixel: threshold


def thr_const_factory(
    image: pyvips.Image, threshold: int = 127,
) -> ThresholdFunc:
    return lambda pixel: threshold


def thr_btw_extr_factory(image: pyvips.Image, _: int | None) -> ThresholdFunc:
    grey = _to_grey(image)
    extrema = (int(grey.min()), int(grey.max()))
    threshold = sum(extrema) / 2
    Debug.log(f'min/max brightness {extrema} -> threshold={threshold}')
    return lambda pixel: threshold


def thr_median_factory(image: pyvips.Image, _: int | None) -> ThresholdFunc:
    return thr_percentile_factory(image, 50)


def thr_local_avg_factory(
    image: pyvips.Image, blur_radius: int = 0
) -> ThresholdFunc:
    def threshold(pixel: tuple[float, float]) -> int:
        if pixel[0] > width or pixel[1] > height:
            return 0
        assert isinstance(
            pixelvalue := pixels[
                int(pixel[0]) + int(pixel[1]) * width
            ], int
        )
        return pixelvalue
    width, height = image.width, image.height
    blur_radius = blur_radius or max(
        12, min(width, height) // 16
    )
    Debug.log(f'gaussian blur radius for `local` mode: {blur_radius}')
    pixels = bytes(_to_grey(image.gaussblur(blur_radius)).write_to_memory())
    return threshold


THRESHOLD_FUNC_FACTORIES: dict[
    str, tuple[ThresholdFuncFactory, tuple[int, int] | None, int | None]
] = {
    'extrema': (thr_btw_extr_factory, None, None),
    'median': (thr_median_factory, None, None),
    'percentile': (thr_percentile_factory, (0, 99), 50),
    'const': (thr_const_factory, (0, 255), 127),
    'local': (thr_local_avg_factory, (0, 9999), None),
}


def get_threshold_func(
    image: pyvips.Image, options: argparse.Namespace
) -> ThresholdFunc:
    try:
        return THRESHOLD_FUNC_FACTORIES[options.threshold_mode][0](
            image, options.threshold_arg
        )
    except Exception as e:
        Debug.show(sys.stderr)
        raise e


def sharpen(
    image: pyvips.Image, factor: int, blur_radius: float
) -> pyvips.Image:
    if factor < 1:
        return image
    smot = image.gaussblur(blur_radius)
    f = image.cast('float')
    s = smot.cast('float')
    # iter 1: add(image, subtract(image, smot) * factor)
    diff1 = f - s
    f = (f + (diff1 > 0).ifthenelse(diff1 * factor, 0.0)).cast('uchar')
    # iter 2: subtract(image, subtract(smot, image) * factor)
    f2 = f.cast('float')
    diff2 = s - f2
    f = (f2 - (diff2 > 0).ifthenelse(diff2 * factor, 0.0)).cast('uchar')
    Debug.log(f'edge emphasis by factor {factor}')
    return f


def find_thresholds(
    image: pyvips.Image, options: argparse.Namespace,
) -> list[int]:
    func = get_threshold_func(image, options)
    adjust_brightness = 100 / options.brightness
    frequencies: dict[int, int] = defaultdict(int)
    for py in range(0, image.height, 16):
        for px in range(0, image.width, 16):
            threshold = func((px, py)) * adjust_brightness
            frequencies[round(threshold)] += 1
    return [
        frequencies[i] for i in range(256)
    ]


def plot_brightness_and_threshold(
    image: pyvips.Image, options: argparse.Namespace,
    cols: int = 80, rows: int = 8,
    charset: PairCharset = 'ascii',
) -> Iterable[str]:
    hist = histogram(image)
    boxplotcharset: BoxplotCharset = (
        'ascii' if charset == 'ascii' else 'utf8'
    )
    yield from plot(
        hist, c=cols, r=rows,
        fns=boxplotcharset,
        charset=charset,
    )
    thresholds = find_thresholds(image, options)
    yield boxplot(
        thresholds, c=cols, charset=boxplotcharset,
    )
