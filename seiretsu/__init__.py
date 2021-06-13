from seiretsu.alignment.basic import BasicAlignmentEngine
from seiretsu.matrix.basic import CJKKanaBasicScoringMatrix
from seiretsu.universe.leeds_universe import LeedsUniverse


def basic_align(term, num_results=10, gap_penalty=-7.5, kanj_match_score=20, kana_match_score=10, **kwargs):
    """
    Performs most straightforward, common alignment
    :param term:
    :param kwargs:
    :return:
    """

    matrix = CJKKanaBasicScoringMatrix().get(match_scores=[kanj_match_score, kana_match_score])

    universe = LeedsUniverse().get()

    engine = BasicAlignmentEngine(matrix=matrix, universe=universe)

    return engine.align(term, num_results=num_results, gap_penalty=gap_penalty)


if __name__ == "__main__":
    for alignment, score in basic_align("地下鉄", num_results=40):
        print("Score: {}\nAlignment:\n{}".format(score, alignment))
