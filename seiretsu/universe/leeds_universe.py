import pathlib

from seiretsu.universe.universe import Universe


class FileUniverse(Universe):

    def __init__(self, file_name):
        def read_file():
            with open(file_name) as f:
                for l in f:
                    yield l

        self.file_iter = read_file()


class LeedsUniverse(FileUniverse):

    def __init__(self, *args, **kwargs):
        super().__init__(pathlib.Path(__file__).parent / '..' / '..' / 'data' / 'leeds_corpus.txt', *args, **kwargs)
        self.words = []
        for l in self.file_iter:
            _num, _freq, *word = l.split()
            if len(word) == 1:
                self.words.append(word[0])

    def get(self, **kwargs):
        return self.words


if __name__ == "__main__":
    l = LeedsUniverse()
    print(l.get())
