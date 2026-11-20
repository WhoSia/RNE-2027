from collections import Counter
from itertools import product
from unittest import TestCase

from signal_model import Scenario
from storage_information import (BIN_STARTS, DECISION, build_context, decision,
                                 paired_bins, partition)


class StorageInformationTests(TestCase):
    def test_orders_preserve_bin_counts_and_background(self):
        background = ((0, 0), (BIN_STARTS[0], 0), (BIN_STARTS[0], 4),
                      (BIN_STARTS[-1] + 2, 1))
        for bits in ((0,) * len(BIN_STARTS), (1,) * len(BIN_STARTS)):
            rows = paired_bins(background, bits)
            self.assertIn((BIN_STARTS[0], 4), rows)
            self.assertIn((BIN_STARTS[-1] + 2, 1), rows)
            for start in BIN_STARTS:
                counts = Counter(m for tick, m in rows if start <= tick < start + 2 and m < 2)
                self.assertEqual(counts, {0: 1, 1: 1})

    def test_separate_bits_cannot_resolve_a_joint_interaction(self):
        rows = [((), -7 if p == l else 11, p, l) for p, l in product((0, 1), repeat=2)]
        results = partition(rows, 1, 1)
        for name in ("baseline", "pocket_full", "receiver_full"):
            self.assertEqual(results[name]["regret"], 7)
        self.assertEqual(results["both_fullness"]["regret"], 0)
        self.assertEqual(decision([0, 0])["minimax_order"], "either")

    def test_each_storage_context_scores_the_same_arrival_set(self):
        result = build_context(Scenario("test", DECISION + 12, ()))
        for model in result["storage"].values():
            for instrument in model["instruments"].values():
                self.assertEqual(sum(row["worlds"] for row in instrument["branches"].values()), 64)
