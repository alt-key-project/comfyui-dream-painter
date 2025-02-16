# -*- coding: utf-8 -*-
from typing import List

from PIL import Image, ImageFilter, ImageEnhance
from torch import Tensor
from .images import Painter_Image

class BitMapImage:
    TYPE_NAME = "SINGLE_BITMAP"

    def __init__(self, pil_image: Image):
        if pil_image.mode != "1":
            self._pil_image = pil_image.convert("1")
        else:
            self._pil_image = pil_image

    def as_pil_image(self, mode = "1") -> Image:
        if mode == "1":
            return self._pil_image
        else:
            return self._pil_image.convert(mode)

    def as_tensor_image(self, with_alpha = False) -> Tensor:
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