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
from control_mappings import LAYOUT_FRONT, getControlName

# Target Frames per seccond
TARGET_FPS = 30
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
    loaded_games = {}

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
            content = "Select a game:",
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
        self.game_array = []
        self.game_hint_texts = []
        for game_id, game in self.loaded_games.items():
            self.game_array.append(game)

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

            self.addInstance(Text(
                pos = UDim2(0.5, 0, 0.5, 0),
                anchor_point = Vec2(0.5, 0.5),
                content = "cover art",
                font_size = 16,
                color = (0, 0, 0),
                font = "assets/JetBrainsMono-SemiBold.ttf",
                parent = game_root
            ))

            hint_text = self.addInstance(Text(
                pos = UDim2(0.5, 0, 1, 0),
                anchor_point = Vec2(0.5, 0),
                content = f"Push {getControlName(LAYOUT_FRONT.P1_A)} to select",
                font_size = 16,
                color = (0, 0, 0),
                font = "assets/JetBrainsMono-SemiBold.ttf",
                parent = game_root
            ))

            self.game_hint_texts.append(hint_text)

            i += 1

        self.init_particles = []
        for _ in range(50):
            self.init_particles.append(self.addInstance(Circle(
                pos = UDim2(random.random(), 0, random.random(), 0),
                size = UDim2(0.01, 0, 0.01, 0),
                anchor_point = Vec2(1,1),
                parent = self.screen_init,
                color = (255, 255, 255),
                zindex = -1
            )))

        # -- "Play Game" screen --
        
        self.game_screen = Instance(
            pos = UDim2(0, 0, 2, 0),
            size = UDim2(1, 0, 1, 0),
            parent = self.root
        )

        self.addInstance(Rect(
            pos = UDim2(0.25, 0, 0.5, 0),
            size = UDim2(0.4, 0, 0.9, 0),
            anchor_point = Vec2(0.5, 0.5),

            border_radius = 10,

            color = (255, 255, 255),

            parent = self.game_screen
        ))

        self.game_title_text = self.addInstance(Text(
            pos = UDim2(0.1, 0, 0.1, 0),

            color = (0, 0, 0),

            content = "<GameName>",
            font_size = 50,

            parent = self.game_screen
        ))

        self.game_version_text = self.addInstance(Text(
            pos = UDim2(0.1, 0, 0.2, 0),

            color = (0, 0, 0),

            content = "<GameVersion>",
            font_size = 30,

            parent = self.game_screen
        ))

        self.addInstance(Text(
            pos = UDim2(0.1, 0, 0.3, 0),

            color = (0, 0, 0),

            content = f"Push {getControlName(LAYOUT_FRONT.P1_A)} and {getControlName(LAYOUT_FRONT.P1_C)} to start",
            font_size = 30,

            parent = self.game_screen
        ))

        self.loaded_games = self.acmenu.threads["game_manager"].games

        

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

    def loadGameInfo(self):
        loaded_game = self.game_array[self.focused_game_index]
        self.game_title_text.content = loaded_game["friendlyname"]
        self.game_version_text.content = loaded_game["version"]

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

        start_game_hold = False
        start_game_hold_begin = True
        
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

            self.game_screen.pos = UDim2(
                lerp(self.game_screen.pos.xs, self.targetUDim.xs, alpha),
                lerp(self.game_screen.pos.xo, self.targetUDim.xo, alpha),
                lerp(self.game_screen.pos.ys, self.targetUDim.ys + 2, alpha),
                lerp(self.game_screen.pos.yo, self.targetUDim.yo, alpha)
            )

            
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

            for hint_text in self.game_hint_texts:
                delta = abs(hint_text.getPos().x + 80 - width/2)
                c = clamp(-delta + 200, 0, 255)
                hint_text.color = (c, c, c)


            # Update target screen positions depending on key state
            if self.isKeyHeld(pygame.K_ESCAPE):
                self.targetUDim = UDim2(0, 0, 0, 0)
            elif any_key_event and self.screen_init.shouldRender():
                self.targetUDim = UDim2(0, 0, -1, 0)
            elif self.isKeyHeld(LAYOUT_FRONT.P1_A) and self.games_screen.pos.ys > -0.05:
                # Select Game to play
                self.loadGameInfo()
                self.targetUDim = UDim2(0, 0, -2, 0)
            elif self.isKeyHeld(LAYOUT_FRONT.P1_F) and self.game_screen.pos.ys > -0.05:
                self.targetUDim = UDim2(0, 0, -1, 0)


            if self.isKeyHeld(LAYOUT_FRONT.P1_A) and self.isKeyHeld(LAYOUT_FRONT.P1_C):
                if not start_game_hold:
                    start_game_hold = True
                    start_game_hold_begin = time.time()
            else:
                start_game_hold = False

            if start_game_hold_begin + 1 < time.time() and start_game_hold:
                start_game_hold = False

                self.acmenu.threads["game_manager"].start_game(self.game_array[self.focused_game_index].id)

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

        
        
        