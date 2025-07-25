from olygeo import *
import time

t0 = time.perf_counter()
a = ProPoint.unfixed()
b = ProPoint.unfixed()
c = ProPoint.unfixed()
d = ProLine.through(b, c).perpendicular_foot(a)

l = ProLine.unfixed()

t = ProTriangle(a, b, c)

h = t.orthocenter()
o = t.circumcenter()
n = (h + o) / 2

n_circle = ProCircle.from_center_point(n, d)

b1 = Geo.intersection(ProLine.through(a, b), l)
b2 = Geo.intersection(ProLine.through(b, h), l)
c1 = Geo.intersection(ProLine.through(c, a), l)
c2 = Geo.intersection(ProLine.through(c, h), l)

w1 = ProCircle.through(b, b1, b2)
w2 = ProCircle.through(c, c1, c2)
o1 = w1.center()
o2 = w2.center()

l2 = w1.radial_axis(w2)
l3 = ProLine.through(o1, o2)

x = Geo.intersection(l2, l3)
print(n_circle.contains(x))
print(n_circle.contains(o1))

t1 = time.perf_counter()

print(f"{t1 - t0} seconds")

