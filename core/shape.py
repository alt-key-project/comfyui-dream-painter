from typing import List

from typing_extensions import Self

from .vector import Vector2d
from .bitcanvas import BitCanvas

class ShapeContent:
    TYPE_POLYGON = "POLYGON"
    TYPE_LINE = "LINE"

    def __init__(self, vectors: List[Vector2d], tp: str):
        self._vectors = vectors
        self._tp = tp

    def copy(self) -> Self:
        return ShapeContent(self._vectors, self._tp)

    def draw_normal(self, bitcanvas: BitCanvas, fill: bool = True, line_width: float = 1):
        bitcanvas.set_color(BitCanvas.COLOR_WHITE)
        bitcanvas.set_fill(fill)
        if self._tp == ShapeContent.TYPE_LINE:
            a = bitcanvas.multiply_vector_with_dimensions(self._vectors[0])
            b = bitcanvas.multiply_vector_with_dimensions(self._vectors[1])
            bitcanvas.line((a.as_tuple(), b.as_tuple()), width=line_width)
        elif self._tp == ShapeContent.TYPE_POLYGON:
            r = list()
            for v in self._vectors:
                r.append(bitcanvas.multiply_vector_with_dimensions(v).as_tuple())
            if fill:
                bitcanvas.polygon(r)
            else:
                for i in range(len(r)):
                    a = r[i]
                    b = r[(i+1)%len(r)]
                    bitcanvas.line(a[0],a[1],b[0],b[1], line_width)
        bitcanvas.set_color(BitCanvas.COLOR_WHITE)

    def draw_xor(self, bitcanvas: BitCanvas, fill: bool = True, line_width: float = 1):
        cp = bitcanvas.clear_copy()
        self.draw_normal(cp, fill, line_width)
        bitcanvas.combine_xor(cp)

    def apply_vector_op(self, op):
        l = list(map(op, self._vectors))
        self._vectors = l

    def scale(self, factor: float):
        self.apply_vector_op(lambda v: v.multiply(factor))

    def translate(self, x, y):
        self.apply_vector_op(lambda v: Vector2d(v.x + x, v.y + y))

    def rotate(self, center: Vector2d, degrees: float):
        def _r(v : Vector2d):
            a = v.sub(center)
            return center.add(a.rotate(degrees))
        self.apply_vector_op(_r)


class Shape:
    TYPE_NAME = "SHAPE"

    def __init__(self, content: List[ShapeContent|Self]):
        self._content = list(content)

    def copy(self) -> Self:
        l = list()
        for c in self._content:
            l.append(c.copy())
        return Shape(l)

    def apply_vector_op(self,f):
        for c in self._content:
            c.apply_vector_op(f)

    def scale(self, factor):
        for c in self._content:
            c.scale(factor)

    def translate(self, x, y):
        for c in self._content:
            c.translate(x,y)

    def rotate(self, center: Vector2d, degrees: float):
        for c in self._content:
            c.rotate(center, degrees)

    def draw_xor(self, bitcanvas: BitCanvas, fill: bool = True, line_width: float = 1):
        return self.draw(bitcanvas, True, fill, line_width)

    def draw_normal(self, bitcanvas: BitCanvas, fill: bool = True, line_width: float = 1):
        return self.draw(bitcanvas, False, fill, line_width)

    def draw(self, bitcanvas: BitCanvas, draw_xor: bool = False, draw_fill: bool = True, line_width: int|float = 1):
        for c in self._content:
            if draw_xor:
                c.draw_xor(bitcanvas, draw_fill, line_width)
            else:
                c.draw_normal(bitcanvas, draw_fill, line_width)