import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from observed_spat import audit_rows
A=[{'intersection_id':'5502','tmstp_utc':'2025-03-01T00:00:08.156','signalgroup2':'G','signalgroup4':'R'},{'intersection_id':'5502','tmstp_utc':'2025-03-01T00:00:08.259','signalgroup2':'Y','signalgroup4':'R'}]
class T(unittest.TestCase):
 def test_transition_interval(self):
  a=audit_rows(A);self.assertEqual(a['transitions'][0]['interval_width_s'],.103);self.assertTrue(a['observations_not_vehicle_counts'])
 def test_no_exact_instant(self):self.assertNotIn('transition_at',audit_rows(A)['transitions'][0])
 def test_order(self):
  with self.assertRaises(ValueError):audit_rows(A[::-1])
 def test_mixed(self):
  with self.assertRaises(ValueError):audit_rows([A[0],{**A[1],'intersection_id':'other'}])
 def test_invalid_state(self):
  with self.assertRaises(ValueError):audit_rows([A[0],{**A[1],'signalgroup2':'X'}])
 def test_empty(self):
  with self.assertRaises(ValueError):audit_rows([])
if __name__=='__main__':unittest.main()
