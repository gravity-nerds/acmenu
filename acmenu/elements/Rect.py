import pygame

from elements.Instance import *
from libraries.Util import paramDefault

class Rect(Instance):
    def __init__(self, **kwargs):        
        super(Rect, self).__init__(**kwargs) # Run parent initialiser

        self.color = paramDefault(kwargs, "color", (100, 100, 100))
        self.border_radius = paramDefault(kwargs, "border_radius", 0)

    def __repr__(self):
        return f"Rect({self.id})"
    
    def render(self, screen):
        # TODO: apply contextual re-render optimisation
        self.rendered = pygame.Rect(self.getPos().tuple(), self.getSize().tuple())

        pygame.draw.rect(screen, self.color, self.rendered, border_radius=self.border_radius)
