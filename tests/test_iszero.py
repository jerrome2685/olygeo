# benchmark_is_zero.py
import time
import sympy as sp
from olygeo.algebra import is_zero
from olygeo.geo import Eq

def test_is_zero():
    # Prepare
    x, y = sp.symbols('x y')
    conds = [Eq(x**2 - y**3, 2)]           # no extra conditions
    trials = 100

    # Warm‑up
    is_zero(x, conds)
    is_zero(y, conds)
    is_zero(x**2 + y**2, conds)

    # 1) Separate calls
    t0 = time.perf_counter()
    for _ in range(trials):
        is_zero(x, conds)
        is_zero(y, conds)
    t_sep = time.perf_counter() - t0

    # 2) Combined call
    t0 = time.perf_counter()
    for _ in range(trials):
        is_zero(x**2 + y**2, conds, trials=1)
    t_comb = time.perf_counter() - t0

    print(f"is_zero(x) & is_zero(y): {t_sep:.4f}s total, {t_sep/trials*1000:.3f}ms each")
    print(f"is_zero(x**2+y**2):    {t_comb:.4f}s total, {t_comb/trials*1000:.3f}ms each")
