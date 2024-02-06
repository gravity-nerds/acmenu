import pygame
import threading

from libraries.Vec2 import *
from elements.Text import *

class Menu():

    alive = True
    f3_held = False

    instances = []
    clock = pygame.time.Clock()

    def __init__(self, acmenu):

        if acmenu.config["dev"]:
            self.screen = pygame.display.set_mode((1000, 500), pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def mount(self):
        (width, height) = self.screen.get_size()
        self.instances.append(Text(Vec2(width/2, height/2), text="Hello World!"))

    def run(self):

        pygame.init()
        self.mount()
        
        while self.alive:
            # Handle all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.alive = False

            self.screen.fill((255, 255, 255))

            for instance in self.instances:
                instance.render(self.screen)
            
            pygame.display.flip()
            
            # pause thread until ready for next frame
            self.clock.tick_busy_loop(60)

        
        
        