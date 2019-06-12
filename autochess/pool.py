from copy import deepcopy
from random import shuffle

import pandas as pd
import numpy as np

from autochess.piece import Piece


class Pool:

    def shuffle_pool(self):
        for cost in self.pool:
            shuffle(self.pool[cost])

    def __init__(self):
        from autochess.refernece import piece_list, pool_size

        # pool by cost
        self.pool = {}
        for cost in range(1,6):
            self.pool[cost] = []

        for idx, (name, species, class_, cost) in piece_list.iterrows():
            species = frozenset(species.split('/'))
            piece = Piece(name, species, class_, cost)
            self.pool[cost].extend([piece] * pool_size['Chess Pool Size'].iloc[cost - 1])

        self.shuffle_pool()

    def __iter__(self):
        for pool_by_cost in self.pool.values():
            for piece in pool_by_cost:
                yield piece

    def draw(self, chance, inplace=True):

        # select which cost
        pdf = chance
        pool2pick = np.random.choice(5, 5, True, pdf)
        pool2pick += 1 # adjusting to valid cost

        if not inplace:
            original_pool = deepcopy(self.pool)

        drawn_pieces = []
        for cost in pool2pick:
            drawn_pieces.append(self.pool[cost].pop())

        if not inplace:
            self.pool = original_pool

        return drawn_pieces

    def to_dataframe(self):
        from dataclasses import asdict
        return pd.DataFrame([asdict(p) for pool_by_cost in self.pool.values() for p in pool_by_cost])

    def __len__(self):
        return sum([len(p) for p in self.pool.values()])