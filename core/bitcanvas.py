# -*- coding: utf-8 -*-
from typing import List, Tuple

from PIL import Image, ImageFilter, ImageEnhance, ImageOps
from PIL.ImageDraw import ImageDraw

from . import Vector2d
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
    COLOR_BLACK = "black"
    COLOR_WHITE = "white"

    def __init__(self, width: int|float, height: int|float):
        self._pil_image = Image.new(mode="1", size=(int(round(width)),int(round(height))))
        self._draw = ImageDraw(im=self._pil_image,mode="1")
        self._draw.fill = True
        self._fill_color = BitCanvas.COLOR_WHITE

    def combine_xor(self, other):
        self._pil_image = BitMapImage(self._pil_image).logical_xor(BitMapImage(other._pil_image))

    def set_fill(self, fill):
        if fill:
            self._draw.fill = True
        else:
            self._draw.fill = False

    def clear_copy(self):
        return BitCanvas(self.width, self.height)

    @property
    def width(self):
        return self._pil_image.width

    @property
    def height(self):
        return self._pil_image.height

    def multiply_vector_with_dimensions(self, v : Vector2d) -> Vector2d:
        return Vector2d(v.x * self.width, v.y * self.height)

    def flip_draw_color(self):
        if self._fill_color == "white":
            self._fill_color ="black"
        else:
            self._fill_color = "white"

    def set_color(self, color):
        if isinstance(color, str):
            if BitCanvas.COLOR_WHITE == color:
                self._fill_color = color
            else:
                self._fill_color = BitCanvas.COLOR_BLACK
        else:
            if color:
                self._fill_color = BitCanvas.COLOR_WHITE
            else:
                self._fill_color = BitCanvas.COLOR_BLACK

    def _pil_color(self):
        if self._fill_color == "black":
            return (0,)
        else:
            return (1,)

    def line(self, x1, y1, x2, y2, width):
        self._draw.line(xy = ((x1,y1),(x2,y2)), fill=self._pil_color(), width=width)

    def polygon(self, points: List[Tuple[int|float,int|float]]):
        self._draw.polygon(xy=points,fill=self._pil_color(), outline=self._pil_color())

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