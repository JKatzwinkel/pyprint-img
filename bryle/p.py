import argparse
from typing import Callable

from PIL import Image, ImageFilter

from .util import Debug


type ThresholdFunc = Callable[[tuple[float, float]], float]
type ThresholdFuncFactory = Callable[[Image.Image, int], ThresholdFunc]


def percentile(histogram: list[int], percent: int = 50) -> int:
    '''
    >>> percentile([0, 3, 2, 1], 50)
    1

    >>> percentile([0, 3, 2, 1], 66)
    2
    '''
    target = sum(histogram) * percent / 100
    acc = 0
    for i, count in enumerate(histogram):
        if (acc := acc + count) >= target:
            break
    Debug.log(f'{percent}th percentile at brightness level {i}')
    return i


def thr_percentile_factory(
    image: Image.Image, percent: int = 50,
) -> ThresholdFunc:
    threshold = percentile(image.convert('L').histogram(), percent)
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
        if pixel[0] > image.width or pixel[1] > image.height:
            return 0
        assert isinstance(
            pixelvalue := pixels[
                int(pixel[0]) + int(pixel[1]) * image.width
            ], int
        )
        return pixelvalue
    blur_radius = blur_radius or max(
        12, min(image.width, image.height) // 16
    )
    averaged = image.filter(
        ImageFilter.GaussianBlur(blur_radius)
    ).convert('L')
    Debug.log(f'gaussian blur radius for `local` mode: {blur_radius}')
    Debug.log(
        'min/max threshold values used in `local` mode: '
        f'{averaged.getextrema()}'
    )
    pixels = averaged.get_flattened_data()
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
    return THRESHOLD_FUNC_FACTORIES[options.threshold_mode][0](
        image, options.threshold_arg
    )


DITHER_ERROR_RECIPIENTS = {
    'atkinson': [
        (1, 0, 2), (2, 0, 2), (-1, 1, 2), (0, 1, 2), (1, 1, 2), (0, 2, 2),
    ],
    'floyd-steinberg': [
        (1, 0, 7), (-1, 1, 3), (0, 1, 5), (1, 1, 1),
    ],
}
