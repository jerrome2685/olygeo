import sympy as sp
from olygeo import *
import time

t0 = time.perf_counter()
A = ProPoint.unfixed()
B = ProPoint.unfixed()
C = ProPoint.unfixed()
t = sp.symbols('t', real=True)

M = ProPoint((A.x + B.x)/2, (A.y + B.y)/2, 1)

D = ProPoint(M.x + t*(B.x - M.x),
             M.y + t*(B.y - M.y),
             1)

I1 = ProTriangle(A, D, C).incenter()
I2 = ProTriangle(B, D, C).incenter()

angle_expr = Geo.angle(I1, M, I2)
Geo.clear_conditions()
Geo.add_condition(sp.Eq(angle_expr, sp.pi/2))

Geo.add_condition(t > 1e-5)     # t must be positive
Geo.add_condition(t < 1-1e-5)

CA = Geo.distance(C, A)
CB = Geo.distance(C, B)
diff = CA - CB

print("Under ∠I1MI2 = 90°, is CA = CB? →", Geo.is_zero(diff, log=True))

print(Geo.is_zero(Geo.distance(C, A) - Geo.distance(A, B)))
t1 = time.perf_counter()
print(f"{t1 - t0} seconds")

