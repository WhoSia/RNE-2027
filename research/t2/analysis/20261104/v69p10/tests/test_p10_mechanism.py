import unittest
from p10_boundary_trace import run_trace

class MechanismTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.d=run_trace()
  cls.r={x['dt_s']:x for x in cls.d['runs']}
 def test_capacity_threshold(self):
  m=self.d['mechanism'];self.assertLessEqual(m['two_cars_storage_m'],m['link_storage_m']);self.assertGreater(m['three_cars_storage_m'],m['link_storage_m'])
 def test_green_boundary(self):
  self.assertAlmostEqual(self.d['mechanism']['last_side_entry_s'],47.1625)
 def test_first_receive_gate(self):
  self.assertLess(self.r[.05]['link_receives_vehicle_1_at_s'],47.1625)
  self.assertGreater(self.r[.25]['link_receives_vehicle_1_at_s'],47.1625)
 def test_same_cycle_vs_next(self):
  self.assertLess(self.r[.05]['vehicle_8_enters_j0_at_s'],53)
  self.assertGreater(self.r[.25]['vehicle_8_enters_j0_at_s'],53)
 def test_timestamp_backdating(self):
  self.assertAlmostEqual(self.r[.05]['entry_timestamp_before_link_receipt_s'],.05)
  self.assertAlmostEqual(self.r[.5]['entry_timestamp_before_link_receipt_s'],.5)
 def test_all_complete_and_safe_invariants(self):
  for q in self.d['runs']:
   self.assertTrue(q['all_completed']);self.assertEqual(q['state_issues'],0)
 def test_nonmonotone_classification(self):
  self.assertLess(self.r[.5]['vehicle_8_enters_j0_at_s'],53)
  self.assertGreater(self.r[.4]['vehicle_8_enters_j0_at_s'],53)
  self.assertGreater(self.r[.25]['vehicle_8_enters_j0_at_s'],53)
  self.assertLess(self.r[.125]['vehicle_8_enters_j0_at_s'],53)
 def test_capacity_gate_removes_source_backdating_in_this_case(self):
  from p10_capacity_ablation import compare
  data=compare();v={r['dt_s']:r for r in data if r['method']=='capacity-time-gate'}
  self.assertEqual(len(v),8)
  self.assertFalse(any(r['retroactive_capacity_use'] for r in v.values()))
  self.assertTrue(all(r['completed']==63 and r['issues']==0 for r in v.values()))
  self.assertGreater(v[.0625]['vehicle8_enter_s'],53)
  self.assertLess(v[.05]['vehicle8_enter_s'],53)
if __name__=='__main__':unittest.main()
