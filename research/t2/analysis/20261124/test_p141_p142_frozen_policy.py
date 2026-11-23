"""Frozen P141 and P142 demand-share guard regression, no simulator execution."""
import unittest
import p141_demand_guard_holdout as a
import p142_new_route_seed_transfer as b

class RuleTests(unittest.TestCase):
    def setup_state(self,q):
        return {'outside_A':q,'outside_B':0,'approach_A':0,'approach_B':0,
                'pocket_vehicles':0,'receiver_vehicles':0}

    def test_frozen_calendar_and_cutoffs(self):
        for module in (a,b):
            self.assertEqual(module.CALENDAR,
                             {(0,30):60,(15,0):30,(7,15):60,(23,45):30})
            self.assertEqual(module.choose((7,15),self.setup_state(13),.5),60)
            self.assertEqual(module.choose((7,15),self.setup_state(14),.5),30)
            self.assertEqual(module.choose((7,15),self.setup_state(30),.75),60)
            for offset in module.OFFSETS:
                if offset!=(7,15):
                    self.assertEqual(module.choose(offset,self.setup_state(90),.5),module.CALENDAR[offset])

    def test_seed_holds_are_disjoint(self):
        self.assertEqual(a.TIME_SEEDS,(89001,89002))
        self.assertEqual(b.TIME_SEEDS,(89101,89102))
        self.assertEqual(a.LABEL_SEEDS,(86001,86002))
        self.assertEqual(b.LABEL_SEEDS,(86101,86102))
        self.assertTrue(set(a.TIME_SEEDS).isdisjoint(b.TIME_SEEDS))
        self.assertTrue(set(a.LABEL_SEEDS).isdisjoint(b.LABEL_SEEDS))

    def test_p141_and_p142_policy_exact_agreement(self):
        for share in (.5,.75):
            for q in (0,10,13,14,16,100):
                s=self.setup_state(q)
                for offset in a.OFFSETS:
                    self.assertEqual(a.choose(offset,s,share),b.choose(offset,s,share))

if __name__=="__main__":
    unittest.main()
