from .algebra import is_zero, probabilistic_rank, is_non_negative, is_positive, is_nonzero
from sympy.core.relational import Relational
from sympy import Matrix
import sympy as sp
from functools import singledispatch
from multimethod import multimethod


class Geo:

    conditions = []

    @staticmethod
    def add_condition(cond: Relational):
        Geo.conditions.append(cond)

    @staticmethod
    def clear_conditions():
        Geo.conditions.clear()

    @staticmethod
    def is_zero(expr, **kwargs):
        return is_zero(expr, Geo.conditions, **kwargs)

    @staticmethod
    def is_nonzero(expr, **kwargs):
        return is_nonzero(expr, Geo.conditions, **kwargs)

    @staticmethod
    def is_non_negative(expr, **kwargs):
        return is_non_negative(expr, Geo.conditions, **kwargs)

    @staticmethod
    def is_positive(expr, **kwargs):
        return is_positive(expr, Geo.conditions, **kwargs)

    @staticmethod
    def probabilistic_rank(M, **kwargs):
        return probabilistic_rank(M, Geo.conditions, **kwargs)

    @staticmethod
    def is_collinear(pts: list) -> bool:
        if len(pts) < 3:
            return True
        M = Matrix([[p.x, p.y, p.z] for p in pts])
        r = Geo.probabilistic_rank(M)
        return r <= 2

    @staticmethod
    def is_concyclic(pts: list) -> bool:
        if len(pts) < 4:
            return True
        M = Matrix([[p.x**2 + p.y**2, p.x*p.z, p.y*p.z, p.z**2] for p in pts])
        r = Geo.probabilistic_rank(M)
        return r <= 3

    @staticmethod
    def is_concurrent(lines: list) -> bool:
        if len(lines) < 3:
            return True
        M = Matrix([[l.a, l.b, l.c] for l in lines])
        r = Geo.probabilistic_rank(M)
        return r <= 2

    @staticmethod
    @multimethod
    def is_contained(a, b, log=False):
        raise TypeError(f"Cannot interpret {type(a)} contained to {type(b)}")


    @staticmethod
    @multimethod
    def intersection(a, b):
        raise TypeError(f"Don't know how to intersect {type(a)} & {type(b)}")

    @staticmethod
    @multimethod
    def distance(a, b):
        raise TypeError(f"Don't know distance between {type(a)} & {type(b)}")

    @staticmethod
    @multimethod
    def angle(obj1, obj2, obj3=None):
        raise TypeError(f"Cannot compute angle for types: {type(obj1)}")

    @staticmethod
    @multimethod
    def is_eq(a, b, log=False) -> bool:
        return Geo.is_zero(a - b, log=log)



    @staticmethod
    def is_ne(a, b, log=False) -> bool:
        return Geo.is_nonzero(a - b, log=log)

    @staticmethod
    def is_lt(expr1, expr2, log=False) -> bool:
        return Geo.is_positive(expr2 - expr1, log=log)

    @staticmethod
    def is_le(expr1, expr2, log=False) -> bool:
        return Geo.is_non_negative(expr2 - expr1, log=log)

    @staticmethod
    def is_ge(expr1, expr2, log=False) -> bool:
        return Geo.is_non_negative(expr1 - expr2, log=log)

    @staticmethod
    def is_gt(expr1, expr2, log=False) -> bool:
        return Geo.is_positive(expr1 - expr2, log=log)


@singledispatch
def Eq(a, b):
    return sp.Eq(a, b)

def Ne(a, b):
    return sp.Not(Eq(a, b))


def Lt(a, b):
    return sp.Lt(a, b)


def Le(a, b):
    return sp.Le(a, b)


def Gt(a, b):
    return sp.Gt(a, b)


def Ge(a, b):
    return sp.Ge(a, b)

@multimethod
def Contained(a, b):
    return Eq(a, b)
