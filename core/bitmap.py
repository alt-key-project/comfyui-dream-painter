# -*- coding: utf-8 -*-
from io import BytesIO
from typing import List, Tuple

import numpy
import torch
from PIL import Image, ImageFilter, ImageEnhance, ImageChops, ImageOps
from torch import Tensor
from typing_extensions import Self
import PIL

from .images import Painter_Image, PaintColor

def fix_broken_image(pil_image: PIL.Image.Image) -> PIL.Image.Image:
    output = BytesIO()
    pil_image.save(output, format="JPG")
    output.flush()
    output.seek(0)
    return Image.open(output, formats=["JPG"])

class BitMapImage:
    TYPE_NAME = "BITMAP"
    MIN_SIZE_PIXELS = 4

    def __init__(self, pil_image: Image):
        if not isinstance(pil_image, PIL.Image.Image):
            raise Exception("Not a PIL Image - "+str(type(pil_image)))
        if pil_image.mode != "1":
            self._pil_image = pil_image.convert("1")
        else:
            self._pil_image = pil_image
        if self.width < BitMapImage.MIN_SIZE_PIXELS or self.height < BitMapImage.MIN_SIZE_PIXELS:
            factor = max(BitMapImage.MIN_SIZE_PIXELS / self.width, BitMapImage.MIN_SIZE_PIXELS / self.height)
            newimg = self.resize_to(int(round(factor * self.width)), int(round(factor * self.height)))
            self._pil_image = newimg._pil_image


    def paste(self, bitmap : Self, x, y):
        img = self._pil_image.copy()
        img.paste(bitmap._pil_image, (x,y))
        return BitMapImage(img)

    @classmethod
    def new_of_size(cls, width: int, height: int, fill_color = 0):
        return BitMapImage(Image.new("1",(width,height), color=fill_color))

    @property
    def _img(self) -> Image:
        return self._pil_image

    @property
    def width(self) -> int:
        return self._pil_image.size[0]

    @property
    def height(self) -> int:
        return self._pil_image.size[1]

    def resize_to(self, width, height):
        return BitMapImage(self._pil_image.resize((width,height)))

    def crop(self, x, y, width, height):
        return BitMapImage(self._pil_image.crop((x,y,x+width,y+height)))

    def logical_xor(self, other):
        return BitMapImage(ImageChops.logical_xor(self._pil_image, other._pil_image))

    def logical_and(self, other):
        return BitMapImage(ImageChops.logical_and(self._pil_image, other._pil_image))

    def logical_or(self, other):
        return BitMapImage(ImageChops.logical_or(self._pil_image, other._pil_image))

    def invert(self):
        return BitMapImage(ImageChops.invert(self._pil_image))

    def rotate(self, center_x, center_y, degrees, expand = True, fill_color = 0):
        if fill_color:
            fill_color = (1,)
        else:
            fill_color = (0,)
        return BitMapImage(self._pil_image.rotate(degrees, fillcolor = fill_color, resample=Image.BILINEAR, expand = expand, center = (center_x, center_y)))

    def edge_detect(self) -> Self:
        return BitMapImage(self._pil_image.filter(ImageFilter.FIND_EDGES).convert("1"))

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

        converted = self._pil_image.convert("L")
        gray_band = converted.split()[0]

        red_band = gray_band.point(lambda i: int((i // 255) * (red_range[1] - red_range[0]) + red_range[0]))
        green_band = gray_band.point(lambda i: int((i // 255) * (green_range[1] - green_range[0]) + green_range[0]))
        blue_band = gray_band.point(lambda i: int((i // 255) * (blue_range[1] - blue_range[0]) + blue_range[0]))
        if with_alpha:
            alpha_band = gray_band.point(lambda i:int((i // 255) * (alpha_range[1] - alpha_range[0]) + alpha_range[0]))
            return Image.merge("RGBA", (red_band, green_band, blue_band, alpha_band))
        else:
            return Image.merge("RGB", (red_band, green_band, blue_band))

    def as_tensor_image_and_mask(self, col0: PaintColor = PaintColor("000000"),
                     col1: PaintColor = PaintColor("ffffff")) -> Tuple[Tensor, Tensor]:
        def _convert_from_pil_to_tensor(pil_image):
            pil_image = pil_image.convert("RGBA")
            i = ImageOps.exif_transpose(pil_image)
            image = i.convert("RGB")
            image = numpy.array(image).astype(numpy.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            mask = numpy.array(i.getchannel('A')).astype(numpy.float32) / 255.0
            mask = 1. - torch.from_numpy(mask)
            return image, mask
        return _convert_from_pil_to_tensor(self.as_pil_image(with_alpha=True, col0=col0, col1= col1))
