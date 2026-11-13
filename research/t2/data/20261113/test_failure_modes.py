"""Safety regressions for data-quality edge cases."""
import tempfile
from pathlib import Path
from datetime import datetime, timedelta, timezone
import unittest
from audit_dlr_case import audit_signals, audit_volume

class FailureModeTests(unittest.TestCase):
    def test_partial_893_rows_are_flagged_not_filled(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"v.csv"
            base=datetime(2023,9,24,23,30,7,tzinfo=timezone.utc)
            p.write_text("timestamp,A\n"+"".join(f"{(base+timedelta(seconds=i)).isoformat()},0\n" for i in range(893)))
            data=audit_volume(p)
            self.assertTrue(data["partial_window"])
            self.assertEqual(data["rows"],893)
            self.assertAlmostEqual(data["coverage_ratio"],893/900)

    def test_unsorted_volume_rejected_even_at_900_rows(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"v.csv"
            base=datetime(2023,9,24,12,tzinfo=timezone.utc)
            seconds=list(range(900))
            seconds[100],seconds[101]=seconds[101],seconds[100]
            p.write_text("timestamp,A\n"+"".join(f"{(base+timedelta(seconds=i)).isoformat()},0\n" for i in seconds))
            with self.assertRaises(ValueError):
                audit_volume(p)

    def test_duplicate_signal_head_at_same_instant_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"s.csv"
            moment="2023-09-24T12:00:00.990+00:00"
            p.write_text("timestamp,id,state\n"+"".join(f"{moment},{i},3\n" for i in list(range(1,31))+[1]))
            with self.assertRaises(ValueError):
                audit_signals(p)

if __name__=="__main__":
    unittest.main()
