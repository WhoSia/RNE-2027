"""Unit and metrological checks; no external simulation software required."""
import unittest
from dataclasses import replace
from spatial_v05 import Config, validate, signal, simulate, build_arrivals
from experiment_v05 import order_witness, summarize, FORKS, CAPS, MODES

class ModelV05Tests(unittest.TestCase):
    def test_capacity_is_physically_feasible_for_both_forks(self):
        self.assertEqual(validate(Config(fork_cells=-13,bay_limit=4)),6)
        self.assertEqual(validate(Config(fork_cells=-21,bay_limit=4)),10)
        with self.assertRaises(ValueError):
            validate(Config(fork_cells=-13,bay_limit=7))
        with self.assertRaises(ValueError):
            validate(Config(fork_cells=-13,bay_limit=0))

    def test_signals_disjoint_and_greens_correct(self):
        for mode in ('leading','lagging'):
            c=Config(signal_mode=mode)
            signals=[signal(c,t) for t in range(c.cycle)]
            self.assertEqual(sum(s for s,l in signals),c.through_green)
            self.assertEqual(sum(l for s,l in signals),c.left_green)
            self.assertFalse(any(s and l for s,l in signals))
        # Historical mode overlaps greens and is not an exclusive protected signal plan.
        c=Config(signal_mode='legacy_overlap')
        self.assertTrue(signal(c,0)==(True,True))
        with self.assertRaises(ValueError):
            validate(Config(cycle=100,through_green=60,left_green=54))

    def test_paired_arrivals_are_identical_across_geometry_capacity_and_phase(self):
        c=Config(duration=320,seed=21)
        arrival=build_arrivals(c)
        for mode in MODES:
            for f in FORKS:
                for k in CAPS:
                    d=replace(c,signal_mode=mode,fork_cells=f,bay_limit=k)
                    self.assertEqual(build_arrivals(d),arrival)
                    r=simulate(d,arrival,audit=True)
                    self.assertEqual(r['stats']['arrivals'],r['stats']['exits']+r['stats']['remaining'])
                    self.assertLessEqual(r['stats']['bay_physical_slots'],10)

    def test_randomized_audited_safety_and_determinism(self):
        for seed in range(6):
            c=Config(duration=450,seed=seed,fork_cells=(-21,-13)[seed%2],bay_limit=(2,4)[seed%2],signal_mode=('leading','lagging')[seed%2])
            a=simulate(c,audit=True,keep_events=True)
            b=simulate(c,audit=True,keep_events=True)
            self.assertEqual(a,b)
            self.assertEqual(a['stats']['arrivals'],a['stats']['exits']+a['stats']['remaining'])
            for t,ident,kind,x in a['events']:
                if kind.startswith('transfer_'):
                    self.assertEqual(x,c.fork_cells+1)

    def test_arrival_plan_rejects_unsorted_and_misrouted(self):
        c=Config(duration=100)
        for bad in (((7,'L','outer'),),((11,'S','upstream'),(2,'L','upstream')),((500,'S','outer'),)):
            with self.assertRaises(ValueError):
                simulate(c,bad)

    def test_order_witness_same_marginals_distinct_throughput(self):
        w=order_witness()
        self.assertTrue(w['same_arrival_times'])
        self.assertTrue(w['same_route_counts'])
        self.assertEqual((w['exits_A'],w['exits_B']),(7,18))
        self.assertEqual((w['through_A'],w['through_B']),(0,11))

    def test_parallel_updating_is_distinct_but_satisfies_invariants(self):
        c=Config(duration=550,seed=4,fork_cells=-21,bay_limit=4,signal_mode='leading')
        arrivals=build_arrivals(c)
        a=simulate(c,arrivals,audit=True)
        b=simulate(replace(c,update_mode='parallel'),arrivals,audit=True)
        self.assertEqual(a['stats']['arrivals'],b['stats']['arrivals'])
        self.assertEqual(b['stats']['arrivals'],b['stats']['exits']+b['stats']['remaining'])
        self.assertNotEqual(a['cycle_exits'],b['cycle_exits'])
        with self.assertRaises(ValueError):
            validate(replace(c,update_mode='unknown'))

if __name__=='__main__':
    unittest.main(verbosity=2)
