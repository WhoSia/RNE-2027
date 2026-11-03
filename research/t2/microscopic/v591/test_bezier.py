import unittest
from math import isclose
from bezier_dynamics import Cubic,Dynamics,make_profile,crossing_occupancy,example_turn,example_through
class TestGeometryDynamics(unittest.TestCase):
 def test_linear_curve_zero_curvature(self):
  c=example_through();self.assertLess(max(c.curvature(i/20) for i in range(21)),1e-9)
 def test_continuity_endpoints(self):
  c=example_turn();self.assertEqual(c.at(0),c.controls[0]);self.assertEqual(c.at(1),c.controls[3])
 def test_turn_curve_nonzero(self):self.assertGreater(max(example_turn().curvature(i/100) for i in range(101)),0.02)
 def test_lateral_acceleration_limit(self):
  p=make_profile(example_turn(),Dynamics());self.assertLessEqual(max(x['a_lat_mps2'] for x in p),1.800001)
 def test_monotonic_path_time_and_distance(self):
  p=make_profile(example_turn(),Dynamics());self.assertTrue(all(p[i+1]['t_s']>p[i]['t_s'] and p[i+1]['s_m']>p[i]['s_m'] for i in range(len(p)-1)))
 def test_accel_bounds_discrete(self):
  d=Dynamics();p=make_profile(example_turn(),d)
  for i in range(len(p)-1):
   v,w=p[i]['v_mps'],p[i+1]['v_mps'];ds=p[i+1]['s_m']-p[i]['s_m']
   self.assertLessEqual(w*w-v*v,2*d.accel*ds+1e-7)
   self.assertLessEqual(v*v-w*w,2*d.braking*ds+1e-7)
 def test_occupancy_duration_nonzero(self):
  p=make_profile(example_turn(),Dynamics());r=crossing_occupancy(p);self.assertGreater(r['exact_duration_s'],0);self.assertGreaterEqual(r['duration_s'],r['exact_duration_s'])
 def test_slower_speed_longer(self):
  c=example_turn();fast=make_profile(c,Dynamics(max_speed=12,lateral_accel=4));slow=make_profile(c,Dynamics(max_speed=5,lateral_accel=1));self.assertGreater(crossing_occupancy(slow)['duration_s'],crossing_occupancy(fast)['duration_s'])
 def test_stricter_lateral_longer(self):
  c=example_turn();a=make_profile(c,Dynamics(lateral_accel=1));b=make_profile(c,Dynamics(lateral_accel=3));self.assertGreaterEqual(a[-1]['t_s'],b[-1]['t_s'])
 def test_invalid_input(self):
  with self.assertRaises(ValueError):Dynamics(dt=0)
  with self.assertRaises(ValueError):Cubic(((0,0),(1,1)))
  with self.assertRaises(ValueError):make_profile(example_turn(),Dynamics(),float('nan'))
  with self.assertRaises(ValueError):crossing_occupancy(make_profile(example_turn(),Dynamics()),half_width=0)
if __name__=='__main__':unittest.main()
