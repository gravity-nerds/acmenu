import pygame
import threading

from libraries.Vec2 import *
from elements.Text import *

class Menu(threading.Thread):

    alive = True
    f3_held = False

    instances = []
    clock = pygame.time.Clock()

    def __init__(self, acmenu):
        threading.Thread.__init__(self)

        print(acmenu.config["dev"])
        if acmenu.config["dev"]:
            self.screen = pygame.display.set_mode((1000, 500), pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def mount(self):
        self.instances.append(Text(Vec2(), text="Hello World!"))

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
            
            self.clock.tick_busy_loop(60)

        
        
        