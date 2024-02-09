import pygame

# both players at either end of the table
class LAYOUT_GAME:
    P1_UP = pygame.K_w
    P1_LEFT = pygame.K_a
    P1_DOWN = pygame.K_s
    P1_RIGHT = pygame.K_d

    P2_UP = pygame.K_i
    P2_LEFT = pygame.K_j
    P2_DOWN = pygame.K_k
    P2_RIGHT = pygame.K_l

# both players standing at front of table
class LAYOUT_FRONT:
    P1_UP = pygame.K_d
    P1_LEFT = pygame.K_w
    P1_DOWN = pygame.K_a
    P1_RIGHT = pygame.K_s

    P2_UP = pygame.K_l
    P2_LEFT = pygame.K_i
    P2_DOWN = pygame.K_j
    P2_RIGHT = pygame.K_k

# both players at P1 end
class LAYOUT_P1:
    P1_UP = pygame.K_w
    P1_LEFT = pygame.K_a
    P1_DOWN = pygame.K_s
    P1_RIGHT = pygame.K_d

    P2_UP = pygame.K_k
    P2_LEFT = pygame.K_l
    P2_DOWN = pygame.K_i
    P2_RIGHT = pygame.K_j

# both players at P2 end
class LAYOUT_P2:
    P1_UP = pygame.K_s
    P1_LEFT = pygame.K_d
    P1_DOWN = pygame.K_w
    P1_RIGHT = pygame.K_a

    P2_UP = pygame.K_i
    P2_LEFT = pygame.K_j
    P2_DOWN = pygame.K_k
    P2_RIGHT = pygame.K_l