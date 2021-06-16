import itertools


def _kanji_iterator():
    itr = itertools.chain(range(0x3400, 0x4DB5), range(0x4E00, 0x9FCB), range(0xF900, 0xFA6A))
    return (chr(term) for term in itr)


def _kana_iterator():
    itr = itertools.chain(range(0x3041, 0x3096), range(0x30A0, 0x30FF))
    return (chr(term) for term in itr)
