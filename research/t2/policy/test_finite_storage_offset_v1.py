"""D48 finite-link policy acceptance tests (stdlib, no field claim)."""
import unittest
from finite_storage_offset_v1 import (Config,platoons,simulate,sweep,efficiency_key,fairness_key)

class FiniteLinkTests(unittest.TestCase):
    def test_invalid_config(self):
        for kw in ({'east_link_capacity':0},{'west_link_capacity':-1},
                   {'green_s':61},{'offset_B_s':60},{'travel_s':0},
                   {'horizon_s':16},{'cycle_s':1.5},{'offset_B_s':True}):
            with self.subTest(kw=kw),self.assertRaises(ValueError):
                Config(**kw)

    def test_invalid_arrivals(self):
        for seq in ((2,1),(-1,),(600,),(1.5,)):
            with self.subTest(seq=seq),self.assertRaises(ValueError):
                simulate(seq,[],Config())

    def test_no_arrivals(self):
        r=simulate([],[],Config())
        self.assertEqual((r.total_arrivals,r.total_completed,r.total_unserved),(0,0,0))
        self.assertIsNone(r.mean_delay_s)

    def test_capacity_bound(self):
        for cap in (1,2,3,8,20):
            p=Config(east_link_capacity=cap,west_link_capacity=cap)
            for r in sweep(platoons(6,18),platoons(6,18),p):
                self.assertLessEqual(r.east.max_link_occupancy,cap)
                self.assertLessEqual(r.west.max_link_occupancy,cap)

    def test_per_direction_conservation(self):
        p=Config(east_link_capacity=3,west_link_capacity=7)
        for r in sweep(platoons(6,18),platoons(6,12),p):
            for d in (r.east,r.west):
                self.assertEqual(d.arrivals,d.completed+d.unserved)
                self.assertEqual(d.unserved,d.waiting_source_end+d.on_link_end)

    def test_blocking_with_small_link(self):
        r=simulate(platoons(6,18),[],Config(east_link_capacity=2))
        self.assertGreater(r.east.blocked_green_seconds,0)
        self.assertEqual(r.east.max_link_occupancy,2)

    def test_nonbinding_matches_D47(self):
        from bidirectional_offset_v1 import Parameters,simulate as prior
        e,w=platoons(6,12),platoons(6,16)
        for offset in (0,8,12,16,30,48,59):
            a=simulate(e,w,Config(offset_B_s=offset,
                                   east_link_capacity=1000,west_link_capacity=1000))
            b=prior(e,w,Parameters(offset_B_s=offset))
            self.assertEqual(a.total_unserved,b.total_unserved)
            self.assertAlmostEqual(a.mean_delay_s,b.network_mean_delay_s)

    def test_no_completions_are_missing_not_zero(self):
        r=simulate([0],[0],Config(horizon_s=17,travel_s=16,offset_B_s=20))
        self.assertIsNone(r.mean_delay_s)
        self.assertEqual(r.total_unserved,2)

    def test_all_green_offset_independent(self):
        p=Config(cycle_s=10,green_s=10,travel_s=3,horizon_s=100,
                 east_link_capacity=20,west_link_capacity=20)
        v=sweep(platoons(5,6,10),platoons(5,6,10),p)
        self.assertEqual(len({x.mean_delay_s for x in v}),1)

    def test_efficiency_and_fairness_keys(self):
        v=sweep(platoons(6,12),platoons(6,12),
                Config(east_link_capacity=100,west_link_capacity=100))
        a=min(v,key=efficiency_key)
        b=min(v,key=fairness_key)
        self.assertLessEqual(a.mean_delay_s,b.mean_delay_s)
        self.assertLessEqual(b.max_direction_mean_delay_s,a.max_direction_mean_delay_s)

    def test_no_same_tick_space_reuse(self):
        p=Config(cycle_s=10,green_s=10,travel_s=1,horizon_s=10,
                 east_link_capacity=1,west_link_capacity=1)
        r=simulate([0,1],[],p)
        self.assertEqual(r.east.blocked_green_seconds,1)
        self.assertEqual(r.east.completed,2)
        self.assertEqual(r.east.mean_trip_s,1.5)

    def test_horizon_censoring(self):
        p=Config(horizon_s=60,travel_s=16,east_link_capacity=1,west_link_capacity=1)
        r=simulate([0]*30,[0]*30,p)
        self.assertGreater(r.total_unserved,0)
        self.assertEqual(r.total_arrivals,r.total_completed+r.total_unserved)

if __name__=="__main__":
    unittest.main()
