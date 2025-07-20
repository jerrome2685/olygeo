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
