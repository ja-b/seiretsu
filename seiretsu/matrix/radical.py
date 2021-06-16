import json
import pathlib

from seiretsu.matrix import basic, composite


class RadicalScoringMatrix(basic.BasicScoringMatrix):
    """
    Defines a scoring matrix that uses common shared radicals for scoring.
    """

    def __init__(self, seeding_iterator):
        super().__init__(seeding_iterator)

        self.radicals = self._get_radicals()

    @staticmethod
    def _get_radicals():
        with open(pathlib.Path(__file__).parent / '..' / '..' / 'data' / 'radical_scores.json') as f:
            radicals = json.load(f)
        return {tuple(kanji.split(':')): score for kanji, score in radicals.items()}

    def get(self, *, match_score, radical_match_score=1, **kwargs):
        direct_match = super().get(match_score=match_score, **kwargs)
        radical_match = {kanji: rad_match * radical_match_score for kanji, rad_match in self.radicals.items()}
        return {**direct_match, **radical_match}


RadicalHeteroScoringMatrix = composite.create_composite_matrix_impl(RadicalScoringMatrix)
