import pygame

from libraries.Vec2 import *
from libraries.UDim2 import *

id_counter = 0

class Instance:
    def __init__(self, pos=UDim2(0, 0, 0, 0), size=UDim2(1, 0, 1, 0), Parent=None):
        global id_counter 

        self.Parent = Parent or None
        self.pos = pos
        self.size = size

        # Set id and increment global counters
        self.id = (id_counter := id_counter + 1)

    def getPos(self):
        if self.Parent:
            return self.Parent.getPos() + self.pos.toVec2(self.Parent.getSize())
        else:
            return self.pos.toVec2(Vec2())
        
    def getSize(self):
        if self.Parent:
            return self.size.toVec2(self.Parent.getSize())
        else:
            return self.size.toVec2(Vec2())

    def __repr__(self):
        return f"Instance({self.id})"
    
    def render(self, screen):
        pass # do nothing
