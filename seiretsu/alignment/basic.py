import heapq

from seiretsu.alignment.engine import AlignmentEngine


class BasicAlignmentEngine(AlignmentEngine):
    """
    Performs basic DP-alignment in python
    """

    def load_matrix(self, matrix):
        self.matrix = matrix

    def load_universe(self, universe):
        self.universe = universe

    def align(self, term, *, num_results, gap_penalty, **kwargs):
        def gen_results():
            for opposite in self.universe:
                alignment = _gen_alignment_table(term, opposite, self.matrix, gap_penalty)
                yield _resolve_global_alignment_table(alignment, term, opposite)

        return heapq.nlargest(num_results, gen_results(), lambda args: args[1])


def _resolve_global_alignment_table(alignment_table, ref_sequence_left, ref_sequence_right):
    """
    Resolves global alignment, returns the two sequences and the score.
    :param alignment_table:
    :param ref_sequence_left:
    :param ref_sequence_right:
    :return:
    """
    # Get corner
    max_left = max([l for l, _ in alignment_table.keys()])
    max_right = max([r for _, r in alignment_table.keys()])

    # Get score
    score = alignment_table[(max_left, max_right)][0]
    # Traverse until we get to (0,0)
    left = max_left
    right = max_right
    sequence_left = ''
    sequence_right = ''
    matched = ''
    while (left, right) != (0, 0):
        prev_left, prev_right = alignment_table[(left, right)][1]
        if left == prev_left:
            sequence_left += '-'
            sequence_right += ref_sequence_right[right - 1]
            matched += ' '
        elif right == prev_right:
            sequence_left += ref_sequence_left[left - 1]
            sequence_right += '-'
            matched += ' '
        else:
            if ref_sequence_left[left - 1] == ref_sequence_right[right - 1]:
                matched += '|'
            else:
                matched += ' '
            sequence_left += ref_sequence_left[left - 1]
            sequence_right += ref_sequence_right[right - 1]
        left = prev_left
        right = prev_right
    return '\n'.join([sequence_left[::-1], matched[::-1], sequence_right[::-1]]), score


def _gen_alignment_table(sequence_left: str, sequence_right: str, scoring_matrix: dict, gap_penalty, floor=None):
    """
    Common code to generate alignment table given a matrix
    :param sequence_left:
    :param sequence_right:
    :param scoring_matrix:
    :param gap_penalty:
    :param floor:
    :return:
    """
    alignment_table = {(0, 0): (0, (0, 0))}

    # Populate initials
    gap_accum = gap_penalty
    for i, _ in enumerate(sequence_left):
        i = i + 1
        alignment_table[(i, 0)] = (max(gap_accum, floor) if floor is not None else gap_accum, (i - 1, 0))
        gap_accum += gap_penalty

    gap_accum = gap_penalty
    for i, _ in enumerate(sequence_right):
        i = i + 1
        alignment_table[(0, i)] = (max(gap_accum, floor) if floor is not None else gap_accum, (0, i - 1))
        gap_accum += gap_penalty

    for i, c1 in list(enumerate(sequence_left)):
        i = i + 1
        for j, c2 in list(enumerate(sequence_right)):
            j = j + 1

            sub_score = scoring_matrix.get((c1, c2), 0.0)
            alignment_table[(i, j)] = max(
                [
                    (alignment_table[(i - 1, j)][0] + gap_penalty, (i - 1, j)),  # Gap right
                    (alignment_table[(i, j - 1)][0] + gap_penalty, (i, j - 1)),  # Gap up

                    (alignment_table[(i - 1, j - 1)][0] + sub_score, (i - 1, j - 1)),
                    # Accept substitution (or match)
                ],
                key=lambda x: x[0]
            )

            if floor is not None:
                alignment_table[(i, j)] = (max(alignment_table[(i, j)][0], floor), alignment_table[(i, j)][1])
    return alignment_table
