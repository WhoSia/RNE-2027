"""Synthetic integrity tests for D42 categorical signal and count readers."""
import tempfile
import unittest
from pathlib import Path
from signal_volume_gate import categorical_signal_gate, volume_gate, parse_utc

class SourceGateTests(unittest.TestCase):
    def write(self, text):
        f=tempfile.NamedTemporaryFile(mode="w",suffix=".csv",delete=False)
        f.write(text)
        f.close()
        self.addCleanup(lambda:Path(f.name).unlink(missing_ok=True))
        return Path(f.name)

    def test_signal_uncertain_gap(self):
        path=self.write("timestamp,id,state\n"
           "2023-09-24 12:00:00+00:00,1,3\n"
           "2023-09-24 12:00:02+00:00,1,5\n")
        result=categorical_signal_gate(path)
        self.assertEqual((result["rows"],result["heads"]), (2,1))
        self.assertEqual(len(result["gaps"]),1)
        self.assertEqual(result["transition_across_gaps"],1)

    def test_same_state_gap_is_still_gap(self):
        path=self.write("timestamp,id,state\n"
           "2023-09-24 12:00:00+00:00,1,3\n"
           "2023-09-24 12:00:02+00:00,1,3\n")
        result=categorical_signal_gate(path)
        self.assertEqual(len(result["gaps"]),1)
        self.assertEqual(result["transition_count"],0)

    def test_duplicate_light_time_rejected(self):
        path=self.write("timestamp,id,state\n"
           "2023-09-24 12:00:00+00:00,1,3\n"
           "2023-09-24 12:00:00+00:00,1,5\n")
        with self.assertRaises(ValueError):categorical_signal_gate(path)

    def test_count_cells_not_unique_tracks(self):
        path=self.write("timestamp,A,B\n"
           "2023-09-24 12:00:00+00:00,1,2\n"
           "2023-09-24 12:00:01+00:00,0,1\n")
        out=volume_gate(path)
        self.assertEqual((out["seconds"],out["movements"],out["observed_count_cell_sum"]),(2,2,4))

    def test_duplicate_count_time_rejected(self):
        path=self.write("timestamp,A\n"
            "2023-09-24 12:00:00+00:00,1\n"
            "2023-09-24 12:00:00+00:00,1\n")
        with self.assertRaises(ValueError):volume_gate(path)

    def test_negative_count_rejected(self):
        path=self.write("timestamp,A\n2023-09-24 12:00:00+00:00,-1\n")
        with self.assertRaises(ValueError):volume_gate(path)

    def test_timezone_required(self):
        with self.assertRaises(ValueError):parse_utc("2023-09-24 12:00:00")

if __name__=="__main__":unittest.main()
