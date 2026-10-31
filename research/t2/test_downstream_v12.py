"""v1.2: downstream shared-exit stress, without claiming real merge geometry."""
import unittest
from dataclasses import replace
from spatial_v10 import Config,arrivals
from dual_lane_v11 import DualConfig,run

class DownstreamCouplingTests(unittest.TestCase):
    def test_default_off_matches_explicit_zero(self):
        base=Config(duration_s=360)
        a=run(DualConfig(base=base,through_B_share=.5))
        b=run(DualConfig(base=base,through_B_share=.5,downstream_conflict_gap_s=0))
        self.assertEqual(a,b)

    def test_mass_and_storage_under_shared_gate(self):
        for gap in (0,2,4,10,40):
            y=run(DualConfig(base=Config(duration_s=480),
                through_B_share=.5,downstream_conflict_gap_s=gap),trace=True)
            self.assertEqual(y["generated"],y["exit_S"]+y["exit_L"]+y["remaining"])
            for frame in y["frames"]:
                self.assertEqual(len(frame["A"]),len({x for x,_,_ in frame["A"]}))

    def test_shared_gate_breaks_independent_through_lane(self):
        base=Config(duration_s=720,demand_vph=1500,left_fraction=.5,seed=0)
        stream=arrivals(base)
        blocked=run(DualConfig(base=replace(base,pocket_length_m=0),
            through_B_share=1,downstream_conflict_gap_s=40),stream)
        unblocked=run(DualConfig(base=replace(base,pocket_length_m=14),
            through_B_share=1,downstream_conflict_gap_s=40),stream)
        self.assertEqual(blocked["exit_L"],0)
        self.assertGreater(unblocked["exit_L"],0)
        self.assertNotEqual(blocked["exit_S"],unblocked["exit_S"])

    def test_when_shared_gate_off_noninterference_recovers(self):
        base=Config(duration_s=720,demand_vph=1500,left_fraction=.5,seed=0)
        stream=arrivals(base)
        first=run(DualConfig(base=replace(base,pocket_length_m=0),
            through_B_share=1),stream)
        second=run(DualConfig(base=replace(base,pocket_length_m=70),
            through_B_share=1),stream)
        self.assertEqual(first["exit_S"],second["exit_S"])

    def test_reject_negative_shared_gap(self):
        with self.assertRaises(ValueError):
            run(DualConfig(downstream_conflict_gap_s=-1))

if __name__=="__main__":
    unittest.main(verbosity=2)
