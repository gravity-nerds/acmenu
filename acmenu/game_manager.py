import pygame
import threading
import os

class GameManager(threading.Thread):

    current = None

    def __init__(self):
        threading.Thread.__init__(self)

    def load_game(path):
        if os.path.exists(path):
            print("YIPEEE")

    def run(self):
        pass
        
        
        