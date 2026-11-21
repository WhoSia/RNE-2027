"""PHYS-08 preregistered prospective split and policy-age gate contracts."""
import unittest
from physical_checkpoint_freshness_fallback import (
    SEEDS, DELAYS, REGIMES, FALLBACK_AGE_S,
    freshness_choice, evaluate)


class FreshnessFallbackTests(unittest.TestCase):
    def test_prospective_seeds_disjoint_from_all_exploration(self):
        self.assertEqual(SEEDS, tuple(range(40, 56)))
        self.assertFalse(set(SEEDS) & set(range(40)))
        self.assertEqual(len(SEEDS) * 3 * 3 * 2, 288)

    def test_policy_switch_at_locked_twelve_seconds(self):
        self.assertEqual(FALLBACK_AGE_S, 12)
        self.assertEqual(DELAYS, (0, 6, 12, 24))
        for age in (0, 3, 6, 11):
            self.assertTrue(freshness_choice(age, True, False))
            self.assertFalse(freshness_choice(age, False, True))
        for age in (12, 13, 24):
            self.assertFalse(freshness_choice(age, True, False))
            self.assertTrue(freshness_choice(age, False, True))

    def test_invalid_age_or_threshold_rejected(self):
        for age in (-1, 3.5, None, True):
            with self.subTest(age=age):
                with self.assertRaisesRegex(ValueError, 'telemetry age'):
                    freshness_choice(age, True, False)
        for threshold in (0, -1, 2.1, True):
            with self.subTest(threshold=threshold):
                with self.assertRaisesRegex(ValueError, 'telemetry age'):
                    freshness_choice(4, True, False, threshold)

    def test_fixed_regimes_and_no_target_label_in_gate(self):
        self.assertEqual(REGIMES, (('uniform_baseline', 1800, .5),
                                   ('uniform_lowturn', 1350, .3)))
        self.assertEqual(freshness_choice(24, True, False), False)
        self.assertEqual(freshness_choice(24, False, True), True)

    def test_incomplete_training_fails_before_simulation(self):
        with self.assertRaisesRegex(ValueError, 'training'):
            evaluate([])


if __name__ == '__main__':
    unittest.main()
