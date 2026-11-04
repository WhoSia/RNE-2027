import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from network import Lane,Movement,Phase,SignalPlan,Network
from events import Demand,EventEngine

def case(first_arrival):
 n=Network((Lane('up',80,40),Lane('out',8,8)),
  (Movement('m','J','up','out','straight',2),),
  (SignalPlan('J',(Phase(50,frozenset({'m'})),Phase(10,frozenset()))),))
 return n,(Demand('v1','m',first_arrival),Demand('v2','m',47.0))
class BoundaryCausalTests(unittest.TestCase):
 def test_early_release_enables_before_last_green(self):
  n,ds=case(45.1);z=EventEngine(n,ds,125).run()
  a={x['vehicle']:x['t_s'] for x in z['events'] if x['event']=='admit'}
  self.assertAlmostEqual(a['v1'],45.1);self.assertAlmostEqual(a['v2'],47.1)
 def test_late_release_misses_phase_window(self):
  n,ds=case(46.2);z=EventEngine(n,ds,125).run()
  a={x['vehicle']:x['t_s'] for x in z['events'] if x['event']=='admit'}
  self.assertAlmostEqual(a['v1'],46.2);self.assertAlmostEqual(a['v2'],60.0)
 def test_admission_after_legal_capacity_release(self):
  for first in (45.1,46.2):
   n,ds=case(first);z=EventEngine(n,ds,125).run()
   t={}
   for e in z['events']:
    if e['vehicle']=='v1' and e['event']=='release':t['release']=e['t_s']
    if e['vehicle']=='v2' and e['event']=='admit':t['admit']=e['t_s']
   self.assertGreaterEqual(t['admit'],t['release'])
if __name__=='__main__':unittest.main()
