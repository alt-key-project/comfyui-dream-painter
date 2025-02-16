from ..conf import NodeCategories
from ..core import BitMapImage, BitMapImageList
from torch import Tensor

from ..core.images import Painter_Image, PaintColor


class DPaint_BitmapToImage:
    NODE_NAME = "Bitmap To Image"
    ICON = "🙾"
    CATEGORY = NodeCategories.BITMAP_CONVERTERS
    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("IMAGE", )
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImageList.TYPE_NAME, {}),
                "color_0_hex": ("STRING", {"default": "000000"}),
                "color_1_hex": ("STRING", {"default": "ffffff"}),
                "mode": (["RGB", "RGBA"], {"default": "RGB"})
            }
        }

    def result(self, BITMAP : BitMapImageList, color_0_hex: str, color_1_hex: str, mode: str):
        pil_images = [Painter_Image(pil_image=bm.as_pil_image(mode, PaintColor(color_0_hex), PaintColor(color_1_hex))) for bm in BITMAP]
        return (Painter_Image.join_to_tensor_data(pil_images),)


class DPaint_ImageToBitmap:
    NODE_NAME = "Image To Bitmap"
    ICON = "🙾"
    CATEGORY = NodeCategories.BITMAP_CONVERTERS
    RETURN_TYPES = (BitMapImageList.TYPE_NAME, )
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
        bitmaps = [BitMapImage(pimg.point_1(lambda p: p > t and 255, "1").pil_image) for pimg in painter_images]
        return (bitmaps,)
