from ..conf import NodeCategories
from ..core import BitMapImage


class DPaint_LogicalInvert:
    """Bitmap inverter."""
    NODE_NAME = "Bitmap Invert"
    ICON = "◈"
    CATEGORY = NodeCategories.BITMAP_PROCESSING
    RETURN_TYPES = (BitMapImage.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImage.TYPE_NAME, {})
            }
        }

    def result(self, BITMAP: BitMapImage):
        return (BITMAP.invert(),)


class DPaint_LogicalOR:
    """OR bitmap combine operation."""
    NODE_NAME = "Bitmap OR"
    ICON = "∨"
    CATEGORY = NodeCategories.BITMAP_COMBINERS
    RETURN_TYPES = (BitMapImage.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImage.TYPE_NAME, {}),
                "BITMAP2": (BitMapImage.TYPE_NAME, {})
            }
        }

    def result(self, BITMAP: BitMapImage, BITMAP2: BitMapImage):
        return (BITMAP.logical_or(BITMAP2),)


class DPaint_LogicalAND:
    """AND bitmap combine operation."""
    NODE_NAME = "Bitmap AND"
    ICON = "∧"
    CATEGORY = NodeCategories.BITMAP_COMBINERS
    RETURN_TYPES = (BitMapImage.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImage.TYPE_NAME, {}),
                "BITMAP2": (BitMapImage.TYPE_NAME, {})
            }
        }

    def result(self, BITMAP: BitMapImage, BITMAP2: BitMapImage):
        return (BITMAP.logical_and(BITMAP2),)


class DPaint_LogicalXOR:
    """Exclusive OR bitmap combine operation."""
    NODE_NAME = "Bitmap XOR"
    ICON = "⊻"
    CATEGORY = NodeCategories.BITMAP_COMBINERS
    RETURN_TYPES = (BitMapImage.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImage.TYPE_NAME, {}),
                "BITMAP2": (BitMapImage.TYPE_NAME, {})
            }
        }

    def result(self, BITMAP: BitMapImage, BITMAP2: BitMapImage):
        return (BITMAP.logical_xor(BITMAP2),)


class DPaint_BitmapResize:
    """Resize/scale of bitmap."""
    NODE_NAME = "Bitmap Resize"
    ICON = "🔎"
    CATEGORY = NodeCategories.BITMAP_PROCESSING
    RETURN_TYPES = (BitMapImage.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImage.TYPE_NAME, {}),
            },
            "optional": {
                "width_multiplier": ("FLOAT", {"min": 0.05, "max": 1.0, "step": 0.025}),
                "width_pixels": ("INT", {"min": BitMapImage.MIN_SIZE_PIXELS}),
                "height_multiplier": ("FLOAT", {"min": 0.05, "max": 1.0, "step": 0.025}),
                "height_pixels": ("INT", {"min": BitMapImage.MIN_SIZE_PIXELS}),
            }
        }

    def result(self, BITMAP: BitMapImage, **kwargs):
        bm = BITMAP
        current_width = bm.width
        current_height = bm.height
        new_width = max(1, kwargs.get("width_pixels", int(round(kwargs.get("width_multiplier", 1.0) * current_width))))
        new_height = max(1,
                         kwargs.get("height_pixels", int(round(kwargs.get("height_multiplier", 1.0) * current_height))))
        if current_width != new_width or current_height != new_height:
            return (bm.resize_to(max(BitMapImage.MIN_SIZE_PIXELS, new_width), max(BitMapImage.MIN_SIZE_PIXELS, new_height)),)
        else:
            return (bm,)


class DPaint_BitmapCropCenter:
    """Crops the center of a bitmap image."""
    NODE_NAME = "Bitmap Crop Center"
    ICON = "🔎"
    CATEGORY = NodeCategories.BITMAP_PROCESSING
    RETURN_TYPES = (BitMapImage.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImage.TYPE_NAME, {}),
                "width_multiplier": ("FLOAT", {"min": 0.0, "max": 1.0, "step": 0.025, "default": 0}),
                "width_pixels": ("INT", {"min": 0, "default": 0}),
                "height_multiplier": ("FLOAT", {"min": 0.0, "max": 1.0, "step": 0.025, "default": 0}),
                "height_pixels": ("INT", {"min": 0, "default": 0}),
            }
        }

    def result(self, BITMAP: BitMapImage, width_multiplier, width_pixels, height_multiplier, height_pixels):
        bm = BITMAP
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
            return (bm.crop(x, y, max(BitMapImage.MIN_SIZE_PIXELS,new_width), max(BitMapImage.MIN_SIZE_PIXELS,new_height)),)
        else:
            return (bm,)


class DPaint_BitmapExpandCanvas:
    """Expends the canvas of a bitmap image by adding a border."""
    NODE_NAME = "Bitmap Expand Canvas"
    ICON = "🔎"
    CATEGORY = NodeCategories.BITMAP_PROCESSING
    RETURN_TYPES = (BitMapImage.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImage.TYPE_NAME, {}),
                "color": (["black", "white"],),
                "border_pixels": ("INT", {"min": 0, "default": 16}),
            }
        }

    def result(self, BITMAP: BitMapImage, color, border_pixels):
        bm = BITMAP
        new_width = bm.width + 2 * border_pixels
        new_height = bm.height + 2 * border_pixels

        c = (0,)
        if color == "white":
            c = (1,)
        if border_pixels == 0:
            return (bm,)

        new_bm = BitMapImage.new_of_size(new_width, new_height, c)
        return (new_bm.paste(bm, border_pixels, border_pixels),)


class DPaint_BitmapRotate:
    """Rotates a bitmap image."""
    NODE_NAME = "Bitmap Rotate"
    ICON = "🔎"
    CATEGORY = NodeCategories.BITMAP_PROCESSING
    RETURN_TYPES = (BitMapImage.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImage.TYPE_NAME, {}),
                "degrees": ("FLOAT", {"min": -360, "max": 360, "step": 5, "default": 45}),
                "center_x": ("INT", {"min": 1, "default": 256}),
                "center_y": ("INT", {"min": 1, "default": 256}),
                "expand": ("BOOLEAN",),
                "fill_color": (["black", "white"],),
            }
        }

    def result(self, BITMAP: BitMapImage, degrees, center_x, center_y, fill_color, expand):
        bm = BITMAP
        if fill_color == "black":
            fill_color = 0
        else:
            fill_color = 1
        return (bm.rotate(center_x, center_y, degrees, expand, fill_color),)

class DPaint_BitmapEdge:
    """Basic edge detection for bitmap images."""
    NODE_NAME = "Bitmap Edge Detect"
    ICON = "🔎"
    CATEGORY = NodeCategories.BITMAP_PROCESSING
    RETURN_TYPES = (BitMapImage.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "BITMAP": (BitMapImage.TYPE_NAME, {}),
            }
        }

    def result(self, BITMAP: BitMapImage):
        return (BITMAP.edge_detect(),)