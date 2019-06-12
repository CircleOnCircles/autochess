from dataclasses import dataclass
from typing import FrozenSet

@dataclass
class Piece:
    """ piece is a drawable, no level, no position"""
    name: str
    species: FrozenSet[str]
    class_: str
    cost: int

    @property
    def piece_type(self) -> FrozenSet:
        return frozenset([s for s in self.species] + [self.class_])

    def isType(self, type: str) -> bool:
        return type in self.piece_type




