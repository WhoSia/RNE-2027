import unittest
from dataclasses import replace
from link_supply_v19 import ReceivingPolicy,TwoMovementLink

class PriorityTests(unittest.TestCase):
    def test_blockage_requires_shared_receiving_geometry(self):
        p=ReceivingPolicy(capacity_S=1,capacity_L=1,green_S=60,
                          green_L=0,admission_priority="L_first")
        independent=TwoMovementLink(p,20,20)
        common=TwoMovementLink(replace(p,shared_receiver=True),20,20)
        for t in range(120):
            independent.tick(t);common.tick(t)
        self.assertGreater(independent.finished["S"],0)
        self.assertEqual(common.finished["S"],0)
    def test_competition_priority_changes_straight_completion(self):
        p=ReceivingPolicy(capacity_S=1,capacity_L=1,green_S=60,
                          green_L=0,shared_receiver=True)
        s=TwoMovementLink(p,20,20)
        l=TwoMovementLink(replace(p,admission_priority="L_first"),20,20)
        for t in range(120):
            s.tick(t);l.tick(t)
        self.assertGreater(s.finished["S"],l.finished["S"])
    def test_alternating_priority_is_deterministic(self):
        p=ReceivingPolicy(admission_priority="alternate",shared_receiver=True)
        a=TwoMovementLink(p,25,25);b=TwoMovementLink(p,25,25)
        for t in range(90):
            a.tick(t);b.tick(t)
        self.assertEqual(a.result(),b.result())

if __name__=="__main__":unittest.main()
