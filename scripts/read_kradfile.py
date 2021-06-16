import json


def get_radical_records(fp):
    for l in fp.readlines():
        if not l.startswith('#'):
            symbols = l.split()
            yield symbols[0], symbols[2:]


def generate_shared_radicals(kanji, radicals_table, significant=4):
    def get_radical_scores():
        for l in kanji:
            for r in kanji:
                if l != r:
                    if l in radicals_table and r in radicals_table:
                        common = len(radicals_table[l] & radicals_table[r])
                        if common >= significant:
                            yield "{}:{}".format(l, r), common

    shared_radical_counts = {kanji: rad_match for kanji, rad_match in get_radical_scores()}
    return shared_radical_counts


if __name__ == '__main__':
    with open('../data/kradfile-u.txt') as f:
        radicals = {kanji: set(radicals) for kanji, radicals in get_radical_records(f)}
        shared_counts = generate_shared_radicals(radicals.keys(), radicals)
        with open('../data/radical_scores.json', 'w+') as j:
            json.dump(shared_counts, j)
