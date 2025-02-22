import numpy, torch
from PIL import ImageOps

from ..conf import NodeCategories
from ..core import BitMapImage
from ..core import Shape, BitCanvas
from torch import Tensor

from ..core.images import Painter_Image, PaintColor


class DPaint_BitmapToImage:
    NODE_NAME = "Bitmap To Image & Mask"
    ICON = "🙾"
    CATEGORY = NodeCategories.BITMAP_CONVERTERS
    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("IMAGE", "MASK")
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImage.TYPE_NAME, {}),
                "color_0_hex": ("STRING", {"default": "000000"}),
                "color_1_hex": ("STRING", {"default": "ffffff"})
            }
        }

    def result(self, BITMAP : BitMapImage, color_0_hex: str, color_1_hex: str):
        return BITMAP.as_tensor_image_and_mask(PaintColor(color_0_hex), PaintColor(color_1_hex))


class DPaint_ImageToBitmap:
    NODE_NAME = "Image To Bitmap"
    ICON = "🙾"
    CATEGORY = NodeCategories.BITMAP_CONVERTERS
    RETURN_TYPES = (BitMapImage.TYPE_NAME, )
    RETURN_NAMES = ("BITMAP", )
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "IMAGE": ("IMAGE", {}),
                "threshold": ("FLOAT", {"default": 0.5, "min": 0, "max": 1.0, "step": 0.05})
            }
        }

    def result(self, IMAGE: Tensor, threshold: float):
        t = int(round(255 * threshold))
        painter_images = Painter_Image.images_from_tensor_data(IMAGE)
        if painter_images:
            return (BitMapImage(painter_images[0].point_1(lambda p: p > t and 255, "1").pil_image),)
        else:
            return (BitMapImage.new_of_size(1,1),)

class DPaint_BitmapDrawShape:
    NODE_NAME = "Draw Shape As Bitmap"
    ICON = "✎"
    CATEGORY = NodeCategories.BITMAP_GENERATE
    RETURN_TYPES = (BitMapImage.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "SHAPE": (Shape.TYPE_NAME,),
                "fill": (["yes", "no"],),
                "draw_mode": (["normal", "xor"],),
                "bitmap_width": ("INT", {"default": 512}),
                "bitmap_height": ("INT", {"default": 512}),
                "shape_offset_x": ("INT", {"default": 0}),
                "shape_offset_y": ("INT", {"default": 0}),
                "line_width": ("INT", {"default": 1}),
            }
        }

    def result(self, SHAPE, bitmap_width, bitmap_height, shape_offset_x, shape_offset_y, fill: str, line_width, draw_mode):
        canvas = BitCanvas(bitmap_width, bitmap_height)
        s = SHAPE
        if shape_offset_x or shape_offset_y:
            s = s.copy()
            s.translate(shape_offset_x / bitmap_width, shape_offset_y / bitmap_width)
        if draw_mode == "normal":
            s.draw_normal(canvas, fill == "yes", line_width)
        elif draw_mode == "xor":
            s.draw_xor(canvas, fill == "yes", line_width)
        return (canvas.bitmap(),)