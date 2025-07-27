import sympy as sp
from multimethod import multimethod


class Relation:
    @staticmethod
    @multimethod
    def eq(a, b):
        return sp.Eq(a, b)

    @staticmethod
    def ne(a, b):
        return sp.Not(Relation.eq(a, b))

    @staticmethod
    def lt(a, b):
        return sp.Lt(a, b)

    @staticmethod
    def le(a, b):
        return sp.Le(a, b)

    @staticmethod
    def gt(a, b):
        return sp.Gt(a, b)

    @staticmethod
    def ge(a, b):
        return sp.Ge(a, b)

    @staticmethod
    @multimethod
    def contained(a, b):
        return sp.Eq(a, b)