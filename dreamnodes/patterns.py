import os, math

from ..core import Painter_Image
from ..conf import NodeCategories
from ..core import BitMapImage, BitMapImageList, BitCanvas

WHITE = "#ffffff"
BLACK = "#000000"


class DPaint_Bullseye:
    NODE_NAME = "Generate Bullseye"
    ICON = "🞋"
    CATEGORY = NodeCategories.BITMAP_GENERATE
    RETURN_TYPES = (BitMapImageList.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "height": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "circle_width": ("INT", {"min": 1, "max": 10000, "default": 64}),
            }
        }

    def result(self, width, height, circle_width):
        max_distance = round(math.sqrt(width*width+height*height))
        num_circles = 1 + int(round(max_distance / circle_width))
        canvas = BitCanvas(width, height)
        cx = round(width /2)
        cy = round(height/2)
        for i in range(num_circles):
            diameter = round((num_circles - i) * circle_width)
            radius = diameter / 2
            canvas.ellipse((cx - radius, cy - radius), (cx + radius, cx + radius))
            canvas.flip_draw_color()
        return (BitMapImageList([canvas.bitmap()]),)


class DPaint_CheckerBoard:
    NODE_NAME = "Generate Checkerboard"
    ICON = "🙾"
    CATEGORY = NodeCategories.BITMAP_GENERATE
    RETURN_TYPES = (BitMapImageList.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "height": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "columns": ("INT", {"min": 1, "max": 100, "default": 8}),
                "rows": ("INT", {"min": 1, "max": 100, "default": 4}),
            }
        }

    def result(self, width, height, columns, rows):
        canvas = BitCanvas(width, height)
        step_x = width / float(columns)
        step_y = height / float(rows)
        for r in range(rows):
            for c in range(columns):
                x = round(c * step_x)
                y = round(r * step_y)
                if (r + c) % 2 == 0:
                    canvas.rectangle((x, y), (x + step_x, y + step_y))
        return (BitMapImageList([canvas.bitmap()]),)
