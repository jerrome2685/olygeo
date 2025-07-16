from olygeo import *
from olygeo.geometry.triangle import ProTriangle

def test_euler_line():
    A = ProPoint.unfixed()
    B = ProPoint.unfixed()
    C = ProPoint.unfixed()

    tri = ProTriangle(A, B, C)
    H = tri.orthocenter()
    G = tri.centroid()
    O = tri.circumcenter()
    I = tri.incenter()

    Geo.clear_conditions()

    assert Geo.is_collinear([H, G, O]), "H, G, O should be collinear on the Euler line"
    assert not Geo.is_collinear([H, O, I])
