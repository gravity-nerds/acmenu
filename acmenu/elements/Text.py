import pygame

from elements.Instance import *
from libraries.Util import paramDefault

class Text(Instance):
    def __init__(self, **kwargs):
        super(Text, self).__init__(size=UDim2(), **kwargs) # Run parent initialiser

        self.font = pygame.font.Font(
            paramDefault(kwargs, "font", None),
            paramDefault(kwargs, "font_size", 20)
        )

        self.color = paramDefault(kwargs, "color", (100, 100, 100))
        self.content = paramDefault(kwargs, "content", "")

        self._last_content = None

    def __repr__(self):
        return f"Text({self.id} text={self.content})"
    
    def render(self, screen):
        # Only render the text if it has changed from last frames
        if self.content != self._last_content:
            self.rendered = self.font.render(self.content, True, self.color)
            
            # Adjust internal size so anchor point gets computed correctly
            width, height = self.rendered.get_rect().width, self.rendered.get_rect().height
            self.size = UDim2(0, width, 0, height)

        # draw the rendered text onto the screen
        screen.blit(self.rendered, self.getPos().tuple())
