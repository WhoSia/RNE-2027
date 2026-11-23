"""P140 frozen rule and objective accounting tests, independent of T2 runs."""
import unittest
import p140_upstream_queue_holdout as p140

class P140Tests(unittest.TestCase):
    def test_policy_map_is_exact(self):
        self.assertEqual(p140.CALENDAR, {
            (0,30):60,(15,0):30,(7,15):60,(23,45):30
        })
    def test_boundary(self):
        s={'outside_A':5,'outside_B':0,'approach_A':3,'approach_B':3,
           'pocket_vehicles':2,'receiver_vehicles':4}
        self.assertEqual(p140.q_upstream(s),13)
        self.assertEqual(p140.choose((7,15),s),60)
        s['outside_A']=6
        self.assertEqual(p140.q_upstream(s),14)
        self.assertEqual(p140.choose((7,15),s),30)
        for off in p140.OFFSETS:
            if off!=(7,15):
                self.assertEqual(p140.choose(off,s),p140.CALENDAR[off])
    def test_never_uses_receiver_occupancy(self):
        s={'outside_A':8,'outside_B':0,'approach_A':3,'approach_B':2,
           'pocket_vehicles':1,'receiver_vehicles':0}
        a=p140.choose((7,15),s)
        s['receiver_vehicles']=4
        self.assertEqual(p140.choose((7,15),s),a)
    def test_regret_invariant(self):
        row={'arms':{'30':{'cost':120},'60':{'cost':100}},
             'choices':{'calendar':60,'guard':30,'fixed30':30,'fixed60':60}}
        self.assertEqual(p140.regret(row,60),0)
        self.assertEqual(p140.regret(row,30),20)
        r=p140.summary([row])
        self.assertEqual(r['guard']['total_regret'],20)
        self.assertEqual(r['calendar']['total_regret'],0)
        self.assertEqual(r['harmful'],1)
        self.assertEqual(r['triggered'],1)

if __name__=='__main__':unittest.main()
