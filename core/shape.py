from typing import List, Tuple

from typing_extensions import Self

from .vector import Vector2d
from .bitcanvas import BitCanvas


class ShapeContent:
    TYPE_POLYGON = "POLYGON"
    TYPE_LINE = "LINE"

    def __init__(self, vectors: List[Vector2d], tp: str):
        self._vectors = vectors
        self._tp = tp

    def dimensions(self) -> Tuple[float, float]:
        a, b = self.get_bounds()
        return (b.x - a.x, b.y - a.y)

    def get_bounds(self) -> Tuple[Vector2d, Vector2d]:
        if self._vectors:
            min_x = min(map(lambda v: v.x, self._vectors))
            max_x = max(map(lambda v: v.x, self._vectors))
            min_y = min(map(lambda v: v.y, self._vectors))
            max_y = max(map(lambda v: v.y, self._vectors))
            return (Vector2d(min_x, min_y), Vector2d(max_x, max_y))
        else:
            return (Vector2d(0, 0), Vector2d(1, 1))

    def copy(self) -> Self:
        return ShapeContent(self._vectors, self._tp)

    def _check_viewport(self, viewport: Tuple[Vector2d, Vector2d]):
        if (viewport[1].x <= viewport[0].x or viewport[1].y <= viewport[0].y):
            raise Exception("Bad viewport! " + str(viewport))
        else:
            print("Drawing in viewport: "+str(viewport))

    def draw_normal(self, bitcanvas: BitCanvas, fill: bool = True, line_width: float = 1,
                    viewport: Tuple[Vector2d, Vector2d] = (Vector2d(0, 0), Vector2d(1, 1))):
        bitcanvas.set_color(BitCanvas.COLOR_WHITE)
        bitcanvas.set_fill(fill)
        self._check_viewport(viewport)
        if self._tp == ShapeContent.TYPE_LINE:
            a = bitcanvas.multiply_vector_with_dimensions(self._vectors[0], viewport)
            b = bitcanvas.multiply_vector_with_dimensions(self._vectors[1], viewport)
            bitcanvas.line((a.as_tuple(), b.as_tuple()), width=line_width)
        elif self._tp == ShapeContent.TYPE_POLYGON:
            r = list()
            for v in self._vectors:
                r.append(bitcanvas.multiply_vector_with_dimensions(v, viewport).as_tuple())
            if fill:
                bitcanvas.polygon(r)
            else:
                l = list()
                for i in range(len(r) + 1):
                    l.append(r[(i) % len(r)])
                bitcanvas.polyline(l, line_width)
        bitcanvas.set_color(BitCanvas.COLOR_WHITE)

    def draw_xor(self, bitcanvas: BitCanvas, fill: bool = True, line_width: float = 1,
                 viewport: Tuple[Vector2d, Vector2d] = (Vector2d(0, 0), Vector2d(1, 1))):
        cp = bitcanvas.clear_copy()
        self.draw_normal(cp, fill, line_width, viewport)
        bitcanvas.combine_xor(cp)

    def apply_vector_op(self, op) -> Self:
        l = list(map(op, self._vectors))
        self._vectors = l
        return self

    def scale(self, factor_x, factor_y=None) -> Self:
        if factor_y is None:
            factor_y = factor_x
        return self.apply_vector_op(lambda v: Vector2d(v.x * factor_x, v.y * factor_y))

    def center(self) -> Vector2d:
        bound = self.get_bounds()
        cx = (bound[1].x + bound[0].x) * 0.5
        cy = (bound[1].y + bound[0].y) * 0.5
        return Vector2d(cx, cy)

    def recenter(self):
        c = self.center()
        self.translate(0.5 - c.x, 0.5 - c.y)

    def translate(self, x, y):
        self.apply_vector_op(lambda v: Vector2d(v.x + x, v.y + y))

    def rotate(self, center: Vector2d, degrees: float):
        def _r(v: Vector2d):
            a = v.sub(center)
            return center.add(a.rotate(degrees))

        self.apply_vector_op(_r)

    def flip(self, horizontal: bool, vertical: bool, center: Vector2d):
        def _flip_x(v: Vector2d, cx: float):
            return Vector2d(cx + cx - v.x, v.y)

        def _flip_y(v: Vector2d, cy: float):
            return Vector2d(v.x, cy + cy - v.y)

        if horizontal and vertical:
            return self.apply_vector_op(lambda v: _flip_x(_flip_y(v, center.y), center.x))
        elif horizontal:
            return self.apply_vector_op(lambda v: _flip_x(v, center.x))
        elif vertical:
            return self.apply_vector_op(lambda v: _flip_y(v, center.y))
        else:
            return self

    def __str__(self):
        b = self.get_bounds()
        return f"ShapeContent[{b[0]},{b[1]}]"


class Shape:
    TYPE_NAME = "SHAPE"

    def __init__(self, content: List[ShapeContent | Self]):
        self._content = list(content)

    def copy(self) -> Self:
        l = list()
        for c in self._content:
            l.append(c.copy())
        return Shape(l)

    def dimensions(self) -> Tuple[float, float]:
        a, b = self.get_bounds()
        return (b.x - a.x, b.y - a.y)

    def get_bounds(self) -> Tuple[Vector2d, Vector2d]:
        if not self._content:
            return (Vector2d(0, 0), Vector2d(1, 1))

        min_x = None
        max_x = None
        min_y = None
        max_y = None

        for c in self._content:
            min_v, max_v = c.get_bounds()
            if min_x is None or min_x > min_v.x:
                min_x = min_v.x
            if min_y is None or min_y > min_v.y:
                min_y = min_v.y
            if max_x is None or max_x < max_v.x:
                max_x = max_v.x
            if max_y is None or max_y < max_v.y:
                max_y = max_v.y
        return (Vector2d(min_x, min_y), Vector2d(max_x, max_y))

    def move_to(self, x, y):
        translation = Vector2d(x, y).sub(self.center())
        return self.translate(translation.x, translation.y)

    def recenter(self):
        return self.move_to(0.5, 0.5)

    def center(self) -> Vector2d:
        bound = self.get_bounds()
        cx = (bound[1].x + bound[0].x) * 0.5
        cy = (bound[1].y + bound[0].y) * 0.5
        return Vector2d(cx, cy)

    def normalize(self):
        min_v, max_v = self.get_bounds()
        w = max_v.x - min_v.x
        h = max_v.y - min_v.y
        self.translate(min_v.neg().x, min_v.neg().y)
        self.scale(1.0 / w, 1.0 / h)

    def apply_vector_op(self, f):
        for c in self._content:
            c.apply_vector_op(f)

    def scale(self, factor_x, factor_y=None):
        if factor_y is None:
            factor_y = factor_x
        for c in self._content:
            c.scale(factor_x, factor_y)

    def translate(self, x, y):
        for c in self._content:
            c.translate(x, y)

    def flip(self, horizontal: bool, vertical: bool, center: Vector2d = None):
        if center is None:
            center = self.center()
        for c in self._content:
            c.flip(horizontal, vertical, center)

    def rotate(self, center: Vector2d, degrees: float):
        for c in self._content:
            c.rotate(center, degrees)

    def draw_xor(self, bitcanvas: BitCanvas, fill: bool = True, line_width: float = 1,
                 viewport: Tuple[Vector2d, Vector2d] = (Vector2d(0, 0), Vector2d(1, 1))):
        return self.draw(bitcanvas, True, fill, line_width, viewport)

    def draw_normal(self, bitcanvas: BitCanvas, fill: bool = True, line_width: float = 1,
                    viewport: Tuple[Vector2d, Vector2d] = (Vector2d(0, 0), Vector2d(1, 1))):
        return self.draw(bitcanvas, False, fill, line_width, viewport)

    def draw(self, bitcanvas: BitCanvas, draw_xor: bool = False, draw_fill: bool = True, line_width: int | float = 1,
             viewport: Tuple[Vector2d, Vector2d] = (Vector2d(0, 0), Vector2d(1, 1))):
        for c in self._content:
            if draw_xor:
                c.draw_xor(bitcanvas, draw_fill, line_width, viewport)
            else:
                c.draw_normal(bitcanvas, draw_fill, line_width, viewport)

    def __str__(self):
        b = self.get_bounds()
        return f"Shape[{b[0]},{b[1]}]"
