import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from controllers import PhaseController,Observation,PhaseGuard

def O(t,m=0,s=0,md=100,sd=100):return Observation(t,m,s,md,sd)
class PolicyTest(unittest.TestCase):
 def test_fixed_switch_requires_min(self):
  c=PhaseController('fixed');self.assertEqual(c.observe(O(3)),('main','green'));self.assertEqual(c.observe(O(8)),('main','yellow'))
 def test_yellow_then_all_red_then_side(self):
  c=PhaseController('fixed');c.observe(O(8));self.assertEqual(c.observe(O(10)),('main','yellow'));self.assertEqual(c.observe(O(11)),('main','all_red'));self.assertEqual(c.observe(O(12)),('side','green'))
 def test_pressure_prefers_blocked_downstream(self):
  c=PhaseController('pressure');self.assertEqual(c.observe(O(4,12,6,0,8)),('main','yellow'))
 def test_actuated_empty_and_other_calls(self):
  c=PhaseController('actuated');self.assertEqual(c.observe(O(4,0,3)),('main','yellow'))
 def test_actuated_does_not_switch_if_own_queue(self):
  c=PhaseController('actuated');self.assertEqual(c.observe(O(4,4,3)),('main','green'))
 def test_max_green_bound(self):
  c=PhaseController('pressure');self.assertEqual(c.observe(O(15,15,0)),('main','yellow'))
 def test_no_reverse_time(self):
  c=PhaseController('fixed');c.observe(O(4));
  with self.assertRaises(ValueError):c.observe(O(3))
 def test_invalid_guard(self):
  with self.assertRaises(ValueError):PhaseGuard(10,5)
 def test_bad_observation(self):
  with self.assertRaises(ValueError):Observation(0,-1,0,0,0)
 def test_no_safety_skip_in_time_jump(self):
  c=PhaseController('fixed');c.observe(O(8));c.observe(O(12));self.assertEqual([x[2] for x in c.log],['green','yellow','all_red','green'])
if __name__=='__main__':unittest.main()

class SparseObservationTests(unittest.TestCase):
 def test_sparse_obs_does_not_extend_max_green(self):
  c=PhaseController('pressure',PhaseGuard(4,15,3,1))
  c.observe(O(42,10,0))
  self.assertIn((15.,'main','yellow'),c.log)
  self.assertIn((18.,'main','all_red'),c.log)
  self.assertIn((19.,'side','green'),c.log)
 def test_fixed_deadlines_do_not_wait_for_detector(self):
  c=PhaseController('fixed')
  c.observe(O(50))
  self.assertIn((8.,'main','yellow'),c.log)
  self.assertIn((12.,'side','green'),c.log)
