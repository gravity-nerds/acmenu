import pygame

x1 = 20
y1 = 20
x2 = 1000
y2 = 500

my_font = None

def tick(screen):
    global my_font

    text_surface = my_font.render(f'x1,y1: ({x1},{y1}); x2,y2: ({x2},{y2}); w,h: ({x2-x1},{y2-y1})', False, (0, 0, 0))

    screen.fill((255, 0, 0)) 
    pygame.draw.rect(screen,(0, 255, 0),(x1, y1, x2-x1, y2-y1))
    screen.blit(text_surface, (x1, y1))
    
    pygame.display.flip()


def main():
    global x1
    global x2
    global y1
    global y2
    global my_font

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 
    running = True

    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', 30)

    pygame.key.set_repeat(200, 0)

    shift = False

    while running:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    shift = False

            if event.type == pygame.KEYDOWN:
                print(f'x1,y1: ({x1},{y1}); x2,y2: ({x2},{y2}); w,h: ({x2-x1},{y2-y1})')

                inc = 1

                if shift:
                    inc = 10

                if event.key == pygame.K_LSHIFT:
                    shift = True

                if event.key == pygame.K_a:
                    y1 = y1 - inc

                if event.key == pygame.K_d:
                    y1 = y1 + inc

                if event.key == pygame.K_s:
                    x1 = x1 - inc

                if event.key == pygame.K_w:
                    x1 = x1 + inc

                if event.key == pygame.K_l:
                    y2 = y2 - inc

                if event.key == pygame.K_j:
                    y2 = y2 + inc

                if event.key == pygame.K_i:
                    x2 = x2 - inc

                if event.key == pygame.K_k:
                    x2 = x2 + inc
        
        tick(screen)


if __name__ == "__main__":
    main()