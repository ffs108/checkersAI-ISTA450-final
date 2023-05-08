import random
import pygame
import copy
import numpy as np
from Checkers.game import Game
from Checkers.board import Board, Piece
from Checkers.constants import POPULATION_SIZE, MUTATION_RATE, NUM_GAMES, TOURN_SIZE, RED, WHITE, tWID, tHGT
from AI.alphaBeta import abControl

WINDOW = pygame.display.set_mode((tWID, tHGT))


class GeneticAgent:
    def __init__(self, color, depth):
        self.pop_size = POPULATION_SIZE
        self.mutation_rate = MUTATION_RATE
        self.color = color
        self.depth = depth
        self.generation = 0
        self.population = [Individual([random.random()]) for i in range(self.pop_size)]
        self.cur_Indiv = random.choice(self.population)
    
    def best_action(self, state):
        features = state.get_features()
        values = np.dot(self.cur_Indiv.weights, features)
        actions = getSuccessors(state, self.color)
        best_action = None
        best_value = float('-inf')
        for action in actions:
            if values > best_value:
                best_action = action
                best_value = values
        return best_action

    def _generate_policy(self, board):
        policy = []
        for i in range(self.depth):
            moves = getSuccessors(board, self.color)
            if not moves:
                break
            policy.append(random.choice(moves))
        return policy
    
    def _fitness(self):
        wins = 0
        games = 0
        for i in range(NUM_GAMES):
            game = Game(WINDOW)
            active = True
            while active:
                currentState = game.cur_state()
                if game.get_turn() == WHITE:
                    game.white_agent_life_check()
                    action, value = abControl(currentState, 2, game)
                    if action is None:
                        game.alphabeta_agent_concede()
                        active = False
                        break
                    game.agent_move(action)
                if game.get_turn() == RED:
                    action = self.best_action(currentState)
                    game.agent_move(action)
            if game.winner() == 'The winner is: RED':
                wins += 1
            games += 1
        if self.generation < NUM_GAMES : self.train()
        return wins/games

    def _breed(self, parent1, parent2):
        pass

    def _mutate(self, policy):
        pass

    def train(self):
        self.generation += 1
        for indiv in self.population:
            indiv.update_fit(self._fitness())
        new_pop = []
        for i in range(self.pop_size):
            parent1 = self.gauntlet_select()
            parent2 = self.gauntlet_select()
            child = parent1.crossover(parent2)
            child = child.mutate()
            new_pop.append(child)
        self.population = new_pop
        #self.population = self.population.sort(key=lambda x: x.weights)
        self.cur_Indiv = self.population[0]
    
    def gauntlet_select(self):
        participants = random.sample(self.population, TOURN_SIZE)
        winner = max(participants, key=lambda x: x.weights)
        return winner
    
    def reassess_fit(self, fitness_measure):
        for indiv in self.population:
            indiv.fitness = indiv.weights[0] * fitness_measure


class Individual:
    def __init__(self, weights):
        self.weights = weights
        self.fitness = None
        
    def __repr__(self):
        return "{Individual: " + self.weights + "; Fitness: " + self.fitness + "}"
    
    def update_fit(self, newfit):
        self.fitness = newfit
    
    def crossover(self, other):
        # perform crossover between self and other
        # return a new Individual object with the resulting genetic information
        weights = []
        for i in range(len(self.weights)):
            if random.random() < 0.5:
                weights.append(self.weights[i])
            else:
                weights.append(other.weights[i])
        return Individual(weights)
    
    def mutate(self):
        # perform mutation on self
        # return a new Individual object with the resulting genetic information
        weights = copy.deepcopy(self.weights)
        for i in range(len(weights)):
            if random.random() < MUTATION_RATE:
                weights[i] += random.uniform(-0.1, 0.1)
        return Individual(weights)



def getSuccessors(currentState, color):
    successors = list()
    for piece in currentState.get_all_pieces_of_color(color):
        legal_moves = currentState.valid_moves(piece)
        #print(legal_moves)
        for move in legal_moves:
            #print(move)
            temp = copy.deepcopy(currentState) #this is to make a copy of the instance of the board obj
            curPiece = temp.get_piece(piece.row, piece.col)
            potentialBoard = proposedTransition(curPiece, move, temp, legal_moves[move])
            successors.append(potentialBoard)
    return successors

def proposedTransition(piece, action, board, skip):
    board.move(piece, action[0], action[1])
    if skip:
        board.remove(skip)
    return board