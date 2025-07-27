from olygeo import *


a = ProPoint.unfixed()
b = ProPoint.unfixed()
c = ProPoint.unfixed()
m = (b + c) * 0.5


def not_b(P):
    return Relation.ne((P.x * b.z - b.x * P.z), 0) | Relation.ne((P.y * b.z - b.y * P.z), 0)

p = ProLine.through(a, m).perpendicular_foot(c)
circ = ProCircle.through(a, b, p)
pts = Geo.intersection(circ, ProLine.through(b, c))
assert len(pts) == 2
q = pts.choose(not_b)

n = (a + q) / 2
# n = (a + pts[0] + pts[1] - b) / 2
print(Geo.is_zero(Geo.distance(n, b) - Geo.distance(n, c)))



