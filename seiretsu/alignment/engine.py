

class AlignmentEngine(object):

    def __init__(self, *, matrix, universe, **kwargs):
        self.load_matrix(matrix)
        self.load_universe(universe)
        self.kwargs = kwargs

    def load_matrix(self, matrix):
        """
        Loads scoring matrix
        :param matrix:
        :return:
        """

        raise NotImplementedError

    def load_universe(self, universe):
        """
        Loads universe of words
        :param universe:
        :return:
        """

        raise NotImplementedError

    def align(self, term, **kwargs):
        """
        Performs alignment on one term against items in universe
        :param term:
        :return:
        """

        raise NotImplementedError
