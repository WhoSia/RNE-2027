import unittest
from dataclasses import replace
from d50_turn_pocket import Config,Vehicle,simulate,periodic_arrivals,sweep

class TurnPocketTests(unittest.TestCase):
    def test_invalid_configuration(self):
        for kw in ({'left_capacity':0},{'through_capacity':0},{'cycle_s':0},
                   {'through_green_s':60},{'left_green_s':0},{'mode':'X'},
                   {'left_capacity':True},{'horizon_s':0}):
            with self.subTest(kw=kw),self.assertRaises(ValueError): Config(**kw)

    def test_empty(self):
        r=simulate(())
        self.assertEqual((r.total_arrivals,r.completed_through,r.completed_left),(0,0,0))
        self.assertIsNone(r.mean_through_delay_s)

    def test_vehicle_validation(self):
        cases=((Vehicle(-1,'T',0),),(Vehicle(600,'T',0),),
               (Vehicle(2,'T',0),Vehicle(1,'L',1)),
               (Vehicle(0,'T',0),Vehicle(1,'L',0)),(Vehicle(0,'X',0),))
        for case in cases:
            with self.subTest(case=case),self.assertRaises(ValueError): simulate(case)

    def test_capacity_and_conservation(self):
        for mode in ('shared','independent'):
            for cap in (1,2,4,12):
                r=simulate(periodic_arrivals(),Config(left_capacity=cap,mode=mode))
                self.assertEqual(r.total_arrivals,r.completed_through+r.completed_left+
                                 r.unserved_through+r.unserved_left)
                self.assertLessEqual(r.maximum_left_pocket,cap)
                self.assertLessEqual(r.maximum_through_bay,12)

    def test_separate_feeders_never_trap_through_behind_left(self):
        r=simulate(periodic_arrivals(),Config(left_capacity=1,mode='independent'))
        self.assertEqual(r.blocked_through_behind_left_seconds,0)

    def test_shared_lane_pocket_blockage(self):
        r=simulate(periodic_arrivals(),Config(left_capacity=1,mode='shared'))
        self.assertGreater(r.blocked_through_behind_left_seconds,0)

    def test_shared_pocket_effect_on_through(self):
        xs=periodic_arrivals()
        small=simulate(xs,Config(left_capacity=1,mode='shared'))
        large=simulate(xs,Config(left_capacity=20,mode='shared'))
        self.assertGreater(small.mean_through_delay_s,large.mean_through_delay_s)

    def test_model_comparator(self):
        xs=periodic_arrivals()
        shared=simulate(xs,Config(left_capacity=1,mode='shared'))
        independent=simulate(xs,Config(left_capacity=1,mode='independent'))
        self.assertGreater(shared.blocked_through_behind_left_seconds,
                           independent.blocked_through_behind_left_seconds)

    def test_no_left_arrivals(self):
        xs=tuple(Vehicle(i,'T',i) for i in range(10))
        a=simulate(xs,Config(mode='shared'))
        b=simulate(xs,Config(mode='independent'))
        self.assertEqual(a.mean_through_delay_s,b.mean_through_delay_s)
        self.assertEqual(a.completed_through,b.completed_through)

    def test_no_through_arrivals(self):
        xs=tuple(Vehicle(i,'L',i) for i in range(10))
        a=simulate(xs,Config(mode='shared'))
        b=simulate(xs,Config(mode='independent'))
        self.assertEqual(a.mean_left_delay_s,b.mean_left_delay_s)

    def test_source_fifo_under_shared_mode(self):
        xs=(Vehicle(0,'L',0),Vehicle(0,'L',1),Vehicle(0,'T',2))
        r=simulate(xs,Config(horizon_s=25,left_capacity=1,mode='shared'))
        self.assertGreater(r.blocked_through_behind_left_seconds,0)
        self.assertEqual(r.completed_through,0)

    def test_sweep_count(self):
        self.assertEqual(len(sweep(periodic_arrivals(),capacities=(1,2,3))),6)

    def test_demand_contract(self):
        for kw in ({'left_every':0},{'per_cycle':61},{'ncycles':0},{'phase_s':60}):
            with self.subTest(kw=kw),self.assertRaises(ValueError): periodic_arrivals(**kw)

if __name__=='__main__': unittest.main()
