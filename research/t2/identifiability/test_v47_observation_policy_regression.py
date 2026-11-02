import unittest
from v47_observation_policy_regression import World,run,witness_count
class Tests(unittest.TestCase):
 def test_historical_reproduced(self):self.assertEqual(witness_count(),12)
 def test_observation_policy_matters(self):self.assertEqual(witness_count(baseline=3),0)
 def test_snapshot_not_sufficient(self):self.assertEqual(witness_count(snapshot=True),12)
 def test_minimum_green_not_sufficient(self):self.assertEqual(witness_count(min_green=1),12)
 def test_cycle_eight_not_sufficient(self):self.assertEqual(witness_count(cycle=8),12)
 def test_cycle_eight_observation_changes(self):self.assertEqual(witness_count(cycle=8,baseline=3),0)
 def test_original_witness_exits(self):self.assertEqual(run(World(2,2,2),5),96)
 def test_bad_policy(self):
  with self.assertRaises(ValueError):run(World(2,2,2),6)
if __name__=='__main__':unittest.main()
