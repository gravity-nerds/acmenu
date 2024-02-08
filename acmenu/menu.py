import pygame
import threading
import time

from libraries.Vec2 import *
from elements.Text import *
from elements.Rect import *

# Target Frames per seccond
TARGET_FPS = 60

# Menu Class (Holds UI Tree logic)
class Menu():

    # alive = process running
    alive = True

    # array of all instances to be rendered
    instances = []

    # map of which keys are held (used by isKeyHeld)
    keys = {}

    def __init__(self, acmenu):
        # If in dev mode, dont launch in fullscreen
        if acmenu.config["dev"]:
            self.screen = pygame.display.set_mode((1000, 500), pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    
    # Create all UI instances
    def mount(self):
        (width, height) = self.screen.get_size()

        self.root = Instance(size=UDim2(0, width, 0, height))


        frame = self.addInstance(Rect(
            UDim2(0.5, 0, 0.5, 0),
            UDim2(0.5, 0, 0.5, 0),
            Parent=self.root,
            border_radius=10
        ))
        self.addInstance(Text(UDim2(0.1, 0, 0.1, 0), text="Game1", color=(255, 255, 255), fontSize=100, Parent=frame))

        # create f3 text
        # this is rendered last seperately
        self.f3_text = Text(UDim2(), "", font = "assets/JetBrainsMono-SemiBold.ttf")

    def addInstance(self, instance):
        self.instances.append(instance)
        return instance

    # Check if key is held down
    def isKeyHeld(self, key):
        if not key in self.keys:
            return False # Key is not in the set (because key has not been pushed yet)
        else:
            return self.keys[key] # self.keys[key] = true or false

    def run(self):

        # Initalisise pygame
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("ACMENU")

        # Create all ui instances
        self.mount()
        
        # Main Loop
        while self.alive:
            # We keep track of the beginning of the frame so we can lock the framerate
            self._tick_begin = time.time()

            # Get the current width/height
            (width, height) = self.screen.get_size()

            # Update the root ui instance's size to resize children
            self.root.size = UDim2(0, width, 0, height)

            # Handle all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.alive = False

                if event.type == pygame.KEYDOWN:
                    self.keys[event.key] = True

                if event.type == pygame.KEYUP:
                    self.keys[event.key] = False

            # Sets background color and clears previous frame
            self.screen.fill((255, 255, 255))

            # Render every instance onto self.screen
            for instance in self.instances:
                instance.render(self.screen)

            # If holding debug key (F3) draw debug text
            if self.isKeyHeld(pygame.K_F3):
                # fps = (1 seccond) / (end time - start time + time for one frame)
                fps = 1/(time.time() - self._tick_begin + (1/TARGET_FPS))

                self.f3_text.content =  f"fps: {round(int(fps), 0)}/{round(TARGET_FPS, 0)} UIObjects: {len(self.instances)}"
                
                self.f3_text.render(self.screen)

            # force pygame to update the screen
            pygame.display.flip()
            
            # pause thread until ready for next frame
            next_frame_target = self._tick_begin + (1/TARGET_FPS)
            time.sleep(max(0, time.time() - next_frame_target))

        
        
        