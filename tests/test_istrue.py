from sympy import Eq, symbols, Or, And
from olygeo.algebra import is_true


def test_literal_boolean():
    # Direct Python bools
    assert is_true(True, conditions = [])
    assert not is_true(False, conditions = [])


def test_no_symbols():
    # Expressions without free symbols evaluate directly
    assert is_true(Eq(1+1, 2), conditions=[])
    assert not is_true(Eq(1+1, 3), conditions=[])


def test_simple_condition_true():
    x = symbols('x')
    # With matching condition, is_true should return True
    assert is_true(Eq(x, 1), conditions=[Eq(x, 1)])


def test_simple_condition_false():
    x = symbols('x')
    # Without condition, random x rarely equals 1 ⇒ False
    assert not is_true(Eq(x, 1), conditions=[])


def test_branch_conditions_false():
    x = symbols('x')
    # condition: x == 1 or x == 2
    cond = Or(Eq(x, 1), Eq(x, 2))
    # relation x == 1 only holds for branch x=1, fails for x=2 ⇒ overall False
    assert not is_true(Eq(x, 1), conditions=[cond])


def test_branch_conditions_true():
    x = symbols('x')
    # condition: x == 1 or x == -1
    cond = Or(Eq(x, 1), Eq(x, -1))
    # relation x^2 == 1 holds for both x=1 and x=-1 branches ⇒ True
    assert is_true(Eq(x**2, 1), conditions=[cond])


def test_multiple_symbols_true():
    x, y = symbols('x y')
    # conditions: x=2 and y=3
    conds = [Eq(x, 2), Eq(y, 3)]
    # relation x+y == 5 holds under these conditions
    assert is_true(Eq(x + y, 5), conditions=conds)


def test_multiple_symbols_false():
    x, y = symbols('x y')
    conds = [Eq(x, 2), Eq(y, 3)]
    # relation x-y == 0 fails under these conditions
    assert not is_true(Eq(x - y, 0), conditions=conds)

def test_nested_boolean_relations():
    x, y = symbols('x y')
    rel = Or(And(Eq(x, 1), Eq(y, 2)), And(Eq(x, 3), Eq(y, 4)))
    assert not is_true(rel, conditions=[])
    cond1 = [Eq(x, 1), Eq(y, 2)]
    cond2 = [Eq(x, 3), Eq(y, 4)]
    cond = Or(And(*cond1), And(*cond2))
    assert is_true(rel, conditions=[cond])
