import pygame
from Checkers.constants import WIDTH, HEIGHT, TILE, WHITE, RED
from Checkers.game import Game
from AI.alphaBeta import abControl
from AI.deepQLearning import deepQAgent
from AI.geneticAgent import GeneticAgent


FPS = 60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('ISTA 450 - Final Project - Francisco Figueroa')

def mouse_pos(pos):
    x,y = pos
    row = y // TILE
    col = x // TILE
    return int(row), int(col)

def console_out(curState, newState):
    if curState != newState:
        print(newState)
        #return newState()


def main():
    #deepLearningAgent = deepQAgent()
    genAgent = GeneticAgent(RED, 10)
    genAgent.train()
    print(genAgent.population)
    active = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)
    while active:
        currentState = game.cur_state()
        console_out(currentState, game.cur_state())
        clock.tick(FPS)

        if game.get_turn() == WHITE:
            game.white_agent_life_check()
            action, value = abControl(currentState, 2, game)
            if action is None:
                game.alphabeta_agent_concede()
                active = False
                break
            pygame.time.wait(1000)
            game.agent_move(action)

        if game.get_turn() == RED:
            action = genAgent.best_action(game.cur_state())
            pygame.time.wait(1000)
            game.agent_move(action)

        if game.winner() != None:
            #print(game.winner())
            active = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = mouse_pos(pos)
                game.select(row, col)
        
        console_out(currentState, game.cur_state())

        game.update()
    print(game.cur_state())
    print(game.winner())
    pygame.quit()

main()
