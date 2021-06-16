import string
import unittest

from seiretsu import CJKKanaBasicScoringMatrix
from seiretsu.alignment.basic import BasicAlignmentEngine
from seiretsu.matrix.cjk import CJKBasicScoringMatrix, CJKKanaRadicalScoringMatrix, CJKRadicalScoringMatrix
from seiretsu.universe.leeds_universe import LeedsUniverse


class MyTestCase(unittest.TestCase):
    def test_simple_alignment(self):
        matrix = {(c, c): 10 for c in string.ascii_lowercase}

        universe = ['hello', 'goodbye', 'what', 'notebook', 'samurai']

        engine = BasicAlignmentEngine(matrix=matrix, universe=universe)

        expected = [('go-d---\n|| |   \ngoodbye', 22), ('g---od\n    | \nhello-', 2.0),
                    ('god-----\n |      \nnotebook', 0.0), ('god-\n    \nwhat', -2.0),
                    ('god----\n       \nsamurai', -8.0)]

        self.assertEqual(expected,
                         engine.align('god', num_results=5, gap_penalty=-2, unicode=False, sub_constant_cost=0.0))

    def test_small_universe_alignment(self):
        matrix = CJKBasicScoringMatrix().get(match_score=10)

        universe = [
            "財界",
            "無形文化財",
            "財布",
            "日本",
            "日本料理",
            "財閥"
        ]

        engine = BasicAlignmentEngine(matrix=matrix, universe=universe)

        expected = [('財閥解体\n||  \n財閥--', 10), ('財閥解体\n|   \n財界--', 0.0), ('財閥解体\n|   \n財布--', 0.0),
                    ('財閥解体\n    \n日本料理', 0.0), ('財閥解体-\n     \n無形文化財', -5.0)]

        self.assertEqual(expected,
                         engine.align("財閥解体", num_results=5, gap_penalty=-5, unicode=False, sub_constant_cost=0.0))

    def test_large_universe_alignment(self):
        matrix = CJKKanaBasicScoringMatrix().get(match_scores=[20, 10])

        universe = LeedsUniverse().get()

        engine = BasicAlignmentEngine(matrix=matrix, universe=universe)

        expected = [('衆院\n||\n衆院', 40), ('衆-院\n| |\n衆議院', 32.5), ('衆院\n |\n病院', 20.0), ('衆院\n |\n入院', 20.0),
                    ('衆院\n |\n寺院', 20.0), ('衆院\n |\n退院', 20.0), ('衆院\n |\n学院', 20.0), ('衆院\n |\n医院', 20.0),
                    ('衆院\n |\n上院', 20.0), ('衆院\n |\n参院', 20.0)]

        self.assertEqual(expected,
                         engine.align("衆院", num_results=10, gap_penalty=-7.5, unicode=False, sub_constant_cost=0.0))

    def test_radical_alignment(self):
        matrix = CJKRadicalScoringMatrix().get(match_score=20, radical_match_score=3)

        universe = LeedsUniverse().get()

        engine = BasicAlignmentEngine(matrix=matrix, universe=universe)

        expected = [('国鉄\n||\n国鉄', 26), ('国鉄\n| \n国-', 7.5), ('国鉄\n |\n-鉄', 7.5), ('国鉄\n| \n国民', 6.0),
                    ('国鉄\n| \n国際', 6.0), ('国鉄\n| \n国家', 6.0), ('国鉄\n| \n国内', 6.0), ('国鉄\n| \n国会', 6.0),
                    ('国鉄\n| \n国連', 6.0), ('国鉄\n| \n国立', 6.0), ('国鉄\n| \n国籍', 6.0), ('国鉄\n| \n国境', 6.0)]

        res = engine.align("国鉄", num_results=12, gap_penalty=-5.5, unicode=False, sub_constant_cost=-7)

        print(res)

        self.assertEqual(expected, res)


if __name__ == '__main__':
    unittest.main()
