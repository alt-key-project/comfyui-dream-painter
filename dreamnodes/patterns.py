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
                "circle_width_x": ("INT", {"min": 1, "max": 10000, "default": 32}),
                "circle_width_y": ("INT", {"min": 1, "max": 10000, "default": 32}),
                "center_x": ("INT", {"min": 1, "max": 10000, "default": 256}),
                "center_y": ("INT", {"min": 1, "max": 10000, "default": 256}),
            }
        }

    def result(self, width, height, circle_width_x, circle_width_y, center_x, center_y):
        dist_x = max(abs(width-center_x), abs(center_x))
        dist_y = max(abs(height-center_y), abs(center_y))
        num_circles = 1 + max(int(round(dist_x / circle_width_x)),int(round(dist_y / circle_width_y)))
        canvas = BitCanvas(width, height)
        for i in range(num_circles):
            radius_x = round(circle_width_x * (num_circles-i))
            radius_y = round(circle_width_y * (num_circles-i))
            canvas.ellipse((center_x - radius_x, center_y - radius_y),
                           (center_x + radius_x, center_y + radius_y))
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
