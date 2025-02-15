from ..conf import NodeCategories
from ..core import BitMapImage
from torch import Tensor

from ..core.images import Painter_Image


class DPaint_BitmapToImage:
    NODE_NAME = "Bitmap To Image"
    ICON = "🙾"
    CATEGORY = NodeCategories.IMAGE_CONVERTERS
    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("image", )
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bitmap": (BitMapImage.TYPE_NAME, {}),
                "mode": (["RGB", "RGBA"], {"default": "RGB"})
            }
        }

    def result(self, bitmap : BitMapImage, mode: str):
        return (bitmap.as_tensor_image(mode.endswith("A")),)

class DPaint_ImageToBitmap:
    NODE_NAME = "Image To Bitmap"
    ICON = "🙾"
    CATEGORY = NodeCategories.IMAGE_CONVERTERS
    RETURN_TYPES = (BitMapImage.TYPE_NAME, )
    RETURN_NAMES = ("bitmap", )
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", {}),
                "threshold": ("FLOAT", {"default": 0.5, "min": 0, "max": 1.0, "step": 0.05})
            }
        }

    def result(self, image: Tensor, threshold: float):
        t = int(round(255 * threshold))
        return (BitMapImage(Painter_Image(tensor_image=image).point(lambda p: p > t and 255, "1")),)
