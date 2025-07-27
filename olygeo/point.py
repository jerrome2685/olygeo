from sympy import Symbol, Expr
import sympy as sp
from .geo import Geo
from .relation import Relation
from typing import Union


class ProPoint:
    _unfixed_counter = 0

    def __init__(self, x: Union[Expr, int], y: Union[Expr, int], z: Union[Expr, int] = 1):
        self.x, self.y, self.z = sp.sympify(x), sp.sympify(y), sp.sympify(z)

    def __repr__(self):
        return f"ProPoint({self.x}:{self.y}:{self.z})"

    def __add__(self, other):
        return ProPoint(
            self.x * other.z + other.x * self.z,
            self.y * other.z + other.y * self.z,
            self.z * other.z
        )

    def __sub__(self, other):
        return ProPoint(
            self.x * other.z - other.x * self.z,
            self.y * other.z - other.y * self.z,
            self.z * other.z
        )

    def __mul__(self, k):
        return ProPoint(self.x * k, self.y * k, self.z)

    __rmul__ = __mul__

    def __truediv__(self, k):
        return ProPoint(self.x / k, self.y / k, self.z)

    def __eq__(self, other):
        return (
                self.x == other.x and
                self.y == other.y and
                self.z == other.z
        )

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    @classmethod
    def unfixed(cls):
        name = f"{cls.__name__}_{cls._unfixed_counter}"
        cls._unfixed_counter += 1
        return cls(Symbol(f"{name}_x"), Symbol(f"{name}_y"))

    def is_eq(self, other, log=False) -> bool:
        return Geo.is_zero((self.x * other.z - other.x * self.z) ** 2 + (self.y * other.z - other.y * self.z) ** 2,
                           log=log)

    def is_ne(self, other, log=False) -> bool:
        return Geo.is_nonzero((self.x * other.z - other.x * self.z) ** 2 +
                              (self.y * other.z - other.y * self.z) ** 2, log=log)


@Geo.is_eq.register
def _(a: ProPoint, b: ProPoint, log=False) -> bool:
    return a.is_eq(b, log)

@Geo.is_ne.register
def _(a: ProPoint, b: ProPoint, log=False) -> bool:
    return a.is_ne(b, log)

@Relation.eq.register
def _(a: ProPoint, b: ProPoint):
    return sp.And(
        sp.Eq(a.x * b.z - b.x * a.z, 0),
        sp.Eq(a.y * b.z - b.y * a.z, 0),
    )
