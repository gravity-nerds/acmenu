import pygame

from libraries.Vec2 import *

id_counter = 0

class Instance:
    def __init__(self, pos):
        global id_counter 

        self.pos = pos or Vec2()

        # Set id and increment global counters
        self.id = (id_counter := id_counter + 1)

    def __repr__(self):
        return f"Instance({self.id})"
    
    def render(self, screen):
        pass
