import pygame
import time
from control_mappings import LAYOUT_GAME

p1 = 30
p2 = 30

bx = 50
by = 50
bvx = 1
bvy = 1

gaming = True

def tick(screen):
    global p1
    global p2
    global bx
    global bvx
    global by
    global bvy
    global gaming

    keys = pygame.key.get_pressed()
    (w, h) = screen.get_size()


    if keys[LAYOUT_GAME.P1_RIGHT] and gaming:
        p1 += 1
        if p1 > h:
            p1 = h
    if keys[LAYOUT_GAME.P1_LEFT] and gaming:
        p1 -= 1
        if p1 < 0:
            p1 = 0

    if keys[LAYOUT_GAME.P2_LEFT] and gaming:
        p2 += 1
        if p2 > h:
            p2 = h
    if keys[LAYOUT_GAME.P2_RIGHT] and gaming:
        p2 -= 1
        if p2 < 0:
            p2 = 0

    if gaming:
        bx += bvx
        by += bvy

    if by < 0:
        bvy = 1
    if by > h:
        bvy = -1

    if bx < 0 or bx > w:
        gaming = False

        time.sleep(1)
        p1 = h//2
        p2 = h//2

        bx = w//2
        by = h//2

        gaming = True

    if bx < 150 and abs(by-p1) < 100:
        bvx = 1

    if bx > w - 150  and abs(by-p2) < 100:
        bvx = -1

    screen.fill((0, 0, 0))

    pygame.draw.circle(screen, (255, 255, 255), (bx-10, by-10), 20)
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((100, p1-100), (10,200)))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((w-120, p2-100), (10,200)))

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

    screen = pygame.display.set_mode((1000, 500), pygame.FULLSCREEN) 
    running = True

    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', 30)

    (w, h) = screen.get_size()

    bx = w//2
    by = h//2

    while running:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False

        tick(screen)


if __name__ == "__main__":
    main()