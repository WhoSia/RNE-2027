import unittest
from spatial_v10 import Config
from dual_lane_v11 import DualConfig,run
from diagnose_spillback_v16 import diagnose

class TraceTests(unittest.TestCase):
    def test_requires_trace(self):
        with self.assertRaises(ValueError):
            diagnose(run(DualConfig(base=Config(duration_s=120))))
    def test_requires_physical_receiver(self):
        with self.assertRaises(ValueError):
            diagnose(run(DualConfig(base=Config(duration_s=120)),trace=True))
    def test_downstream_red_signatures(self):
        cfg=DualConfig(base=Config(duration_s=360,demand_vph=1800),
             receiver_mode="cells",receiver_slots=2,downstream_green_s=0)
        result=run(cfg,trace=True)
        audit=diagnose(result)
        self.assertEqual(audit["frames"],360)
        self.assertGreater(audit["signatures"]["receiver_entry_cell_occupied_frames"],0)
        self.assertEqual(result["generated"],
            result["network_out_S"]+result["network_out_L"]+result["remaining"])
    def test_replay(self):
        c=DualConfig(base=Config(duration_s=240,seed=8),
                     receiver_mode="cells",receiver_slots=4)
        self.assertEqual(diagnose(run(c,trace=True)),diagnose(run(c,trace=True)))
    def test_no_demand(self):
        c=DualConfig(base=Config(duration_s=120,demand_vph=0),
                     receiver_mode="cells",receiver_slots=4)
        r=diagnose(run(c,trace=True))
        self.assertEqual(r["signatures"],{})
        self.assertEqual(r["stopped_vehicle_seconds_total"],0)

if __name__=="__main__":
    unittest.main(verbosity=2)
