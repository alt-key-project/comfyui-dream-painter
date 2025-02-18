# -*- coding: utf-8 -*-
from typing import List, Tuple

from PIL import Image, ImageFilter, ImageEnhance, ImageOps
from PIL.ImageDraw import ImageDraw

from .bitmap import BitMapImage


def _cf(v: int|float):
    if (isinstance(v, float)):
        v = round(v)
    return int(v)

def _coord_box(c1: tuple, c2: tuple):
    x0 = min(_cf(c1[0]), _cf(c2[0]))
    x1 = max(_cf(c1[0]), _cf(c2[0]))
    y0 = min(_cf(c1[1]), _cf(c2[1]))
    y1 = max(_cf(c1[1]), _cf(c2[1]))
    return [(x0,y0),(x1,y1)]

class BitCanvas:
    def __init__(self, width: int|float, height: int|float):
        self._pil_image = Image.new(mode="1", size=(int(round(width)),int(round(height))))
        self._draw = ImageDraw(im=self._pil_image,mode="1")
        self._draw.fill = True
        self._fill_color = "white"

    def flip_draw_color(self):
        if self._fill_color == "white":
            self._fill_color ="black"
        else:
            self._fill_color = "white"

    def color_black(self):
        self._fill_color = "black"

    def color_white(self):
        self._fill_color = "white"

    def ellipse(self, coordinate1: Tuple[int|float,int|float], coordinate2: Tuple[int|float,int|float]):
        self._draw.ellipse(_coord_box(coordinate1, coordinate2), fill=self._fill_color, width=0)

    def rectangle(self, coordinate1: Tuple[int|float,int|float], coordinate2: Tuple[int|float,int|float]):
        self._draw.rectangle(_coord_box(coordinate1, coordinate2), fill=self._fill_color, width=0)

    def bitmap(self):
        return BitMapImage(self._pil_image.convert("1"))