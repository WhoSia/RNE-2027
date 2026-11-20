from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from dlr_followers import green_clock
from dlr_joint_observability import (Gate, ZONES, features, frame_slot,
                                     gate_crossing, read_block)


class JointObservabilityTests(TestCase):
    def test_gate_candidate_keeps_only_a_short_lane_valid_positive_bracket(self):
        lanes = ((-6, -3), (-3, 0))
        self.assertEqual(gate_crossing([(0.10,-1,-4), (0.15,1,-4)], lanes, 0),
                         (0, (0.10, 0.15)))
        self.assertEqual(gate_crossing([(0.48,-1,-4), (0.53,1,-4)], lanes, 0),
                         (None, (0.48, 0.53)))
        self.assertIsNone(gate_crossing([(0.10,-1,-4), (0.21,1,-4)], lanes, 0))
        self.assertIsNone(gate_crossing([(0.10,-1,1), (0.15,1,1)], lanes, 0))
        self.assertIsNone(gate_crossing([(0.10,1,-4), (0.15,-1,-4)], lanes, 0))

    def test_nearby_frames_do_not_pool_disjoint_detections(self):
        with TemporaryDirectory() as d:
            path = Path(d)/"track.csv"
            path.write_text(
                "timestamp,id,center_easting,center_northing,interpolated,"
                "classifications_car,classifications_van,classifications_truck,velocity_magnitude\n"
                "2023-09-24T12:30:00.980000+00:00,1,604763.1,5792795.1,False,1,0,0,1\n"
                "2023-09-24T12:30:01.016000+00:00,2,604763.4,5792795.1,False,1,0,0,1\n"
                "2023-09-24T12:30:01.500000+00:00,3,604763.1,5792795.1,True,1,0,0,1\n",
                encoding="utf-8")
            frames, _ = read_block(path, {"a": {(0,0)}, "b": {(1,0)}},
                                   Gate(0,0,1,0,()), 0)
        self.assertEqual(set(frames), {2})
        self.assertEqual(frames[2][2:], ({"b"}, {"b"}))

    def test_crossing_and_zone_presence_are_distinct(self):
        result = features(set(ZONES), {"near_stop","receiver_entry"}, 0)
        self.assertTrue(result["near_stop_and_receiver_slow"])
        self.assertTrue(result["all_zone_presence"])
        self.assertFalse(result["all_zone_presence_and_crossing"])
        self.assertFalse(result["connector_and_receiver_slow"])

    def test_sample_boundary_and_source_end_remain_outside_slots(self):
        self.assertIsNone(frame_slot(.031,0))
        self.assertIsNone(frame_slot(900,0))
        self.assertEqual(frame_slot(.510,0)[0], 1)

    def test_second_signal_head_uses_its_own_samples(self):
        with TemporaryDirectory() as d:
            path = Path(d)/"signal.csv"
            path.write_text(
                "timestamp,id,state\n"
                "2023-09-24T12:30:00+00:00,3,5\n"
                "2023-09-24T12:30:00+00:00,4,3\n"
                "2023-09-24T12:30:01+00:00,3,5\n"
                "2023-09-24T12:30:01+00:00,4,3\n",
                encoding="utf-8")
            self.assertEqual(green_clock(path, 3)(10), "green")
            self.assertEqual(green_clock(path, 4)(10), "non_green")
