data = "https://dotaautochess.gamepedia.com/Chess_pieces"

import pandas as pd
import numpy as np
from requests_html import HTMLSession, Element

session = HTMLSession()
r = session.get(data)
tables = r.html.find('table')

def convert2html(element: Element) -> pd.DataFrame:
    dfs = pd.read_html(element.html)
    return dfs[0]

pool_size, reroll_chance, piece_list = map(convert2html,tables)
pool_size = pool_size.sort_values('Chess Cost')
reroll_chance = reroll_chance.sort_values('Rank')
chance_col = [col for col in reroll_chance.columns if '$' in col]
reroll_chance[chance_col] = reroll_chance[chance_col].apply(lambda x: x.str.strip('*%')).astype('int64')
reroll_chance = reroll_chance.set_index('Rank')
assert np.all(reroll_chance.sum(axis=1)==100)
reroll_chance = reroll_chance / 100

classes = frozenset(piece_list.Class.to_list())
species = frozenset([sp for maybe2species in set(piece_list.Species.to_list()) for sp in maybe2species.split('/')])
types = frozenset(classes.union(species))