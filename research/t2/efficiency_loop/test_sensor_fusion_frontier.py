from fractions import Fraction as F
from unittest import TestCase
from sensor_fusion_frontier import incremental_value,boundary,report

class FrontierTests(TestCase):
    def test_exact_zero_noise_gives_extra_value(self):
        self.assertGreater(incremental_value(F(0),F(1,10)),20)
    def test_large_mode_noise_destroys_arrival_increment(self):
        self.assertAlmostEqual(incremental_value(F(1,10),F(1,10)),0,places=5)
    def test_breakpoint_bracket(self):
        b=boundary(F(1,10))
        self.assertGreater(b,0.025)
        self.assertLess(b,0.04)
    def test_causal_budget_cases(self):
        r=report()['availability_and_cost_examples']
        self.assertEqual(r['both_predecision']['sources'],('structure','arrival'))
        self.assertEqual(r['forecast_late']['sources'],('structure',))
        self.assertEqual(r['cost_budget_one']['sources'],('structure',))
        self.assertEqual(r['no_budget']['sources'],())
