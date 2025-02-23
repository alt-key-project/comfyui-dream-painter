# -*- coding: utf-8 -*-
from typing import List, Tuple, Iterable

from PIL import Image, ImageFilter, ImageEnhance, ImageOps, ImageChops
from PIL.ImageDraw import ImageDraw
from typing_extensions import Self

from . import Vector2d
from .bitmap import BitMapImage


def _cf(v: int | float):
    if (isinstance(v, float)):
        v = round(v)
    return int(v)


def _coord_box(c1: tuple, c2: tuple):
    x0 = min(_cf(c1[0]), _cf(c2[0]))
    x1 = max(_cf(c1[0]), _cf(c2[0]))
    y0 = min(_cf(c1[1]), _cf(c2[1]))
    y1 = max(_cf(c1[1]), _cf(c2[1]))
    return [(x0, y0), (x1, y1)]


class BitCanvas:
    COLOR_BLACK = "black"
    COLOR_WHITE = "white"

    def __init__(self, width: int | float, height: int | float):
        self._pil_image = Image.new(mode="1", size=(int(round(width)), int(round(height))))
        self._draw = ImageDraw(im=self._pil_image, mode="1")
        self._draw.fill = True
        self._fill_color = BitCanvas.COLOR_WHITE
        self.width = self._pil_image.width
        self.height = self._pil_image.height
        self.last_x = self.width - 1
        self.last_y = self.height - 1

    def combine_xor(self, other: Self):
        self._pil_image = ImageChops.logical_xor(self._pil_image, other._pil_image)

    def set_fill(self, fill):
        if fill:
            self._draw.fill = True
        else:
            self._draw.fill = False

    def clear_copy(self):
        return BitCanvas(self.width, self.height)

    def multiply_vector_with_dimensions(self, v: Vector2d, viewport: Tuple[Vector2d, Vector2d]) -> Vector2d:
        viewport_width = viewport[1].x - viewport[0].x
        viewport_height = viewport[1].y - viewport[0].y
        normalized_v = Vector2d(
            (v.x - viewport[0].x) / viewport_width,
            (v.y - viewport[0].y) / viewport_height,
        )
        vout = Vector2d(normalized_v.x * self.last_x, normalized_v.y * self.last_y)
        if (vout.x < 0 or vout.x > self.last_x or vout.y < 0 or vout.y > self.last_y):
            print("VECTOR OUTSIDE VIEWPORT "+str(v)+" -> "+str(vout))
        return vout

    def flip_draw_color(self):
        if self._fill_color == "white":
            self._fill_color = "black"
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
        self._draw.line(xy=((x1, y1), (x2, y2)), fill=self._pil_color(), width=width)

    def polyline(self, xy: Iterable[Tuple[int | float, int | float]], width):
        self._draw.line(xy=xy, fill=self._pil_color(), width=width)

    def polygon(self, points: List[Tuple[int | float, int | float]]):
        self._draw.polygon(xy=points, fill=self._pil_color(), outline=self._pil_color())

    def color_black(self):
        self._fill_color = "black"

    def color_white(self):
        self._fill_color = "white"

    def ellipse(self, coordinate1: Tuple[int | float, int | float], coordinate2: Tuple[int | float, int | float]):
        self._draw.ellipse(_coord_box(coordinate1, coordinate2), fill=self._fill_color, width=0)

    def rectangle(self, coordinate1: Tuple[int | float, int | float], coordinate2: Tuple[int | float, int | float]):
        self._draw.rectangle(_coord_box(coordinate1, coordinate2), fill=self._fill_color, width=0)

    def bitmap(self):
        return BitMapImage(self._pil_image.convert("1"))
