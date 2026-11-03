import unittest
from bezier_dynamics import make_profile, Dynamics, example_turn, example_through
class EntryAudit(unittest.TestCase):
 def test_infeasible_entry_speed_must_be_rejected_in_strict_mode(self):
  with self.assertRaisesRegex(ValueError,"brake upstream"):
   make_profile(example_turn(),Dynamics(max_speed=25,lateral_accel=1,braking=.5),13,strict_entry=True)
 def test_feasible_entry_preserved_exactly(self):
  p=make_profile(example_turn(),Dynamics(),7,strict_entry=True)
  self.assertAlmostEqual(p[0]['v_mps'],7)
 def test_legacy_default_behavior_unchanged(self):
  d=Dynamics(max_speed=25,lateral_accel=1,braking=.5)
  p=make_profile(example_turn(),d,13)
  self.assertLess(p[0]['v_mps'],13)
 def test_straight_admission_no_unnecessary_braking(self):
  p=make_profile(example_through(),Dynamics(),13,strict_entry=True)
  self.assertAlmostEqual(p[0]['v_mps'],13)
if __name__=='__main__': unittest.main()
