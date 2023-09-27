import numpy as np
import pandas as pd

class BackMapper:
    def __init__(self) -> None:
        self._set_basedict()
        self._load_puzzle_pieces()
    
    def _set_basedict(self):
        all_pieces = []

        for ii in range(4):
            for ij in range(4):
                for ji in range(4):
                    for jj in range(4):
                        all_pieces.append(np.array([[ii, ij], [ji,jj]]))

        self.pieces_dict = dict(zip(range(256), all_pieces))

    def _load_puzzle_pieces(self):
        mapping_df = pd.read_csv('./utils/puzzle_piece_id_to_numeric.csv')
        self.evas_dict = dict(zip(mapping_df.my_id, mapping_df.Idc))

    def map_values(self,
                   current_dict: dict, 
                   current_indices: list):
        mapping_dict_new = {}
        for key_stand, val_stand in self.pieces_dict.items():
            for key_good, val_good in current_dict.items():
                if np.all(val_stand == val_good):
                    mapping_dict_new[key_good] = key_stand

        original_mappings = [mapping_dict_new[val_] for val_ in current_indices]
        evas_map = [self.evas_dict[val_] for val_ in original_mappings]

        return evas_map