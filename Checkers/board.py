import pygame
import copy
from .constants import *


class Board:
    
    def __init__(self):
        self.board = [] #2d array
        self.create_board()
        self.selected_piece = None
        self.red_alive = 5
        self.white_alive = 5
        self.red_kings = 0
        self.white_kings = 0
        self.captures_for_red = 0
        self.captures_for_white = 0

    def draw_tiles(self, window):
        window.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, RED, (row * TILE, col * TILE, TILE, TILE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 2: #3 for 8x8
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 2: #was 4 for 8x8
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(None)
                else:
                    self.board[row].append(None)
    
    def draw(self, window):
        self.draw_tiles(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece is not None:
                    piece.draw(window)

    def move(self, piece, row, col):
        #swap places
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if row == (ROWS - 1)  or row == 0:
            piece.make_king()
            if piece.color == RED:
                self.red_kings += 1
            else:
                self.white_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col] 
    
    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = None
            if piece is not None:
                if piece.color == RED:
                    self.red_alive -= 1
                    self.captures_for_white += 1
                else:
                    self.white_alive -= 1
                    self.captures_for_red += 1
    
    def clear_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] is not None:
                    self.board[row][col] = None
                else: continue

    def winner(self):
        retval = 'The winner is: '
        if self.red_alive == 0:
            return retval + 'WHITE'
        elif self.white_alive == 0:
            return retval + 'RED'
        return None
    
    def cur_winner(self):
        if self.red_alive > self.white_alive:
            return 'RED'
        elif self.white_alive > self.red_alive:
            return 'WHITE'
        else:
            return 0
    
    def valid_moves(self, piece):
        moves = dict()
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        if piece.color == RED or piece.isKing:
            moves.update(self.traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self.traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.isKing:
            moves.update(self.traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self.traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))
        return moves
    

    def all_valid_move_by_color(self, color):
        if color == WHITE:
            return self.all_valid_moves_white()
        else:
            return self.all_valid_moves_red()

    def all_valid_moves_white(self):
        moves = list()
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row,col)
                if piece is not None and piece.color == WHITE:
                    moves.append(self.valid_moves(piece))
        #print(moves)
        if len(moves) == 0:
            self.white_alive == 0

    def all_valid_moves_red(self):
        moves = list()
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row,col)
                if piece is not None and piece.color == RED:
                    moves.append(self.valid_moves(piece))
        #print(moves)
        if len(moves) == 0:
            self.white_alive == 0


    def proposedTransition(self, piece, action, skip):
        self.move(piece, action[0], action[1])
        if skip:
            self.remove(skip)
        return self.board

    
    def traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == None:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self.traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self.traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current == None:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self.traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self.traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            right += 1
        return moves
    
    def get_all_pieces_of_color(self, chosenColor):
        retval = []
        for row in self.board:
            for piece in row:
                if piece is not None and piece.color == chosenColor:
                    retval.append(piece)
        return retval
    
    def get_red_preformace(self):
        return self.red_alive, self.red_kings
    
    def get_white_preformance(self):
        return self.white_alive, self.white_kings
    
    def get_white_mid_control(self):
        count = 0
        for piece in self.board[2]: 
            if piece is not None:
                count += 1 if piece.color == WHITE else count
        return count

    def get_red_mid_control(self):
        count = 0
        for piece in self.board[2]: 
            if piece is not None:
                count += 1 if piece.color == RED else count
        return count
    
    def is_capture_for_red(self, other):
        if self.white_alive > other.white_alive:
            return True
        return False
    
    def is_kinging_for_red(self, other):
        if self.red_kings < other.red_kings:
            return True
        return False
    
    def integer_repr(self):
        int_repr = copy.deepcopy(self.board)
        for piece in int_repr:
            if piece is None:
                piece = 0
            elif piece.color == WHITE:
                piece = 1
            else:
                piece = -1
        return int_repr



    def __str__(self):
        retval = '\nCURRENT STATE: Red Alive - ' + str(self.red_alive) + ' || White Alive - ' + str(self.white_alive)
        retval += '\n________________________________________________ \n\n'
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] is not None:
                    retval += self.board[row][col].__repr__()
                else:
                    retval += ' .  '
            retval += '\n'
        retval += '\n________________________________________________ \n'
        return retval
    
    def __eq__(self, other):
        if str(self) == str(other):
            return True
        else:
            return False






class Piece:

    PADDING = 10
    OUTLINE = 3

    def __init__(self, row, column, color):
        self.x = 0
        self.y = 0
        self.row = row
        self.col = column
        self.color = color
        self.isKing = False
        self.board_pos()

    def board_pos(self):
        self.x = TILE * self.col + TILE // 2
        self.y = TILE * self.row + TILE // 2

    def make_king(self):
        self.isKing = True

    def draw(self, window):
        radius = TILE // 2 - self.PADDING
        pygame.draw.circle(window, SHADOW, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius -1 )
        if self.isKing:
            window.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.board_pos()

    def __repr__(self):
        colorRep = ' w ' if self.color[1] == 255 else ' r '
        return colorRep if not self.isKing else colorRep[:2] + 'K '
    