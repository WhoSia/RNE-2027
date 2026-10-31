import unittest
from dataclasses import replace
from spatial_v10 import Config
from dual_lane_v11 import DualConfig,run

class IntegratedLinkTests(unittest.TestCase):
    def test_fifo_remains_default(self):
        c=DualConfig(base=Config(duration_s=240),receiver_slots=3)
        self.assertEqual(run(c),run(replace(c,receiver_mode="fifo")))
    def test_conservation_and_geometry(self):
        for n in (1,2,4,8):
            for offset in (0,20,40):
                c=DualConfig(base=Config(duration_s=360),receiver_slots=n,
                    receiver_mode="cells",downstream_offset_s=offset)
                r=run(c,trace=True)
                self.assertEqual(r["generated"],
                    r["network_out_S"]+r["network_out_L"]+r["remaining"])
                self.assertLessEqual(r["max_receiver"],n)
                self.assertTrue(all(len(f["receiver"])<=n for f in r["frames"]))
    def test_red_downstream_propagates_backpressure(self):
        c=DualConfig(base=Config(duration_s=720,demand_vph=1800),
            receiver_mode="cells",receiver_slots=2,downstream_green_s=0)
        r=run(c)
        self.assertEqual(r["network_out_S"]+r["network_out_L"],0)
        self.assertLessEqual(r["exit_S"]+r["exit_L"],2)
        self.assertGreater(r["receiver_full_denied_s"],0)
    def test_downstream_green_passes_traffic(self):
        c=DualConfig(base=Config(duration_s=480),receiver_mode="cells",
            receiver_slots=4,downstream_green_s=60)
        r=run(c)
        self.assertGreater(r["network_out_S"]+r["network_out_L"],0)
    def test_invalid_mode_and_zero_length(self):
        with self.assertRaises(ValueError):run(DualConfig(receiver_mode="bad"))
        with self.assertRaises(ValueError):
            run(DualConfig(receiver_mode="cells",receiver_slots=0))

if __name__=="__main__":unittest.main(verbosity=2)
