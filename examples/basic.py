from olygeo import *

A = ProPoint(0,0,1)
B = ProPoint(1,0,1)
C = ProPoint(0,1,1)
D = ProPoint.unfixed()
tri = ProTriangle(A, B, C)
I = tri.incenter()

print(I)
print(Relation.eq(A, D))
print(Relation.eq(A, B))