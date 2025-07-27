from olygeo import *

def test_triangle_incenter():
    A = ProPoint(0,0,1)
    B = ProPoint(1,0,1)
    C = ProPoint(0,1,1)
    tri = ProTriangle(A, B, C)
    I = tri.incenter()
    assert Geo.is_zero(I.x - I.y)
