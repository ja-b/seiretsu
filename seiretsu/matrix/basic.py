import itertools
from collections import ChainMap

from seiretsu.matrix.scoring_matrix import ScoringMatrix


class BasicScoringMatrix(ScoringMatrix):
    """
    Defines a basic exact match CJK scoring matrix
    """

    def __init__(self, seeding_iterator):
        self.symbols = list(seeding_iterator)

    def get(self, *, match_score, **kwargs):
        return {(s, s): match_score for s in self.symbols}


def _kanji_iterator():
    itr = itertools.chain(range(0x3400, 0x4DB5), range(0x4E00, 0x9FCB), range(0xF900, 0xFA6A))
    return (chr(term) for term in itr)


CJKBasicScoringMatrix = lambda: BasicScoringMatrix(_kanji_iterator())


class BasicHeteroScoringMatrix(ScoringMatrix):
    """
    Same as above except accepts varying match scores
    """

    def __init__(self, *seeding_iterators):
        self.matrices = [BasicScoringMatrix(itr) for itr in seeding_iterators]

    def get(self, *, match_scores, **kwargs):
        return dict(ChainMap(*[mat.get(match_score=score) for mat, score in zip(self.matrices, match_scores)]))


def _kana_iterator():
    itr = itertools.chain(range(0x3041, 0x3096), range(0x30A0, 0x30FF))
    return (chr(term) for term in itr)


CJKKanaBasicScoringMatrix = lambda: BasicHeteroScoringMatrix(_kanji_iterator(), _kana_iterator())

if __name__ == '__main__':
    print(list(_kana_iterator()))
