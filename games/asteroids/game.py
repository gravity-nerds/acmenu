import pygame
import time
from control_mappings import LAYOUT_GAME
import math
import random

alive = True

px, py = 100, 100
pvx, pvy = 0, 0
pvr = 0
pr = 0

# x, y, r, vx ,vy, vr, seed
asteroids = []



def tick(screen):
    global px, py
    global pvx, pvy
    global pr, pvr

    keys = pygame.key.get_pressed()
    (w, h) = screen.get_size()
    if keys[pygame.K_w]:
        pvx += math.cos(pr) * 0.5
        pvy += math.sin(pr) * 0.5
    if keys[pygame.K_a]:
        pvr -= 0.01
    if keys[pygame.K_d]:
        pvr += 0.01

    pr += pvr
    px += pvx
    py += pvy

    pvr *= 0.9
    pvx *= 0.99
    pvy *= 0.99

    if px < 0:
        px = w
    if px > w:
        px = 0
    if py < 0:
        py = h
    if py > h:
        py = 0


    screen.fill((0, 0, 0))


    SIZE = 50
    for index, asteroid in enumerate(asteroids):
        POINTS = 10
        random.seed(asteroid[6])
        rng = [random.random() for _ in range(POINTS)]
        rng.append(rng[0])

        asteroid[0] += asteroid[3] # TODO: FIX
        asteroid[1] += asteroid[4]

        for i in range(POINTS):
            a1 = asteroid[2] + i * ((math.pi * 2) / POINTS)
            a2 = asteroid[2] + (i + 1) * ((math.pi * 2) / POINTS)

            pygame.draw.line(
                screen,
                (255, 255, 255),
                (asteroid[0] + math.cos(a1) * SIZE * rng[i], asteroid[1] + math.sin(a1) * SIZE * rng[i]),
                (asteroid[0] + math.cos(a2) * SIZE * rng[i + 1], asteroid[1] + math.sin(a2) * SIZE * rng[i + 1]),
                2
            )

    SIZE = 25

    pygame.draw.line(screen, (255, 255, 255), (px + math.cos(pr) * SIZE, py + math.sin(pr) * SIZE), (px + math.cos(pr + 2.5) * SIZE, py + math.sin(pr + 2.5) * SIZE), 2)
    pygame.draw.line(screen, (255, 255, 255), (px + math.cos(pr) * SIZE, py + math.sin(pr) * SIZE), (px + math.cos(pr - 2.5) * SIZE, py + math.sin(pr - 2.5) * SIZE), 2)
    pygame.draw.line(screen, (255, 255, 255), (px + math.cos(pr + math.pi) * SIZE / 2, py + math.sin(pr + math.pi) * SIZE / 2), (px + math.cos(pr + 2.5) * SIZE, py + math.sin(pr + 2.5) * SIZE), 2)
    pygame.draw.line(screen, (255, 255, 255), (px + math.cos(pr + math.pi) * SIZE / 2, py + math.sin(pr + math.pi) * SIZE / 2), (px + math.cos(pr - 2.5) * SIZE, py + math.sin(pr - 2.5) * SIZE), 2)

    pygame.display.flip()


def main():
    global x1
    global x2
    global bx
    global by
    global y1
    global y2
    global my_font
    global gaming

    screen = pygame.display.set_mode((1000, 500)) 
    running = True

    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', 30)

    (w, h) = screen.get_size()

    bx = w//2
    by = h//2

    for i in range(100):
        asteroids.append([bx + random.randint(-500, 500), by + random.randint(-500, 500),  2 * (random.random() - 0.5),  2 * (random.random() - 0.5),  2 * (random.random() - 0.5),  2 * (random.random() - 0.5), random.randint(-500, 500)])

    while running:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False
        startime = time.time();
        tick(screen)

        time.sleep( max(0, (1/60) - (time.time() - startime)))


if __name__ == "__main__":
    main()