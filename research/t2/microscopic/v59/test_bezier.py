import unittest
from bezier_dynamics import Cubic,Dynamics,make_profile,crossing_occupancy,example_turn,example_through
class Tests(unittest.TestCase):
 def test_straight_curvature(self):self.assertLess(max(example_through().curvature(i/20) for i in range(21)),1e-9)
 def test_endpoints(self):
  c=example_turn();self.assertEqual(c.at(0),c.controls[0]);self.assertEqual(c.at(1),c.controls[3])
 def test_turn_curvature(self):self.assertGreater(max(example_turn().curvature(i/100) for i in range(101)),.02)
 def test_lateral_limit(self):self.assertLessEqual(max(p['a_lat_mps2'] for p in make_profile(example_turn(),Dynamics())),1.800001)
 def test_time_monotone(self):
  p=make_profile(example_turn(),Dynamics());self.assertTrue(all(p[i+1]['t_s']>p[i]['t_s'] for i in range(len(p)-1)))
 def test_accel_brake(self):
  d=Dynamics();p=make_profile(example_turn(),d)
  for a,b in zip(p,p[1:]):
   ds=b['s_m']-a['s_m']
   self.assertLessEqual(b['v_mps']**2-a['v_mps']**2,2*d.accel*ds+1e-7)
   self.assertLessEqual(a['v_mps']**2-b['v_mps']**2,2*d.braking*ds+1e-7)
 def test_occupancy(self):
  o=crossing_occupancy(make_profile(example_turn(),Dynamics()));self.assertGreater(o['exact_duration_s'],0);self.assertGreaterEqual(o['duration_s'],o['exact_duration_s'])
 def test_slow_turn(self):
  c=example_turn();a=make_profile(c,Dynamics(max_speed=5,lateral_accel=1));b=make_profile(c,Dynamics(max_speed=12,lateral_accel=4));self.assertGreater(crossing_occupancy(a)['duration_s'],crossing_occupancy(b)['duration_s'])
 def test_tighter_lat(self):
  c=example_turn();self.assertGreaterEqual(make_profile(c,Dynamics(lateral_accel=1))[-1]['t_s'],make_profile(c,Dynamics(lateral_accel=3))[-1]['t_s'])
 def test_reject_bad_input(self):
  with self.assertRaises(ValueError):Dynamics(dt=0)
  with self.assertRaises(ValueError):Cubic(((0,0),(1,1)))
  with self.assertRaises(ValueError):make_profile(example_turn(),Dynamics(),float('nan'))
  with self.assertRaises(ValueError):crossing_occupancy(make_profile(example_turn(),Dynamics()),half_width=0)
if __name__=='__main__':unittest.main()
