"""RF12 mathematical counterexample tests; no real RF signal inputs."""
import unittest
from math import sqrt
from rf12_static_occupancy_audit import features,compare_to_frozen_empty,counterexamples


class RF12Tests(unittest.TestCase):
    def test_empty_and_static_equal_zero_temporal_variance(self):
        a=features([10.,10.,10.,10.]);b=features([15.,15.,15.,15.])
        self.assertEqual(a.temporal_dispersion,0)
        self.assertEqual(b.temporal_dispersion,0)
        self.assertNotEqual(a.amplitude_mean,b.amplitude_mean)

    def test_frozen_baseline_contrast_not_a_calibrated_class(self):
        empty=features([10.,10.,10.,10.]);static=features([15.,15.,15.,15.])
        s=compare_to_frozen_empty(static,empty)
        self.assertEqual(s['absolute_mean_shift'],5)
        self.assertNotIn('predicted_label',s)

    def test_environment_drift_is_identical_to_static_object(self):
        worlds=counterexamples()['worlds']
        self.assertEqual(worlds['static_object'],worlds['environment_drift'])
        self.assertEqual(worlds['static_object']['temporal_dispersion'],0)

    def test_motion_has_positive_temporal_variation(self):
        m=features([10.,12.,14.,16.])
        self.assertAlmostEqual(m.temporal_dispersion,sqrt(5))

    def test_malformed_and_undersampled_are_rejected(self):
        for sample in ([1.],[float('nan'),1.],[float('inf'),1.],[-1.,1.],[True,1.]):
            with self.subTest(sample=sample),self.assertRaises(ValueError):features(sample)

if __name__=='__main__':unittest.main()
