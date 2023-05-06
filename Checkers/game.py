import pygame
import sys
from .constants import RED, WHITE, GREEN, TILE
from .board import Board

class Game:
    def __init__(self, window):
        self._init()
        self.window = window

    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self): #this is the isWin() equivalent
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece is not None and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.valid_moves(piece)
            return True
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece is None and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.window, GREEN, (col * TILE + TILE // 2, row * TILE + TILE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED


    def get_turn(self):
        return self.turn


    def cur_state(self):
        return self.board
    
    def agent_move(self, board):
        self.board = board
        self.change_turn()
    

    # what should be the heuristic evaluation??
        # main idea: (num of pawns{for agent} + num of kings{for agent}) - num of vulnerable pieces and incorporate control of mid. of board
        # can go simpler for αβ and make it: num of pieces{for agent} + num of kings{for agent} - 

    def alpha_beta_evaluation(self):
        #aise "not implemented yet"
        whites = self.board.get_white_preformance()
        pieces_alive = whites[0]
        kings = whites[1]
        whiteMidControl = self.board.get_white_mid_control()
        redMidControl = self.board.get_red_mid_control()
        reds = self.board.get_red_preformace()
        redPawns = reds[0]
        redKings = reds[1]
        return ((pieces_alive + kings) * whiteMidControl) - ((redPawns + redKings) * redMidControl * redPawns)



