#!/usr/bin/env python3
import array
import math
import os.path
import sys
import argparse
from collections import Counter
from itertools import chain
from typing import AnyStr

import matplotlib.pyplot as plt
from PIL import Image


def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


class EntropyGrapher:
    entropies = []
    file_data = b""


    def __init__(self, filename: AnyStr, _chunk_size=256):
        self.chunk_size = _chunk_size
        self.entropies = EntropyGrapher._get_entropies_from_file(filename, _chunk_size)
        self.entropies = EntropyGrapher._normalize_entropies(self.entropies)
        with open(filename, "rb") as f:
            self.file_data = f.read()

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

    def plot_entropies_show(self):
        self.plot_entropies()
        plt.show()

    def save_entropies_to_file(self, filename):
        self.plot_entropies()
        plt.savefig(filename)

    def save_img_from_file_data(self, filename):
        self.input_data = self.file_data

        x = self.chunk_size
        y = len(self.input_data) // x

        # Preparing data to import as HSV
        # Saturation and value are static, Hue = x
        # https://upload.wikimedia.org/wikipedia/commons/0/0d/HSV_color_solid_cylinder_alpha_lowgamma.png
        data = array.array('B', chain.from_iterable([(x, 200, 200) for x in self.input_data])).tostring()

        #print(3 * x * y)
        #print(len(data))
        img = Image.frombytes("HSV", (x, y), data)
        img = img.convert("RGB")
        # img = img.resize((4*x, 4*y))

        # Save with format .ext from filename if possible
        with open(filename, "wb") as f:
            img.save(f, format=os.path.splitext(filename)[1][1:])

    @staticmethod
    def _get_entropies_from_file(filename, chk_size=256):
        _entropies = []
        with open(filename, "rb") as f:
            for piece in read_in_chunks(f, chk_size):
                entropy = EntropyGrapher._get_entropy(piece)
                _entropies.append(entropy)
        return _entropies

    @staticmethod
    def _get_entropy(data):
        counter_obj = Counter(data)
        len_data = len(data)
        probabilities = [v / len_data for k, v in counter_obj.items()]
        entropy = -sum(x * math.log(x) for x in probabilities)
        return entropy

    @staticmethod
    def _normalize_entropies(_entropies):
        max_ent = max(_entropies)
        min_ent = min(_entropies)
        normalized_entropies = _entropies
        diff = max_ent - min_ent
        if diff:
            normalized_entropies = [((x - min_ent) / diff) for x in _entropies]
        return normalized_entropies



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple tool for file visualization")
    parser.add_argument('filename', metavar='filename', type=str, help="name of the file to analyze")
    parser.add_argument("-c", "--chk_size", type=int)
    parser.add_argument("-o", "--output")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-e", "--entropy", action='store_true')
    group.add_argument("-i", "--image", action='store_true')

    args = parser.parse_args()
    if args.chk_size:
        eg = EntropyGrapher(args.filename, args.chk_size)
    else:
        eg = EntropyGrapher(args.filename)

    if args.image:
        if args.output:
            eg.save_img_from_file_data(args.output)
        else:
            print("Provide output file")
            sys.exit(0)
    elif args.entropy:
        if args.output:
            eg.save_entropies_to_file(args.output)
        else:
            eg.plot_entropies_show()

    print(args)


