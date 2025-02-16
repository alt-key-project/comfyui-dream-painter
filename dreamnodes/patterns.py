import os

from ..core import Painter_Image
from ..conf import NodeCategories
from ..core import BitMapImage, BitMapImageList
import drawsvg as draw
import tempfile

WHITE = "#ffffff"
BLACK = "#000000"

def _render_drawing(d: draw.Drawing):
    tmp = tempfile.NamedTemporaryFile(mode="wb", suffix = ".png", delete=False)
    d.save_png(tmp.name)
    im = Painter_Image(filepath = tmp.name)
    os.unlink(tmp.name)
    return BitMapImage(im.pil_image)


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
                "width": ("INT", {"min":1, "max": 10000, "default": 512}),
                "height": ("INT", {"min":1, "max": 10000, "default": 512}),
                "columns": ("INT", {"min":1, "max": 100, "default": 8}),
                "rows": ("INT", {"min":1, "max": 100, "default": 4}),
            }
        }

    def result(self, width, height, columns, rows):
        d = draw.Drawing(width, height, origin=(0,0))
        step_x = width / float(columns)
        step_y = height / float(rows)
        for r in range(rows):
            for c in range(columns):
                x = round(c * step_x)
                y = round(r * step_y)
                color = WHITE
                if ((r+c)%2 == 0):
                    color = BLACK
                d.append(draw.Rectangle(x, y, round(step_x), round(step_y), fill = color, stroke_width=0))
        return (BitMapImageList([_render_drawing(d)]),)