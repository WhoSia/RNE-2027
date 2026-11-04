import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
import dt_convergence as d

class NumericalGateTests(unittest.TestCase):
 def test_policy_grid_and_no_mutation(self):
  self.assertEqual(len(d.PLANS),27)
  a=d.arrivals_for(d.SCENARIOS[0],211)
  original=list(a)
  d.one(d.PLANS[0],a,18.,.5,630)
  self.assertEqual(original,a)
 def test_determinism(self):
  a=d.arrivals_for(d.SCENARIOS[0],211)
  self.assertEqual(d.one(d.PLANS[0],a,18.,.25),d.one(d.PLANS[0],a,18.,.25))
 def test_conservation_with_both_dt(self):
  a=d.arrivals_for(d.SCENARIOS[-1],223)
  for dt in d.DTS:
   q=d.one(d.PLANS[1],a,60,dt)
   self.assertEqual(q['issues'],0)
   self.assertEqual(q['generated'],q['completed']+q['unfinished'])
 def test_numeric_comparison_tie_policy(self):
  a={'(24,24,0)':{'objective':10},'(24,30,0)':{'objective':12}}
  b={'(24,24,0)':{'objective':11},'(24,30,0)':{'objective':13}}
  self.assertEqual(min(a,key=lambda x:(a[x]['objective'],x)),min(b,key=lambda x:(b[x]['objective'],x)))
 def test_fixed_horizon_completed(self):
  a=d.arrivals_for(d.SCENARIOS[0],211)
  for dt in d.DTS:
   q=d.one(d.PLANS[0],a,18.,dt)
   self.assertEqual(q['unfinished'],0)

if __name__=='__main__':unittest.main()
