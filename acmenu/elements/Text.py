import pygame

from elements.Instance import *

class Text(Instance):
    def __init__(self, pos=UDim2(0, 0, 0, 0), text="", font=None, fontSize=25, color=(100, 100, 100), Parent=None):
        super(Text, self).__init__(pos, UDim2(0,0,0,0), Parent) # Run parent initialiser

        self.font = pygame.font.Font(font, fontSize)
        self.color = color
        self.content = text

        self._last_content = ""

    def __repr__(self):
        return f"Text({self.id} text={self.content})"
    
    def render(self, screen):
        # Only render the text if it has changed from last frames
        if self.content != self._last_content:
            self.rendered = self.font.render(self.content, True, self.color)

        # draw the rendered text onto the screen
        screen.blit(self.rendered, self.getPos().tuple())
