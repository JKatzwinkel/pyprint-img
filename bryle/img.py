import argparse
import array
from collections import defaultdict
from typing import Callable, Iterable
import sys

from PIL import Image, ImageChops, ImageFilter

from .chars import PairCharset
from .util import Debug
from .stat import BoxplotCharset, boxplot, percentile, plot


class ImgData:
    def __init__(self, image: Image.Image):
        self.pixels = array.array(  # type: ignore[type-var]
            'B', image.get_flattened_data()
        )
        self.width, self.height = image.size


type ThresholdFunc = Callable[[tuple[float, float]], float]
type ThresholdFuncFactory = Callable[[Image.Image, int], ThresholdFunc]


def thr_percentile_factory(
    image: Image.Image, percent: int = 50,
) -> ThresholdFunc:
    threshold = percentile(image.convert('L').histogram(), percent)
    Debug.log(f'{percent}th percentile at brightness level {threshold}')
    return lambda pixel: threshold


def thr_const_factory(
    image: Image.Image, threshold: int = 127,
) -> ThresholdFunc:
    return lambda pixel: threshold


def thr_btw_extr_factory(image: Image.Image, _: int | None) -> ThresholdFunc:
    threshold = sum(
        (extrema := image.convert('L').getextrema())  # type: ignore[arg-type]
    ) / 2
    Debug.log(f'min/max brightness {extrema} -> threshold={threshold}')
    return lambda pixel: threshold


def thr_median_factory(image: Image.Image, _: int | None) -> ThresholdFunc:
    return thr_percentile_factory(image, 50)


def thr_local_avg_factory(
    image: Image.Image, blur_radius: int = 0
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
    width, height = image.size
    blur_radius = blur_radius or max(
        12, min(width, height) // 16
    )
    Debug.log(f'gaussian blur radius for `local` mode: {blur_radius}')
    pixels = image.filter(
        ImageFilter.GaussianBlur(blur_radius)
    ).convert('L').get_flattened_data()
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
    image: Image.Image, options: argparse.Namespace
) -> ThresholdFunc:
    try:
        return THRESHOLD_FUNC_FACTORIES[options.threshold_mode][0](
            image, options.threshold_arg
        )
    except Exception as e:
        Debug.show(sys.stderr)
        raise e


def sharpen(
    image: Image.Image, factor: int, blur_radius: float
) -> Image.Image:
    if factor < 1:
        return image
    smot = image.filter(ImageFilter.GaussianBlur(blur_radius))
    for chops, images in (
        (ImageChops.add, (image, smot)), (ImageChops.subtract, (smot, image))
    ):
        image = chops(
            image, ImageChops.subtract(*images).point(
                lambda p: p * factor
            )
        )
    Debug.log(f'edge emphasis by factor {factor}')
    return image


def find_thresholds(
    image: Image.Image, options: argparse.Namespace,
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
    image: Image.Image, options: argparse.Namespace,
    cols: int = 80, rows: int = 8,
    charset: PairCharset = 'ascii',
) -> Iterable[str]:
    histogram = image.histogram()
    boxplotcharset: BoxplotCharset = (
        'ascii' if charset == 'ascii' else 'utf8'
    )
    yield from plot(
        histogram, c=cols, r=rows,
        fns=boxplotcharset,
        charset=charset,
    )
    thresholds = find_thresholds(image, options)
    yield boxplot(
        thresholds, c=cols, charset=boxplotcharset,
    )
