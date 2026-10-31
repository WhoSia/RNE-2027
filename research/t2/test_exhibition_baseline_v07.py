"""Regression checks for the T2 finite-pocket exhibition baseline."""
import unittest
from dataclasses import replace
from exhibition_baseline_v07 import Scenario,capacity,greens,arrivals,simulate,signal_service_ceiling

class BaselineTests(unittest.TestCase):
    def test_length_to_slots(self):
        self.assertEqual(capacity(Scenario(pocket_m=35,standing_pitch_m=7)),5)
        self.assertEqual(capacity(Scenario(pocket_m=13.9,standing_pitch_m=7)),1)
        self.assertEqual(capacity(Scenario(pocket_m=0)),0)

    def test_phases_never_conflict(self):
        for phase in ('leading','lagging'):
            c=Scenario(phase=phase)
            flags=[greens(c,t) for t in range(c.cycle_s)]
            self.assertEqual(sum(x for x,y in flags),c.through_green_s)
            self.assertEqual(sum(y for x,y in flags),c.left_green_s)
            self.assertTrue(all(not(x and y) for x,y in flags))
            with self.assertRaises(ValueError):
                capacity(replace(c,cycle_s=80))

    def test_conservation_and_cycle_metrics(self):
        c=Scenario(duration_s=600,demand_vph=1800,pocket_m=21)
        r=simulate(c)
        self.assertEqual(r['arrivals'],r['total_exits']+r['remaining'])
        self.assertLessEqual(r['max_pocket_queue'],3)
        self.assertEqual(len(r['cycles']),5)
        self.assertEqual(r['cycles'][-1]['through_exits_cumulative'],r['through_exits'])
        self.assertEqual(r['cycles'][-1]['left_exits_cumulative'],r['left_exits'])

    def test_paired_inputs(self):
        base=Scenario(duration_s=600,demand_vph=1800,seed=99)
        stream=arrivals(base)
        results=[simulate(replace(base,pocket_m=L),stream)
                 for L in (14,28,42)]
        self.assertEqual({r['arrivals'] for r in results},{300})
        for r in results:
            self.assertEqual(r['total_exits']+r['remaining'],300)

    def test_all_through_negative_control(self):
        c=Scenario(duration_s=600,demand_vph=1800,left_fraction=0)
        stream=arrivals(c)
        x=simulate(replace(c,pocket_m=7),stream)
        y=simulate(replace(c,pocket_m=70),stream)
        self.assertEqual(x['through_exits'],y['through_exits'])
        self.assertEqual(x['spillback_block_seconds'],0)
        self.assertEqual(y['spillback_block_seconds'],0)

    def test_exact_signal_service_ceiling(self):
        c=Scenario(duration_s=120,cycle_s=120,through_green_s=50,
                   left_green_s=35,through_headway_s=2,left_headway_s=2)
        self.assertEqual(signal_service_ceiling(c),{'left':18,'through':25})
        c=replace(c,duration_s=480,demand_vph=2700)
        r=simulate(c)
        self.assertLessEqual(r['left_exits'],r['signal_service_ceiling_left'])
        self.assertLessEqual(r['through_exits'],r['signal_service_ceiling_through'])

    def test_zero_demand_and_no_pocket(self):
        c=Scenario(duration_s=60,demand_vph=0,pocket_m=0)
        r=simulate(c)
        self.assertEqual((r['arrivals'],r['total_exits'],r['remaining']),(0,0,0))
        c=Scenario(duration_s=60,demand_vph=3600,left_fraction=1,pocket_m=0)
        r=simulate(c)
        self.assertEqual(r['total_exits'],0)
        self.assertEqual(r['remaining'],60)
        self.assertGreater(r['spillback_block_seconds'],0)

if __name__=='__main__':
    unittest.main(verbosity=2)
