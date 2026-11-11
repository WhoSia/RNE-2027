import unittest
from bidirectional_offset_v1 import (Parameters,simulate,platoons,sweep,
                                     efficiency_key,fairness_key,green)

class TrafficTests(unittest.TestCase):
    def test_invalid_parameters(self):
        for kw in (dict(cycle_s=0),dict(green_s=61),dict(travel_s=0),
                   dict(offset_B_s=60),dict(horizon_s=10,travel_s=10)):
            with self.subTest(kwargs=kw),self.assertRaises(ValueError):
                Parameters(**kw)

    def test_arrival_validation(self):
        with self.assertRaises(ValueError): simulate([2,1],[],Parameters())
        with self.assertRaises(ValueError): simulate([-1],[],Parameters())
        with self.assertRaises(ValueError): simulate([600],[],Parameters())

    def test_empty(self):
        r=simulate([],[],Parameters())
        self.assertEqual((r.total_completed,r.total_unserved),(0,0))
        self.assertIsNone(r.network_mean_delay_s)

    def test_full_cycle_green(self):
        p=Parameters(cycle_s=10,green_s=10,travel_s=3,horizon_s=90)
        values=sweep([0,1,2,3],[0,1,2,3],p)
        self.assertEqual(len(set(r.network_mean_delay_s for r in values)),1)

    def test_per_direction_conservation(self):
        for r in sweep(platoons(6,12),platoons(6,9),Parameters()):
            self.assertEqual(r.eastbound.arrival_count,
                             r.eastbound.completed+r.eastbound.unserved)
            self.assertEqual(r.westbound.arrival_count,
                             r.westbound.completed+r.westbound.unserved)

    def test_two_direction_completion(self):
        e=platoons(6,12)
        results=sweep(e,e,Parameters())
        self.assertEqual(len(results),60)
        self.assertEqual(simulate(e,e,Parameters()).total_completed,144)

    def test_censoring(self):
        p=Parameters(horizon_s=45,travel_s=16)
        r=simulate([0]*20,[0]*20,p)
        self.assertGreater(r.total_unserved,0)
        self.assertEqual(r.total_completed+r.total_unserved,40)

    def test_rank_prioritizes_unserved(self):
        vals=sweep(platoons(7,20),platoons(7,20),
                   Parameters(horizon_s=430))
        self.assertEqual(min(vals,key=efficiency_key).total_unserved,
                         min(r.total_unserved for r in vals))

    def test_fairness_tradeoff(self):
        vals=sweep(platoons(6,12),platoons(6,12),Parameters())
        eff=min(vals,key=efficiency_key)
        fair=min(vals,key=fairness_key)
        self.assertEqual((eff.offset_B_s,fair.offset_B_s),(8,0))
        self.assertGreater(eff.worst_direction_mean_delay_s,
                           fair.worst_direction_mean_delay_s)

    def test_green_wrap(self):
        p=Parameters()
        self.assertTrue(green(0,59,p))
        self.assertFalse(green(20,0,p))

if __name__=="__main__":
    unittest.main()
