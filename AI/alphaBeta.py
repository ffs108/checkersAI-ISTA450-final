import pygame
import copy
##from Checkers.game import Game
from Checkers.constants import WHITE



def abControl(gameState, depth, gameObj, color=WHITE):
    alpha = float('-inf')
    beta = float('inf')
    cur_depth = 0
    agent = 0
    agentNum = 1
    alphaBetaVar = alphaBeta(agent, agentNum, gameState, alpha, beta, cur_depth, depth, color, gameObj)
    if alphaBetaVar == (None,None):
        gameObj.white_agent_life_check()
    return alphaBetaVar

def alphaBeta(agent, agentNum, gameState, alpha, beta, cur_depth, depth, color, gameObj):
    if agent >= agentNum:
        agent = 0
        cur_depth += 1
    if gameObj.winner() is not None or cur_depth == depth:
        return gameState, gameObj.alpha_beta_evaluation()
    cur_optimal = None; best_action = None
    for successor in getSuccessors(gameState, color, gameObj):
        resulting_score = alphaBeta(agent + 1, agentNum, successor, alpha, beta, cur_depth, depth, color, gameObj)[1]
        if resulting_score is not None:
            if agent == 0: #white - the max
                if cur_optimal is None or resulting_score > cur_optimal:
                    cur_optimal = resulting_score
                    best_action = successor
                    alpha = max(alpha, resulting_score) # alpha = MAX(α, util val)
            else: #player or deepQ/genetic
                if cur_optimal is None or resulting_score < cur_optimal:
                    cur_optimal = resulting_score
                    best_action = successor
                    beta = min(beta, resulting_score) # beta = MIN(β, util val)
            if alpha > beta:#prune point
                break
    return best_action, cur_optimal


def getSuccessors(board, color, gameObj):
    successors = list()
    for piece in board.get_all_pieces_of_color(color):
        legal_moves = board.valid_moves(piece)
        #print(legal_moves)
        for move in legal_moves:
            #print(move)
            temp = copy.deepcopy(board) #this is to make a copy of the instance of the board obj
            curPiece = temp.get_piece(piece.row, piece.col)
            potentialBoard = proposedTransition(curPiece, move, temp, gameObj, legal_moves[move])
            successors.append(potentialBoard)
    return successors


def proposedTransition(piece, action, board, game, skip):
    board.move(piece, action[0], action[1])
    if skip:
        board.remove(skip)
    return board

