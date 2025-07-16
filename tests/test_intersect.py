import sympy as sp

from olygeo import *

def test_symbolic_choose_not_A():
    A = ProPoint.unfixed(); B = ProPoint.unfixed(); C = ProPoint.unfixed()
    D = ProPoint.unfixed()

    w = ProCircle.through(A, B, C)
    pts = w.intersection(ProLine.through(A, D))
    assert len(pts) == 2

    def not_A(P):
        return sp.Or(Ne(P.x*A.z - A.x*P.z, 0), Ne(P.y*A.z - A.y*P.z, 0))

    Q = pts.choose(not_A)
    assert Geo.is_ne(A, Q)


