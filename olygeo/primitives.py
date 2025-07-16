from sympy import Symbol
import sympy as sp
from .geo import Geo, Eq, Ge
from .choice import ChoiceList
from multimethod import multimethod



class ProPoint:
    _unfixed_counter = 0


    def __init__(self, x, y, z=sp.sympify(1)):
        self.x, self.y, self.z = x, y, z


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

    def parallel_through(self, L: "ProLine"):
        A, B = L.a, L.b
        return ProLine(
            A * self.z,
            B * self.z,
            -(A * self.x + B * self.y)
        )

    def perpendicular_through(self, L: "ProLine"):
        A, B = L.b, -L.a
        return ProLine(
            A * self.z,
            B * self.z,
            -(A * self.x + B * self.y)
        )

    def perpendicular_foot(self, L: "ProLine"):
        return L.intersection(self.perpendicular_through(L))

    def is_eq(self, other) -> bool:
        return Geo.is_zero(self.x * other.z - other.x * self.z) \
            and Geo.is_zero(self.y * other.z - other.y * self.z)

    def is_ne(self, other) -> bool:
        return not self.is_eq(other)


class ProLine:
    _unfixed_counter = 0

    def __init__(self, a, b, c=sp.sympify(1)):
        self.a, self.b, self.c = a, b, c

    @classmethod
    def through(cls, P: ProPoint, Q: ProPoint):
        a = P.y * Q.z - Q.y * P.z
        b = Q.x * P.z - P.x * Q.z
        c = P.x * Q.y - Q.x * P.y
        return cls(a, b, c)

    @classmethod
    def unfixed(cls):
        name = f"{cls.__name__}_{cls._unfixed_counter}"
        cls._unfixed_counter += 1
        return cls(Symbol(f"{name}_a"), Symbol(f"{name}_b"))

    def contains(self, P: ProPoint):
        expr = self.a*P.x + self.b*P.y + self.c*P.z
        return Geo.is_zero(expr)

    @multimethod
    def intersection(self, other):
        raise TypeError(f"Cannot intersect ProLine with {type(other).__name__}")


    def __eq__(self, other):
        return (
                self.a == other.a and
                self.b == other.b and
                self.c == other.c
        )

    def __hash__(self):
        return hash((self.a, self.b, self.c))

    def __repr__(self):
        return f"ProLine({self.a}*x+{self.b}*y+{self.c}*z=0)"

    def is_eq(self, other) -> bool:
        return Geo.is_zero(self.a * other.b - other.a * self.b) \
            and Geo.is_zero(self.a * other.c - other.a * self.c)

    def is_ne(self, other) -> bool:
        return not self.is_eq(other)



class ProCircle:
    _unfixed_counter = 0

    def __init__(self, a, d, e, f=sp.sympify(1)):
        self.a, self.d, self.e, self.f = a, d, e, f

    @classmethod
    def unfixed(cls):
        name = f"{cls.__name__}_{cls._unfixed_counter}"
        cls._unfixed_counter += 1
        return cls(Symbol(f"{name}_a"), Symbol(f"{name}_d"), Symbol(f"{name}_e"))

    @classmethod
    def through(cls, P: ProPoint, Q: ProPoint, R: ProPoint):
        M_PQ = (P + Q) / 2
        M_QR = (Q + R) / 2

        bis_PQ = M_PQ.perpendicular_through(ProLine.through(P, Q))
        bis_QR = M_QR.perpendicular_through(ProLine.through(Q, R))

        O = bis_PQ.intersection(bis_QR)
        return cls.from_center_point(O, P)

    @classmethod
    def from_center_point(cls, O: ProPoint, Q: ProPoint):
        Ox, Oy, Oz = O.x, O.y, O.z
        Qx, Qy, Qz = Q.x, Q.y, Q.z

        a = Oz ** 2 * Qz ** 2
        d = -2 * Ox * Oz * Qz ** 2
        e = -2 * Oy * Oz * Qz ** 2
        f = (Ox ** 2 + Oy ** 2) * Qz ** 2 - (Qx * Oz - Ox * Qz) ** 2 + (Qy * Oz - Oy * Qz) ** 2
        return cls(a, d, e, f)

    def contains(self, P: ProPoint):
        expr = (self.a*(P.x**2 + P.y**2)
                + self.d*(P.x*P.z)
                + self.e*(P.y*P.z)
                + self.f*(P.z**2))
        return Geo.is_zero(expr)

    def power(self, P: ProPoint):
        return self.contains(P)

    def radial_axis(self, other):
        A = self.d*other.a - other.d*self.a
        B = self.e*other.a - other.e*self.a
        C = self.f*other.a - other.f*self.a
        return ProLine(A, B, C)

    @multimethod
    def intersection(self, other):
        raise TypeError(f"Cannot intersect ProCircle with {type(other).__name__}")

    @intersection.register
    def _(self, line: ProLine, *, require_real=True):
        a1, b1, c1 = line.a, line.b, line.c
        A, d, e, f = self.a, self.d, self.e, self.f

        C2 = A * (b1 ** 2 + a1 ** 2)
        C1 = -2 * A * b1 * c1 + d * a1 * b1 - e * a1 ** 2
        C0 = A * c1 ** 2 - d * a1 * c1 + f * a1 ** 2

        D = C1 ** 2 - 4 * C2 * C0
        sD = sp.sqrt(D)

        if require_real:
            Geo.add_condition(Ge(D, 0))

        u_plus, t_plus = -C1 + sD, 2 * C2
        u_minus, t_minus = -C1 - sD, 2 * C2

        x_p = b1 * u_plus - c1 * t_plus
        y_p = -a1 * u_plus
        z_p = a1 * t_plus

        x_m = b1 * u_minus - c1 * t_minus
        y_m = -a1 * u_minus
        z_m = a1 * t_minus

        return ChoiceList([
            ProPoint(x_p, y_p, z_p),
            ProPoint(x_m, y_m, z_m),
        ])

    def center(self):
        return ProPoint(-self.d, -self.e, 2 * self.a)

    def __eq__(self, other):
        return (
            self.a == other.a and
            self.d == other.d and
            self.e == other.e and
            self.f == other.f
        )

    def __hash__(self):
        return hash((self.a, self.d, self.e, self.f))

    def __repr__(self):
        return f"ProCircle({self.a}*(x^2+y^2)+{self.d}*x*z+{self.e}*y*z+{self.f}*z^2=0)"

    def is_eq(self, other: "ProCircle") -> bool:
        return (
            Geo.is_zero(self.d * other.a - other.d * self.a) and
            Geo.is_zero(self.e * other.a - other.e * self.a) and
            Geo.is_zero(self.f * other.a - other.f * self.a)
        )

    def is_ne(self, other: "ProCircle") -> bool:
        return not self.is_eq(other)

@ProLine.intersection.register
def _(self, other: ProLine):
    x = self.b * other.c - other.b * self.c
    y = other.a * self.c - self.a * other.c
    z = self.a * other.b - other.a * self.b
    return ProPoint(x, y, z)

@ProLine.intersection.register
def _(self, other: ProCircle):
    return other.intersection(self)


@ProCircle.intersection.register
def _(self: ProCircle, other: ProCircle):
    rad = self.radial_axis(other)
    pts = self.intersection(rad)
    return pts

@Geo.intersection.register
def _(L1: ProLine, L2: ProLine):
    return L1.intersection(L2)

@Geo.intersection.register
def _(C: ProCircle, L: ProLine):
    return C.intersection(L)

@Geo.intersection.register
def _(L: ProLine, C: ProCircle):
    return C.intersection(L)

@Geo.intersection.register
def _(C1: ProCircle, C2: ProCircle):
    return C1.intersection(C2)

@Geo.is_eq.register
def _(A: ProPoint, B: ProPoint) -> bool:
    return A.is_eq(B)

@Geo.is_eq.register
def _(L1: ProLine, L2: ProLine) -> bool:
    return L1.is_eq(L2)

@Geo.is_eq.register
def _(C1: ProCircle, C2: ProCircle) -> bool:
    return C1.is_eq(C2)

@Geo.distance.register
def _(P1: ProPoint, P2: ProPoint):
    if Geo.is_zero(P1.z) or Geo.is_zero(P2.z):
        return sp.oo
    dx = P1.x*P2.z - P2.x*P1.z
    dy = P1.y*P2.z - P2.y*P1.z
    denom = P1.z * P2.z
    return sp.sqrt((dx/denom)**2 + (dy/denom)**2)

@Geo.distance.register
def _(P: ProPoint, L: ProLine):
    if Geo.is_zero(P.z):
        return 0 if L.contains(P) else sp.oo
    if Geo.is_zero(L.a) and Geo.is_zero(L.b):
        return sp.oo
    num = abs(L.a*P.x + L.b*P.y + L.c*P.z)
    den = sp.sqrt(L.a**2 + L.b**2)*abs(P.z)
    return num/den

@Geo.distance.register
def _(L: ProLine, P: ProPoint):
    return Geo.distance(P, L)

@Geo.angle.register
def _(l1: ProLine, l2: ProLine, _unused=None):
    a1, b1 = l1.a, l1.b
    a2, b2 = l2.a, l2.b
    if (Geo.is_zero(a1) and Geo.is_zero(b1)) or (Geo.is_zero(a2) and Geo.is_zero(b2)):
        raise ValueError("Cannot take angle with the line at infinity")
    dot = a1 * a2 + b1 * b2
    n1 = sp.sqrt(a1 ** 2 + b1 ** 2)
    n2 = sp.sqrt(a2 ** 2 + b2 ** 2)
    return sp.acos(dot / (n1 * n2))


@Geo.angle.register
def _(A: ProPoint, B: ProPoint, C: ProPoint):
    if A.is_eq(B) or B.is_eq(C):
        return sp.sympify(0)
    v1 = sp.Matrix([A.x * B.z - B.x * A.z, A.y * B.z - B.y * A.z])
    v2 = sp.Matrix([C.x * B.z - B.x * C.z, C.y * B.z - B.y * C.z])
    dot = v1.dot(v2)
    n1 = sp.sqrt(v1.dot(v1))
    n2 = sp.sqrt(v2.dot(v2))
    return sp.acos(dot / (n1 * n2))

@Eq.register
def _(A: ProPoint, B: ProPoint):
    return sp.And(
        sp.Eq(A.x * B.z - B.x * A.z, 0),
        sp.Eq(A.y * B.z - B.y * A.z, 0),
    )

@Eq.register
def _(a: ProLine, b:ProLine):
    return sp.And(
        sp.Eq(a.a * b.b - b.a * a.b, 0),
        sp.Eq(a.a * b.c - b.a * a.c, 0),
        sp.Eq(a.b * b.c - b.b * a.c, 0),
    )

@Eq.register
def _(a: ProCircle, b:ProCircle):
    return sp.And(
        sp.Eq(a.d * b.a - b.d * a.a, 0),
        sp.Eq(a.e * b.a - b.e * a.a, 0),
        sp.Eq(a.f * b.a - b.f * a.a, 0),
    )




