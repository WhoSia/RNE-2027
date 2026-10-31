"""Downstream receiving queue checks; synthetic and explicitly non-calibrated."""
import unittest
from dataclasses import replace
from spatial_v10 import Config,arrivals
from dual_lane_v11 import DualConfig,run

class ReceiverTests(unittest.TestCase):
    def test_disabled_matches_prior_output(self):
        y=run(DualConfig(base=Config(duration_s=400)))
        self.assertEqual(y["network_out_S"],y["exit_S"])
        self.assertEqual(y["network_out_L"],y["exit_L"])
        self.assertEqual(y["receiver_final"],0)
    def test_conservation_and_finite_storage(self):
        for slots in (1,2,4,8):
            for headway in (2,4,8):
                cfg=DualConfig(base=Config(duration_s=720,demand_vph=2100),
                    receiver_slots=slots,receiver_headway_s=headway,through_B_share=.5)
                y=run(cfg,trace=True)
                self.assertEqual(y["generated"],
                    y["remaining"]+y["network_out_S"]+y["network_out_L"])
                self.assertLessEqual(y["max_receiver"],slots)
                self.assertEqual(y["receiver_final"],
                    y["exit_S"]+y["exit_L"]-y["network_out_S"]-y["network_out_L"])
                self.assertTrue(all(len(f["receiver"])<=slots for f in y["frames"]))
    def test_coupled_downstream_breaks_lane_separation(self):
        base=Config(duration_s=720,demand_vph=1500,left_fraction=.5,seed=0)
        stream=arrivals(base)
        a=run(DualConfig(base=replace(base,pocket_length_m=0),
            through_B_share=1,receiver_slots=2,receiver_headway_s=4),stream)
        b=run(DualConfig(base=replace(base,pocket_length_m=14),
            through_B_share=1,receiver_slots=2,receiver_headway_s=4),stream)
        self.assertNotEqual(a["exit_S"],b["exit_S"])
        self.assertEqual(a["network_out_L"],0)
        self.assertGreater(b["network_out_L"],0)
    def test_invalid_receiving_configuration(self):
        with self.assertRaises(ValueError):run(DualConfig(receiver_slots=-1))
        with self.assertRaises(ValueError):run(DualConfig(receiver_slots=2,receiver_headway_s=0))
    def test_receiver_backpressure(self):
        b=Config(duration_s=720,left_fraction=.3)
        constrained=run(DualConfig(base=b,receiver_slots=1,receiver_headway_s=8))
        free=run(DualConfig(base=b))
        self.assertGreater(constrained["receiver_full_denied_s"],0)
        self.assertLess(constrained["exit_S"]+constrained["exit_L"],free["exit_S"]+free["exit_L"])

if __name__=="__main__":
    unittest.main(verbosity=2)
