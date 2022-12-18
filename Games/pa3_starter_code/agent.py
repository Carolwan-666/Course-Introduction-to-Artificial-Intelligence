"""
An AI agent for land bidding process.
"""

import random
import sys
import time

# You can use the functions in utilities to write your AI
from utilities import find_lines, get_possible_moves, get_score, play_move

s = {}

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)

# Method to compute utility value of terminal state
def compute_utility(board, color):
    p1_count, p2_count = get_score(board)
    u = 0
    if color == 1:
        u = p1_count - p2_count
    elif color == 2:
        u = p2_count - p1_count
    return u

    #IMPLEMENT
    # return 0 #change this!

# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    return 0 #change this!

############ MINIMAX ###############################

def opp(color):
    if color == 1:
        return 2
    elif color == 2:
        return 1


def cach(board, color, caching):
    if caching == 1 and (board, color) in s.keys():
            return s[(board, color)]
    return 0

def mm_min_node(board, color, limit, caching = 0):
    #IMPLEMENT (and replace the line below)
    op = opp(color)
    min_u = float("inf")
    min_idx = 0
    mvs = get_possible_moves(board, op)
    if cach(board, color, caching):
        return cach(board, color, caching)
    elif limit == 0:
        return None, compute_utility(board, color)
    elif mvs == []: #final
        return None, compute_utility(board, color)
    else:
        d = {}
        for mv in mvs:
            idx = mvs.index(mv)
            nb = play_move(board, op, mv[0], mv[1])
            d[idx] = mm_max_node(nb, color, limit - 1, caching)[1]
        min_idx, min_u = min(d.items(), key=lambda k: k[1])
        min_mv = mvs[min_idx]
        s[(board, color)] = (min_mv, min_u)
        return min_mv, min_u


def mm_max_node(board, color, limit, caching = 0):
    max_u = -float("inf")
    max_idx = 0
    mvs = get_possible_moves(board, color)
    if cach(board, color, caching):
        return cach(board, color, caching)
    elif limit == 0 or mvs == []:
        return None, compute_utility(board, color)
    else:
        d = {}
        for mv in mvs:
            idx = mvs.index(mv)
            nb = play_move(board, color, mv[0], mv[1])
            d[idx] = mm_min_node(nb, color, limit - 1, caching)[1]
        max_idx, max_u = max(d.items(), key=lambda k: k[1])
        max_mv = mvs[max_idx]
        s[(board, color)] = (max_mv, max_u)
        return max_mv, max_u


def claim_mm(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    """
    t = mm_max_node(board, color, limit, caching)
    return t[0]


############ ALPHA-BETA PRUNING #####################
def check(alpha, beta):
    return alpha >= beta

def ab_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    min_u = float("Inf")
    bst = None
    if cach(board, color, caching):
        return cach(board, color, caching)
    elif limit == 0:
        return None, compute_utility(board, color)
    d = {}
    lst1 = []
    lst2 = []
    op = opp(color)
    mvs = get_possible_moves(board, op)
    for mv in mvs:
        idx = mvs.index(mv)
        nb = play_move(board, op, mv[0], mv[1])
        u = compute_utility(nb, color)
        d[idx] = (mv, nb, u)
        lst1.append((mv, nb, u))
    if lst1 == []:
        return None, compute_utility(board, color)
    temp_lst = sorted(d.items(), key=lambda x: -x[1][2])
    for t in temp_lst:
        lst2.append(t[1])
    if ordering == 0: # ordering is 1
        for c1 in lst1:
            mv = c1[0]
            bd = c1[1]
            # next
            m, u = ab_max_node(bd, color, alpha, beta, limit-1, caching, ordering)
            if u < min_u:
                min_u = u
                bst = mv
            if min_u < beta:
                beta = min_u
            if check(alpha, beta):
                s[(board, color)] = (bst, min_u)
                return bst, min_u
        s[(board, color)] = (bst, min_u)
        return bst, min_u
    elif ordering == 1: #ordering is 1
        for c2 in lst2:
            mv = c2[0]
            bd = c2[1]
            m, u = ab_max_node(bd, color, alpha, beta, limit-1, caching, ordering)
            if u < min_u:
                min_u = u
                bst = mv
            if min_u < beta:
                beta = min_u
            if check(alpha, beta):
                s[(board, color)] = (bst, min_u)
                return bst, min_u
        s[(board, color)] = (bst, min_u)
        return bst, min_u

def ab_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):

    max_u = -float("Inf")
    bst = None
    if cach(board, color, caching):
        return cach(board, color, caching)
    elif limit == 0:
        return None, compute_utility(board, color)
    d = {}
    lst1 = []
    lst2 = []
    mvs = get_possible_moves(board, color)
    for mv in mvs:
        idx = mvs.index(mv)
        nb = play_move(board, color, mv[0], mv[1])
        u = compute_utility(nb, color)
        d[idx] = (mv, nb, u)
        lst1.append((mv, nb, u))
    if lst1 == []:
        return None, compute_utility(board, color)
    temp_lst = sorted(d.items(), key=lambda x: -x[1][2])
    for t in temp_lst:
        lst2.append(t[1])
    if ordering == 0:  # ordering is 0
        for c1 in lst1:
            mv = c1[0]
            bd = c1[1]
            # next
            m, u = ab_min_node(bd, color, alpha, beta, limit - 1, caching, ordering)
            if u > max_u:
                max_u = u
                bst = mv
            if max_u > alpha:
                alpha = max_u
            if check(alpha, beta):
                s[(board, color)] = (bst, max_u)
                return bst, max_u
        s[(board, color)] = (bst, max_u)
        return bst, max_u
    elif ordering == 1:  # ordering is 1
        for c2 in lst2:
            mv = c2[0]
            bd = c2[1]
            m, u = ab_min_node(bd, color, alpha, beta, limit - 1, caching, ordering)
            if u > max_u:
                max_u = u
                bst = mv
            if max_u > alpha:
                alpha = max_u
            if check(alpha, beta):
                s[(board, color)] = (bst, max_u)
                return bst, max_u
        s[(board, color)] = (bst, max_u)
        return bst, max_u

def claim_ab(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations.
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations.
    """
    t = (ab_max_node(board, color, -float("Inf"), float("Inf"), limit, caching, ordering))
    return t[0]

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Bidding AI") # First line is the name of this AI
    arguments = input().split(",")

    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light.
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = claim_mm(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = claim_ab(board, color, limit, caching, ordering)

            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
