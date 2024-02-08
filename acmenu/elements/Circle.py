import pygame

from elements.Instance import *
from libraries.Util import paramDefault

class Circle(Instance):
    def __init__(self, **kwargs):        
        super(Circle, self).__init__(**kwargs) # Run parent initialiser

        self.color = paramDefault(kwargs, "color", (100, 100, 100))

    def __repr__(self):
        return f"Rect({self.id})"
    
    def getSize(self):
        if self.parent:
            return self.size.toVec2(self.parent.getSize()).minSquare()
        else:
            return self.size.toVec2(Vec2()).minSquare()
    
    def render(self, screen):
        root_pos = self.getPos()
        root_size = self.getSize()

        centered_pos = root_pos + (root_size * 0.5)

        pygame.draw.circle(screen, self.color, centered_pos.tuple(), min(root_size.x, root_size.y)/2)
