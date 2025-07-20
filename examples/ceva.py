from olygeo import *
import sympy as sp

A = ProPoint.unfixed()
B = ProPoint.unfixed()
C = ProPoint.unfixed()

t, u, v = sp.symbols('t u v', real=True)

D = ProPoint((1 - t) * B.x + t * C.x,
             (1 - t) * B.y + t * C.y,
             1)
E = ProPoint((1 - u) * C.x + u * A.x,
             (1 - u) * C.y + u * A.y,
             1)
F = ProPoint((1 - v) * A.x + v * B.x,
             (1 - v) * A.y + v * B.y,
             1)

Geo.clear_conditions()
Geo.add_condition(Gt(t, 0)); Geo.add_condition(Lt(t, 1))
Geo.add_condition(Gt(u, 0)); Geo.add_condition(Lt(u, 1))
Geo.add_condition(Gt(v, 0)); Geo.add_condition(Lt(v, 1))
Geo.add_condition(sp.Eq((t / (1 - t)) *
                        (u / (1 - u)) *
                        (v / (1 - v)), 1))

AD = ProLine.through(A, D)
BE = ProLine.through(B, E)
CF = ProLine.through(C, F)

print(Geo.is_concurrent([AD, BE, CF]))