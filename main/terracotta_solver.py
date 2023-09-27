"""
Module that implements both the Terracotta puzzle as a class and contains 
a recersive solver. If the module is called directly, a seed number can
be given as argument to shuffle the created pieces
"""
import numpy as np
from itertools import groupby
from copy import deepcopy, copy
import sys
import random

class TerracottaPuzzle():
    def __init__(self, all_pieces, order):
        self.all_pieces = all_pieces
        self.order = order
        self.idx_above = list(np.flip(np.arange(0,35)))
        self.idx_left = list(np.arange(0,70)-7)
        self.side_dict = {
                            0: (slice(1), slice(0,2)), 
                            1: (slice(0,3), slice(1,2)), 
                            2: (slice(1,2), slice(0,2)),
                            3: (slice(0,3), slice(0,1))
                        }

    def fit_between_two(self, 
                        piece_1, side_1, # First piece
                        piece_2, side_2): # Second piece
        return np.all(piece_1[self.side_dict[side_1]] -
                      piece_2[self.side_dict[side_2]] == 0)

    def fit_pos_10_7(self, place_index, piece_):
        if place_index > 6:
            left_idx = self.idx_left[place_index]
            piece_left = self.all_pieces[self.order[left_idx]]

            if place_index in [0,7,14,21,28,35,42,49,56,63]:
                fits = self.fit_between_two(piece_, 3, 
                                            piece_left, 1)
            
            else:
                piece_above = self.all_pieces[self.order[place_index - 1]]

                fits_above = self.fit_between_two(piece_, 0, 
                                                 piece_above, 2)
                

                fits_left = self.fit_between_two(piece_, 3, 
                                                 piece_left, 1)
                
                fits = np.all([fits_left, fits_above])

        elif place_index <= 6 and place_index > 0:
            piece_above = self.all_pieces[self.order[place_index - 1]]

            fits = self.fit_between_two(piece_, 0, 
                                              piece_above, 2)
            
        elif place_index == 0:
            fits = True


        return fits
    
class TerraCottaSolver():
    def __init__(self,
                 cousin_dict, 
                 order_init=list(np.repeat(-1,70))):
        self.cousin_dict = cousin_dict
        self.highest_index = 0
        self.best_order = []
        self.order_init_ = order_init

    def terracotta_solver(self, all_pieces, init_stack):
        def solve(current_index, puzzle_class, available_stack):
            if current_index > self.highest_index:
                self.highest_index = current_index
                self.best_order = puzzle_class.order
                print(self.best_order)

            for new_piece_index in available_stack.keys():
                new_piece_index = int(new_piece_index)

                new_piece = available_stack[new_piece_index]

                if puzzle_class.fit_pos_10_7(current_index, new_piece):
                    next_puzzle_class = copy(puzzle_class)

                    next_puzzle_class.order[current_index] = new_piece_index
                    next_available_stack = deepcopy(available_stack)

                    for elem_ in self.cousin_dict[new_piece_index]:
                        next_available_stack.pop(elem_)
                    
                    solve(current_index + 1, next_puzzle_class, next_available_stack)

                if current_index == 0:
                    break

        available_stack = init_stack
        puzzle_class = TerracottaPuzzle(all_pieces, order=self.order_init_)
        solve(0, puzzle_class, available_stack)


def prepare_dicts(seed_=42):

    all_pieces = []

    for ii in range(4):
        for ij in range(4):
            for ji in range(4):
                for jj in range(4):
                    all_pieces.append(np.array([[ii, ij], [ji,jj]]))

    random.Random(seed_).shuffle(all_pieces)
    pieces_dictionary = dict(zip(range(256), all_pieces))

    rotation_dict = {}
    idx_ = 0
    for piece_index, piece_ in pieces_dictionary.items():
        piece_rot_prep = deepcopy(piece_)
        rot_cousins = []
        rot_cousins.append(piece_.tolist())
        for rot_ in np.arange(1,4):
            piece_rot_prep = piece_rot_prep + 1
            piece_rot_prep[piece_rot_prep == 4] = np.repeat(0, len(piece_rot_prep[piece_rot_prep == 4]))
            rot_cousins.append(np.rot90(piece_rot_prep, k=rot_).tolist())

        empty_ = [k for k,v in groupby(sorted(rot_cousins))]

        rotation_dict[piece_index] = [np.array(ar_) for ar_ in empty_]
        idx_ += 1

    # Get the "cousins"
    cousin_dictionary = {}
    for check_idx in range(256):
        rel_array = pieces_dictionary[check_idx]
        cousin_pieces = []
        for lookup_index in range(256):
            if np.any([np.all(rel_array == k_) for k_ in rotation_dict[lookup_index]]):
                cousin_pieces.append(lookup_index)
                
        cousin_dictionary[check_idx] = cousin_pieces


    return all_pieces, pieces_dictionary, cousin_dictionary



if __name__ == "__main__":
    # Create all pieces
    all_pieces = []

    for ii in range(4):
        for ij in range(4):
            for ji in range(4):
                for jj in range(4):
                    all_pieces.append(np.array([[ii, ij], [ji,jj]]))

    random.Random(sys.argv[1]).shuffle(all_pieces)
    pieces_dict = dict(zip(range(256), all_pieces))

    # Find all
    rotation_dict = {}
    idx_ = 0
    for piece_index, piece_ in pieces_dict.items():
        piece_rot_prep = deepcopy(piece_)
        rot_cousins = []
        rot_cousins.append(piece_.tolist())
        for rot_ in np.arange(1,4):
            piece_rot_prep = piece_rot_prep + 1
            piece_rot_prep[piece_rot_prep == 4] = np.repeat(0, len(piece_rot_prep[piece_rot_prep == 4]))
            rot_cousins.append(np.rot90(piece_rot_prep, k=rot_).tolist())

        empty_ = [k for k,v in groupby(sorted(rot_cousins))]

        rotation_dict[piece_index] = [np.array(ar_) for ar_ in empty_]
        idx_ += 1

    # Get the "cousins"
    cousin_dictionary = {}
    for check_idx in range(256):
        rel_array = pieces_dict[check_idx]
        cousin_pieces = []
        for lookup_index in range(256):
            if np.any([np.all(rel_array == k_) for k_ in rotation_dict[lookup_index]]):
                cousin_pieces.append(lookup_index)
                
        cousin_dictionary[check_idx] = cousin_pieces


    init_stack = pieces_dict
    check_class = TerraCottaSolver(cousin_dictionary)

    check_class.terracotta_solver(all_pieces, init_stack)

