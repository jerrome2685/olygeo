from olygeo import *
import sympy as sp
from sympy.core.relational import Relational

def test_collinear_numeric_true():
    A = ProPoint(0, 0)
    B = ProPoint(1, 1)
    C = ProPoint(2, 2)
    assert Collinear([A, B, C])


def test_collinear_numeric_false():
    A = ProPoint(0, 0)
    B = ProPoint(1, 2)
    C = ProPoint(2, 1)
    assert not Collinear([A, B, C])


def test_collinear_symbolic():
    A = ProPoint.unfixed()
    B = ProPoint.unfixed()
    C = ProPoint.unfixed()
    expr = Collinear([A, B, C])
    assert isinstance(expr, Relational)
    assert expr != sp.true


def test_concyclic_numeric_true():
    pts = [ProPoint(0, 0), ProPoint(1, 0), ProPoint(1, 1), ProPoint(0, 1)]
    assert Concyclic(pts)


def test_concyclic_numeric_false():
    # three on unit circle, one off
    pts = [ProPoint(1, 0), ProPoint(0, 1), ProPoint(-1, 0), ProPoint(2, 0)]
    assert not Concyclic(pts)


def test_concyclic_symbolic():
    A = ProPoint.unfixed()
    B = ProPoint.unfixed()
    C = ProPoint.unfixed()
    D = ProPoint.unfixed()
    assert Concyclic([A, B, C, D]) != sp.true


def test_concurrent_numeric_true():
    # lines through origin
    L1 = ProLine.through(ProPoint(0, 0), ProPoint(1, 1))
    L2 = ProLine.through(ProPoint(0, 0), ProPoint(1, 2))
    L3 = ProLine.through(ProPoint(0, 0), ProPoint(2, 1))
    assert Concurrent([L1, L2, L3])


def test_concurrent_numeric_false():
    L1 = ProLine.through(ProPoint(0, 0), ProPoint(1, 0))
    L2 = ProLine.through(ProPoint(0, 1), ProPoint(1, 1))
    L3 = ProLine.through(ProPoint(0, 2), ProPoint(1, 2))
    assert Concurrent([L1, L2, L3])


def test_concurrent_symbolic():
    # three lines through symbolic point A
    A = ProPoint.unfixed()
    B = ProPoint.unfixed()
    C = ProPoint.unfixed()
    L1 = ProLine.through(A, B)
    L2 = ProLine.through(A, C)
    L3 = ProLine.through(A, ProPoint.unfixed())
    assert Concurrent([L1, L2, L3])