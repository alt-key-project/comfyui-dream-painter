import math

from ..core import Vector2d
from ..conf import NodeCategories
from ..core import Shape, ShapeContent




class DPaint_NPolygon:
    NODE_NAME = "N-Polygon Shape"
    ICON = "◯"
    CATEGORY = NodeCategories.SHAPE
    RETURN_TYPES = (Shape.TYPE_NAME,)
    RETURN_NAMES = ("SHAPE",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "shape_width": ("FLOAT", {"default": 0.75, "step": 0.01}),
                "shape_height": ("FLOAT", {"default": 0.75, "step": 0.01}),
                "center_x": ("FLOAT", { "default": 0.5, "step": 0.01}),
                "center_y": ("FLOAT", {"default": 0.5, "step": 0.01}),
                "edges": ("INT", {"min": 3, "max": 1000, "default": 12}),
            }
        }

    def result(self, shape_width, shape_height, center_x, center_y, edges):
        c = Vector2d(center_x, center_y)
        vectors = list()
        for i in range(edges):
            r = i / edges
            x = shape_width * 0.5 * math.sin(r * 2 * math.pi)
            y = shape_height * 0.5 * math.cos(r * 2 * math.pi)
            v = Vector2d(x,y)
            vectors.append(c.add(v))
        return (Shape([ShapeContent(vectors, ShapeContent.TYPE_POLYGON)]),)


class DPaint_Rectangle:
    NODE_NAME = "Rectangle Shape"
    ICON = "▅"
    CATEGORY = NodeCategories.SHAPE
    RETURN_TYPES = (Shape.TYPE_NAME,)
    RETURN_NAMES = ("SHAPE",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "shape_width": ("FLOAT", {"default": 0.75, "step": 0.01}),
                "shape_height": ("FLOAT", {"default": 0.75, "step": 0.01}),
                "center_x": ("FLOAT", { "default": 0.5, "step": 0.01}),
                "center_y": ("FLOAT", {"default": 0.5, "step": 0.01}),
            }
        }

    def result(self, shape_width, shape_height, center_x, center_y):
        vectors = [
            Vector2d(center_x + shape_width * 0.5, center_y + shape_height * 0.5),
            Vector2d(center_x + shape_width * 0.5, center_y - shape_height * 0.5),
            Vector2d(center_x - shape_width * 0.5, center_y - shape_height * 0.5),
            Vector2d(center_x - shape_width * 0.5, center_y + shape_height * 0.5),
        ]
        return (Shape([ShapeContent(vectors, ShapeContent.TYPE_POLYGON)]),)

class DPaint_Star:
    NODE_NAME = "Star Shape"
    ICON = "☆"
    CATEGORY = NodeCategories.SHAPE
    RETURN_TYPES = (Shape.TYPE_NAME,)
    RETURN_NAMES = ("SHAPE",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "size": ("INT", { "default": 5, "min": 3, "max": 100}),
                "outer_diameter": ("FLOAT", {"default": 0.75, "step": 0.01, "min": 0.01}),
                "inner_diameter": ("FLOAT", {"default": 0.35, "step": 0.01, "min": 0.01}),
                "center_x": ("FLOAT", { "default": 0.5, "step": 0.01}),
                "center_y": ("FLOAT", {"default": 0.5, "step": 0.01}),
            }
        }

    def result(self, size, outer_diameter, inner_diameter, center_x, center_y):
        vectors = list()
        c=Vector2d(center_x, center_y)
        step = 360.0 / (size * 2)
        vi = Vector2d(0, inner_diameter * 0.5)
        vo = Vector2d(0, outer_diameter * 0.5)
        for i in range(size+size):
            if i%2==0:
                vectors.append(c.add(vi.rotate(step * i)))
            else:
                vectors.append(c.add(vo.rotate(step * i)))
        return (Shape([ShapeContent(vectors, ShapeContent.TYPE_POLYGON)]),)

class DPaint_ShapeGrid:
    NODE_NAME = "Shape Grid"
    ICON = "⩩"
    CATEGORY = NodeCategories.SHAPE
    RETURN_TYPES = (Shape.TYPE_NAME,)
    RETURN_NAMES = ("SHAPE",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "SHAPE": (Shape.TYPE_NAME,),
                "width": ("FLOAT", {"default": 0.75, "step": 0.01}),
                "height": ("FLOAT", {"default": 0.75, "step": 0.01}),
                "columns": ("INT", { "default": 10, "min": 1, "max": 256}),
                "rows": ("INT", { "default": 10, "min": 1, "max": 256}),
                "inbetween_skip": ("INT", { "default": 0, "min": 0, "max": 256}),
                "row_skip_offset": ("INT", { "default": 0, "min": 0, "max": 256}),
            }
        }

    def result(self, SHAPE, width, height, columns, rows, row_skip_offset, inbetween_skip):
        scale_x = width/columns
        scale_y = height/rows
        scaled_grid_shape = SHAPE.copy()
        scaled_grid_shape.scale(min(scale_x, scale_y))

        start_x = 0.5 - width * 0.5
        start_y = 0.5 - width * 0.5
        step_x = width / columns
        step_y = height / rows
        center = Vector2d(0.5, 0.5)

        sub_shapes = list()
        counter = 0
        for row in range(rows):
            for column in range(columns):
                counter+=1
                if (counter + (row_skip_offset * row)) % (inbetween_skip + 1) == 0:
                    c=scaled_grid_shape.copy()
                    pos = Vector2d(start_x+column*step_x, start_y+row*step_y)
                    translation = pos.sub(center)
                    c.translate(translation.x, translation.y)
                    sub_shapes.append(c)

        s = Shape(sub_shapes)
        s.normalize()
        s.scale(width, height)
        s.translate((1-width)*0.5, (1-height)*0.5)
        return (s,)


class DPaint_ShapeCombiner:
    NODE_NAME = "Combine Shapes"
    ICON = "⟏"
    CATEGORY = NodeCategories.SHAPE
    RETURN_TYPES = (Shape.TYPE_NAME,)
    RETURN_NAMES = ("SHAPE",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "SHAPE": (Shape.TYPE_NAME, ),
                "SHAPE2": (Shape.TYPE_NAME, ),
                "SHAPE3": (Shape.TYPE_NAME, ),
                "SHAPE4": (Shape.TYPE_NAME, ),
            }
        }

    def result(self, *args, **kwargs):
        shapes = [kwargs.get("SHAPE", None),
                kwargs.get("SHAPE2", None),
            kwargs.get("SHAPE3", None),
            kwargs.get("SHAPE4", None)]
        actual_shapes = list(filter(lambda s: s is not None,  shapes))
        return (Shape(actual_shapes),)