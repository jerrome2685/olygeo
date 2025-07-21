import sympy as sp
import mpmath as mp

from olygeo.algebra import (
    split_conditions,
    evaluate_condition,
    draw_valid_subs
)

x, y = sp.symbols('x y')

def test_split_conditions_empty():
    eq_br, oth_br = split_conditions([])
    assert len(eq_br) == 1
    assert eq_br[0] == []
    assert len(oth_br) == 1
    assert isinstance(oth_br[0][0], sp.logic.boolalg.BooleanAtom)

def test_split_conditions_and_or():
    cond = sp.And(sp.Eq(x,1), sp.Lt(y,2))
    eq_br, oth_br = split_conditions([cond])
    assert eq_br == [[sp.Eq(x,1)]]
    assert oth_br == [[sp.Lt(y,2)]]

    cond2 = sp.Or(sp.Eq(x,1), sp.Eq(x,-1))
    eq_br2, oth_br2 = split_conditions([cond2])
    assert len(eq_br2) == 2
    assert all(len(eqs)==1 for eqs in eq_br2)
    assert {tuple(eqs)[0] for eqs in eq_br2} == {sp.Eq(x,1), sp.Eq(x,-1)}
    assert oth_br2 == [[], []]

def test_evaluate_condition_relational():
    subs = {x: mp.mpf('1.0'), y: mp.mpf('2.0')}
    assert not evaluate_condition(sp.Eq(x,y), subs)
    assert not evaluate_condition(sp.Eq(x,2), subs)
    assert evaluate_condition(sp.Ne(x,2), subs)
    assert not evaluate_condition(sp.Ne(x,1), subs)
    assert evaluate_condition(sp.Lt(x,y), subs)
    assert evaluate_condition(sp.Le(x,y), subs)
    assert evaluate_condition(sp.Gt(y,x), subs)
    assert evaluate_condition(sp.Ge(y,x), subs)
    assert not evaluate_condition(sp.Lt(y,x), subs)
    c = sp.And(sp.Eq(x,1), sp.Lt(y,3))
    assert evaluate_condition(c, subs)
    c2 = sp.Or(sp.Eq(x,0), sp.Eq(y,2))
    assert evaluate_condition(c2, subs)
    c3 = sp.Not(sp.Eq(y,1))
    assert evaluate_condition(c3, subs)

def test_draw_valid_subs_simple_eq():
    eqb, othb = split_conditions([sp.Eq(x,0)])
    subs = draw_valid_subs([x], eqb[0], othb[0], low=-1, high=1)
    assert subs is not None
    assert abs(subs[x]) < 1e-3

def test_draw_valid_subs_disjunction():
    cond = sp.Or(sp.Eq(x,1), sp.Eq(x,-1))
    eqb, othb = split_conditions([cond])
    for i in range(2):
        subs = draw_valid_subs([x], eqb[i], othb[i], low=-2, high=2)
        assert subs is not None
        val = subs[x]
        assert abs(abs(val) - 1) < 1e-3

def test_draw_valid_subs_unsolvable():
    cond = sp.Eq(x**2 + 1, 0)
    eqb, othb = split_conditions([cond])
    subs = draw_valid_subs([x], eqb[0], othb[0], low=-2, high=2, max_depth=100)
    assert subs is None
