from olygeo import *
import sympy as sp


def test_midpoint():
    B = ProPoint.unfixed()
    C = ProPoint.unfixed()

    t = sp.symbols('t', real=True)
    M = ProPoint(B.x + t * (C.x - B.x), B.y + t * (C.y - B.y))


    Geo.add_condition( Relation.eq(Geo.distance(B, M), Geo.distance(M, C)) )

    M2 = (B + C) / 2

    assert M.is_eq(M2)
    Geo.clear_conditions()
