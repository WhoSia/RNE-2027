from fractions import Fraction as F
from unittest import TestCase
from finite_sensor_information import (
  worlds, randomized_regret, deterministic_regret, partitioned_regret,
  binary_noisy_regret, solve3, report)

class FinitePolicyTest(TestCase):
 def test_vertices_solve_linear_system(self):
  self.assertEqual(solve3(((1,0,0,1),(0,1,0,2),(0,0,1,3))),(1,2,3))
 def test_empty_or_known_regrets(self):
  self.assertEqual(randomized_regret([-27,346]),F(9342,373))
  self.assertEqual(deterministic_regret([-27,346]),27)
  self.assertEqual(partitioned_regret(worlds(),lambda m,b:(m,b)),0)
 def test_noisy_zero_and_half_error_bounds(self):
  w=worlds()
  base=randomized_regret(d for _,_,d in w)
  self.assertEqual(binary_noisy_regret(w,lambda m,b:int(m==1),F(1,2))[2],base)
  self.assertEqual(binary_noisy_regret(w,lambda m,b:int(m==1),F(0))[2],
                   partitioned_regret(w,lambda m,b:m))
 def test_info_never_hurts_and_error_monotonic(self):
  w=worlds()
  base=randomized_regret(d for _,_,d in w)
  for selector in [lambda m,b:int(m==1),lambda m,b:b[0],lambda m,b:b[1],lambda m,b:b[2]]:
   scores=[binary_noisy_regret(w,selector,e)[2] for e in (F(0),F(1,10),F(3,10),F(1,2))]
   self.assertEqual(scores,sorted(scores));self.assertLessEqual(scores[-1],base)
 def test_report_is_stable(self):
  result=report()
  self.assertIn('physical_mode',result['binary_forecast_error_by_actual_world']['3/10'])
