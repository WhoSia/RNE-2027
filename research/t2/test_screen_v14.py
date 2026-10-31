import unittest
from dataclasses import replace
from screen_v14 import config_for,summarize,LEVELS
from arrival_design_v14 import ArrivalProfile,make_arrivals
from dual_lane_v11 import run

class ScreenTests(unittest.TestCase):
    def test_every_level_is_feasible(self):
        stream=make_arrivals(ArrivalProfile(duration_s=120))
        for lever,levels in LEVELS.items():
            for level in levels:
                cfg=config_for(0,lever,level)
                cfg=replace(cfg,base=replace(cfg.base,duration_s=120))
                r=run(cfg,stream)
                self.assertEqual(r['generated'],
                    r['network_out_S']+r['network_out_L']+r['remaining'])
    def test_incomplete_screen_rejected(self):
        with self.assertRaises(AssertionError):summarize([])

if __name__=='__main__':unittest.main(verbosity=2)
