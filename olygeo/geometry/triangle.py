import sympy as sp
from ..geo import Geo
from ..primitives import ProPoint, ProLine, ProCircle

class ProTriangle:
    def __init__(self, A: ProPoint, B: ProPoint, C: ProPoint):
        self.A, self.B, self.C = A, B, C

    @property
    def a(self): return Geo.distance(self.B, self.C)
    @property
    def b(self): return Geo.distance(self.C, self.A)
    @property
    def c(self): return Geo.distance(self.A, self.B)
    @property
    def perimeter(self): return self.a + self.b + self.c
    @property
    def semiperimeter(self): return self.perimeter / 2

    def area(self):
        M = sp.Matrix([
            [self.A.x, self.A.y, self.A.z],
            [self.B.x, self.B.y, self.B.z],
            [self.C.x, self.C.y, self.C.z]
        ])
        det = sp.simplify(M.det(method='bareiss'))
        denom = self.A.z * self.B.z * self.C.z
        if denom == 0:
            return sp.oo
        else:
            return abs(det) / denom

    def centroid(self):
        X = self.A.x + self.B.x + self.C.x
        Y = self.A.y + self.B.y + self.C.y
        Z = self.A.z + self.B.z + self.C.z
        return ProPoint(X, Y, Z)

    def circumcenter(self):
        circ = ProCircle.through(self.A, self.B, self.C)
        return ProPoint(-circ.d, -circ.e, 2*circ.a)

    def circumcircle(self):
        return ProCircle.through(self.A, self.B, self.C)

    def orthocenter(self):
        O = self.circumcenter()
        return (self.A + self.B + self.C) - (O * 2)

    def incenter(self):
        a, b, c = self.a, self.b, self.c
        X = a*self.A.x + b*self.B.x + c*self.C.x
        Y = a*self.A.y + b*self.B.y + c*self.C.y
        Z = a*self.A.z + b*self.B.z + c*self.C.z
        return ProPoint(X, Y, Z)

    def incircle(self):
        O = self.incenter()
        BC = ProLine.through(self.B, self.C)
        foot = O.perpendicular_foot(BC)
        return ProCircle.from_center_point(O, foot)

    def excenter(self, vertex: str):
        a, b, c = self.a, self.b, self.c
        if vertex == 'A': w = (-a, b, c)
        elif vertex == 'B': w = (a, -b, c)
        elif vertex == 'C': w = (a, b, -c)
        else: raise ValueError("vertex must be 'A','B', or 'C'")
        wA, wB, wC = w
        X = wA*self.A.x + wB*self.B.x + wC*self.C.x
        Y = wA*self.A.y + wB*self.B.y + wC*self.C.y
        Z = wA*self.A.z + wB*self.B.z + wC*self.C.z
        return ProPoint(X, Y, Z)

    def excircle(self, vertex: str):
        E = self.excenter(vertex)
        if vertex == 'A': S1, S2 = self.B, self.C
        elif vertex == 'B': S1, S2 = self.C, self.A
        else: S1, S2 = self.A, self.B
        side = ProLine.through(S1, S2)
        foot = E.perpendicular_foot(side)
        return ProCircle.from_center_point(E, foot)

    def angle_bisector(self, vertex: str, internal=True):
        if vertex == 'A': P = self.A; Ctr = self.incenter() if internal else self.excenter('A')
        elif vertex == 'B': P = self.B; Ctr = self.incenter() if internal else self.excenter('B')
        elif vertex == 'C': P = self.C; Ctr = self.incenter() if internal else self.excenter('C')
        else: raise ValueError("vertex must be 'A','B', or 'C'")
        return ProLine.through(P, Ctr)

    def __repr__(self):
        return f"ProTriangle(A={self.A}, B={self.B}, C={self.C})"