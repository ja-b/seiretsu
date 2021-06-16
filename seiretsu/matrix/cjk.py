from seiretsu import utils
from seiretsu.matrix import basic, radical

CJKBasicScoringMatrix = lambda: basic.BasicScoringMatrix(utils._kanji_iterator())

CJKKanaBasicScoringMatrix = lambda: basic.BasicHeteroScoringMatrix(utils._kanji_iterator(), utils._kana_iterator())

CJKRadicalScoringMatrix = lambda: radical.RadicalScoringMatrix(utils._kanji_iterator())

CJKKanaRadicalScoringMatrix = lambda: radical.RadicalHeteroScoringMatrix(utils._kanji_iterator(), utils._kana_iterator())
