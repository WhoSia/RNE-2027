import unittest
from replay_provenance import replay
class HistoricalP10(unittest.TestCase):
 def test_original_p10_mechanism_and_sha(self):
  r=replay()
  self.assertEqual(r['tests_passed'],8)
  self.assertEqual(r['trace_runs_match'],8)
  self.assertEqual(r['original_dt_vehicle8']['0.5'],47.0)
  self.assertEqual(r['original_dt_vehicle8']['0.25'],87.25)
if __name__=='__main__':unittest.main()
