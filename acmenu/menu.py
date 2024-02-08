import pygame
import time
import random

from libraries.Vec2 import *
from elements.Text import *
from elements.Rect import *
from elements.Circle import *

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

        self.root = Instance(
            size = UDim2(0, width, 0, height)
        )

        # -- "Press Any Key" screen --

        self.screen_init = Instance(
            size = UDim2(1, 0, 1, 0),
            parent = self.root
        )

        self.addInstance(Text(
            pos = UDim2(0.5, 0, 0.5, 0),
            anchor_point = Vec2(0.5, 0.5),
            content = "Press Any Key",
            font_size = 50,
            font = "assets/JetBrainsMono-SemiBold.ttf",
            parent = self.screen_init
        ))

        self.init_particles = []
        self.particle_velocities = []
        for _ in range(100):
            self.particle_velocities.append(Vec2())
            self.init_particles.append(self.addInstance(Circle(
                pos = UDim2(random.random(), 0, random.random(), 0),
                size = UDim2(0.05, 0, 0.05, 0),
                anchor_point = Vec2(0.5, 0.5),
                parent = self.screen_init,
                color = (255, 255, 255),
                zindex = -1
            )))

        # -- Debug --

        self.f3_text = Text(
            pos = UDim2(),
            text = "",
            font = "assets/JetBrainsMono-SemiBold.ttf"
        )

        
        # Resort ZIndexes once (could do whenever an instance is added, however that would hurt)
        self.sortZIndex()

    # Add instance while also providing a reference
    def addInstance(self, instance):
        self.instances.append(instance)

        return instance

    def sortZIndex(self):
        self.instances.sort(key=lambda instance: instance.zindex)

    # Check if key is held down
    def isKeyHeld(self, key):
        if not key in self.keys:
            return False # Key is not in the set (because key has not been pushed yet)
        else:
            return self.keys[key] # self.keys[key] = true or false

    # Entrypoint
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

                # Update self.keys
                if event.type == pygame.KEYDOWN:
                    self.keys[event.key] = True

                if event.type == pygame.KEYUP:
                    self.keys[event.key] = False

            # Sets background color and clears previous frame
            self.screen.fill((0,0,0))

            # If visible, tick the press any key particle sim
            if self.screen_init.shouldRender():
                # yes this is O(n^2 + n), no i dont care

                
                for index, particle in enumerate(self.init_particles):
                    netVel = Vec2()
                    for other_particle in self.init_particles:
                        if other_particle != particle:
                            delta = other_particle.getPos() - particle.getPos()
                            magnitude = delta.Magnitude()
                            if magnitude < 100:
                                netVel += (delta / magnitude) * 10/(magnitude)
                    self.particle_velocities[index] = netVel

                for index, particle in enumerate(self.init_particles):
                    newVel = self.particle_velocities[index]

                    particle.pos = UDim2(particle.pos.xs + newVel.x / 1000, 0, particle.pos.ys + newVel.y / 1000, 0)

            # Render every instance onto self.screen
            for instance in self.instances:
                if instance.shouldRender():
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

        pygame.quit()
        exit()

        
        
        