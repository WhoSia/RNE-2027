"""No RF hardware involved; locked scalar math contracts for RF04 prereg."""
import json
import math
import unittest

from open_csi_quiet_calibration_analogue import (
    QuietBaseline, compare_two_zones, preregistered_fixture_audit
)


def quiet(values):
    model = QuietBaseline()
    for value in values:
        model.ingest_known_quiet(value)
    model.freeze()
    return model


class QuietOpenCSIAnalogueTests(unittest.TestCase):
    def test_welford_sample_statistics_exact(self):
        q = quiet([9, 10, 11, 10, 10])
        self.assertEqual(q.n, 5)
        self.assertAlmostEqual(q.mean, 10)
        self.assertAlmostEqual(q.m2 / (q.n - 1), 0.5)

    def test_affine_receiver_gain_invariance_in_locked_fixture(self):
        x = [9, 10, 11, 10, 10]
        baseline = quiet(x).score(13)
        transformed = quiet([2*t+7 for t in x]).score(33)
        self.assertAlmostEqual(baseline["z"], transformed["z"], places=12)
        self.assertEqual(baseline["flagged"], transformed["flagged"])

    def test_extra_calibration_noise_breaks_same_threshold(self):
        a = quiet([9, 10, 11, 10, 10]).score(13)
        b = quiet([8, 10, 12, 10, 10]).score(13)
        self.assertTrue(a["flagged"])
        self.assertFalse(b["flagged"])
        self.assertGreater(a["z"], b["z"])

    def test_occupied_bootstrap_absorbs_occupancy_signature(self):
        a = quiet([12, 13, 14, 13, 13]).score(13)
        self.assertEqual(a["z"], 0)
        self.assertFalse(a["flagged"])

    def test_quiet_drift_can_look_like_occupancy(self):
        a = quiet([9, 10, 11, 10, 10]).score(14)
        self.assertTrue(a["flagged"])
        self.assertGreater(a["z"], 5)

    def test_zero_variance_and_insufficient_samples_abstain(self):
        q = quiet([10]*5).score(13)
        self.assertEqual(q["status"], "ABSTAIN_ZERO_VARIANCE")
        self.assertIsNone(q["flagged"])
        a = quiet([10, 11]).score(13)
        self.assertEqual(a["status"], "ABSTAIN_TOO_FEW_QUIET")

    def test_pre_freeze_does_not_make_prediction_or_modify_baseline(self):
        q = QuietBaseline()
        for x in [9, 10, 11]: q.ingest_known_quiet(x)
        out = q.score(13)
        self.assertEqual(out["status"], "ABSTAIN_NOT_FROZEN")
        self.assertEqual(q.n, 3)
        q.freeze()
        with self.assertRaisesRegex(ValueError, "frozen"):
            q.ingest_known_quiet(13)
        self.assertEqual(q.n, 3)

    def test_two_zones_never_claim_physical_cause(self):
        q = {"pocket":quiet([9,10,11,10,10]),
             "downstream":quiet([9,10,11,10,10])}
        r = compare_two_zones(q, {"pocket":13,"downstream":10})
        self.assertEqual(r["status"],"TWO_SCALAR_DEVIATIONS_NOT_CAUSAL_CLASSIFICATION")
        self.assertIsNone(r["cause"])
        m=compare_two_zones(q, {"pocket":13,"downstream":None})
        self.assertEqual(m["status"],"ABSTAIN_MISSING_LINK")
        self.assertIsNone(m["cause"])

    def test_reject_malformed_nonnumeric_and_nonfinite(self):
        for bad in (True, None, float("nan"), float("inf"), "13"):
            with self.subTest(bad=bad),self.assertRaises(ValueError):
                quiet([9,10,11,10,10]).score(bad)
        for n in (0,2,3.0,True):
            with self.subTest(n=n),self.assertRaises(ValueError):
                QuietBaseline(min_samples=n)
        for t in (0,-1,float("inf")):
            with self.subTest(t=t),self.assertRaises(ValueError):
                quiet([9,10,11,10,10]).score(13,threshold=t)

    def test_locked_fixture_complete_and_deterministic(self):
        a=preregistered_fixture_audit()
        self.assertEqual(a,preregistered_fixture_audit())
        self.assertEqual(a["evidence"],"SYNTHETIC_MATH_ONLY_NOT_RF_DATA")
        self.assertTrue(a["original"]["flagged"])
        self.assertEqual(a["original"]["z"],a["affine_gain"]["z"])
        self.assertFalse(a["higher_quiet_variance"]["flagged"])
        self.assertFalse(a["occupied_bootstrap_contamination"]["flagged"])
        self.assertTrue(a["quiet_drift"]["flagged"])
        self.assertEqual(a["zero_variance"]["status"],"ABSTAIN_ZERO_VARIANCE")


if __name__=="__main__":
    unittest.main()
