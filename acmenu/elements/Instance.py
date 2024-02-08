import pygame

from libraries.Vec2 import *
from libraries.UDim2 import *
from libraries.Util import paramDefault

id_counter = 0

class Instance:
    def __init__(self, **kwargs):
        global id_counter 

        self.parent = paramDefault(kwargs, "parent", None)
        self.pos = paramDefault(kwargs, "pos", UDim2(0, 0, 0, 0))
        self.size = paramDefault(kwargs, "size", UDim2(1, 0, 1, 0))

        self.anchor_point = paramDefault(kwargs, "anchor_point", Vec2())
        self.visible = paramDefault(kwargs, "visible", True)

        # Set id and increment global counters
        self.id = (id_counter := id_counter + 1)

    def getPos(self):
        if self.parent:
            self_offset = self.pos.toVec2(self.parent.getSize())
            self_size = self.getSize()

            self_anchor_offset = Vec2(
                self_size.x * self.anchor_point.x,
                self_size.y * self.anchor_point.y
            )

            return self.parent.getPos() + self_offset - self_anchor_offset
        else:
            return self.pos.toVec2(Vec2())
        
    def getSize(self):
        if self.parent:
            return self.size.toVec2(self.parent.getSize())
        else:
            return self.size.toVec2(Vec2())

    def shouldRender(self):
        return self.parent.shouldRender() and self.visible

    def __repr__(self):
        return f"Instance({self.id})"
    
    def render(self, screen):
        pass # do nothing
