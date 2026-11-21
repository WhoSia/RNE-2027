"""Standalone numerical contracts; no Wi-Fi CSI hardware or field replication."""
import math
import unittest
from witraffic_emd_baseline import emd_1d, nearest_profile_by_emd


class WiTrafficTransportAnalogueTests(unittest.TestCase):
    def test_equal_histogram_zero_independent_of_total_mass(self):
        self.assertAlmostEqual(emd_1d([1, 2, 1], [4, 8, 4]), 0.0)

    def test_unit_mass_move_one_bin(self):
        self.assertAlmostEqual(emd_1d([1, 0, 0], [0, 1, 0]), 1.0)
        self.assertAlmostEqual(emd_1d([1, 0, 0], [0, 0, 1]), 2.0)
        self.assertAlmostEqual(emd_1d([1, 0, 0], [0, 0, 1],
                                       bin_centers=[0, .25, .75]), .75)

    def test_symmetry_and_absolute_cdf_decomposition(self):
        a, b = [2, 1, 1], [0, 1, 3]
        self.assertAlmostEqual(emd_1d(a, b), 1.0)
        self.assertAlmostEqual(emd_1d(b, a), 1.0)

    def test_metric_triangle_inequality_for_three_examples(self):
        a, b, c = [1, 0, 0], [0, 1, 0], [0, 0, 1]
        self.assertLessEqual(emd_1d(a, c),
                             emd_1d(a, b) + emd_1d(b, c) + 1e-12)

    def test_missing_negative_nan_malformed_and_bin_order_are_rejected(self):
        cases=[([], [1, 2], None), ([1], [1], None),
               ([0, 0], [1, 0], None), ([1, -1], [1, 0], None),
               ([math.nan, 1], [1, 0], None), ([True, 0], [0, 1], None),
               ([1, 0], [1, 0, 0], None), ([1, 0], [0, 1], [0, 0]),
               ([1, 0], [0, 1], [1, 0]), ([1, 0], [0, 1], [0])]
        for a,b,centers in cases:
            with self.subTest(a=a,b=b,centers=centers):
                with self.assertRaises(ValueError):
                    emd_1d(a,b,bin_centers=centers)

    def test_frozen_profile_decision_only_not_empirical_lane_confidence(self):
        r=nearest_profile_by_emd([0, 0, 1], {
            "profile_a": [1, 0, 0], "profile_b": [0, 0, 1]})
        self.assertEqual(r['best_label'], 'profile_b')
        self.assertAlmostEqual(r['distances']['profile_b'], 0.)
        self.assertEqual(r['evidence_status'], 'MATHEMATICAL_BASELINE_ONLY_NOT_MEASURED_CSI')
        self.assertAlmostEqual(r['best_minus_second_margin'], 2.)

    def test_tie_is_deterministic_and_not_confident(self):
        r=nearest_profile_by_emd([0, 1], {"z":[1, 0], "a":[0, 1]})
        self.assertEqual(r['best_label'], "a")
        self.assertAlmostEqual(r['best_minus_second_margin'], 1.)
        identical=nearest_profile_by_emd([0, 1], {"z":[0, 1], "a":[0, 1]})
        self.assertEqual(identical['best_label'], "a")
        self.assertEqual(identical['best_minus_second_margin'], 0.)

if __name__=='__main__':unittest.main()
