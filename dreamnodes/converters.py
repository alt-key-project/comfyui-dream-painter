from ..conf import NodeCategories
from ..core import BitMapImage, BitMapImageList
from torch import Tensor

from ..core.images import Painter_Image


class DPaint_BitmapToImage:
    NODE_NAME = "Bitmap To Image"
    ICON = "🙾"
    CATEGORY = NodeCategories.IMAGE_CONVERTERS
    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("IMAGE", )
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImageList.TYPE_NAME, {}),
                "mode": (["RGB", "RGBA"], {"default": "RGB"})
            }
        }

    def result(self, BITMAP : BitMapImageList, mode: str):
        pil_images = [Painter_Image(pil_image=bm.as_pil_image(mode)) for bm in BITMAP]
        return (Painter_Image.join_to_tensor_data(pil_images),)


class DPaint_ImageToBitmap:
    NODE_NAME = "Image To Bitmap"
    ICON = "🙾"
    CATEGORY = NodeCategories.IMAGE_CONVERTERS
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
        #for bm in bitmaps:

        return (bitmaps,)
