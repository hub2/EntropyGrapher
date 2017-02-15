#!/usr/bin/env python3
import math
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.colors as clrs
import matplotlib.ticker as ticker
from typing import Sequence, AnyStr
import sys


def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


class EntropyGrapher:
    chunk_size = 64
    entropies = []

    def __init__(self, data: Sequence):
        self.entropies = EntropyGrapher._get_entropy(data)
        self.entropies = EntropyGrapher._normalize_entropies(self.entropies)

    @classmethod
    def from_file(cls, filename: AnyStr, _chunk_size=chunk_size):
        obj = cls.__new__(cls)
        obj.chunk_size = _chunk_size
        obj.entropies = EntropyGrapher._get_entropies_from_file(filename)
        obj.entropies = EntropyGrapher._normalize_entropies(obj.entropies)
        return obj

    def plot_entropies(self):
        axes = plt.gca()  # get handle on axes
        axes.set_xmargin(0)  # set padding on data to 0
        barlist = plt.bar(range(len(self.entropies)), self.entropies,
                          width=1.0, align='edge')

        for i in barlist:
            y = i.get_height()  # (i.get_height()-min_ent) / (max_ent - min_ent)
            c = (1, 1, 1)
            if y >= 0.8:
                c = (1, 0.07, 0.07)
            elif 0.5 < y < 0.8:
                c = (0.8, 0.8, 0.2)
            elif y <= 0.5:
                c = (0, 0, 1)
            i.set_color(c)
        plt.show()

    @staticmethod
    def _get_entropies_from_file(filename, chk_size=chunk_size):
        _entropies = []
        with open(filename, "rb") as f:
            for piece in read_in_chunks(f, chk_size):
                entropy = EntropyGrapher._get_entropy(piece)
                _entropies.append(entropy)
        return _entropies

    @staticmethod
    def _get_entropy(data):
        counter_obj = Counter(data)
        probabilities_dict = {k: v / len(data) for k, v in dict(counter_obj).items()}
        probabilities = list(probabilities_dict.values())
        entropy = -sum([x * math.log(x) for x in probabilities])
        return entropy

    @staticmethod
    def _normalize_entropies(_entropies):
        max_ent = max(_entropies)
        min_ent = min(_entropies)
        # print("min_ent: ", min_ent)
        # print("max_ent: ", max_ent)
        normalized_entropies = [((x - min_ent) / (max_ent - min_ent)) for x in _entropies]
        return normalized_entropies


if __name__ == "__main__":
    eg = EntropyGrapher.from_file(sys.argv[1])
    eg.plot_entropies()
