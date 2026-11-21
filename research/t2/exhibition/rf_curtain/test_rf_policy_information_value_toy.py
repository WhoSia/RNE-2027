"""RF06 policy-value mathematical toy tests, never live traffic or CSI."""
import json
import unittest
from fractions import Fraction
from rf_policy_information_value_toy import (
    evaluate_information_value, frozen_policy_summary, synthetic_delta_cost
)


class RF06ExactPolicyValueTests(unittest.TestCase):
    def test_no_sensor_regret_and_oracle(self):
        r=evaluate_information_value(())
        self.assertEqual(r["expected_toy_cost"],Fraction(0))
        self.assertEqual(r["perfect_state_oracle_toy_cost"],Fraction(-1))
        self.assertEqual(r["regret_relative_to_oracle"],Fraction(1))
        self.assertEqual(r["policy"]["()"],"baseline")

    def test_aggregate_treats_only_both(self):
        r=evaluate_information_value(("aggregate_count",))
        self.assertEqual(r["expected_toy_cost"],Fraction(-1,2))
        self.assertEqual(r["regret_relative_to_oracle"],Fraction(1,2))
        self.assertEqual(r["policy"]["(2,)"],"hypothetical_treatment")
        self.assertEqual(r["policy"]["(1,)"],"baseline")

    def test_local_pocket_probe_one_bit_beats_aggregate(self):
        coarse=evaluate_information_value(("aggregate_count",))
        direct=evaluate_information_value(("pocket_probe",))
        self.assertGreater(coarse["full_state_information_bits"],direct["full_state_information_bits"])
        self.assertEqual(direct["expected_toy_cost"],Fraction(-1))
        self.assertEqual(direct["regret_relative_to_oracle"],0)

    def test_hypothetical_rf_or_and_downstream(self):
        rf=evaluate_information_value(("any_rf_change",))
        self.assertEqual(rf["expected_toy_cost"],Fraction(-1,4))
        self.assertEqual(rf["regret_relative_to_oracle"],Fraction(3,4))
        self.assertEqual(rf["policy"]["(1,)"],"hypothetical_treatment")
        downstream=evaluate_information_value(("downstream_probe",))
        self.assertEqual(downstream["expected_toy_cost"],0)
        self.assertEqual(downstream["regret_relative_to_oracle"],1)

    def test_coarse_source_ambiguity_can_still_suffice_for_one_action(self):
        rf_p=evaluate_information_value(("any_rf_change","pocket_probe"))
        self.assertEqual(rf_p["regret_relative_to_oracle"],0)
        self.assertEqual(rf_p["expected_toy_cost"],-1)
        self.assertEqual(evaluate_information_value(
            ("aggregate_count","pocket_probe"))["regret_relative_to_oracle"],0)

    def test_stationary_motion_only_and_tie_break(self):
        m=evaluate_information_value(("motion_event",))
        self.assertEqual(m["expected_toy_cost"],0)
        self.assertEqual(m["regret_relative_to_oracle"],1)

    def test_nonuniform_prior_is_applied(self):
        a=evaluate_information_value((),weights=(7,1,1,1))
        self.assertEqual(a["perfect_state_oracle_toy_cost"],Fraction(-2,5))
        self.assertEqual(a["expected_toy_cost"],0)
        self.assertEqual(a["regret_relative_to_oracle"],Fraction(2,5))
        self.assertEqual(evaluate_information_value(("pocket_probe",),weights=(7,1,1,1))[
                         "regret_relative_to_oracle"],0)

    def test_bad_data_and_unknown_sensor(self):
        for channels in (["pocket_probe"],("bad_sensor",),
                         ("pocket_probe","pocket_probe")):
            with self.subTest(channels=channels),self.assertRaises(ValueError):
                evaluate_information_value(channels)
        with self.assertRaises(ValueError):
            synthetic_delta_cost((3,0))

    def test_results_are_reproducible_and_not_real_policy(self):
        data=frozen_policy_summary()
        self.assertEqual(data,frozen_policy_summary())
        o=json.loads(data)
        self.assertEqual(o["status"],"ARBITRARY_HYPOTHETICAL_COSTS_NOT_ACTUAL_T2_DELTAJ")
        self.assertEqual(o["cases"]["aggregate"]["regret"],"1/2")
        self.assertEqual(o["cases"]["pocket"]["regret"],"0")


if __name__=="__main__":
    unittest.main()
