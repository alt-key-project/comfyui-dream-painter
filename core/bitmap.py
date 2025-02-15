# -*- coding: utf-8 -*-
from PIL import Image, ImageFilter, ImageEnhance
from PIL.Image import Resampling
from PIL.ImageDraw import ImageDraw
from torch import Tensor
from .images import Painter_Image

class BitMapImage:
    TYPE_NAME = "BITMAP"

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

