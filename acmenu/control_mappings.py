import pygame

NAMES = {
    pygame.K_w: "STICK",
    pygame.K_a: "STICK",
    pygame.K_s: "STICK",
    pygame.K_d: "STICK",

    pygame.K_e: "YELLOW",
    pygame.K_r: "WHITE",
    pygame.K_f: "BLACK",
    pygame.K_v: "GREEN",
    pygame.K_c: "RED",
    pygame.K_x: "BLUE",

    pygame.K_i: "STICK",
    pygame.K_j: "STICK",
    pygame.K_k: "STICK",
    pygame.K_l: "STICK",

    pygame.K_u: "YELLOW",
    pygame.K_y: "WHITE",
    pygame.K_h: "BLACK",
    pygame.K_b: "GREEN",
    pygame.K_n: "RED",
    pygame.K_m: "BLUE",

    pygame.K_t: "SIDE",
    pygame.K_t: "SIDE",
}

def getControlName(key):
    if key in NAMES:
        return NAMES[key]
    return "UNBOUND"

# both players at either end of the table
class LAYOUT_GAME:
    P1_UP = pygame.K_w
    P1_LEFT = pygame.K_a
    P1_DOWN = pygame.K_s
    P1_RIGHT = pygame.K_d

    P1_A = pygame.K_e
    P1_B = pygame.K_r
    P1_C = pygame.K_f
    P1_D = pygame.K_v
    P1_E = pygame.K_c
    P1_F = pygame.K_x

    P2_UP = pygame.K_i
    P2_LEFT = pygame.K_j
    P2_DOWN = pygame.K_k
    P2_RIGHT = pygame.K_l

    P2_A = pygame.K_u
    P2_B = pygame.K_y
    P2_C = pygame.K_h
    P2_D = pygame.K_b
    P2_E = pygame.K_n
    P2_F = pygame.K_m

# both players standing at front of table
class LAYOUT_FRONT:
    P1_UP = pygame.K_d
    P1_LEFT = pygame.K_s
    P1_DOWN = pygame.K_a
    P1_RIGHT = pygame.K_w

    P1_A = pygame.K_e
    P1_B = pygame.K_r
    P1_C = pygame.K_f
    P1_D = pygame.K_v
    P1_E = pygame.K_c
    P1_F = pygame.K_x

    P2_UP = pygame.K_l
    P2_LEFT = pygame.K_i
    P2_DOWN = pygame.K_j
    P2_RIGHT = pygame.K_k

    P2_A = pygame.K_u
    P2_B = pygame.K_y
    P2_C = pygame.K_h
    P2_D = pygame.K_b
    P2_E = pygame.K_n
    P2_F = pygame.K_m

# both players at P1 end
class LAYOUT_P1:
    P1_UP = pygame.K_w
    P1_LEFT = pygame.K_a
    P1_DOWN = pygame.K_s
    P1_RIGHT = pygame.K_d

    P1_A = pygame.K_e
    P1_B = pygame.K_r
    P1_C = pygame.K_f
    P1_D = pygame.K_v
    P1_E = pygame.K_c
    P1_F = pygame.K_x

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

    P2_A = pygame.K_u
    P2_B = pygame.K_y
    P2_C = pygame.K_h
    P2_D = pygame.K_b
    P2_E = pygame.K_n
    P2_F = pygame.K_m