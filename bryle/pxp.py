from typing import Callable, Iterable

from .args import DitherMethod
from .chars import braille
from .img import ImgData, ThresholdFunc
from .util import Debug


def sample_func(
    img: ImgData,
    sx: float, sy: float,
    interpolate: bool = True,
) -> Callable[[int, int], int]:

    def getpixel(px: int, py: int) -> int:
        pixelvalue = img.pixels[px + py * img.width]
        assert isinstance(pixelvalue, int), f'{pixelvalue}'
        return pixelvalue

    def getvalues(px: float, py: float) -> tuple[int, int, int, int]:
        x1, y1 = int(px), int(py)
        V = [getpixel(x1, y1)] * 4
        if x1 + 1 < img.width:
            V[1] = getpixel(x1 + 1, y1)
            if y1 + 1 < img.height:
                V[3] = getpixel(x1 + 1, y1 + 1)
        if y1 + 1 < img.height:
            V[2] = getpixel(x1, y1 + 1)
        return (
            V[0], V[1],
            V[2], V[3],
        )

    def sample(x: int, y: int) -> int:
        px, py = sx * x, sy * y
        if px > img.width or py > img.height:
            return 0
        if not interpolate:
            return getpixel(int(px), int(py))
        v1, v2, v3, v4 = getvalues(px, py)
        dx = px - int(px)
        wx1 = v1 + (v2 - v1) * dx
        wx2 = v3 + (v4 - v3) * dx
        dy = py - int(py)
        result = wx1 + (wx2 - wx1) * dy
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
            error = (value - (255 * approx)) * dither / 16
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
