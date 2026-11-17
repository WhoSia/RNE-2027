import unittest
from dataclasses import replace
from d50_turn_pocket import Vehicle,periodic_arrivals,Config as PriorConfig,simulate as prior_simulate
from d51_phase_order import Params,phase,simulate,key

class OrderTests(unittest.TestCase):
    def test_config(self):
        for kw in ({'cycle_s':0},{'left_green_s':0},{'through_green_s':49},
                   {'left_capacity':0},{'through_capacity':0},{'left_first':1},{'horizon_s':0}):
            with self.subTest(kw=kw),self.assertRaises(ValueError):Params(**kw)
    def test_order(self):
        x=Params()
        self.assertEqual([phase(t,x) for t in (0,23,24,35,36)],['T','T','L','L','R'])
        y=replace(x,left_first=True)
        self.assertEqual([phase(t,y) for t in (0,11,12,35,36)],['L','L','T','T','R'])
    def test_validation(self):
        for xs in ((Vehicle(-1,'T',0),),(Vehicle(600,'L',0),),
                   (Vehicle(1,'L',0),Vehicle(0,'T',1)),
                   (Vehicle(0,'T',0),Vehicle(0,'L',0)),(Vehicle(0,'X',0),)):
            with self.subTest(xs=xs),self.assertRaises(ValueError):simulate(xs,Params())
    def test_empty(self):
        for lead in (False,True):
            r=simulate([],Params(left_first=lead))
            self.assertEqual(r.unserved,0)
            self.assertIsNone(r.mean_vehicle_delay_s)
    def test_conservation_and_occupancy(self):
        xs=periodic_arrivals(ncycles=6,per_cycle=24,left_every=2)
        for cap in (1,2,4,12):
            for lead in (False,True):
                r=simulate(xs,Params(left_capacity=cap,left_first=lead))
                self.assertEqual(r.arrivals_left,r.completed_left+r.unserved_left)
                self.assertEqual(r.arrivals_through,r.completed_through+r.unserved_through)
                self.assertLessEqual(r.maximum_left_occupancy,cap)
                self.assertLessEqual(r.maximum_through_occupancy,12)
    def test_lagging_agrees_with_d50(self):
        xs=periodic_arrivals()
        for cap in (1,2,4,8,12):
            a=simulate(xs,Params(left_capacity=cap))
            b=prior_simulate(xs,PriorConfig(left_capacity=cap,mode='shared'))
            self.assertEqual((a.completed_through,a.completed_left,a.unserved_through,a.unserved_left),
                             (b.completed_through,b.completed_left,b.unserved_through,b.unserved_left))
            self.assertEqual(a.mean_through_delay_s,b.mean_through_delay_s)
            self.assertEqual(a.mean_left_delay_s,b.mean_left_delay_s)
            self.assertEqual(a.through_behind_left_seconds,b.blocked_through_behind_left_seconds)
    def test_no_left(self):
        xs=tuple(Vehicle(i,'T',i) for i in range(12))
        for lead in (False,True):
            r=simulate(xs,Params(left_first=lead))
            self.assertEqual(r.completed_through,12)
            self.assertEqual(r.completed_left,0)
    def test_no_through(self):
        xs=tuple(Vehicle(i,'L',i) for i in range(12))
        for lead in (False,True):
            r=simulate(xs,Params(left_first=lead))
            self.assertEqual(r.completed_left,12)
    def test_head_block_event(self):
        xs=(Vehicle(0,'L',0),Vehicle(0,'L',1),Vehicle(0,'T',2))
        r=simulate(xs,Params(left_capacity=1,horizon_s=40))
        self.assertGreater(r.through_behind_left_seconds,0)
    def test_no_same_tick_reuse(self):
        xs=tuple(Vehicle(0,'L',i) for i in range(3))
        r=simulate(xs,Params(cycle_s=4,through_green_s=1,left_green_s=2,left_capacity=1,horizon_s=12,left_first=True))
        self.assertEqual(r.completed_left,3)
        self.assertGreater(r.left_head_blocked_seconds,0)
    def test_fair_comparison(self):
        x=periodic_arrivals()
        a=simulate(x,Params(left_first=True))
        b=simulate(x,Params(left_first=False))
        self.assertEqual((a.arrivals_through,a.arrivals_left),(b.arrivals_through,b.arrivals_left))
    def test_periodic_wrap(self):
        p=Params(left_first=True)
        self.assertEqual(phase(0,p),phase(60,p))
        self.assertEqual(phase(18,p),phase(78,p))

if __name__=='__main__':unittest.main()
