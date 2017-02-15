from unittest import TestCase
from entropy import EntropyGrapher, read_in_chunks
from collections import Counter
from scipy.stats import entropy


class TestEntropyCalculations(TestCase):
    def test(self):
        with open("test/test1", "rb") as f1:
            with open("test/test1.jpg", "rb") as f2:
                for f in [f1, f2]:
                    for i in read_in_chunks(f, 64):
                        # My entropy
                        my_entropy = EntropyGrapher._get_entropy(i)

                        # scipy entropy
                        counter_obj = Counter(i)
                        probabilities_dict = {k: v/len(i) for k, v in dict(counter_obj).items()}
                        probabilities = list(probabilities_dict.values())
                        scipy_entropy = entropy(probabilities)
                        self.assertAlmostEqual(my_entropy, scipy_entropy)


class TestEntropyCalculations2(TestCase):
    def test(self):
        my_entropy = EntropyGrapher._get_entropy("AAAAAAAAAAAAAAAAAAAAA")
        self.assertEqual(my_entropy, 0)




