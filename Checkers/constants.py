import pygame 

# pygame window proportions
WIDTH = 600
HEIGHT = 600
    #training window
tWID = 400
tHGT = 400

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


#genetic constants
POPULATION_SIZE = 100
MUTATION_RATE = 0.1
NUM_GAMES = 10
TOURN_SIZE = 10

#Sprites
CROWN = pygame.transform.scale(pygame.image.load('Assets/crown.png'), (90, 70))

