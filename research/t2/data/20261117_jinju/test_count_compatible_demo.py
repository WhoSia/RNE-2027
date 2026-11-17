from unittest import TestCase

from count_compatible_demo import counts_window


class CountCompatibleTest(TestCase):
    def test_incomplete_order_can_reverse_the_preferred_plan(self):
        result = counts_window(8)
        self.assertEqual(result["sequences"], 14 * 14 + 14)
        lo, hi = result["lead_minus_lag_bounds_s"]
        self.assertLess(lo, 0)
        self.assertGreater(hi, 0)
        self.assertEqual(result["minimax_regret_s"], {"lag": -lo, "lead": hi})
        for key in ("low_witness", "high_witness"):
            delta, order, lag, lead = result[key]
            self.assertEqual(sorted(move for _, move in order), ["L", "T"])
            self.assertEqual(delta, lead - lag)
            self.assertTrue(all(8 <= tick < 22 for tick, _ in order))
