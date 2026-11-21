"""Regression: checkpoint_at=0 is valid and must be resumable."""
import pickle
import unittest
from dual_lane_v11 import DualConfig, run
from spatial_v10 import Config, arrivals


class InitialCheckpointBoundaryTests(unittest.TestCase):
    def test_zero_checkpoint_replays_uninterrupted_for_trace_and_gap_confirmation(self):
        for confirm in (1, 2, 3):
            for trace in (False, True):
                with self.subTest(confirm=confirm, trace=trace):
                    c = DualConfig(base=Config(duration_s=240, seed=37,
                                               demand_vph=1800, left_fraction=.5),
                                   allow_lane_changes=True, through_B_share=.5,
                                   receiver_mode='cells', receiver_slots=4,
                                   lane_change_gap_confirmation_s=confirm)
                    events = arrivals(c.base)
                    cp = run(c, events, trace=trace, checkpoint_at=0)
                    self.assertEqual(cp['next_tick'], 0)
                    stored_bytes = pickle.dumps(cp, protocol=4)
                    self.assertEqual(run(c, events, trace=trace),
                                     run(c, events, trace=trace, resume_from=cp))
                    self.assertEqual(stored_bytes, pickle.dumps(cp, protocol=4))

    def test_existing_nonzero_checkpoint_replay_remains_valid(self):
        c = DualConfig(base=Config(duration_s=240, seed=41),
                       receiver_mode='cells', receiver_slots=4)
        events = arrivals(c.base)
        for tick in (1, 84, 239):
            with self.subTest(tick=tick):
                cp = run(c, events, checkpoint_at=tick)
                self.assertEqual(run(c, events), run(c, events, resume_from=cp))

    def test_boolean_checkpoint_boundaries_are_rejected(self):
        c = DualConfig(base=Config(duration_s=240),
                       receiver_mode='cells', receiver_slots=4)
        events = arrivals(c.base)
        for bad in (True, False, -1, 240, 1.5):
            with self.subTest(bad=bad):
                with self.assertRaisesRegex(ValueError, 'invalid checkpoint tick'):
                    run(c, events, checkpoint_at=bad)

    def test_malformed_negative_checkpoint_boundary_is_rejected(self):
        c = DualConfig(base=Config(duration_s=240),
                       receiver_mode='cells', receiver_slots=4)
        events = arrivals(c.base)
        cp = run(c, events, checkpoint_at=0)
        cp['next_tick'] = -1
        with self.assertRaisesRegex(ValueError, 'invalid checkpoint boundary'):
            run(c, events, resume_from=cp)


if __name__ == '__main__':
    unittest.main()
