from unittest import TestCase
from two_stage_queue_estimator import ScalarFilter,TwoStageQueueEstimator,synthetic_example

class EstimatorTests(TestCase):
    def test_scalar_kalman_update_keeps_nonnegative_covariance(self):
        f=ScalarFilter(5.,4.)
        f.predict(drift=2,process_variance=1)
        gain=f.observe(9.,4.)
        self.assertTrue(0<gain<1)
        self.assertTrue(7<f.mean<9)
        self.assertTrue(0<=f.variance<5.)
    def test_queue_updates_use_only_timestamped_inputs(self):
        f=TwoStageQueueEstimator()
        a=f.update(20,detector_total=10,probe_left=2,probe_total=5,left_discharge=1)
        with self.assertRaises(ValueError):f.update(20,detector_total=10,probe_left=2,probe_total=5,left_discharge=1)
        self.assertTrue(0<=a['estimated_turn_fraction']<=1)
        self.assertGreaterEqual(a['estimated_queue'],0)
    def test_probe_missing_does_not_imply_zero_turns(self):
        f=TwoStageQueueEstimator(prior_turn_fraction=.6)
        r=f.update(0,detector_total=10,probe_left=0,probe_total=0,left_discharge=1)
        self.assertAlmostEqual(r['estimated_turn_fraction'],.6)
    def test_bad_counts_and_queue_rejected(self):
        f=TwoStageQueueEstimator()
        with self.assertRaises(ValueError):f.update(0,detector_total=3,probe_left=4,probe_total=4,left_discharge=0)
        initial_tick=f.tick
        with self.assertRaises(ValueError):f.update(1,detector_total=3,probe_left=2,probe_total=2,left_discharge=0,queue_measurement=-1)
        self.assertEqual(f.tick,initial_tick)
        f.update(1,detector_total=3,probe_left=2,probe_total=2,left_discharge=0,queue_measurement=1)
    def test_noisy_queue_reader_updates_belief(self):
        f=TwoStageQueueEstimator()
        r=f.update(0,detector_total=20,probe_left=6,probe_total=10,
                   left_discharge=7,queue_measurement=6,queue_measurement_variance=1)
        self.assertLess(abs(r['estimated_queue']-6),2)
    def test_synthetic_example_trends_towards_true_turn_fraction(self):
        series=synthetic_example()
        self.assertEqual(len(series),8)
        self.assertLess(abs(series[-1]['estimated_turn_fraction']-.6),
                        abs(.4-.6))
        self.assertEqual(series[-1]['true_queue'],40)
