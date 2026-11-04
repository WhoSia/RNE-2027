import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from network import Lane,Movement,Phase,SignalPlan,Network
from events import Demand,EventEngine
from demo import NET,CASES
from policy_search import alternatives,optimize,score

class OptimizerTests(unittest.TestCase):
 def test_18_feasible_policies(self):
  self.assertEqual(len(list(alternatives(NET,'J',12,(3,4,5,6,7,8),(0,1,2)))),18)
 def test_all_candidates_valid_and_fixed_cycle(self):
  for _,_,n in alternatives(NET,'J',12,(3,4,5,6,7,8),(0,1,2)):
   self.assertEqual(n.plan('J').cycle_s,12)
 def test_fixed_demand_never_mutates(self):
  a=CASES['balanced'];original=tuple(a)
  optimize(NET,'J',a,100,12,(3,4,5,6,7,8),(0,1,2))
  self.assertEqual(a,original)
 def test_all_3_synthetic_cases_complete(self):
  for name,a in CASES.items():
   r=optimize(NET,'J',a,100,12,(3,4,5,6,7,8),(0,1,2))
   self.assertEqual(r[0].completed,len(a),name)
 def test_main_peak_prefers_more_main_green(self):
  r=optimize(NET,'J',CASES['main_peak'],100,12,(3,4,5,6,7,8),(0,1,2))
  self.assertEqual((r[0].split_main_s,r[0].offset_s),(7,1))
 def test_side_peak_prefers_less_main_green(self):
  r=optimize(NET,'J',CASES['side_peak'],100,12,(3,4,5,6,7,8),(0,1,2))
  self.assertEqual((r[0].split_main_s,r[0].offset_s),(3,2))
 def test_two_junction_different_cycles(self):
  n=Network((Lane('a',50,20),Lane('b',50,20),Lane('c',50,20),Lane('d',50,20)),
   (Movement('x','J0','a','b','straight',1),Movement('y','J1','c','d','straight',1)),
   (SignalPlan('J0',(Phase(4,frozenset({'x'})),Phase(2,frozenset()))),SignalPlan('J1',(Phase(5,frozenset({'y'})),Phase(3,frozenset())),1)))
  self.assertEqual([p.cycle_s for p in n.plans],[6,8])
  r=EventEngine(n,(Demand('X','x',0),Demand('Y','y',1)),20).run()
  self.assertEqual((r['completed'],r['unfinished']),(2,0))
 def test_unfeasible_candidates_rejected(self):
  with self.assertRaises(ValueError):optimize(NET,'J',CASES['balanced'],100,12,(0,12),(0,))
if __name__=='__main__':unittest.main()
