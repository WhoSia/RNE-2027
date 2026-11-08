"""Unit tests for D44 stopping feasibility oracle (offline only)."""
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from stopping_feasibility import evaluate_stopping

class Audit(unittest.TestCase):
    def test_red_signal_witness(self):
        x=evaluate_stopping(3,3,.25)
        self.assertAlmostEqual(x.required_decel_mps2,1.5)
        self.assertFalse(x.feasible_without_reaction)
    def test_long_distance(self):
        self.assertTrue(evaluate_stopping(2,20,.25).feasible_without_reaction)
    def test_at_rest_boundary(self):
        self.assertTrue(evaluate_stopping(0,0,.25).feasible_without_reaction)
    def test_positive_speed_at_boundary(self):
        self.assertFalse(evaluate_stopping(1,0,.25).feasible_without_reaction)
    def test_negative_speed(self):
        with self.assertRaises(ValueError):evaluate_stopping(-1,2,.25)
    def test_negative_distance(self):
        with self.assertRaises(ValueError):evaluate_stopping(1,-2,.25)
    def test_zero_deceleration(self):
        with self.assertRaises(ValueError):evaluate_stopping(1,2,0)
    def test_nonfinite(self):
        with self.assertRaises(ValueError):evaluate_stopping(float("nan"),2,.25)

if __name__=="__main__":
    unittest.main()
