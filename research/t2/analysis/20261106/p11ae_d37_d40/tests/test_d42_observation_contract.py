"""Ten synthetic-fixture tests only; not a DLR raw-data validation."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from d42_observation_contract import (
    Sample,SignalSample,audit_trajectories,align_signal_at_event,crossing_event
)

class D42AuditTests(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(audit_trajectories([
            Sample(0,"v","L",1,3),Sample(.05,"v","L",1.15,3)]),[])
    def test_tracking_gap(self):
        self.assertIn(("tracking_gap","v"),audit_trajectories([
            Sample(0,"v","L",1,0),Sample(.4,"v","L",1,0)]))
    def test_position_jump(self):
        self.assertIn(("position_jump","v"),audit_trajectories([
            Sample(0,"v","L",1,1),Sample(.05,"v","L",50,1)]))
    def test_invalid(self):
        self.assertIn(("invalid_record","v"),audit_trajectories([
            Sample(0,"v","L",float("nan"),1)]))
    def test_sampled_signal_not_truth(self):
        o=align_signal_at_event(.5,[SignalSample(0,"H","GREEN")],head_id="H")
        self.assertEqual(o["status"],"LAST_OBSERVED_NOT_EVENT_TRUTH")
    def test_stale_signal(self):
        o=align_signal_at_event(2,[SignalSample(0,"H","GREEN")],head_id="H")
        self.assertEqual(o["status"],"UNKNOWN")
    def test_missing_signal(self):
        self.assertEqual(align_signal_at_event(.2,[],head_id="H")["status"],"UNKNOWN")
    def test_crossing_interval(self):
        a=Sample(0,"v","L",9.8,4);b=Sample(.05,"v","L",10.1,4)
        self.assertEqual(crossing_event(a,b,10)["t_upper_s"],.05)
    def test_no_crossing(self):
        a=Sample(0,"v","L",9.8,0);b=Sample(.05,"v","L",9.9,0)
        self.assertIsNone(crossing_event(a,b,10))
    def test_lane_mismatch(self):
        a=Sample(0,"v","L1",9.8,4);b=Sample(.05,"v","L2",10.1,4)
        self.assertIsNone(crossing_event(a,b,10))

if __name__=="__main__":
    unittest.main()
