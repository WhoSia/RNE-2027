from fractions import Fraction
from unittest import TestCase

from decision_time_gate import Evidence, binary_certificate, conditional_regret, fixed_regret


class TimeGateTests(TestCase):
    def test_latest_observation_must_arrive_by_commitment(self):
        self.assertTrue(Evidence("previous", 83, 1).admissible())
        self.assertFalse(Evidence("gap_open", 84, 1).admissible())
        self.assertFalse(Evidence("future_window", 90).admissible())
        self.assertTrue(Evidence("instant_at_commitment", 84).admissible())
        with self.assertRaisesRegex(ValueError, "negative"):
            Evidence("invalid", 82, -1).admissible()

    def test_no_causal_discrimination_without_distinct_observations(self):
        worlds = [("e", -113), ("l", 31)]
        hidden = conditional_regret(worlds, {"e": (1, 0), "l": (1, 0)})
        self.assertEqual(hidden["before"]["minimax"], 31)
        self.assertEqual(hidden["after"], 31)
        oracle = conditional_regret(worlds, {"e": "early", "l": "late"})
        self.assertEqual(oracle["after"], 0)
        self.assertEqual(oracle["guaranteed_reduction"], 31)

    def test_reported_error_thresholds_and_objective_sensitivity(self):
        stable = binary_certificate(-113, 31)
        self.assertEqual(stable["error_bound_for_strict_gain_vs_fixed"], "31/113")
        self.assertEqual(stable["error_bound_for_strict_gain_vs_mixed"], str(Fraction(31, 144)))
        self.assertEqual(stable["max_regret_with_error_one_tenth"], "113/10")
        self.assertFalse(stable["one_tick_latency_current_gap_admissible"])
        legacy = binary_certificate(-3, 35)
        self.assertEqual(legacy["fixed"], 3)
        self.assertEqual(legacy["error_bound_for_strict_gain_vs_fixed"], "3/35")

    def test_missing_or_empty_or_tied_inputs_rejected(self):
        with self.assertRaises(ValueError):
            fixed_regret([])
        with self.assertRaises(ValueError):
            conditional_regret([("e", 1)], {})
        with self.assertRaises(ValueError):
            binary_certificate(0, 2)
