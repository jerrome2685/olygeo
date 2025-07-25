from sympy import Expr, Integer
import sympy as sp
from .geo import Geo, Eq, Ge, Contained
from .utils import ChoiceList
from .container import ProContainer
from .point import ProPoint




class ProLine(ProContainer):
    a: Expr
    b: Expr
    c: Expr

    _fields   = ('a', 'b', 'c')
    _defaults = {'c': Integer(1)}

    @classmethod
    def through(cls, p: ProPoint, q: ProPoint):
        a = p.y * q.z - q.y * p.z
        b = q.x * p.z - p.x * q.z
        c = p.x * q.y - q.x * p.y
        return cls(a, b, c)

    def contains(self, p: ProPoint, log=False):
        expr = self.a * p.x + self.b * p.y + self.c * p.z
        return Geo.is_zero(expr, log=log)


    def parallel_through(self, p: ProPoint):
        return ProLine(
            self.a * p.z,
            self.b * p.z,
            -(self.a * p.x + self.b * p.y)
        )

    def perpendicular_through(self, p: ProPoint):
        return ProLine(
            self.b * p.z,
            -self.a * p.z,
            -(self.b * p.x - self.a * p.y)
        )

    def perpendicular_foot(self, p: ProPoint):
        return self.intersection(self.perpendicular_through(p))

    def is_eq(self, other, log=False) -> bool:
        return Geo.is_zero((self.a * other.b - other.a * self.b)**2 + (self.a * other.c - other.a * self.c)**2, log=log)

    def is_ne(self, other, log=False) -> bool:
        return Geo.is_nonzero((self.a * other.b - other.a * self.b) ** 2 +
                              (self.a * other.c - other.a * self.c) ** 2, log=log)


    def __repr__(self):
        return f"ProLine({self.a}*x + {self.b}*y + {self.c}*z = 0)"




class ProCircle(ProContainer):
    a: Expr
    d: Expr
    e: Expr
    f: Expr
    _fields   = ('a', 'd', 'e', 'f')
    _defaults = {'f': 1}

    @classmethod
    def from_center_point(cls, o: ProPoint, q: ProPoint):
        ox, oy, oz = o.x, o.y, o.z
        qx, qy, qz = q.x, q.y, q.z

        a = oz ** 2 * qz ** 2
        d = -2 * ox * oz * qz ** 2
        e = -2 * oy * oz * qz ** 2
        f = (ox ** 2 + oy ** 2) * qz ** 2 - (qx * oz - ox * qz) ** 2 - (qy * oz - oy * qz) ** 2
        return cls(a, d, e, f)

    @classmethod
    def through(cls, p: ProPoint, q: ProPoint, r: ProPoint):
        m_pq = (p + q) / 2
        m_qr = (q + r) / 2

        bis_pq = ProLine.through(p, q).perpendicular_through(m_pq)
        bis_qr = ProLine.through(q, r).perpendicular_through(m_qr)
        o = bis_pq.intersection(bis_qr)
        return cls.from_center_point(o, p)


    def power(self, p: ProPoint):
        return (
                self.a * (p.x ** 2 + p.y ** 2)
                + self.d * (p.x * p.z)
                + self.e * (p.y * p.z)
                + self.f * (p.z ** 2)
        )

    def contains(self, p: ProPoint, log=False):
        return Geo.is_zero(self.power(p), log=log)


    def radial_axis(self, other: "ProCircle"):
        return ProLine(self.d*other.a - other.d*self.a,
                       self.e*other.a - other.e*self.a, self.f*other.a - other.f*self.a)

    def center(self):
        return ProPoint(-self.d, -self.e, 2 * self.a)

    def __repr__(self):
        return (f"ProCircle({self.a}*(x²+y²) + {self.d}*x*z + "
                f"{self.e}*y*z + {self.f}*z² = 0)")

    def is_eq(self, other: "ProCircle", log=False) -> bool:
        return (
            Geo.is_zero((self.d * other.a - other.d * self.a)**2 + (self.e * other.a - other.e * self.a)**2
                        + (self.f * other.a - other.f * self.a)**2, log=log)
        )

    def is_ne(self, other: "ProCircle", log=False) -> bool:
        return (
            Geo.is_nonzero((self.d * other.a - other.d * self.a)**2 + (self.e * other.a - other.e * self.a)**2
                        + (self.f * other.a - other.f * self.a)**2, log=log)
        )


@ProContainer.intersection.register(ProLine, ProLine)
def _line_line(l1: ProLine, l2: ProLine) -> ProPoint:
    x = l1.b*l2.c - l2.b*l1.c
    y = l2.a*l1.c - l1.a*l2.c
    z = l1.a*l2.b - l2.a*l1.b
    return ProPoint(x, y, z)

@ProContainer.intersection.register(ProLine, ProCircle)
def _line_circle(line: ProLine, circle: ProCircle, require_real: bool = True) -> ChoiceList[ProPoint]:
    a1, b1, c1 = line.a, line.b, line.c
    a, d, e, f = circle.a, circle.d, circle.e, circle.f

    c2 = a * (b1 ** 2 + a1 ** 2)
    c11 = -2 * a * b1 * c1 + d * a1 * b1 - e * a1 ** 2
    c0 = a * c1 ** 2 - d * a1 * c1 + f * a1 ** 2

    de = c11 ** 2 - 4 * c2 * c0
    s_d = sp.sqrt(de)

    if require_real:
        Geo.add_condition(Ge(de, 0))

    u_plus, t_plus = -c11 + s_d, 2 * c2
    u_minus, t_minus = -c11 - s_d, 2 * c2

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

@ProContainer.intersection.register(ProCircle, ProLine)
def _(circle: ProCircle, line: ProLine, require_real: bool = True) -> ChoiceList[ProPoint]:
    return _line_circle(line, circle, require_real=require_real)

@ProContainer.intersection.register(ProCircle, ProCircle)
def _circle_circle(c1: ProCircle, c2: ProCircle, require_real: bool = False) -> ChoiceList[ProPoint]:
    return _line_circle(c1.radial_axis(c2), c2, require_real=require_real)



@Geo.is_eq.register
def _(c1: ProContainer, c2: ProContainer, log=False) -> bool:
    return c1.is_eq(c2, log)

@Geo.is_ne.register
def _(c1: ProContainer, c2: ProContainer, log=False) -> bool:
    return c1.is_ne(c2, log)

@Geo.distance.register
def _(p1: ProPoint, p2: ProPoint):
    if Geo.is_zero(p1.z) or Geo.is_zero(p2.z):
        return sp.oo
    dx = p1.x * p2.z - p2.x * p1.z
    dy = p1.y * p2.z - p2.y * p1.z
    denom = p1.z * p2.z
    return sp.sqrt((dx/denom)**2 + (dy/denom)**2)

@Geo.distance.register
def _(p: ProPoint, l: ProLine):
    if Geo.is_zero(p.z):
        return 0 if l.contains(p) else sp.oo
    if Geo.is_zero(l.a) and Geo.is_zero(l.b):
        return sp.oo
    num = abs(l.a * p.x + l.b * p.y + l.c * p.z)
    den = sp.sqrt(l.a ** 2 + l.b ** 2) * abs(p.z)
    return num/den

@Geo.distance.register
def _(l: ProLine, p: ProPoint):
    return Geo.distance(p, l)

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
def _(a: ProPoint, b: ProPoint, c: ProPoint):
    if a.is_eq(b) or b.is_eq(c):
        return sp.sympify(0)
    v1 = sp.Matrix([a.x * b.z - b.x * a.z, a.y * b.z - b.y * a.z])
    v2 = sp.Matrix([c.x * b.z - b.x * c.z, c.y * b.z - b.y * c.z])
    dot = v1.dot(v2)
    n1 = sp.sqrt(v1.dot(v1))
    n2 = sp.sqrt(v2.dot(v2))
    return sp.acos(dot / (n1 * n2))



@Contained.register
def _(p: ProPoint, l: ProLine):
    return sp.Eq(l.a * p.x + l.b * p.y + l.c * p.z, 0)

@Contained.register
def _(p: ProPoint, c: ProCircle):
    return sp.Eq(c.a * (p.x ** 2 + p.y ** 2) + c.d * (p.x * p.z) + c.e * (p.y * p.z) + c.f * (p.z ** 2),0)

# @Contained.register
# def _(p: ProPoint, seg: ProSegment):
#     on_line = sp.Eq(seg.a * p.x + seg.b * p.y + seg.c * p.z, 0)
#     u_x = p.x*seg.A.z - seg.A.x*p.z
#     u_y = p.y*seg.A.z - seg.A.y*p.z
#     v_x = p.x*seg.B.z - seg.B.x*p.z
#     v_y = p.y*seg.B.z - seg.B.y*p.z
#     return sp.And(on_line, sp.Le(u_x*v_x + u_y*v_y, 0))



@Eq.register
def _(a: ProLine, b:ProLine):
    return sp.And(
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

# @Eq.register
# def _(a: ProSegment, b:ProSegment):
#     A1 = a.A
#     B1 = a.B
#     A2 = b.A
#     B2 = b.B
#     return sp.Or(
#         sp.And(Eq(A1, A2), Eq(B1, B2)),
#         sp.And(Eq(A1, B2), Eq(A2, B1))
#     )

'''
intersection btw segment & line / seg & seg
contained for seg & line


'''

#



