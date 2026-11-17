from fractions import Fraction
from types import SimpleNamespace
from unittest import TestCase

from uncertain_pocket_sensing import bounded_error, erasure_policy, reading_support


def two_worlds(high_count):
    return {
        0: SimpleNamespace(low=5, high=5),
        high_count: SimpleNamespace(low=-7, high=-7),
    }


class BoundedCountError(TestCase):
    def test_common_reading_recreates_unobserved_minimax(self):
        for capacity in (1, 2):
            with self.subTest(capacity=capacity):
                supports = [reading_support(n, capacity, "off_by_one") for n in range(capacity+1)]
                self.assertIn(1, set.intersection(*supports))
                report = bounded_error(two_worlds(capacity), capacity, "off_by_one")
                self.assertEqual(report["worst_regret"], 5)
                self.assertEqual(report["branches"][1]["delta"], [-7, 5])

    def test_separated_counts_can_still_select_the_correct_phase(self):
        report = bounded_error(two_worlds(3), 3, "off_by_one")
        self.assertEqual(report["worst_regret"], 0)
        self.assertEqual([row["choice"] for row in report["branches"].values()],
                         ["lag", "lag", "lead", "lead"])

    def test_one_sided_error_respects_sensor_support(self):
        self.assertEqual(reading_support(0, 2, "miss_one"), {0})
        self.assertEqual(reading_support(2, 2, "miss_one"), {1, 2})
        self.assertEqual(bounded_error(two_worlds(2), 2, "miss_one")["worst_regret"], 0)


class FlaggedErasure(TestCase):
    def test_fallback_minimizes_expected_regret_at_worst_probability(self):
        groups = two_worlds(3)
        value, policy = erasure_policy(groups, Fraction(1, 2))
        self.assertEqual(value, Fraction(5, 2))
        self.assertEqual(policy, {"fallback": "lead", "readable": {0: "lag", 3: "lead"}})
        self.assertEqual(erasure_policy(groups, Fraction(0))[0], 0)
        self.assertEqual(erasure_policy(groups, Fraction(1))[0], 5)

    def test_rejects_probability_outside_unit_interval(self):
        for probability in (Fraction(-1, 10), Fraction(11, 10)):
            with self.subTest(probability=probability), self.assertRaises(ValueError):
                erasure_policy(two_worlds(3), probability)


class DecisionThreshold(TestCase):
    def test_separated_extremes_do_not_guarantee_improvement(self):
        groups = {**two_worlds(3), 1: SimpleNamespace(low=-5, high=0)}
        report = bounded_error(groups, 3, "off_by_one")
        self.assertEqual(report["worst_regret"], 5)
        self.assertEqual(report["branches"][0]["delta"], [-5, 5])
