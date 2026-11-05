import unittest,sys,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from friction_demand import PhysicsPoint,demand,G
class TestFrictionPhysics(unittest.TestCase):
 def test_flat_zero(self):self.assertEqual(demand(PhysicsPoint(0,0,0,0)).mu_required,0)
 def test_flat_circle(self):self.assertAlmostEqual(demand(PhysicsPoint(10,.02,0,0)).mu_required,2/G)
 def test_speed_quadratic(self):
  low=demand(PhysicsPoint(5,.02,0,0)).mu_required
  self.assertAlmostEqual(demand(PhysicsPoint(10,.02,0,0)).mu_required/low,4)
 def test_bank_demand_reduction_in_case(self):
  a=demand(PhysicsPoint(10,.02,0,0)).mu_required
  b=demand(PhysicsPoint(10,.02,.1,0)).mu_required
  self.assertLess(b,a)
 def test_grade_stationary_demand(self):self.assertAlmostEqual(demand(PhysicsPoint(0,0,0,.1)).mu_required,math.tan(.1))
 def test_combined_brake_and_turn(self):
  r=demand(PhysicsPoint(10,.02,0,0,-3))
  self.assertAlmostEqual(r.mu_required,math.hypot(2,3)/G)
 def test_no_unverified_default(self):self.assertIsNone(demand(PhysicsPoint(10,.02,0,0)).margin)
 def test_signed_curvature_bank_mismatch(self):
  a=demand(PhysicsPoint(10,.02,.1,0)).mu_required
  b=demand(PhysicsPoint(10,-.02,.1,0)).mu_required
  self.assertLess(a,b)
 def test_nonpositive_normal(self):self.assertEqual(demand(PhysicsPoint(20,-.05,.8,0)).status,'UNKNOWN_NONPOSITIVE_NORMAL')
 def test_invalid_speed(self):
  with self.assertRaises(ValueError):demand(PhysicsPoint(-1,0,0,0))
 def test_invalid_mu(self):
  with self.assertRaises(ValueError):demand(PhysicsPoint(1,0,0,0),effective_mu=-.2)
 def test_hypothesis_not_certification(self):self.assertEqual(demand(PhysicsPoint(10,.02,0,0),effective_mu=.5).status,'HYPOTHETICAL_COMPARISON')
if __name__=='__main__':unittest.main()
