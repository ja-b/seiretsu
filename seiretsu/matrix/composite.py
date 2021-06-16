from collections import ChainMap

from seiretsu.matrix.scoring_matrix import ScoringMatrix


def create_composite_matrix_impl(matrix_impl):
    class CompositeScoringMatrix(ScoringMatrix):
        def __init__(self, *seeding_iterators):
            self.matrices = [matrix_impl(itr) for itr in seeding_iterators]

        def get(self, *, match_scores, **kwargs):
            return dict(ChainMap(*[mat.get(match_score=score) for mat, score in zip(self.matrices, match_scores)]))

    return CompositeScoringMatrix
