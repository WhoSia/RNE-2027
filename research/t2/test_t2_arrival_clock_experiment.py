"""T2 randomized request-clock and green-only signal envelope contracts."""
import collections
import unittest
from spatial_v10 import Config, arrivals
from dual_lane_v11 import run, DualConfig
from t2_arrival_clock_experiment import generate, FAMILIES, time_hash, tape_hash
from t2_green_envelope_arrival_test import GREEN_TICKS, TEST_SEEDS, signal_plan

class ArrivalClockContracts(unittest.TestCase):
    def test_legacy_preserved_and_seeds_do_not_change_timestamps(self):
        base=Config(duration_s=240,demand_vph=1800,seed=88,left_fraction=.45)
        self.assertEqual(generate(base,'legacy_deterministic'),arrivals(base))
        times=[tuple(t for t,_ in generate(Config(duration_s=240,demand_vph=1800,seed=seed), 'legacy_deterministic')) for seed in TEST_SEEDS]
        self.assertEqual(len(set(times)),1)

    def test_independent_random_clocks_are_seed_sensitive(self):
        base=Config(duration_s=240,demand_vph=1800,seed=88,left_fraction=.45)
        for family in FAMILIES:
            self.assertEqual(generate(base,family),generate(base,family))
        for family in ('fixed_count_uniform','poisson_exponential'):
            times={time_hash(generate(Config(duration_s=240,demand_vph=1800,seed=s),family)) for s in TEST_SEEDS}
            self.assertEqual(len(times),8)

    def test_fixed_total_and_poisson_change_event_statistics(self):
        fixed=[generate(Config(duration_s=240,demand_vph=1800,seed=s), 'fixed_count_uniform') for s in TEST_SEEDS]
        self.assertTrue(all(len(tape)==120 for tape in fixed))
        poisson=[generate(Config(duration_s=240,demand_vph=1800,seed=s), 'poisson_exponential') for s in TEST_SEEDS]
        self.assertGreater(len({len(tape) for tape in poisson}),1)
        self.assertTrue(any(max(collections.Counter(t for t,_ in tape).values(),default=0)>1 for tape in fixed))
        for tape in fixed+poisson:
            self.assertTrue(all(0<=t<240 and route in ('L','S') for t,route in tape))
            self.assertEqual(list(tape),sorted(tape,key=lambda x:x[0]))
            self.assertEqual(len(tape_hash(tape)),64)

    def test_synthetic_plan_is_three_separated_intervals_not_real_yellow(self):
        self.assertEqual(GREEN_TICKS,(4,8,12,20))
        self.assertEqual(signal_plan(4),((84,87,'-'),(87,91,'L'),(91,120,'-')))
        for width in GREEN_TICKS:
            config=DualConfig(base=Config(duration_s=240,seed=88), receiver_mode='cells',receiver_slots=4)
            events=generate(config.base,'fixed_count_uniform')
            cp=run(config,events,checkpoint_at=84)
            result=run(config,events,resume_from=cp,phase_overrides=signal_plan(width))
            self.assertEqual(result['generated'],result['remaining']+result['network_out_S']+result['network_out_L'])
        for invalid in (0,True,3,21,8.0,None):
            with self.assertRaises(ValueError):signal_plan(invalid)

    def test_unregistered_clock_rejected(self):
        with self.assertRaisesRegex(ValueError,'unknown arrival-clock'):
            generate(Config(),'not_a_clock')

if __name__=='__main__':unittest.main()
