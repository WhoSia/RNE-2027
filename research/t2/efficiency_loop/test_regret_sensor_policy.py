from fractions import Fraction
from unittest import TestCase
from regret_sensor_policy import optimize, worst_regret, report


class RobustSignalTests(TestCase):
    def test_no_error_oracle(self):
        r = optimize(-113, 31, Fraction(0))
        self.assertEqual((r.left_on_early, r.left_on_late, r.regret), (1,0,0))

    def test_no_useful_forecast_at_fifty_percent(self):
        r = optimize(-113, 31, Fraction(1, 2))
        self.assertEqual(r.left_on_early, r.left_on_late)
        self.assertEqual(r.regret, Fraction(3503,144))

    def test_improvement_beyond_deterministic_rule_threshold(self):
        r = optimize(-113, 31, Fraction(3,10))
        self.assertLess(r.regret, r.fixed_randomized_regret)
        self.assertGreater(r.forecast_follow_regret, r.fixed_deterministic_regret)

    def test_adversary_may_choose_no_error(self):
        self.assertEqual(worst_regret(113,31,Fraction(1,4),0,1), 113)

    def test_bruteforce_grid(self):
        for a,b in ((113,31),(3,35),(5,5)):
            for e in (Fraction(0),Fraction(1,10),Fraction(1,4),Fraction(49,100),Fraction(1,2),Fraction(3,4)):
                ans = optimize(-a,b,e)
                for ai in range(21):
                    for bi in range(21):
                        brute = worst_regret(a,b,e,Fraction(ai,20),Fraction(bi,20))
                        self.assertLessEqual(ans.regret,brute, (a,b,e,ai,bi))

    def test_policy_input_validation(self):
        with self.assertRaises(ValueError): optimize(0,31,Fraction(1,5))
        with self.assertRaises(ValueError): optimize(-31,113,Fraction(-1,5))
        with self.assertRaises(ValueError): worst_regret(113,31,Fraction(1,4),2,0)

    def test_report_has_two_cases(self):
        rows=report()
        self.assertEqual(len(rows['new_seed_337']),6)
        self.assertEqual(len(rows['legacy']),6)
