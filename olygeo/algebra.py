import random
import numpy as np
import sympy as sp
import mpmath as mp
from sympy.core.expr import Expr
from sympy import Matrix
from sympy.logic.boolalg import to_dnf, And, BooleanFunction, BooleanAtom
from sympy.core.relational import Equality, Relational
from functools import lru_cache

mp.mp.dps = 1000
mp.mp.epsilon = mp.mpf('1e-100')

tol = mp.mpf('1e-100')

@lru_cache(maxsize=None)
def _lamb_cache(expr, syms):
    return sp.lambdify(syms, expr, modules=[mp], cse=True)

def lambdify_mpmath(expr, syms):
    return _lamb_cache(expr, tuple(syms))


def flatten_and(cond):
    if isinstance(cond, And):
        for arg in cond.args:
            yield from flatten_and(arg)
    elif isinstance(cond, (BooleanFunction, BooleanAtom, Relational)):
        yield cond


def split_conditions(conditions):
    big = And(*conditions) if conditions else True
    dnf = to_dnf(big, simplify=False)
    branches = list(dnf.args) if isinstance(dnf, sp.Or) else [dnf]

    eq_br, other_br = [], []
    for br in branches:
        leaves = list(flatten_and(br))
        eqs   = [leaf for leaf in leaves if isinstance(leaf, Equality)]
        neqs  = [leaf for leaf in leaves if not isinstance(leaf, Equality)]
        eq_br.append(eqs)
        other_br.append(neqs)
    return eq_br, other_br


def evaluate_condition(cond, subs):
    if isinstance(cond, BooleanFunction):
        if cond.func is sp.And:
            return all(evaluate_condition(a, subs) for a in cond.args)
        if cond.func is sp.Or:
            return any(evaluate_condition(a, subs) for a in cond.args)
        if cond.func is sp.Not:
            return not evaluate_condition(cond.args[0], subs)
        return bool(cond.xreplace(subs))

    if isinstance(cond, BooleanAtom):
        return bool(cond)

    if isinstance(cond, Relational):
        lhs = float(cond.lhs.subs(subs).evalf())
        rhs = float(cond.rhs.subs(subs).evalf())
        diff = lhs - rhs
        if cond.func is sp.Eq: return abs(diff) < tol
        if cond.func is sp.Ne: return abs(diff) > tol
        if cond.func is sp.Lt: return diff < -tol
        if cond.func is sp.Le: return diff <= tol
        if cond.func is sp.Gt: return diff > tol
        if cond.func is sp.Ge: return diff >= tol

    raise ValueError(f'Cannot evaluate condition: {cond}')


def draw_valid_subs(base_syms, eq_branches, other_branches,
                    low=-2.0, high=2.0, max_depth=5000):
    for eqs, ineqs in zip(eq_branches, other_branches):
        funcs_syms = [(eq.lhs - eq.rhs) for eq in eqs]
        all_eq_syms = list({s for f in funcs_syms for s in f.free_symbols})
        if len(funcs_syms) > len(all_eq_syms): continue

        eq_funcs = [lambdify_mpmath(f, all_eq_syms) for f in funcs_syms]
        for _ in range(max_depth):
            subs = {s: mp.mpf(random.uniform(low, high)) for s in base_syms}
            if funcs_syms:
                solve_vars = random.sample(all_eq_syms, len(funcs_syms))
                def sysfun(*vals):
                    a = subs.copy()
                    for v,val in zip(solve_vars, vals): a[v] = val
                    return [eq_funcs[i](*[a[s] for s in all_eq_syms]) for i in range(len(funcs_syms))]
                guesses = [subs[v] for v in solve_vars]
                try: sol = mp.findroot(sysfun, guesses)
                except Exception: continue
                sol = sol if hasattr(sol, '__iter__') else [sol]
                ok = True
                for v,val in zip(solve_vars, sol):
                    if abs(mp.im(val)) > tol: ok=False; break
                    subs[v] = mp.re(val)
                if not ok: continue
            if all(evaluate_condition(c, subs) for c in ineqs): return subs
    print(f'No valid assignment found for conditions: {eq_branches}, {other_branches}')
    return None


def is_zero(expr: Expr, conditions, *, trials=10, low=-2.0, high=2.0, log=False) -> bool:
    if not isinstance(expr, Expr) or not expr.free_symbols:
        return abs(float(expr)) < tol
    cond_syms = set().union(*(c.free_symbols for c in conditions))
    base_syms = list(set(expr.free_symbols) | cond_syms)
    f_mp = lambdify_mpmath(expr, base_syms)
    eq_br, other_br = split_conditions(conditions)
    for i in range(trials):
        subs = draw_valid_subs(base_syms, eq_br, other_br, low, high)
        if subs is None: return False
        val = f_mp(*[subs[s] for s in base_syms])
        if log:
            print(f' trial {i+1}: expr ≈ {mp.nstr(val, 10)}')
        if abs(val) > tol: return False
    return True


def is_nonnegative(expr: Expr, conditions, *, trials=10, low=-2.0, high=2.0, log=False) -> bool:
    if not isinstance(expr, Expr) or not expr.free_symbols:
        return float(expr) >= -tol
    cond_syms = set().union(*(c.free_symbols for c in conditions))
    base_syms = list(set(expr.free_symbols) | cond_syms)
    f_mp = lambdify_mpmath(expr, base_syms)
    eq_br, other_br = split_conditions(conditions)
    for i in range(trials):
        subs = draw_valid_subs(base_syms, eq_br, other_br, low, high)
        if subs is None: return False
        val = f_mp(*[subs[s] for s in base_syms])
        if log:
            print(f' trial {i+1}: val ≈ {mp.nstr(val, 10)}')
        if val < -tol: return False
    return True


def probabilistic_rank(M: Matrix, conditions, *, trials=10, low=-2.0, high=2.0) -> int:
    cond_syms = set().union(*(c.free_symbols for c in conditions))
    base_syms = list(set(M.free_symbols) | cond_syms)
    entry_funcs = [lambdify_mpmath(M[i,j], base_syms) for i in range(M.rows) for j in range(M.cols)]
    eq_br, other_br = split_conditions(conditions)
    max_rank = 0
    for _ in range(trials):
        subs = draw_valid_subs(base_syms, eq_br, other_br, low, high, 100)
        if subs is None: continue
        A_mp = sp.Matrix([[entry_funcs[i * M.cols + j](*[subs[s] for s in base_syms])
                           for j in range(M.cols)]
                          for i in range(M.rows)])
        _, U, _ = mp.lu(A_mp)
        r = sum(1 for i in range(min(M.rows, M.cols)) if abs(U[i, i]) > tol)
        max_rank = max(max_rank, r)
    return max_rank
