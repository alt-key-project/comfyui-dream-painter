import math

from ..core import Vector2d, BitCanvas
from ..conf import NodeCategories
from ..core import BitMapImage, BitMapImageList, Shape, ShapeContent

class DPaint_BitmapDrawShape:
    NODE_NAME = "Draw Shape As Bitmap"
    ICON = "🖌"
    CATEGORY = NodeCategories.BITMAP_GENERATE
    RETURN_TYPES = (BitMapImageList.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "SHAPE": (Shape.TYPE_NAME,),
                "fill": (["yes", "no"],),
                "bitmap_width": ("INT", {"default": 512}),
                "bitmap_height": ("INT", {"default": 512}),
                "shape_offset_x": ("INT", {"default": 0}),
                "shape_offset_y": ("INT", {"default": 0}),
                "line_width": ("INT", {"default": 1}),
            }
        }

    def result(self, SHAPE, bitmap_width, bitmap_height, shape_offset_x, shape_offset_y, fill: str, line_width):
        canvas = BitCanvas(bitmap_width, bitmap_height)
        s = SHAPE
        if shape_offset_x or shape_offset_y:
            s = s.copy()
            s.translate(shape_offset_x / bitmap_width, shape_offset_y / bitmap_width)
        s.draw_normal(canvas, fill == "yes", line_width)
        return (BitMapImageList([canvas.bitmap()]),)


class DPaint_Ellipse:
    NODE_NAME = "Ellipse Shape"
    ICON = "◯"
    CATEGORY = NodeCategories.SHAPE
    RETURN_TYPES = (Shape.TYPE_NAME,)
    RETURN_NAMES = ("SHAPE",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "shape_width": ("FLOAT", {"default": 0.75, "step": 0.01}),
                "shape_height": ("FLOAT", {"default": 0.75, "step": 0.01}),
                "center_x": ("FLOAT", { "default": 0.5, "step": 0.01}),
                "center_y": ("FLOAT", {"default": 0.5, "step": 0.01}),
                "shape_resolution": ("INT", {"min": 3, "max": 1000, "default": 24}),
            }
        }

    def result(self, shape_width, shape_height, center_x, center_y, shape_resolution):
        c = Vector2d(center_x, center_y)
        vectors = list()
        for i in range(shape_resolution):
            r = i / shape_resolution
            x = shape_width * 0.5 * math.sin(r * 2 * math.pi)
            y = shape_height * 0.5 * math.cos(r * 2 * math.pi)
            v = Vector2d(x,y)
            vectors.append(c.add(v))
        return (Shape([ShapeContent(vectors, ShapeContent.TYPE_POLYGON)]),)


