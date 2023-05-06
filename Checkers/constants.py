import pygame 

# pygame window proportions
WIDTH = 500
HEIGHT = 500

# checkers board rows and columns
ROWS = 5
COLS = 5

# size of each tile in checkers board
TILE = WIDTH/COLS

#RGB vals
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)
SHADOW = (36, 32, 24)


#Sprites
CROWN = pygame.transform.scale(pygame.image.load('Assets/crown.png'), (90, 70))

