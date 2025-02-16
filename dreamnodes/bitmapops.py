from ..conf import NodeCategories
from ..core import BitMapImage, BitMapImageList

class DPaint_LogicalInvert:
    NODE_NAME = "Bitmap Invert"
    ICON = "◈"
    CATEGORY = NodeCategories.BITMAP_PROCESSING
    RETURN_TYPES = (BitMapImageList.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImageList.TYPE_NAME, {})
            }
        }

    def result(self, BITMAP : BitMapImageList):
        res = list()
        for bm in BITMAP:
            res.append(bm.invert())
        return (BitMapImageList(res),)

class DPaint_LogicalOR:
    NODE_NAME = "Bitmap OR"
    ICON = "∨"
    CATEGORY = NodeCategories.BITMAP_COMBINERS
    RETURN_TYPES = (BitMapImageList.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImageList.TYPE_NAME, {}),
                "BITMAP2": (BitMapImageList.TYPE_NAME, {})
            }
        }

    def result(self, BITMAP : BitMapImageList, BITMAP2 : BitMapImageList):
        res = list()
        for i in range(min(len(BITMAP2), len(BITMAP2))):
            res.append(BITMAP[i].logical_or(BITMAP2[i]))
        return (BitMapImageList(res),)

class DPaint_LogicalAND:
    NODE_NAME = "Bitmap AND"
    ICON = "∧"
    CATEGORY = NodeCategories.BITMAP_COMBINERS
    RETURN_TYPES = (BitMapImageList.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImageList.TYPE_NAME, {}),
                "BITMAP2": (BitMapImageList.TYPE_NAME, {})
            }
        }

    def result(self, BITMAP : BitMapImageList, BITMAP2 : BitMapImageList):
        res = list()
        for i in range(min(len(BITMAP2), len(BITMAP2))):
            res.append(BITMAP[i].logical_and(BITMAP2[i]))
        return (BitMapImageList(res),)

class DPaint_LogicalXOR:
    NODE_NAME = "Bitmap XOR"
    ICON = "⊻"
    CATEGORY = NodeCategories.BITMAP_COMBINERS
    RETURN_TYPES = (BitMapImageList.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImageList.TYPE_NAME, {}),
                "BITMAP2": (BitMapImageList.TYPE_NAME, {})
            }
        }

    def result(self, BITMAP : BitMapImageList, BITMAP2 : BitMapImageList):
        res = list()
        for i in range(min(len(BITMAP2), len(BITMAP2))):
            res.append(BITMAP[i].logical_xor(BITMAP2[i]))
        return (BitMapImageList(res),)
