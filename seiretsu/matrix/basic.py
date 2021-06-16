from collections import ChainMap

from seiretsu.matrix import composite
from seiretsu.matrix.scoring_matrix import ScoringMatrix


class BasicScoringMatrix(ScoringMatrix):
    """
    Defines a basic exact match CJK scoring matrix
    """

    def __init__(self, seeding_iterator):
        self.symbols = list(seeding_iterator)

    def get(self, *, match_score, **kwargs):
        return {(s, s): match_score for s in self.symbols}


BasicHeteroScoringMatrix = composite.create_composite_matrix_impl(BasicScoringMatrix)
