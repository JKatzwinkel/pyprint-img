# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: profile=True

from typing import Callable, Iterable

import cython

from .args import DitherMethod
from .chars import braille
from .img import ImgData, ThresholdFunc
from .util import Debug


def sample_func(
    img: ImgData,
    sx: cython.double,
    sy: cython.double,
    interpolate: cython.bint = True,
) -> Callable[[int, int], int]:
    width: cython.int = img.width
    height: cython.int = img.height

    def getpixel(px: cython.int, py: cython.int) -> cython.int:
        pixelvalue = img.pixels[px + py * width]
        return pixelvalue

    def getvalues(px: cython.double, py: cython.double) -> cython.int[4]:
        x1: cython.int = int(px)
        y1: cython.int = int(py)
        V: cython.int[4] = [getpixel(x1, y1)] * 4
        if x1 + 1 < width:
            V[1] = getpixel(x1 + 1, y1)
            if y1 + 1 < height:
                V[3] = getpixel(x1 + 1, y1 + 1)
        if y1 + 1 < height:
            V[2] = getpixel(x1, y1 + 1)
        return V

    def sample(x: cython.int, y: cython.int) -> cython.int:
        px: cython.float = sx * x
        py: cython.float = sy * y
        if px > width or py > height:
            return 0
        if not interpolate:
            return getpixel(int(px), int(py))
        V = getvalues(px, py)
        dx: cython.double = px - int(px)
        wx1: cython.double = V[0] + (V[1] - V[0]) * dx
        wx2: cython.double = V[2] + (V[3] - V[2]) * dx
        dy: cython.double = py - int(py)
        result: cython.double = wx1 + (wx2 - wx1) * dy
        return round(result)

    return sample


DITHER_ERROR_RECIPIENTS = {
    'atkinson': [
        (1, 0, 2), (2, 0, 2), (-1, 1, 2), (0, 1, 2), (1, 1, 2), (0, 2, 2),
    ],
    'floyd-steinberg': [
        (1, 0, 7), (-1, 1, 3), (0, 1, 5), (1, 1, 1),
    ],
}


def rasterize(
    imdat: ImgData,
    r: int, c: int, w: int, h: int,
    /, *,
    zoom: float, crop_y: bool,
    interpolate: bool,
    threshold: ThresholdFunc,
    dither_method: DitherMethod,
    adjust_brightness: float,
    dither: float,
    inverted: bool,
) -> Iterable[str]:

    error_recipients = DITHER_ERROR_RECIPIENTS[dither_method]

    def dither_victims(x: int, y: int) -> Iterable[
        tuple[int, int, float]
    ]:
        for dx, dy, weight in error_recipients:
            if not 0 <= (rx := x + dx) < max_col * 2:
                continue
            if (ry := y + dy) >= max_row * 4:
                continue
            yield rx, ry, weight

    cw, ch = w / c, h / r
    sx, sy = cw / zoom / 2, ch / zoom / 4
    Debug.log(
        f'xterm window dimensions: {w}×{h} pixels, {c}×{r} characters'
    ).log(
        f'character size in pixels: {cw:.2f}×{ch:.2f}'
    ).log(
        f'sample rate in pixels: {sx:.2f} horizontal, {sy:.2f} vertical'
    )
    max_row = round(imdat.height * zoom / ch) if not crop_y else min(
        round(imdat.height * zoom / ch), r
    )
    max_col = min(round(imdat.width * zoom / cw), c)
    Debug.log(f'using {max_col} columns × {max_row} rows')
    sample = sample_func(imdat, sx, sy, interpolate=interpolate)
    grid: list[float] = [
        sample(x, y)
        for y in range(max_row * 4)
        for x in range(max_col * 2)
    ]
    mono = []
    for y in range(max_row * 4):
        for x in range(max_col * 2):
            approx = (
                value := grid[y * max_col * 2 + x]
            ) * adjust_brightness >= threshold(
                (sx * x, sy * y)
            )
            mono.append(approx)
            error = (value - (247 * approx)) * dither / 16
            for dx, dy, weight in dither_victims(x, y):
                grid[dy * max_col * 2 + dx] += error * weight
    yield from characterize(
        mono, max_col, max_row, inverted,
    )


def characterize(
    mono: list[bool], max_col: int, max_row: int, inverted: bool,
) -> Iterable[str]:
    row: list[str] = []
    for cy in range(max_row):
        for cx in range(max_col):
            registers = [
                mono[
                    max_col * 2 * (cy * 4 + dy) + cx * 2 + dx
                ]
                for dx, dy in (
                    (0, 0), (1, 0),
                    (0, 1), (1, 1),
                    (0, 2), (1, 2),
                    (0, 3), (1, 3),
                )
            ]
            row.append(braille(registers, inverted=inverted))
        yield ''.join(row)
        row.clear()
