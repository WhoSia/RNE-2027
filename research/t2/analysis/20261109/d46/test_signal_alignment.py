"""Tests for the conservative as-of event rule (no assumed red/green codes)."""
import unittest
from datetime import datetime,timedelta,timezone
from signal_alignment import asof_state
BASE=datetime(2023,9,24,12,0,tzinfo=timezone.utc)
class TestAsOf(unittest.TestCase):
    def test_exact(self): self.assertEqual(asof_state([BASE],[3],BASE).raw_state,3)
    def test_before_first(self): self.assertEqual(asof_state([BASE],[3],BASE-timedelta(milliseconds=1)).reason,"no_prior_sample")
    def test_prior_within_limit(self): self.assertEqual(asof_state([BASE],[7],BASE+timedelta(seconds=1)).raw_state,7)
    def test_stale(self): self.assertEqual(asof_state([BASE],[7],BASE+timedelta(seconds=1.1)).reason,"stale")
    def test_future_not_read(self):
        self.assertEqual(asof_state([BASE+timedelta(seconds=1),BASE+timedelta(seconds=2)],[3,5],BASE+timedelta(seconds=1.5)).raw_state,3)
    def test_gap_remains_unknown(self):
        self.assertIsNone(asof_state([BASE,BASE+timedelta(seconds=3)],[3,5],BASE+timedelta(seconds=2)).raw_state)
    def test_duplicate_source_rejected(self):
        with self.assertRaises(ValueError): asof_state([BASE,BASE],[1,2],BASE)
    def test_empty_rejected(self):
        with self.assertRaises(ValueError): asof_state([],[],BASE)
    def test_mismatched_lengths(self):
        with self.assertRaises(ValueError): asof_state([BASE],[],BASE)
    def test_negative_limit(self):
        with self.assertRaises(ValueError): asof_state([BASE],[3],BASE,-1)
    def test_zero_exact(self): self.assertEqual(asof_state([BASE],[3],BASE,0).raw_state,3)
    def test_zero_not_exact(self):
        self.assertIsNone(asof_state([BASE],[3],BASE+timedelta(microseconds=1),0).raw_state)
if __name__=="__main__": unittest.main()
