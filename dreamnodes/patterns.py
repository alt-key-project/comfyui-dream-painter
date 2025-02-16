import os

from ..core import Painter_Image
from ..conf import NodeCategories
from ..core import BitMapImage, BitMapImageList, BitCanvas

WHITE = "#ffffff"
BLACK = "#000000"


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
