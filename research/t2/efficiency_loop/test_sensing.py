from unittest import TestCase

from d51_phase_order import Params
from sensing import MOVEMENT, PRESENCE, compare
from timing_bounds import exact


class Sensing(TestCase):
    def test_only_predecision_and_deterministic(self):
        p = Params(left_capacity=1, horizon_s=180)
        bins = ((1,1),(2,0),(2,0),(1,1))
        initial = (("",0,0),("",0,1))
        a = compare(3,bins,p,4,PRESENCE,2,initial)
        b = compare(3,bins,p,4,MOVEMENT,2,initial)
        self.assertLessEqual(b["adaptive_regret"], b["fixed"][0])
        self.assertLessEqual(b["adaptive_regret"], a["adaptive_regret"])
        self.assertLess(max(b["fixed"][1]),4)
        self.assertEqual(exact(3,bins,p,initial=initial,decision_tick=4).paths, b["paths"])
