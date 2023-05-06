import pygame
from Checkers.constants import WIDTH, HEIGHT, TILE, WHITE, RED
from Checkers.game import Game
from AI.alphaBeta import abControl


FPS = 60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('ISTA 450 - Final Project - Francisco Figueroa')

def mouse_pos(pos):
    x,y = pos
    row = y // TILE
    col = x // TILE
    return int(row), int(col)


def main():
    active = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)
    while active:
        clock.tick(FPS)

        if game.get_turn() == WHITE:
            action, value = abControl(game.cur_state(), 2, game)
            pygame.time.wait(1000)
            game.agent_move(action)


        # if game.get_turn() == RED:
        #     pygame.time.wait(2000)
        #     action, value = abControl(game.cur_state(), 2, game, color=RED)
        #     game.agent_move(action)
            

        #print(game.cur_state().winner())

        if game.winner() != None:
            print(game.winner())
            active = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = mouse_pos(pos)
                game.select(row, col)
                print(str(game.board))

        game.update()
    
    pygame.quit()

main()
