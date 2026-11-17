from unittest import TestCase

from late_arrival_experiment import classification, experiment


class LateArrivalExperimentTest(TestCase):
    def test_classifies_ties_separately_from_reversals(self):
        self.assertEqual(classification(1, -1), "strict_reversal")
        self.assertEqual(classification(1, 0), "tie_transition")
        self.assertEqual(classification(0, -1), "tie_transition")
        self.assertEqual(classification(2, 1), "same_sign_change")
        self.assertEqual(classification(0, 0), "unchanged")

    def test_reproduces_the_known_witness_and_full_design(self):
        report = experiment()
        rows = {row[:5]: row[5:] for row in report["rows"]}
        self.assertEqual(len(rows), 252)
        self.assertEqual(sum(report["total"].values()), len(rows))
        witness = rows[("early_edge", 11, "left", 1, 1)]
        self.assertEqual(witness[4:], (31, -17, "strict_reversal"))
        for lag0, lead0, lag3, lead3, before, after, category in rows.values():
            self.assertEqual((before, after), (lead0 - lag0, lead3 - lag3))
            self.assertEqual(category, classification(before, after))
