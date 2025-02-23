import math

from ..core import Vector2d
from ..conf import NodeCategories
from ..core import Shape, ShapeContent


class DPaint_NPolygon:
    """Generates a rounded polygon with N edges."""
    NODE_NAME = "Shape of N-Polygon"
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
                "center_x": ("FLOAT", {"default": 0.5, "step": 0.01}),
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
            v = Vector2d(x, y)
            vectors.append(c.add(v))
        return (Shape([ShapeContent(vectors, ShapeContent.TYPE_POLYGON)]),)


class DPaint_Rectangle:
    """Generates a rectangle shape."""
    NODE_NAME = "Shape of Rectangle"
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
                "center_x": ("FLOAT", {"default": 0.5, "step": 0.01}),
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
    """Generates a star shape."""
    NODE_NAME = "Shape of Star"
    ICON = "☆"
    CATEGORY = NodeCategories.SHAPE
    RETURN_TYPES = (Shape.TYPE_NAME,)
    RETURN_NAMES = ("SHAPE",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "size": ("INT", {"default": 5, "min": 3, "max": 100}),
                "outer_diameter": ("FLOAT", {"default": 0.75, "step": 0.01, "min": 0.01}),
                "inner_diameter": ("FLOAT", {"default": 0.35, "step": 0.01, "min": 0.01}),
                "center_x": ("FLOAT", {"default": 0.5, "step": 0.01}),
                "center_y": ("FLOAT", {"default": 0.5, "step": 0.01}),
            }
        }

    def result(self, size, outer_diameter, inner_diameter, center_x, center_y):
        vectors = list()
        c = Vector2d(center_x, center_y)
        step = 360.0 / (size * 2)
        vi = Vector2d(0, inner_diameter * 0.5)
        vo = Vector2d(0, outer_diameter * 0.5)
        for i in range(size + size):
            if i % 2 == 0:
                vectors.append(c.add(vi.rotate(step * i)))
            else:
                vectors.append(c.add(vo.rotate(step * i)))
        return (Shape([ShapeContent(vectors, ShapeContent.TYPE_POLYGON)]),)


class DPaint_ShapeGrid:
    """Creates a grid with scaled copies of the provided input shape."""
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
                "columns": ("INT", {"default": 10, "min": 1, "max": 256}),
                "rows": ("INT", {"default": 10, "min": 1, "max": 256}),
                "inbetween_skip": ("INT", {"default": 0, "min": 0, "max": 256}),
                "row_skip_offset": ("INT", {"default": 0, "min": 0, "max": 256}),
            }
        }

    def result(self, SHAPE, width, height, columns, rows, row_skip_offset, inbetween_skip):
        scale_x = width / columns
        scale_y = height / rows
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
                counter += 1
                if (counter + (row_skip_offset * row)) % (inbetween_skip + 1) == 0:
                    c = scaled_grid_shape.copy()
                    pos = Vector2d(start_x + column * step_x, start_y + row * step_y)
                    translation = pos.sub(center)
                    c.translate(translation.x, translation.y)
                    sub_shapes.append(c)

        s = Shape(sub_shapes)
        s.normalize()
        s.scale(width, height)
        s.translate((1 - width) * 0.5, (1 - height) * 0.5)
        return (s,)


class DPaint_ShapeCombiner:
    """Combines multiple shapes into a single shape."""
    NODE_NAME = "Shape Combiner"
    ICON = "⟏"
    CATEGORY = NodeCategories.SHAPE
    RETURN_TYPES = (Shape.TYPE_NAME,)
    RETURN_NAMES = ("SHAPE",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "SHAPE": (Shape.TYPE_NAME,),
                "SHAPE2": (Shape.TYPE_NAME,),
                "SHAPE3": (Shape.TYPE_NAME,),
                "SHAPE4": (Shape.TYPE_NAME,),
            }
        }

    def result(self, *args, **kwargs):
        shapes = [kwargs.get("SHAPE", None),
                  kwargs.get("SHAPE2", None),
                  kwargs.get("SHAPE3", None),
                  kwargs.get("SHAPE4", None)]
        actual_shapes = list(filter(lambda s: s is not None, shapes))
        return (Shape(actual_shapes),)


class DPaint_ShapeRotate:
    """Rotates a shape around its own center."""
    NODE_NAME = "Shape Rotate"
    ICON = "⭮"
    CATEGORY = NodeCategories.SHAPE
    RETURN_TYPES = (Shape.TYPE_NAME,)
    RETURN_NAMES = ("SHAPE",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "SHAPE": (Shape.TYPE_NAME,),
                "degrees": ("FLOAT", {"min": -360, "max": 360, "step": 1}),
            }
        }

    def result(self, SHAPE, degrees):
        s = SHAPE.copy()
        center = s.center()
        s.rotate(center, degrees)
        return (s,)


class DPaint_ShapeResize:
    """Resizes/scales a shape. Scaling is either in global coordinates or shape coordinates."""
    NODE_NAME = "Shape Resize"
    ICON = "⮔"
    CATEGORY = NodeCategories.SHAPE
    RETURN_TYPES = (Shape.TYPE_NAME,)
    RETURN_NAMES = ("SHAPE",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "SHAPE": (Shape.TYPE_NAME,),
                "shape_centered": (["yes", "no"],),
                "factor_x": ("FLOAT", {"min": 0.01, "max": 100.0, "default": 1}),
                "factor_y": ("FLOAT", {"min": 0.01, "max": 100.0, "default": 1}),
            }
        }

    def result(self, SHAPE, shape_centered, factor_x, factor_y):
        s = SHAPE.copy()
        if shape_centered == "yes":
            center = s.center()
            s.recenter()
            s.scale(factor_x, factor_y)
            s.translate(center.x, center.y)
        else:
            s.scale(factor_x, factor_y)
        return (s,)


class DPaint_ShapeCenterAndFit:
    """Centers a shape and fits it within [0,0]-[1,1]."""
    NODE_NAME = "Shape Center & Fit"
    ICON = "⌧"
    CATEGORY = NodeCategories.SHAPE
    RETURN_TYPES = (Shape.TYPE_NAME,)
    RETURN_NAMES = ("SHAPE",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "SHAPE": (Shape.TYPE_NAME,),
                "proportional": (["yes", "no"],),
                "border": ("FLOAT", {"min": 0.00, "max": .49, "default": 0.0, "step": 0.01}),
            }
        }

    def result(self, SHAPE, proportional, border):
        s = SHAPE.copy()
        proportional = proportional == "yes"
        new_size = 1.0 - 2 * border
        dim_x, dim_y = s.dimensions()

        x_factor = new_size / dim_x
        y_factor = new_size / dim_y

        if proportional:
            s.scale(min(x_factor, y_factor))
        else:
            s.scale(x_factor, y_factor)
        s.recenter()
        return (s,)


class DPaint_Rays:
    """Circular rays shape"""
    NODE_NAME = "Shape of Circular Rays"
    ICON = "☀"
    CATEGORY = NodeCategories.SHAPE
    RETURN_TYPES = (Shape.TYPE_NAME,)
    RETURN_NAMES = ("SHAPE",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "ray_origin_x": ("FLOAT", {"default": 0.5, "step": 0.01, "min": -3, "max": 3}),
                "ray_origin_y": ("FLOAT", {"default": 0.5, "step": 0.01, "min": -3, "max": 3}),
                "center_x": ("FLOAT", {"default": 0.5, "step": 0.01, "min": -3, "max": 3}),
                "center_y": ("FLOAT", {"default": 0.5, "step": 0.01, "min": -3, "max": 3}),
                "diameter": ("FLOAT", {"default": 2.0, "step": 0.01}),
                "rays": ("INT", {"min": 2, "max": 1000, "default": 12}),
            }
        }

    def result(self, ray_origin_x, ray_origin_y, center_x, center_y, rays, diameter):
        c = Vector2d(center_x, center_y)
        o = Vector2d(ray_origin_x, ray_origin_y)
        step = 360.0 / rays
        v = Vector2d(0, diameter * 0.5)
        vectors = list()
        for i in range(rays):
            v_rotated = v.rotate(step * i)
            vectors.append(o)
            vectors.append(c.add(v_rotated))
            v_rotated = v.rotate(step * i + step * 0.5)
            vectors.append(c.add(v_rotated))

        return (Shape([ShapeContent(vectors, ShapeContent.TYPE_POLYGON)]),)


class DPaint_CopyCat:
    """Creates copies of shapes with translation, rotation and scale adjustments."""
    NODE_NAME = "Shape Copycat Tool"
    ICON = "🞖"
    CATEGORY = NodeCategories.SHAPE
    RETURN_TYPES = (Shape.TYPE_NAME,)
    RETURN_NAMES = ("SHAPE",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "SHAPE": (Shape.TYPE_NAME,),
                "copies": ("INT", {"min": 0, "max": 1000, "default": 2}),
                "copy_translation_x": ("FLOAT", {"default": 0, "step": 0.01, "min": -3, "max": 3}),
                "copy_translation_y": ("FLOAT", {"default": 0, "step": 0.01, "min": -3, "max": 3}),
                "copy_rotation_degrees": ("FLOAT", {"default": 0, "step": 1, "min": -360, "max": 360}),
                "copy_scale_factor": ("FLOAT", {"default": 1, "step": 0.001, "min": 0.25, "max": 4}),
                "apply_scale_to_translation": (["yes", "no"],),
                "apply_rotation_to_translation": (["yes", "no"],),
            }
        }

    def result(self, SHAPE, copies, copy_translation_x, copy_translation_y, copy_rotation_degrees, copy_scale_factor,
               apply_scale_to_translation, apply_rotation_to_translation):
        shapes = list()
        shapes.append(SHAPE)
        previous = SHAPE
        for i in range(1, copies + 1):
            s = previous.copy()
            t = Vector2d(copy_translation_x, copy_translation_y)
            if apply_scale_to_translation == "yes":
                t = t.multiply(copy_scale_factor * i)
            if apply_rotation_to_translation == "yes":
                t.rotate(copy_rotation_degrees * i)
            new_position = s.center().add(t)
            s.translate(t.x, t.y)
            c = s.center()
            s.rotate(c, copy_rotation_degrees)
            s.scale(copy_scale_factor)
            s.move_to(new_position.x, new_position.y)
            shapes.append(s)
            previous = s

        return (Shape(shapes),)


class DPaint_ShapeBounds:
    """Calculates the bounds and center of a shape."""
    NODE_NAME = "Shape Find Bounds"
    ICON = "⬚"
    CATEGORY = NodeCategories.SHAPE
    RETURN_TYPES = ("FLOAT", "FLOAT", "FLOAT", "FLOAT", "FLOAT", "FLOAT")
    RETURN_NAMES = ("min_x", "max_x", "min_y", "max_y", "center_x", "center_y")
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "SHAPE": (Shape.TYPE_NAME,),
            }
        }

    def result(self, SHAPE):
        v1, v2 = SHAPE.get_bounds()
        return (v1.x, v2.x, v1.y, v2.y, (v1.x + v2.x) * 0.5, (v1.y + v2.y) * 0.5)

class DPaint_ShapeFlip:
    """Flips a shape horizontally or vertically."""
    NODE_NAME = "Shape Flip"
    ICON = "🔃"
    CATEGORY = NodeCategories.SHAPE
    RETURN_TYPES = (Shape.TYPE_NAME,)
    RETURN_NAMES = ("SHAPE",)
    FUNCTION = "result"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "SHAPE": (Shape.TYPE_NAME,),
                "direction": (["vertical", "horizontal"],),
            }
        }

    def result(self, SHAPE, direction: str):
        s = SHAPE.copy()
        s.flip(direction == "horizontal", direction == "vertical", s.center())
        return (s,)
