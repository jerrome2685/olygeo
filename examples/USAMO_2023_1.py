from olygeo import *
from sympy.core.relational import Ne


a = ProPoint.unfixed()
b = ProPoint.unfixed()
c = ProPoint.unfixed()
m = (b + c) * 0.5

print(b.x)

def not_B(P):
    return Ne((P.x * b.z - b.x * P.z), 0) | Ne((P.y * b.z - b.y * P.z), 0)

p = c.perpendicular_foot(ProLine.through(a, m))
circ = ProCircle.through(a, b, p)
pts = Geo.intersection(circ, ProLine.through(b, c))
assert len(pts) == 2
q = pts.choose(not_B)

n = (a + q) / 2
# n = (a + pts[0] + pts[1] - b) / 2
print(Geo.is_zero(Geo.distance(n, b).expr - Geo.distance(n, c).expr))



