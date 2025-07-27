from .primitives import *
from .relation import Relation
import sympy as sp


class GeoRelation:
    @staticmethod
    def collinear(pts):
        if len(pts) < 3:
            return sp.true
        a = pts[0]
        idx1 = next((i for i in range(1, len(pts)) if not pts[i] == a), None)
        if idx1 is None:
            return sp.true
        b = pts[idx1]

        l = ProLine.through(a, b)
        exprs = []
        for P in pts[1:]:
            if P == a or P == b:
                continue
            exprs.append(Relation.contained(P, l))
        return sp.And(*exprs)

    @staticmethod
    def concyclic(pts):
        if len(pts) < 4:
            return sp.true

        a = pts[0]

        idx1 = next((i for i in range(1, len(pts)) if not pts[i] == a), None)
        if idx1 is None:
            return sp.true
        b = pts[idx1]

        idx2 = next((i for i in range(idx1+1, len(pts))
                     if not pts[i] == a and not pts[i] == b), None)
        if idx2 is None:
            return sp.true
        c = pts[idx2]

        circ = ProCircle.through(a, b, c)
        exprs = []
        for P in pts[1:]:
            if P == a or P == b or P == c:
                continue
            exprs.append(Relation.contained(P, circ))

        return sp.And(*exprs)


    @staticmethod
    def concurrent(lines):
        if len(lines) < 2:
            return sp.true
        l0 = lines[0]
        idx1 = next((i for i in range(1, len(lines)) if not lines[i] == l0), None)
        if idx1 is None:
            return sp.true
        l1 = lines[idx1]

        p = l0.intersection(l1)
        exprs = []
        for L in lines:
            exprs.append(Relation.contained(p, L))
        return sp.And(*exprs)

    @staticmethod
    def same_side(p: ProPoint, q: ProPoint, l: ProLine):
        val_p = l.a * p.x + l.b * p.y + l.c * p.z
        val_q = l.a * q.x + l.b * q.y + l.c * q.z
        return Relation.ge(val_p*val_q, 0)

    @staticmethod
    def different_side(p: ProPoint, q: ProPoint, l: ProLine):
        return sp.Not(GeoRelation.same_side(p, q, l))

    @staticmethod
    def in_circle(p: ProPoint, c: ProCircle):
        expr = (
                c.a * (p.x ** 2 + p.y ** 2)
                + c.d * (p.x * p.z)
                + c.e * (p.y * p.z)
                + c.f * (p.z ** 2)
        )
        return Relation.le(expr, 0)

    @staticmethod
    def out_circle(p: ProPoint, c: ProCircle):
        return sp.Not(GeoRelation.in_circle(p, c))

    @staticmethod
    def parallel(l1: ProLine, l2: ProLine):
        return Relation.eq(l1.a * l2.b - l1.b * l2.a, 0)

    @staticmethod
    def perpendicular(l1: ProLine, l2: ProLine):
        return Relation.eq(l1.a * l2.a + l1.b * l2.b, 0)

