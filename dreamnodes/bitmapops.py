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

class DPaint_BitmapResize:
    NODE_NAME = "Bitmap Resize"
    ICON = "🔎"
    CATEGORY = NodeCategories.BITMAP_PROCESSING
    RETURN_TYPES = (BitMapImageList.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImageList.TYPE_NAME, {}),
            },
            "optional": {
                "width_multiplier": ("FLOAT",{"min": 0.05, "max": 1.0, "step": 0.025}),
                "width_pixels": ("INT",{"min":1}),
                "height_multiplier": ("FLOAT",{"min": 0.05, "max": 1.0, "step": 0.025}),
                "height_pixels": ("INT",{"min":1}),
            }
        }

    def result(self, BITMAP : BitMapImageList, **kwargs):
        result = list()
        for bm in BITMAP:
            current_width = bm.width
            current_height = bm.height
            new_width = max(1,kwargs.get("width_pixels", int(round(kwargs.get("width_multiplier", 1.0)*current_width))))
            new_height = max(1, kwargs.get("height_pixels", int(round(kwargs.get("height_multiplier", 1.0)*current_height))))
            if current_width != new_width or current_height != new_height:
                result.append(bm.resize_to(new_width, new_height))
            else:
                result.append(bm)
        return (BitMapImageList(result),)

class DPaint_BitmapCropCenter:
    NODE_NAME = "Bitmap Crop Center"
    ICON = "🔎"
    CATEGORY = NodeCategories.BITMAP_PROCESSING
    RETURN_TYPES = (BitMapImageList.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImageList.TYPE_NAME, {}),
                "width_multiplier": ("FLOAT", {"min": 0.0, "max": 1.0, "step": 0.025, "default": 0}),
                "width_pixels": ("INT", {"min": 0, "default": 0}),
                "height_multiplier": ("FLOAT", {"min": 0.0, "max": 1.0, "step": 0.025, "default": 0}),
                "height_pixels": ("INT", {"min": 0, "default": 0}),
            }
        }

    def result(self, BITMAP : BitMapImageList, width_multiplier, width_pixels, height_multiplier, height_pixels):
        result = list()
        for bm in BITMAP:
            current_width = bm.width
            current_height = bm.height
            new_width = width_pixels
            if new_width == 0:
                new_width = current_width * width_multiplier
            if new_width < 1:
                new_width = current_width
            new_height = height_pixels
            if new_height == 0:
                new_height = current_height * height_multiplier
            if new_height < 1:
                new_height = current_height
            new_height = min(new_height, current_height)
            new_width = min(new_width, current_width)
            if current_width != new_width or current_height != new_height:
                x = int(round((current_width - new_width) * 0.5))
                y = int(round((current_height - new_height) * 0.5))
                result.append(bm.crop(x,y,new_width, new_height))
            else:
                result.append(bm)
        return (BitMapImageList(result),)


class DPaint_BitmapExpandCanvas:
    NODE_NAME = "Bitmap Expand Canvas"
    ICON = "🔎"
    CATEGORY = NodeCategories.BITMAP_PROCESSING
    RETURN_TYPES = (BitMapImageList.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImageList.TYPE_NAME, {}),
                "color": (["black","white"],),
                "border_pixels": ("INT", {"min": 1, "default": 16}),
            }
        }

    def result(self, BITMAP : BitMapImageList, color, border_pixels):
        result = list()
        for bm in BITMAP:
            new_width = bm.width + 2 * border_pixels
            new_height = bm.height + 2 * border_pixels

            c = (0,)
            if color == "white":
                c = (1,)

            new_bm = BitMapImage.new_of_size(new_width, new_height, c)
            result.append(new_bm.paste(bm, border_pixels, border_pixels))
        return (BitMapImageList(result),)

class DPaint_BitmapRotate:
    NODE_NAME = "Bitmap Rotate"
    ICON = "🔎"
    CATEGORY = NodeCategories.BITMAP_PROCESSING
    RETURN_TYPES = (BitMapImageList.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImageList.TYPE_NAME, {}),
                "degrees": ("FLOAT", {"min": -360, "max": 360, "step": 5, "default": 45}),
                "center_x": ("INT", {"min": 1, "default": 256}),
                "center_y": ("INT", {"min": 1, "default": 256}),
                "expand": ("BOOLEAN",),
                "fill_color": (["black","white"],),
            }
        }

    def result(self, BITMAP : BitMapImageList,degrees, center_x, center_y, fill_color, expand):
        result = list()
        for bm in BITMAP:
            if fill_color == "black":
                fill_color = 0
            else:
                fill_color = 1

            result.append(bm.rotate(center_x, center_y, degrees, expand, fill_color))
        return (BitMapImageList(result),)