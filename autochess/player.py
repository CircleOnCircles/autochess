import pandas as pd
import numpy as np
import random
import collections

from autochess.pool import Pool

class Player:
    level = 1
    health = 100
    _money = 1

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, val):
        if val < 0:
            raise Exception('Money Cannot Be Negative')
        self._money = val

    def __init__(self, pool: Pool):
        self.pool = pool

    def reroll(self, free=False, inplace=True):
        if not free:
            cost = 2
            self.money -= cost

        return self.pool.draw(self.get_reroll_chance(), inplace=inplace)

    def get_reroll_chance(self):
        from autochess.refernece import reroll_chance
        return reroll_chance.iloc[self.level - 1].values


    def calculate_reroll_chance(self, name=None, piece_type=None) -> float:
        df = self.pool.to_dataframe()
        chance = pd.DataFrame({
                'Cost': range(1,6),
                'Chance': self.get_reroll_chance()
        })
        df.merge(chance,on='Cost')
        
