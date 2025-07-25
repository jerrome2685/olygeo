# class ProSegment(ProLine):
#     def __init__(self, A: ProPoint, B: ProPoint):
#         L = ProLine.through(A, B)
#         super().__init__(L.a, L.b, L.c)
#         self.A = A
#         self.B = B
#
#     @classmethod
#     def unfixed(cls):
#         return cls(ProPoint.unfixed(), ProPoint.unfixed())
#
#     def contains(self, P: ProPoint, log=False):
#         on_line = super().contains(P, log=log)
#         u_x = P.x * self.A.z - self.A.x * P.z
#         u_y = P.y * self.A.z - self.A.y * P.z
#         v_x = P.x * self.B.z - self.B.x * P.z
#         v_y = P.y * self.B.z - self.B.y * P.z
#         return on_line and Geo.is_non_negative(- (u_x*v_x + u_y*v_y), log=log)
#
#     def length(self):
#         return Geo.distance(self.A, self.B)
#
#     def __eq__(self, other):
#         if not isinstance(other, ProSegment):
#             return False
#         return ((self.A == other.A and self.B == other.B)
#                 or (self.A == other.B and self.B == other.A))
#
#     def __hash__(self):
#         pts = sorted(
#             [(self.A.x, self.A.y, self.A.z), (self.B.x, self.B.y, self.B.z)]
#         )
#         return hash(tuple(pts))
#
#     def __repr__(self):
#         return f"ProSegment({self.A}, {self.B})"
#
#     def is_eq(self, other, log=False):
#         return ((self.A.is_eq(other.A, log=log) and self.B.is_eq(other.B, log=log))
#                 or (self.A.is_eq(other.B, log=log) and self.B.is_eq(other.A, log=log)))
#
#     def is_ne(self, other, log=False):
#         return not self.is_eq(other, log=log)