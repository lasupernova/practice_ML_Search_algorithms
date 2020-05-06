"""
Tic Tac Toe Player
"""

import math
import collections
import copy
import random

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    initial = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

    return initial


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        user = X
    else:
        # initiate counter
        c = collections.Counter()
        # iterate over rows and add row values to counter
        for x in board:
            c.update(x)
        # check if more X than O values
        if c['X'] > c['O']:
            user =  O
        else:
            user = X
    return user

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    pos_moves= set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                pos_moves.add((i,j))
    return pos_moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if action not in actions(board):
        raise ValueError('This is not a valid move!')
    else:
        new_board = copy.deepcopy(board)
        if player(board) == X:
            new_board[i][j] = X
        elif player(board) == O:
            new_board[i][j] = O
        else:
            raise ValueError(f'{player(board)} is not a valid player!')
        return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check if any row has all equal values (not None)
    for row in board:
        # check if length of set made from row is 1 but not none--> then all values in row are equal
        if (len(set(row)) == 1) and (set(row).pop() != None):
            return set(row).pop()
    # check if any column has all equal values that are not None
    for colnum in range(3):
            if board[0][colnum] == board[1][colnum] == board[2][colnum] != None:
                return board[0][colnum]
    # check if any diagonal has all equal values that are not none
    if (board[0][0] == board[1][1] == board[2][2] != None) or (board[0][2] == board[1][1] == board[2][0] != None):
        return board[1][1]
    # if none of the rows, columns or diagonals has all equal values --> return None
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if winner is not none or no possible moves are left --> return True as game is over
    if winner(board) != None or len(actions(board)) == 0:
        return True
    # else return False as game is not over
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board) == True:
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # if game is over, return None
    if terminal(board) == True:
        return None
    else:
        # create random i,j values
        i = random.randint(0, 2)
        j = random.randint(0, 2)
        best_move = (i,j)
        if player(board) == X:
            if board == initial_state():
                return best_move
            # value
            value = -math.inf
            for action in actions(board):
                new_val = min_value(result(board, action))
                if new_val > value:
                    value = new_val
                    best_move = action
        else:
            if board == initial_state():
                return best_move
            # value
            value = math.inf
            for action in actions(board):
                new_val = max_value(result(board, action))
                if new_val < value:
                    value = new_val
                    best_move = action
        return best_move

def min_value(board):
    if terminal(board):
        return utility(board)
    value = math.inf
    for action in actions(board):
        value = min(value, max_value(result(board, action)))
    return value

def max_value(board):
    if terminal(board):
        return utility(board)
    value = -math.inf
    for action in actions(board):
        value = max(value, min_value(result(board, action)))
    return value



