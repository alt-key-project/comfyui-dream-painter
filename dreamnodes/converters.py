from ..core import Vector2d
from ..conf import NodeCategories
from ..core import BitMapImage
from ..core import Shape, BitCanvas
from torch import Tensor

from ..core.images import Painter_Image, PaintColor


class DPaint_BitmapToImage:
    """Converts a bitmap into an RGB image and a mask."""
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

    def result(self, BITMAP: BitMapImage, color_0_hex: str, color_1_hex: str):
        return BITMAP.as_tensor_image_and_mask(PaintColor(color_0_hex), PaintColor(color_1_hex))


class DPaint_ImageToBitmap:
    """Converts an image into a bitmap."""
    NODE_NAME = "Image To Bitmap"
    ICON = "🙾"
    CATEGORY = NodeCategories.BITMAP_CONVERTERS
    RETURN_TYPES = (BitMapImage.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
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
            return (BitMapImage.new_of_size(1, 1),)


class DPaint_BitmapDrawShape:
    """Renders a shape as a bitmap."""
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
                "shape_bound_x_min": ("FLOAT", {"default": 0.0}),
                "shape_bound_y_min": ("FLOAT", {"default": 0.0}),
                "shape_bound_x_max": ("FLOAT", {"default": 1.0}),
                "shape_bound_y_max": ("FLOAT", {"default": 1.0}),
                "bitmap_width": ("INT", {"default": 512, "min": BitMapImage.MIN_SIZE_PIXELS}),
                "bitmap_height": ("INT", {"default": 512, "min": BitMapImage.MIN_SIZE_PIXELS}),
                "line_width": ("INT", {"default": 1}),
            }
        }

    def result(self, SHAPE, bitmap_width, bitmap_height, shape_bound_x_min, shape_bound_y_min, shape_bound_x_max,
               shape_bound_y_max, fill: str, line_width, draw_mode):
        canvas = BitCanvas(bitmap_width, bitmap_height)
        do_fill = fill == "yes"
        s = SHAPE.copy()
        #s.scale(new_width / current_width, new_height / current_height)
        viewport = (Vector2d(shape_bound_x_min, shape_bound_y_min), Vector2d(shape_bound_x_max, shape_bound_y_max))
        if draw_mode == "normal":
            s.draw_normal(canvas, do_fill, line_width, viewport=viewport)
        elif draw_mode == "xor":
            s.draw_xor(canvas, do_fill, line_width, viewport=viewport)
        return (canvas.bitmap(),)
