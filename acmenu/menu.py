import pygame
import threading

class Menu(threading.Thread):
    def __init__(self, acmenu):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN if acmenu.config["dev"] else None)
        
        