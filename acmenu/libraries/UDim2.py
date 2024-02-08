from libraries.Vec2 import *

class UDim2:
    def __init__(self, xs=0, xo=0, ys=0, yo=0):
        self.xs = xs
        self.xo = xo
        self.ys = ys
        self.yo = yo
    
    def toVec2(self, other):
        return Vec2(other.x * self.xs + self.xo, other.y * self.ys + self.yo)
    
    def tuple(self, other):
        return (other.x * self.xs + self.xo, other.y * self.ys + self.yo)

    def __repr__(self):
        return f"Udim2({self.xs},{self.xo},{self.ys},{self.yo})"
    
    def __str__(self):
        return f"Udim2({self.xs},{self.xo},{self.ys},{self.yo})"
