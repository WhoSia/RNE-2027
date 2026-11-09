"""Ten independent D44 prototype checks (not field validation)."""
import unittest
from braking_reference import simulate,InfeasibleStop

class Kinematics(unittest.TestCase):
 def test_speed_trace(self):
  self.assertEqual([s.v_mps for s in simulate()[:8]],[0,1.5,1.25,1,.75,.5,.25,0])
 def test_monotone_position(self):
  x=simulate()
  self.assertTrue(all(a.rear_m<=b.rear_m for a,b in zip(x,x[1:])))
 def test_stopline(self):
  self.assertTrue(all(s.rear_m<=7.5 for s in simulate()))
 def test_bound(self):
  x=simulate()
  self.assertTrue(all(a.v_mps-b.v_mps<=.25+1e-9 for a,b in zip(x,x[1:])))
 def test_stop_position(self):
  self.assertAlmostEqual(simulate()[-1].rear_m,5.25)
 def test_short_road_rejected(self):
  with self.assertRaises(InfeasibleStop): simulate(stop_rear_m=2)
 def test_long_road(self):
  self.assertEqual(len(simulate(stop_rear_m=12)),9)
 def test_negative_road(self):
  with self.assertRaises(ValueError): simulate(stop_rear_m=-1)
 def test_zero_brake(self):
  with self.assertRaises(ValueError): simulate(max_decel=0)
 def test_nonfinite_input(self):
  with self.assertRaises(ValueError): simulate(stop_rear_m=float('nan'))

if __name__=="__main__":unittest.main()
