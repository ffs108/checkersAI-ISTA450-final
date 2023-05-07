import copy
import random
import torch 
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from Checkers.board import Board, Piece
from Checkers.constants import RED, WHITE, ROWS, COLS

# huge problem with time complexity on this -- will have to reread some more into this
# might have to be selective about when the learning can even take place


class QNeuralNetwork(nn.Module):
    def __init__(self, board_size, Hneurons, outputs):
        super().__init__()
        self.fc1 = torch.nn.Linear(board_size, Hneurons)
        self.fc2 = torch.nn.Linear(Hneurons, outputs)

    def forward(self, curState_tensor):
        curState_tensor = torch.relu(self.fc1(curState_tensor))
        curState_tensor = self.fc2(curState_tensor)
        return curState_tensor


def all_states(board, white_pieces, red_pieces):
    if white_pieces == 0 and red_pieces == 0:
        return[board]
    permutations = list()
    if white_pieces > 0:
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 1 and board[row][col] == None:
                    new_board = copy.deepcopy(board)
                    new_board[row][col] = Piece(row, col, WHITE)
                    permutations.extend(all_states(new_board, white_pieces - 1, red_pieces))
    if red_pieces > 0:
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 1 and board[row][col] == None:
                    new_board = copy.deepcopy(board)
                    new_board[row][col] = Piece(row, col, RED)
                    permutations.extend(all_states(new_board, white_pieces, red_pieces - 1))
    return permutations




class deepQAgent():

    def __init__(self, game, alpha=0.1, gamma=0.9, epsilon=0.3, color=RED):
        self.game = game
        self.board = self.game.board
        self.alpha = alpha #learn rate
        self.gamma = gamma #discount
        self.epsilon = epsilon #exploration rate
        self.color = color
        self.prev_state = None 
        self.prev_action = None
        #self.policy = self.get_policy()
        #self.board_flat = [piece for row in self.board for piece in row]
        self.n_network = QNeuralNetwork(5,25,5)
        

    def get_action(self, board_state, valid_actions):
        nboard_state = board_state.integer_repr()
        #print(nboard_state)
        if random.random() < self.epsilon:
            return random.choice(valid_actions[0]) # valid_actions sshould be self.getSuccessorsAndActions()
        else:
            qVals = self.n_network(torch.FloatTensor(nboard_state).unsqueeze(0))#board_state = torch.tensor(board_state, dtype=torch.float).unsqueeze(0)
            qVals = qVals.detach().numpy()[0]
            print(qVals)
            valid_Qs = [qVals[i] for i in range(len(valid_actions))]
            if len(valid_Qs) == 0:
                return self.get_policy()
            else:
                return valid_actions[valid_Qs.index(max(valid_Qs))]
            
        
    def update(self, reward, state, valid_actions):
        if self.prev_state is not None:
            prev_Qs = self.n_network(torch.FloatTensor(self.prev_state).unsqueeze(0))
            prev_Qs = prev_Qs.detach().numpy(0)
            prev_action_index = self.prev_action
            prev_Qs = prev_Qs[prev_action_index]

            qVals = self.n_network(torch.FloatTensor(self.prev_state).unsqueeze(0))
            qVals = qVals.detach().numpy()[0]
            valid_qVals = [qVals[i] for i in range(len(valid_actions))]
            if len(valid_qVals) == 0:
                max_qvalue = 0
            else:
                max_qvalue = max(valid_qVals)
            #SARSA update -- Q(s,a) = Q(s,a) + α (Reward, + γ * Q(s',a') - Q(s,a))
            new_Qs = prev_Qs + self.alpha * (reward + self.gamma * max_qvalue - prev_Qs)
            prev_Qs[prev_action_index] = new_Qs
            target = torch.FloatTensor(prev_Qs)
            prediction = self.n_network(torch.FloatTensor(self.prev_state).unsqueeze(0))
            loss = torch.nn.functional.mse_loss(prediction, target)
            self.n_network.optimizer.zero_grad()
            loss.backward()
            self.n_network.optimizer.step()
        if reward == 1 or reward == -1:
            self.prev_state = None
            self.prev_action = None
        else:
            self.prev_state = state.integer_repr()
            self.prev_action = self.get_action(state.integer_repr(), valid_actions)

            
    def get_policy(self): #rule based policy
        possible_actions = self.getSuccessorsAndActions()
        for state_action in possible_actions: #rule 1: we want to prioritize aggressive play
            if self.board.is_capture_for_red(state_action[0]):
                return state_action[0]
        for state_action in possible_actions: #rule 2: we want to enphasize getting pawns -> kings
            if self.board.is_kinging_for_red(state_action[0]):
                return state_action[0]
        return (random.choice(possible_actions))[0] # else, most likely in beginning turns, just make a move
        
    # def epsilon_greed_factor(self):
    #     if random.uniform(0.0, 1.0) > self.epsilon:
    #         re

    ''' successors are index 0 - actions index 1'''
    def getSuccessorsAndActions(self):
        state_action_pairs = []
        for piece in self.board.get_all_pieces_of_color(RED):
            legal_moves = self.board.valid_moves(piece)
            #print(legal_moves)
            for move in legal_moves:
                #print(move)
                temp = copy.deepcopy(self.board) #this is to make a copy of the instance of the board obj
                curPiece = temp.get_piece(piece.row, piece.col)
                potentialBoard = temp.proposedTransition(curPiece, move, legal_moves[move])
                                        #literally, (s,a)
                state_action_pairs.append((potentialBoard, move))
        return state_action_pairs


    def change_alpha(self, newLearnRate):
        self.alpha = newLearnRate
    
    def change_gamma(self, newExploreRate):
        self.gamma = newExploreRate
