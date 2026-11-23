"""Fixture-level negative controls for P88/P93 zone and movement reconstruction.

Run inside the research environment:
  python -m unittest test_p93_spatial_movement_identity
This is NOT a substitute for full 384-run P88/P93 replay.
"""
import unittest

from p88_spatial_audit import aggregate


class IdentityAccountingTest(unittest.TestCase):
    def setUp(self):
        self.cp = {"state": {"outside": {
            "A": [(0, "L", 70)], "B": [(1, "S", 75)]
        }}}
        self.tape = ((70, "L"), (75, "S"), (84, "L"), (85, "S"))
        self.frames = [
            {"t": 84, "outside": 2, "A": [], "B": [],
             "pocket": [(-1, 0)], "receiver": []},
            {"t": 85, "outside": 1, "A": [(-1, 2, "L")],
             "B": [(-2, 3, "S")], "pocket": [(-1, 0)], "receiver": []},
            {"t": 86, "outside": 0, "A": [(-1, 2, "L")],
             "B": [(-1, 3, "S")], "pocket": [(-1, 0)],
             "receiver": [(0, 1, "S")]}
        ]

    def test_exact_movement_zone_sums(self):
        zones, by_move, by_vehicle = aggregate({"frames": self.frames}, self.cp, self.tape)
        self.assertEqual(zones["outside"], 3)
        self.assertEqual(zones["pocket"], 3)
        self.assertEqual(zones["approach_A"], 2)
        self.assertEqual(zones["approach_B"], 2)
        self.assertEqual(zones["receiver"], 1)
        for zone, value in zones.items():
            self.assertEqual(value, sum(by_move[m].get(zone, 0) for m in ("L", "S")))
        self.assertEqual(sum(zones.values()), sum(sum(v.values()) for v in by_vehicle.values()))
        self.assertEqual(by_move["L"]["outside"], 1)
        self.assertEqual(by_move["S"]["outside"], 2)

    def test_wrong_outside_count_rejected(self):
        self.frames[-1]["outside"] = 1
        with self.assertRaises(AssertionError):
            aggregate({"frames": self.frames}, self.cp, self.tape)

    def test_duplicate_active_id_rejected(self):
        self.frames[0]["A"] = [(-1, 0, "L")]
        with self.assertRaises(AssertionError):
            aggregate({"frames": self.frames}, self.cp, self.tape)


if __name__ == "__main__":
    unittest.main()
