import time
import random
import os

# make pygame shut
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from libraries.Vec2 import *
from elements.Text import *
from elements.Rect import *
from elements.Circle import *
from libraries.Util import lerp, clamp
from control_mappings import LAYOUT_FRONT

# Target Frames per seccond
TARGET_FPS = 60
GAMES_PER_SCREEN = 4

# Menu Class (Holds UI Tree logic)
class Menu():

    # alive = process running
    alive = True

    # array of all instances to be rendered
    instances = []

    # Keep track of current frame number
    frame_counter = 0

    # map of which keys are held (used by isKeyHeld)
    keys = {}

    # target position for the menu shifting system
    targetUDim = UDim2()

    # games
    focused_game_index = 0
    loaded_games = ["Game1", "Game2", "Game3", "Game4", "Game5", "Game6", "Game7", "Game8", "Game9", "Game10"]

    def __init__(self, acmenu):

        self.acmenu = acmenu

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

        # -- "Games" screen --

        self.loaded_games = self.acmenu.threads["game_manager"].games

        self.games_screen = Instance(
            pos = UDim2(0, 0, 1, 0),
            size = UDim2(1, 0, 1, 0),
            parent = self.root
        )

        self.addInstance(Text(
            pos = UDim2(0.5, 0, 0.1, 0),
            anchor_point = Vec2(0.5, 0.5),
            content = "This is the games screen",
            font_size = 20,
            font = "assets/JetBrainsMono-SemiBold.ttf",
            parent = self.games_screen
        ))
        

        self.games_screen_carousel_udim_target = UDim2(0.1, 0, 0.15, 0)
        self.games_screen_carousel = self.addInstance(Instance(
            pos = UDim2(0.5, 0, 0.15, 0),
            anchor_point = Vec2(0.5, 0),
            size = UDim2(len(self.loaded_games) * 1/GAMES_PER_SCREEN, 0, 0.7, 0),
            parent = self.games_screen
        ))

        i = 0
        for game_id, game in self.loaded_games.items():
            game_root = self.addInstance(Rect(
                pos = UDim2(1/len(self.loaded_games)*i, 0, 0, 0),
                anchor_point = Vec2(0.5, 0),
                size = UDim2(1/len(self.loaded_games), -10, 1, 0),
                color = (255, 255, 255),
                parent = self.games_screen_carousel
            ))

            self.addInstance(Text(
                pos = UDim2(0.5, 0, 0.1, 0),
                anchor_point = Vec2(0.5, 0.5),
                content = game["friendlyname"],
                font_size = 25,
                color = (0, 0, 0),
                font = "assets/JetBrainsMono-SemiBold.ttf",
                parent = game_root
            ))

            i += 1

        self.init_particles = []
        for _ in range(50):
            self.init_particles.append(self.addInstance(Circle(
                pos = UDim2(random.random(), 0, random.random(), 0),
                size = UDim2(0.01, 0, 0.01, 0),
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
            any_key_event = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.alive = False

                # Update self.keys
                if event.type == pygame.KEYDOWN:
                    any_key_event = True
                    self.keys[event.key] = True

                    if event.key == LAYOUT_FRONT.P1_RIGHT:
                        self.focused_game_index = clamp(self.focused_game_index + 1, 0, len(self.loaded_games)-1)
                    if event.key == LAYOUT_FRONT.P1_LEFT:
                        self.focused_game_index = clamp(self.focused_game_index - 1, 0, len(self.loaded_games)-1)


                if event.type == pygame.KEYUP:
                    self.keys[event.key] = False

            # Sets background color and clears previous frame
            self.screen.fill((0,0,0))

            # If visible, tick the press any key particle sim
            if self.screen_init.shouldRender():
                for index, particle in enumerate(self.init_particles):
                    calculated_position = UDim2(
                        (math.cos(self.frame_counter / (math.pi * 500) + index * math.pi/25)/3 + 0.5) + math.cos(self.frame_counter / 1000 + index * 10) / 10,
                        0,
                        (math.sin(self.frame_counter / (math.pi * 500) + index * math.pi/25)/3 + 0.5) + math.sin(self.frame_counter / 1000 + index * 10) / 10,
                        0
                    )
                    particle.pos = calculated_position
                    px_pos = particle.getPos()

                    for other_particle in self.init_particles[index-4:index+4]:
                        other_particle_px_pos = other_particle.getPos()

                        m = (px_pos - other_particle_px_pos).Magnitude()
                        if m < 50:
                            pygame.draw.line(self.screen, (math.floor(255 * m/50), math.floor(255 * m/50), math.floor(255 * m/50)), px_pos.tuple(), other_particle_px_pos.tuple())


            # Update screen positions utlising lerp
            # TODO: fix fps increasing after unloading main menu making the transition abruptly change speed
            alpha = 0.02

            self.screen_init.pos = UDim2(
                lerp(self.screen_init.pos.xs, self.targetUDim.xs, alpha),
                lerp(self.screen_init.pos.xo, self.targetUDim.xo, alpha),
                lerp(self.screen_init.pos.ys, self.targetUDim.ys, alpha),
                lerp(self.screen_init.pos.yo, self.targetUDim.yo, alpha)
            )
            self.screen_init.visible = self.screen_init.pos.ys > -0.95
    
            self.games_screen.pos = UDim2(
                lerp(self.games_screen.pos.xs, self.targetUDim.xs, alpha),
                lerp(self.games_screen.pos.xo, self.targetUDim.xo, alpha),
                lerp(self.games_screen.pos.ys, self.targetUDim.ys + 1, alpha),
                lerp(self.games_screen.pos.yo, self.targetUDim.yo, alpha)
            )
            self.games_screen.visible = self.games_screen.pos.ys > -0.95

            
            init_offset = (len(self.loaded_games))/(GAMES_PER_SCREEN)

            if len(self.loaded_games) % 2 == 1:
                init_offset -= (len(self.loaded_games)//2)/GAMES_PER_SCREEN
                init_offset += 1.5/GAMES_PER_SCREEN

            self.games_screen_carousel_udim_target = UDim2(
                init_offset - self.focused_game_index * 1/GAMES_PER_SCREEN,
                0,
                0.15,
                0
            )

            self.games_screen_carousel.pos = UDim2(
                lerp(self.games_screen_carousel.pos.xs, self.games_screen_carousel_udim_target.xs, 0.01),
                self.games_screen_carousel_udim_target.xo,
                self.games_screen_carousel_udim_target.ys,
                self.games_screen_carousel_udim_target.yo
            )

            # Update target screen positions depending on key state
            if self.isKeyHeld(pygame.K_ESCAPE):
                self.targetUDim = UDim2(0, 0, 0, 0)
            elif any_key_event and self.screen_init.shouldRender():
                self.targetUDim = UDim2(0, 0, -1, 0)

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
            self.frame_counter += 1
            
            # pause thread until ready for next frame
            next_frame_target = self._tick_begin + (1/TARGET_FPS)
            time.sleep(max(0, time.time() - next_frame_target))

        # Nuke the process after the window is closed
        pygame.quit()
        exit()

        
        
        