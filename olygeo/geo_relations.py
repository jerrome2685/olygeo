from .primitives import *
from .geo import *
import sympy as sp



def Collinear(pts):
    if len(pts) < 3:
        return sp.true
    A = pts[0]
    idx1 = next((i for i in range(1, len(pts)) if not pts[i] == A), None)
    if idx1 is None:
        return sp.true
    B = pts[idx1]

    L = ProLine.through(A, B)
    exprs = []
    for P in pts[1:]:
        if P == A or P == B:
            continue
        exprs.append(Contained(P, L))
    return sp.And(*exprs)


def Concyclic(pts):
    if len(pts) < 4:
        return sp.true

    A = pts[0]

    idx1 = next((i for i in range(1, len(pts)) if not pts[i] == A), None)
    if idx1 is None:
        return sp.true
    B = pts[idx1]

    idx2 = next((i for i in range(idx1+1, len(pts))
                 if not pts[i] == A and not pts[i] == B), None)
    if idx2 is None:
        return sp.true
    C = pts[idx2]

    circ = ProCircle.through(A, B, C)
    exprs = []
    for P in pts[1:]:
        if P == A or P == B or P == C:
            continue
        exprs.append(Contained(P, circ))

    return sp.And(*exprs)



def Concurrent(lines):
    if len(lines) < 2:
        return sp.true
    L0 = lines[0]
    idx1 = next((i for i in range(1, len(lines)) if not lines[i] == L0), None)
    if idx1 is None:
        return sp.true
    L1 = lines[idx1]

    P = L0.intersection(L1)
    exprs = []
    for L in lines:
        exprs.append(Contained(P, L))
    return sp.And(*exprs)


def Same_side(P: ProPoint, Q: ProPoint, L: ProLine):
    valP = L.a*P.x + L.b*P.y + L.c*P.z
    valQ = L.a*Q.x + L.b*Q.y + L.c*Q.z
    return Ge(valP*valQ, 0)


def Different_side(P: ProPoint, Q: ProPoint, L: ProLine):
    return sp.Not(Same_side(P, Q, L))


def In_circle(P: ProPoint, C: ProCircle):
    expr = (
        C.a*(P.x**2 + P.y**2)
        + C.d*(P.x * P.z)
        + C.e*(P.y * P.z)
        + C.f*(P.z**2)
    )
    return Le(expr, 0)


def Out_circle(P: ProPoint, C: ProCircle):
    return sp.Not(In_circle(P, C))


def Parallel(L1: ProLine, L2: ProLine):
    return Eq(L1.a*L2.b - L1.b*L2.a, 0)


def Perpendicular(L1: ProLine, L2: ProLine):
    return Eq(L1.a*L2.a + L1.b*L2.b, 0)

