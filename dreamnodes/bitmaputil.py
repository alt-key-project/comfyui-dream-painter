from ..conf import NodeCategories
from ..core import BitMapImage

class DPaint_Dimensions:
    """Returns dimensions of a bitmap."""
    NODE_NAME = "Bitmap Dimensions"
    ICON = "🔎"
    CATEGORY = NodeCategories.BITMAP
    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImage.TYPE_NAME, {}),
            }
        }

    def result(self, BITMAP: BitMapImage):
        return (BITMAP.width, BITMAP.height)
