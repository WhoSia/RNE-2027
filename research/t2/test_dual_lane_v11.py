import unittest
from dataclasses import replace
from dual_lane_v11 import DualConfig,run
from spatial_v10 import Config,arrivals

class DualLaneTests(unittest.TestCase):
    def test_vehicle_conservation_and_capacity(self):
        for length in (0,14,28,42,70):
            for share in (0,.5,1):
                y=run(DualConfig(base=Config(duration_s=360,pocket_length_m=length),
                                 through_B_share=share))
                self.assertEqual(y["generated"],y["exit_S"]+y["exit_L"]+y["remaining"])
    def test_lane_changes_conserve(self):
        c=DualConfig(base=Config(duration_s=720,left_fraction=.3),
                     through_B_share=.3,allow_lane_changes=True)
        y=run(c,trace=True)
        self.assertEqual(y["generated"],y["exit_S"]+y["exit_L"]+y["remaining"])
        self.assertEqual(len(y["frames"]),720)
    def test_all_through_B_pocket_placebo(self):
        b=Config(duration_s=480,left_fraction=0)
        y1=run(DualConfig(base=replace(b,pocket_length_m=14),through_B_share=1.0))
        y2=run(DualConfig(base=replace(b,pocket_length_m=70),through_B_share=1.0))
        self.assertEqual(y1["exit_S"],y2["exit_S"])
    def test_zero_pocket_all_left(self):
        y=run(DualConfig(base=Config(duration_s=360,left_fraction=1,pocket_length_m=0)))
        self.assertEqual(y["exit_S"]+y["exit_L"],0)
    def test_matched_stream_replay(self):
        c=Config(duration_s=480)
        stream=arrivals(c)
        self.assertEqual(run(DualConfig(base=c),stream),run(DualConfig(base=c),stream))
    def test_reject_bad_settings(self):
        with self.assertRaises(ValueError):run(DualConfig(through_B_share=1.1))
        with self.assertRaises(ValueError):run(DualConfig(change_zone_m=1000))
if __name__=="__main__":
    unittest.main(verbosity=2)
