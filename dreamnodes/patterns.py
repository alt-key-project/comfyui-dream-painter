
from ..conf import NodeCategories
from ..core import BitMapImageList, BitCanvas, Vector2d
import math

WHITE = "#ffffff"
BLACK = "#000000"

class DPaint_NPolygon:
    NODE_NAME = "Generate Stripes"
    ICON = "▧"
    CATEGORY = NodeCategories.BITMAP_GENERATE
    RETURN_TYPES = (BitMapImageList.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bitmap_width": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "bitmap_height": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "stripe_width": ("INT", {"min": 2, "max": 10000, "default": 32}),
                "rotation_degrees": ("FLOAT",{"min": -360, "max":360.0, "default": 0})
            }
        }

    def result(self, edges, bitmap_width, bitmap_height, stripe_width, rotation_degrees):
        canvas = BitCanvas(bitmap_width, bitmap_height)
        stripe_length = math.sqrt(bitmap_width*bitmap_width + bitmap_height*bitmap_height)

        stripe_vector = Vector2d(0,1).rotate(rotation_degrees)
        num_stripes =round(0.5 * stripe_length / stripe_width)
        

        degrees_per_edge = 360.0 / edges
        start_point = Vector2d(center_x, center_y - shape_size * 0.5)
        center_point = Vector2d(center_x, center_y)
        v = start_point.sub(center_point)
        points = [center_point.add(v.rotate(rotation_degrees)).as_tuple()]
        for i in range(edges-1):
            new_point = center_point.add(v.rotate(rotation_degrees+(i+1)*degrees_per_edge))
            points.append(new_point.as_tuple())
        canvas.polygon(points)
        return (BitMapImageList([canvas.bitmap()]),)

class DPaint_NPolygon:
    NODE_NAME = "Generate N-Polygon"
    ICON = "◄"
    CATEGORY = NodeCategories.BITMAP_GENERATE
    RETURN_TYPES = (BitMapImageList.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "edges": ("INT", {"min": 3, "max": 24, "default": 3}),
                "bitmap_width": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "bitmap_height": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "shape_size": ("INT", {"min": 1, "max": 10000, "default": 400}),
                "center_x": ("INT", {"min": 1, "max": 10000, "default": 256}),
                "center_y": ("INT", {"min": 1, "max": 10000, "default": 256}),
                "rotation_degrees": ("FLOAT",{"min": -360, "max":360.0, "default": 0})
            }
        }

    def result(self, edges, bitmap_width, bitmap_height, shape_size, center_x, center_y, rotation_degrees):
        canvas = BitCanvas(bitmap_width, bitmap_height)
        degrees_per_edge = 360.0 / edges
        start_point = Vector2d(center_x, center_y - shape_size * 0.5)
        center_point = Vector2d(center_x, center_y)
        v = start_point.sub(center_point)
        points = [center_point.add(v.rotate(rotation_degrees)).as_tuple()]
        for i in range(edges-1):
            new_point = center_point.add(v.rotate(rotation_degrees+(i+1)*degrees_per_edge))
            points.append(new_point.as_tuple())
        canvas.polygon(points)
        return (BitMapImageList([canvas.bitmap()]),)

class DPaint_Rectangle:
    NODE_NAME = "Generate Rectangle"
    ICON = "▅"
    CATEGORY = NodeCategories.BITMAP_GENERATE
    RETURN_TYPES = (BitMapImageList.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bitmap_width": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "bitmap_height": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "shape_width": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "shape_height": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "center_x": ("INT", {"min": 1, "max": 10000, "default": 256}),
                "center_y": ("INT", {"min": 1, "max": 10000, "default": 256}),
            }
        }

    def result(self, bitmap_width, bitmap_height, shape_width, shape_height, center_x, center_y):
        canvas = BitCanvas(bitmap_width, bitmap_height)
        canvas.rectangle((center_x - shape_width/2, center_y - shape_height/2),
                         (center_x + shape_width/2, center_y + shape_height/2))
        return (BitMapImageList([canvas.bitmap()]),)

class DPaint_Ellipse:
    NODE_NAME = "Generate Ellipse"
    ICON = "◯"
    CATEGORY = NodeCategories.BITMAP_GENERATE
    RETURN_TYPES = (BitMapImageList.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "bitmap_width": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "bitmap_height": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "shape_width": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "shape_height": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "center_x": ("INT", {"min": 1, "max": 10000, "default": 256}),
                "center_y": ("INT", {"min": 1, "max": 10000, "default": 256}),
            }
        }

    def result(self, bitmap_width, bitmap_height, shape_width, shape_height, center_x, center_y):
        canvas = BitCanvas(bitmap_width, bitmap_height)
        canvas.ellipse((center_x - shape_width/2, center_y - shape_height/2),
                         (center_x + shape_width/2, center_y + shape_height/2))
        return (BitMapImageList([canvas.bitmap()]),)


class DPaint_RectangularBullseye:
    NODE_NAME = "Generate Rectangular Bullseye"
    ICON = "⧈"
    CATEGORY = NodeCategories.BITMAP_GENERATE
    RETURN_TYPES = (BitMapImageList.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "height": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "line_width_x": ("INT", {"min": 1, "max": 10000, "default": 32}),
                "line_width_y": ("INT", {"min": 1, "max": 10000, "default": 32}),
                "center_x": ("INT", {"min": 1, "max": 10000, "default": 256}),
                "center_y": ("INT", {"min": 1, "max": 10000, "default": 256}),
            }
        }

    def result(self, width, height, line_width_x, line_width_y, center_x, center_y):
        dist_x = max(abs(width-center_x), abs(center_x))
        dist_y = max(abs(height-center_y), abs(center_y))
        num_circles = 1 + max(int(round(dist_x / line_width_x)),int(round(dist_y / line_width_y)))
        canvas = BitCanvas(width, height)
        for i in range(num_circles):
            radius_x = round(line_width_x * (num_circles-i))
            radius_y = round(line_width_y * (num_circles-i))
            canvas.rectangle((center_x - radius_x, center_y - radius_y),
                             (center_x + radius_x, center_y + radius_y))
            canvas.flip_draw_color()
        return (BitMapImageList([canvas.bitmap()]),)

class DPaint_Bullseye:
    NODE_NAME = "Generate Bullseye"
    ICON = "🞋"
    CATEGORY = NodeCategories.BITMAP_GENERATE
    RETURN_TYPES = (BitMapImageList.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "height": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "line_width_x": ("INT", {"min": 1, "max": 10000, "default": 32}),
                "line_width_y": ("INT", {"min": 1, "max": 10000, "default": 32}),
                "center_x": ("INT", {"min": 1, "max": 10000, "default": 256}),
                "center_y": ("INT", {"min": 1, "max": 10000, "default": 256}),
            }
        }

    def result(self, width, height, line_width_x, line_width_y, center_x, center_y):
        dist_x = max(abs(width-center_x), abs(center_x))
        dist_y = max(abs(height-center_y), abs(center_y))
        num_circles = 1 + max(int(round(dist_x / line_width_x)),int(round(dist_y / line_width_y)))
        canvas = BitCanvas(width, height)
        for i in range(num_circles):
            radius_x = round(line_width_x * (num_circles-i))
            radius_y = round(line_width_y * (num_circles-i))
            canvas.flip_draw_color()
            canvas.ellipse((center_x - radius_x, center_y - radius_y),
                           (center_x + radius_x, center_y + radius_y))
        return (BitMapImageList([canvas.bitmap()]),)


class DPaint_CheckerBoard:
    NODE_NAME = "Generate Checkerboard"
    ICON = "🙾"
    CATEGORY = NodeCategories.BITMAP_GENERATE
    RETURN_TYPES = (BitMapImageList.TYPE_NAME,)
    RETURN_NAMES = ("BITMAP",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "height": ("INT", {"min": 1, "max": 10000, "default": 512}),
                "columns": ("INT", {"min": 1, "max": 100, "default": 8}),
                "rows": ("INT", {"min": 1, "max": 100, "default": 4}),
            }
        }

    def result(self, width, height, columns, rows):
        canvas = BitCanvas(width, height)
        step_x = width / float(columns)
        step_y = height / float(rows)
        for r in range(rows):
            for c in range(columns):
                x = round(c * step_x)
                y = round(r * step_y)
                if (r + c) % 2 == 0:
                    canvas.rectangle((x, y), (x + step_x, y + step_y))
        return (BitMapImageList([canvas.bitmap()]),)
