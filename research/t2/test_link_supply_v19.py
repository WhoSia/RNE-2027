import unittest
from dataclasses import replace
from link_supply_v19 import ReceivingPolicy,TwoMovementLink

class LinkSupplyTests(unittest.TestCase):
    def test_empty(self):
        m=TwoMovementLink(ReceivingPolicy())
        for t in range(100):m.tick(t)
        self.assertEqual(m.finished,{"S":0,"L":0})
    def test_mass(self):
        m=TwoMovementLink(ReceivingPolicy(capacity_L=2,green_L=15),30,20)
        for t in range(360):m.tick(t,int(t%3==0),int(t%4==0))
        self.assertEqual(m.generated,{"S":150,"L":110})
    def test_independent_receiving(self):
        p=ReceivingPolicy(capacity_S=1,capacity_L=1,green_S=60,green_L=0)
        a=TwoMovementLink(p,0,20)
        b=TwoMovementLink(replace(p,shared_receiver=True),0,20)
        for t in range(120):
            a.tick(t,20 if t==0 else 0)
            b.tick(t,20 if t==0 else 0)
        self.assertGreater(a.finished["S"],b.finished["S"])
    def test_signal(self):
        m=TwoMovementLink(ReceivingPolicy(cycle_s=10,green_S=2,green_L=0,headway_S=1),100)
        for t in range(100):m.tick(t)
        self.assertTrue(all(t%10<2 for t,movement in m.departures))
    def test_invalid(self):
        for p in (ReceivingPolicy(capacity_L=0),ReceivingPolicy(green_S=61),
                  ReceivingPolicy(admission_priority="bogus")):
            with self.assertRaises(ValueError):TwoMovementLink(p)

if __name__=="__main__":unittest.main()
