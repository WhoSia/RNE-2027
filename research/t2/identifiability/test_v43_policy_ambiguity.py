import unittest
from v43_policy_ambiguity import Scenario,observation,outcome,optima,witness
class Tests(unittest.TestCase):
 def test_equal_observation(self):self.assertEqual(observation(Scenario(10,2)),observation(Scenario(2,10)))
 def test_disjoint_optimal_policies(self):self.assertTrue(set(optima(Scenario(10,2))).isdisjoint(optima(Scenario(2,10))))
 def test_a_optimum(self):self.assertEqual(optima(Scenario(10,2)),[10])
 def test_b_optimum(self):self.assertEqual(optima(Scenario(2,10)),[2])
 def test_conservation(self):
  for g in range(13):
   completed,remaining=outcome(Scenario(10,2),g)
   self.assertEqual(completed+remaining,12)
 def test_capacity(self):
  for g in range(13):self.assertLessEqual(outcome(Scenario(10,2),g)[0],12)
 def test_invalid(self):
  with self.assertRaises(ValueError):outcome(Scenario(10,2),13)
if __name__=="__main__":unittest.main()
