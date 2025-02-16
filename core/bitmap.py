# -*- coding: utf-8 -*-
from typing import List

from PIL import Image, ImageFilter, ImageEnhance, ImageChops
from torch import Tensor

from .images import Painter_Image, PaintColor


class BitMapImage:
    TYPE_NAME = "SINGLE_BITMAP"

    def __init__(self, pil_image: Image):
        if pil_image.mode != "1":
            self._pil_image = pil_image.convert("1")
        else:
            self._pil_image = pil_image

    def logical_xor(self, other):
        return BitMapImage(ImageChops.logical_xor(self._pil_image, other._pil_image))

    def logical_and(self, other):
        return BitMapImage(ImageChops.logical_and(self._pil_image, other._pil_image))

    def logical_or(self, other):
        return BitMapImage(ImageChops.logical_or(self._pil_image, other._pil_image))

    def invert(self):
        return BitMapImage(ImageChops.invert(self._pil_image))

    def as_pil_bitmap(self):
        return self._pil_image

    def as_pil_image(self, with_alpha=False, col0: PaintColor = PaintColor("000000"),
                     col1: PaintColor = PaintColor("ffffff")) -> Image:
        mode = "RGB"
        if with_alpha:
            mode += "A"

        red_range = (col0.red_int, col1.red_int)
        green_range = (col0.green_int, col1.green_int)
        blue_range = (col0.blue_int, col1.blue_int)
        alpha_range = (col0.alpha_int, col1.alpha_int)

        converted = self._pil_image.convert(mode)
        bands = converted.split()
        red_band = bands[0]
        green_band = bands[1]
        blue_band = bands[2]
        alpha_band = None
        if with_alpha:
            alpha_band = bands[3]
        red_band = red_band.point(lambda i: (i // 255) * (red_range[1] - red_range[0]) + red_range[0])
        green_band = green_band.point(lambda i: (i // 255) * (green_range[1] - green_range[0]) + green_range[0])
        blue_band = blue_band.point(lambda i: (i // 255) * (blue_range[1] - blue_range[0]) + blue_range[0])
        if with_alpha:
            alpha_band = alpha_band.point(lambda i: (i // 255) * (alpha_range[1] - alpha_range[0]) + alpha_range[0])
        if with_alpha:
            return Image.merge("RGBA", (red_band, green_band, blue_band, alpha_band))
        else:
            return Image.merge("RGB", (red_band, green_band, blue_band))

    def as_tensor_image(self, with_alpha=False) -> Tensor:
        mode = "RGB"
        if with_alpha:
            mode += "A"
        return Painter_Image(pil_image=self._pil_image.convert(mode)).tensor_image


class BitMapImageList:
    TYPE_NAME = "BITMAP"

    def __init__(self, bitmaps: List[BitMapImage]):
        self._bitmaps = bitmaps

    def __iter__(self):
        return iter(self._bitmaps)

    def __getitem__(self, item):
        return self._bitmaps[item]

    def __len__(self):
        return len(self._bitmaps)
