"""Regress v1.7 broad factor inputs and service-window semantics."""
import unittest
from dataclasses import replace
from collections import Counter
from spatial_v10 import Config
from receiving_cells_v15 import ReceivingCells,LinkConfig
from dual_lane_v11 import DualConfig,run
from scoping_v17 import FACTORS,case,stream,evaluate,summary

class ScopingV17Tests(unittest.TestCase):
    def test_arrival_timing_budget(self):
        a=stream(0,"rate_timing","steady")
        b=stream(0,"rate_timing","alternating")
        c=stream(0,"rate_timing","frontloaded")
        self.assertEqual(len(a),len(b))
        self.assertEqual(len(b),len(c))
        self.assertEqual(Counter(r for _,r in a),Counter(r for _,r in b))
    def test_exogenous_outage_half_open(self):
        x=ReceivingCells(LinkConfig(cells=2,downstream_cycle_s=60,
            downstream_green_s=60,closure_windows=((10,20),)))
        self.assertTrue(x.green(9))
        self.assertFalse(x.green(10))
        self.assertFalse(x.green(19))
        self.assertTrue(x.green(20))
    def test_bad_outage_rejected(self):
        with self.assertRaises(ValueError):
            ReceivingCells(LinkConfig(closure_windows=((30,20),)))
    def test_red_outage_preserves_vehicles(self):
        base=Config(duration_s=120)
        c=DualConfig(base=base,receiver_mode="cells",receiver_slots=4,
            receiver_closures=((0,120),))
        r=run(c)
        self.assertEqual(r["generated"],r["remaining"])
        self.assertEqual(r["network_out_S"]+r["network_out_L"],0)
    def test_all_factor_levels_have_conservation(self):
        for factor,levels in FACTORS.items():
            for level in levels:
                x=run(case(0,factor,level,14.),stream(0,factor,level))
                self.assertEqual(x["generated"],
                    x["network_out_S"]+x["network_out_L"]+x["remaining"])
    def test_default_no_outage_is_noop(self):
        c=DualConfig(base=Config(duration_s=120),receiver_mode="cells",receiver_slots=4)
        self.assertEqual(run(c),run(replace(c,receiver_closures=())))

if __name__=="__main__":
    unittest.main(verbosity=2)
