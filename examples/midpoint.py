from olygeo import *
import sympy as sp


B = ProPoint.unfixed()
C = ProPoint.unfixed()

t = sp.symbols('t', real=True)
M = ProPoint(B.x + t * (C.x - B.x), B.y + t * (C.y - B.y))


Geo.add_condition( Eq(Geo.distance(B, M), Geo.distance(M, C)) )

M2 = (B + C) / 2

assert Geo.is_eq(M2, M, True)