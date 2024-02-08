import math

class Vec2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def Magnitude(self):
        ## using pythagoras (a = sqrt(b^2 + c^2))
        return math.sqrt(self.x**2 + self.y**2)
    
    def Unit(self):
        return self / self.Magnitude

    def tuple(self):
        return (self.x, self.y)

    def minSquare(self):
        return Vec2(min(self.x, self.y), min(self.x, self.y))

    def maxSquare(self):
        return Vec2(max(self.x, self.y), max(self.x, self.y))

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)
        
    def __mul__(self, k):
        return Vec2(self.x * k, self.y * k)
    
    def __truediv__(self, k):
        return Vec2(self.x / k, self.y / k)

    def __repr__(self):
        return f"Vec2({self.x},{self.y})"
    
    def __str__(self):
        return f"Vec2({self.x},{self.y})"

    # Static methods for making code cleaner
    @staticmethod
    def xAxis():
        return Vec2(1, 0)
    
    @staticmethod
    def xyxis():
        return Vec2(0, 1)
    
    @staticmethod
    def one():
        return Vec2(1, 1)