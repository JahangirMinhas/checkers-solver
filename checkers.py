import argparse
import copy
import sys
import time

cache = {} # you can use this to implement state caching

class State:
    # This class is used to represent a state.
    # board : a list of lists that represents the 8*8 board
    def __init__(self, board_dict, curr_turn='r'):
        self.board_dict = board_dict

        self.width = 8
        self.height = 8
        self.curr_turn = curr_turn

    def display(self):
        board_str = ""
        for i in range(self.height):
            for j in range(self.width):
                if (j, i) in self.board_dict:
                    board_str += self.board_dict[(j, i)]
                else:
                    board_str += '.'
            board_str +='\n'
        print(board_str)
    
    def evaluate(self, depth):
        player_score = 0
        opp_score = 0

        curr_turn_win = True
        opp_win = True
        for piece in state.board_dict.values():
            if piece == self.curr_turn.upper():
                player_score += 3
            elif piece == self.curr_turn:
                player_score += 1
                
            if piece == get_opp_char(self.curr_turn)[1]:
                opp_score += 3
            elif piece == get_opp_char(self.curr_turn)[0]:
                opp_score += 1
            
        for key in state.board_dict:
            if state.board_dict[key].lower() != state.curr_turn:
                curr_turn_win = False
            if state.board_dict[key].lower() != get_opp_char(state.curr_turn)[0]:
                opp_win = False
        
        if curr_turn_win:
            return 1000 - depth
    
        if opp_win:
            return -1000 + depth
        return player_score - opp_score
    
    def generate_successors(self):
        jump = False
        new_states = []
        for key in self.board_dict:
            moves = []
            jump_moves = []
            value = self.board_dict[key]
            if value.lower() == self.curr_turn:
                # create a list of possible moves depending on the piece color and king status
                if value in ['r', 'R']:
                    possible_moves = [(key[0] - 1, key[1] - 1), (key[0] + 1, key[1] - 1)]
                    if value.isupper():
                        possible_moves.extend([(key[0] + 1, key[1] + 1), (key[0] - 1, key[1] + 1)])
                else:
                    possible_moves = [(key[0] + 1, key[1] + 1), (key[0] - 1, key[1] + 1)]
                    if value.isupper():
                        possible_moves.extend([(key[0] - 1, key[1] - 1), (key[0] + 1, key[1] - 1)])
                    
                for possible_move in possible_moves:
                    if self.in_bounds(possible_move):
                        if possible_move in self.board_dict:
                            if self.board_dict[possible_move] in get_opp_char(value):
                                # possible jump, reset moves and send to helper
                                jump_moves.extend(self.rec_helper(key, copy.deepcopy(self.board_dict)))
                                if jump_moves:
                                    jump = True
                                    break
                        else:
                            # single move
                            moves.append([key, possible_move])

            if jump_moves:
                for jump_move in jump_moves:
                    new_states = []
                    copy_board_dict = copy.deepcopy(self.board_dict)
                    new_state = State(copy_board_dict, get_next_turn(self.curr_turn))
                    move_piece(jump_move, copy_board_dict)
                    new_states.append(new_state)
                break

            else:
                if not jump:
                    for move in moves:
                        copy_board_dict = copy.deepcopy(self.board_dict)
                        new_state = State(copy_board_dict, get_next_turn(self.curr_turn))
                        move_piece(move, copy_board_dict)
                        new_states.append(new_state)
            
        return new_states
            
    def rec_helper(self, key, copy_board):
        jump_moves = []
        if key in copy_board:
            value = copy_board[key]
        else:
            value = '.'

         # create a list of possible moves and possible_jump_moves depending on the piece color and king status
        if self.curr_turn in ['r', 'R']:
            possible_moves = [(key[0] - 1, key[1] - 1), (key[0] + 1, key[1] - 1)]
            possible_jump_moves = [(key[0] - 2, key[1] - 2), (key[0] + 2, key[1] - 2)]
            if value.isupper():
                possible_moves.extend([(key[0] + 1, key[1] + 1), (key[0] - 1, key[1] + 1)])
                possible_jump_moves.extend([(key[0] + 2, key[1] + 2), (key[0] - 2, key[1] + 2)])
        else:
            possible_moves = [(key[0] + 1, key[1] + 1), (key[0] - 1, key[1] + 1)]
            possible_jump_moves = [(key[0] + 2, key[1] + 2), (key[0] - 2, key[1] + 2)]
            if value.isupper():
                possible_moves.extend([(key[0] - 1, key[1] - 1), (key[0] + 1, key[1] - 1)])
                possible_jump_moves.extend([(key[0] - 2, key[1] - 2), (key[0] + 2, key[1] - 2)])
            
        for i in range(len(possible_moves)):
            if self.in_bounds(possible_moves[i]):
                rec_jump_moves = []
                if possible_moves[i] in copy_board:
                    jump_move = [key]
                    if copy_board[possible_moves[i]] in get_opp_char(value):
                        # possible jump move
                        if self.in_bounds(possible_jump_moves[i]) and not possible_jump_moves[i] in copy_board:
                            # valid jump move found
                            jump_move.append(possible_moves[i])
                            jump_move.append(possible_jump_moves[i])
                            # recurse to check for multi jump
                            new_copy = copy.deepcopy(copy_board)
                            move_piece(jump_move, new_copy)
                            rec_jump_moves = self.rec_helper(possible_jump_moves[i], new_copy)
                            
                            for i in range(len(rec_jump_moves)):
                                rec_jump_moves[i] = jump_move + rec_jump_moves[i]
                                
                    if rec_jump_moves:
                        jump_moves.extend(rec_jump_moves)
                    elif jump_move != [key]:
                        jump_moves.append(jump_move)
                        
        return jump_moves
                

    def in_bounds(self, key):
        return key[0] < self.width and key[0] >= 0 and key[1] >= 0 and key[1] < self.height

def is_terminal(state):
    if state.generate_successors() == []:
        return True

    piece = next(iter(state.board_dict))
    for key in state.board_dict:
        if state.board_dict[key].lower() != state.board_dict[piece].lower():
            return False
    
    return True
        

def move_piece(moves, board):
    for i in range(len(moves)):
        if i != 0:
            board[moves[i]] = board.pop(moves[i - 1])
            if moves[i][1] == 0 or moves[i][1] == 7:
                board[moves[i]] = board[moves[i]].upper()

def get_opp_char(player):
    if player in ['b', 'B']:
        return ['r', 'R']
    else:
        return ['b', 'B']

def get_next_turn(curr_turn):
    if curr_turn == 'r':
        return 'b'
    else:
        return 'r'

def mini_max(state, depth, alpha, beta):
    best_move = None

    if is_terminal(state) or depth == 10:
        return best_move, state.evaluate(depth)

    if state.curr_turn == 'r': value = float('-inf')
    if state.curr_turn == 'b': value = float('inf')
    
    successors = state.generate_successors()
    for child in successors:
        nxt_move, nxt_val = mini_max(child, depth + 1, alpha, beta)
        
        if state.curr_turn == 'r':
            if nxt_val > value:
                best_move, value = child, nxt_val
            
            if alpha >= beta:
                break
            alpha = max(alpha, nxt_val)
        else:
            if nxt_val < value:
                best_move, value = child, nxt_val
            
            if alpha >= beta:
                break
            beta = min(beta, nxt_val)
    
    return best_move, value
    

def read_from_file(filename):

    f = open(filename)
    lines = f.readlines()
    board = [[str(x) for x in l.rstrip()] for l in lines]
    board_dict = {(j, i): board[i][j] for i in range(len(board)) for j in range(len(board[i])) if board[i][j] != '.'}
    f.close()

    return board_dict

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()

    board_dict = read_from_file(args.inputfile)
    state = State(board_dict)
    ctr = 0

    curr = state
    path = [state]
    while not is_terminal(curr):
        curr, evalu = mini_max(curr, ctr, float("-inf"), float("inf"))
        path.append(curr)

    sys.stdout = open(args.outputfile, 'w')
    for state in path:
        state.display()

    sys.stdout = sys.__stdout__

