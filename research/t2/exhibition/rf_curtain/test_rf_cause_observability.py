"""RF06-B math-only preregistered toy result checks; no wireless CSI samples."""
import json
import math
import unittest
from fractions import Fraction
from itertools import combinations

from rf_cause_observability import (
    STATES, SENSORS, normalized_prior, partition, study,
    minimum_full_state_sensor_sets, linear_two_state_observability,
    frozen_examples_json
)


class CauseObservabilityContracts(unittest.TestCase):
    def test_prior_normalization_and_abuse(self):
        self.assertEqual(normalized_prior(), (Fraction(1,4),)*4)
        self.assertEqual(normalized_prior((7,1,1,1)),
                         (Fraction(7,10),Fraction(1,10),Fraction(1,10),Fraction(1,10)))
        for weights in ((0,0,0,0),(-1,1,1,1),(1,2,3),
                        (1,1,1,True),(1,1,1,float("nan")),
                        (1,1,1,"1")):
            with self.subTest(weights=weights), self.assertRaises(ValueError):
                normalized_prior(weights)

    def test_four_state_entropy_and_single_channel_information(self):
        self.assertEqual(len(STATES),4)
        self.assertAlmostEqual(study(("aggregate_count",))["observation_entropy_bits"],1.5)
        self.assertAlmostEqual(study(("any_rf_change",))["observation_entropy_bits"],
                               -(1/4)*math.log2(1/4)-(3/4)*math.log2(3/4))
        self.assertAlmostEqual(study(("pocket_probe",))["observation_entropy_bits"],1.)
        self.assertAlmostEqual(study(("motion_event",))["observation_entropy_bits"],0.)

    def test_risk_of_coarse_sensors_for_complete_state(self):
        expected={
            ("aggregate_count",):Fraction(1,4),
            ("any_rf_change",):Fraction(1,2),
            ("pocket_probe",):Fraction(1,2),
            ("motion_event",):Fraction(3,4),
            ("any_rf_change","pocket_probe"):Fraction(1,4),
            ("aggregate_count","pocket_probe"):Fraction(0),
            ("pocket_probe","downstream_probe"):Fraction(0),
        }
        for channels,error in expected.items():
            with self.subTest(channels=channels):
                self.assertEqual(study(channels)["bayes_error_fraction"],error)

    def test_information_not_equivalent_to_pocket_target_risk(self):
        high_info=study(("aggregate_count",),target="pocket")
        low_info=study(("pocket_probe",),target="pocket")
        self.assertGreater(high_info["observation_entropy_bits"],
                           low_info["observation_entropy_bits"])
        self.assertEqual(high_info["bayes_error_fraction"],Fraction(1,4))
        self.assertEqual(low_info["bayes_error_fraction"],Fraction(0))

    def test_aliasing_pocket_vs_downstream_exact(self):
        groups=partition(("aggregate_count",))
        self.assertEqual(groups[(1,)],((0,1),(1,0)))
        rf=partition(("any_rf_change",))
        self.assertEqual(set(rf[(1,)]),{(0,1),(1,0),(1,1)})
        complement=partition(("any_rf_change","pocket_probe"))
        self.assertEqual(complement[(1,1)],((1,0),(1,1)))

    def test_minimum_identifying_set_has_two_ideal_channels(self):
        winners=minimum_full_state_sensor_sets()
        self.assertEqual({len(x) for x in winners},{2})
        self.assertIn(("pocket_probe","downstream_probe"),winners)
        self.assertIn(("aggregate_count","pocket_probe"),winners)
        self.assertIn(("aggregate_count","downstream_probe"),winners)
        self.assertTrue(all(study((x,))["bayes_error_fraction"]>0 for x in SENSORS))
        self.assertNotIn(("aggregate_count","any_rf_change"),winners)

    def test_equal_time_dynamics_fails_but_separated_sensors_identify(self):
        out=linear_two_state_observability(1,1)
        self.assertEqual(out["determinant"],Fraction(0))
        self.assertFalse(out["observable_rank_2"])
        self.assertEqual(out["two_immediate_sensor_matrix_determinant"],-1)

    def test_near_equal_dynamics_is_formally_but_weakly_observable(self):
        out=linear_two_state_observability(Fraction(4,5),Fraction(81,100))
        self.assertEqual(out["determinant"],Fraction(1,100))
        self.assertTrue(out["observable_rank_2"])
        self.assertEqual(out["two_states_first_aggregate"],1)
        self.assertEqual(out["pocket_only_next_reading"],Fraction(4,5))
        self.assertEqual(out["downstream_only_next_reading"],Fraction(81,100))
        self.assertEqual(out["two_states_next_reading_gap"],Fraction(1,100))

    def test_asymmetric_prior_no_silent_uniform_reuse(self):
        out=study(("aggregate_count",), weights=(7,1,1,1),target="pocket")
        self.assertEqual(out["bayes_error_fraction"],Fraction(1,10))
        self.assertNotAlmostEqual(out["observation_entropy_bits"],1.5)
        self.assertEqual(study(("pocket_probe",),weights=(7,1,1,1),
                               target="pocket")["bayes_error_fraction"],0)

    def test_invalid_channels_target_and_dynamics(self):
        for c in ((),("made_up",),("pocket_probe","pocket_probe")):
            with self.subTest(c=c), self.assertRaises(ValueError): partition(c)
        with self.assertRaises(ValueError): study(("pocket_probe",),target="real_signal_safety")
        for coeff in (True, None, float("nan"), float("inf"), "0.8"):
            with self.subTest(coeff=coeff),self.assertRaises(ValueError):
                linear_two_state_observability(coeff,1)

    def test_json_deterministic_and_source_status(self):
        j=frozen_examples_json()
        self.assertEqual(j,frozen_examples_json())
        data=json.loads(j)
        self.assertEqual(data["evidence_status"],"MATHEMATICAL_TOY_NOT_MEASURED_SENSOR")
        self.assertEqual(data["cases"]["aggregate"]["bayes_error"],"1/4")
        self.assertEqual(data["cases"]["pocket_target_local"]["bayes_error"],"0")
        self.assertEqual(data["near_equal_dynamics"]["determinant"],"1/100")


if __name__ == "__main__":
    unittest.main()
