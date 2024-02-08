import pygame

from elements.Instance import *

class Rect(Instance):
    def __init__(self, pos=UDim2(0, 0, 0, 0), size=UDim2(1, 0, 1, 0), color=(100, 100, 100), Parent=None, border_radius=0):
        super(Rect, self).__init__(pos, size, Parent) # Run parent initialiser

        self.color = color
        self.border_radius = border_radius

    def __repr__(self):
        return f"Rect({self.id})"
    
    def render(self, screen):
        # TODO: apply contextual re-render optimisation
        self.rendered = pygame.Rect(self.getPos().tuple(), self.getSize().tuple())

        pygame.draw.rect(screen, self.color, self.rendered, border_radius=self.border_radius)
