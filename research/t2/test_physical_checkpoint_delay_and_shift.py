"""PHYS-07 deterministic contracts, future-event isolation and replay checks."""
import unittest
from physical_checkpoint_delay_and_shift import (
    DECISION_TICK, DELAYS, INTERVENTION, REGIMES, SEED_SHIFT,
    make_config, decision, summarize, experiment)
from dual_lane_v11 import run, checkpoint_observation
from spatial_v10 import arrivals


class PHYS07Tests(unittest.TestCase):
    def test_disjoint_seed_windows_and_lags(self):
        self.assertEqual(list(SEED_SHIFT), list(range(32, 40)))
        self.assertEqual(set(SEED_SHIFT) & set(range(32)), set())
        self.assertEqual(DELAYS, (0, 3, 6, 12, 24))
        self.assertTrue(all(0 < DECISION_TICK - d for d in DELAYS))
        self.assertEqual(len(REGIMES), len(set(x[0] for x in REGIMES)))

    def test_phase_plan_does_not_include_past(self):
        self.assertEqual(INTERVENTION[0][0], DECISION_TICK)
        self.assertEqual(INTERVENTION[0][2], '-')
        self.assertEqual(INTERVENTION[1][2], 'L')

    def test_summary_regret_and_pair_scoring(self):
        rows = [dict(seed=0, delta_p60=-5, fixed=True),
                dict(seed=1, delta_p60=10, fixed=True)]
        s = summarize(rows, ('fixed',))
        self.assertEqual(s['oracle_saved'], 5)
        self.assertEqual(s['policies']['fixed']['saved_vs_always_control'], -5)
        self.assertEqual(s['policies']['fixed']['regret_to_hindsight_oracle'], 10)
        self.assertEqual(s['policies']['fixed']['by_seed_saved'], {'0': 5, '1': -10})

    def test_snapshot_does_not_expose_future_arrival_tape(self):
        c = make_config(0, 4, 14., .5)
        tape = list(arrivals(c.base))
        later = [(t, ('L' if route == 'S' else 'S') if t >= 100 else route)
                 for t, route in tape]
        o1 = checkpoint_observation(run(c, tape, checkpoint_at=DECISION_TICK))
        o2 = checkpoint_observation(run(c, later, checkpoint_at=DECISION_TICK))
        self.assertEqual(o1, o2)
        self.assertFalse(any(x in o1 for x in ('events', 'rng', 'future_arrivals')))

    def test_earlier_snapshot_cannot_use_future_state(self):
        c = make_config(2, 4, 28., .5)
        tape = arrivals(c.base)
        for lag in DELAYS:
            o = checkpoint_observation(run(c, tape, checkpoint_at=DECISION_TICK-lag))
            self.assertEqual(o['decision_tick'], DECISION_TICK-lag)
            self.assertGreaterEqual(o['outside_A'], 0)
            self.assertGreaterEqual(o['outside_B'], 0)

    def test_restarted_future_and_counterfactual_conserve_vehicles(self):
        c = make_config(0, 2, 14., .0)
        tape = arrivals(c.base)
        cp = run(c, tape, checkpoint_at=DECISION_TICK)
        self.assertEqual(run(c, tape), run(c, tape, resume_from=cp))
        for result in (run(c, tape, resume_from=cp),
                       run(c, tape, resume_from=cp, phase_overrides=INTERVENTION)):
            self.assertEqual(result['generated'], result['remaining'] +
                             result['network_out_S'] + result['network_out_L'])

    def test_invalid_training_data_rejected_before_simulation(self):
        with self.assertRaisesRegex(ValueError, 'training requires'):
            experiment([], [])


if __name__ == '__main__':
    unittest.main()
