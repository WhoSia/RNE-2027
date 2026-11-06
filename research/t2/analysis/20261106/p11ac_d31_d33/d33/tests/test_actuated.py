import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from actuated import Actuated
from policy_audit import compare,aggregate,controller_at
from micro_world import Road,Vehicle,run

class ActuatedTests(unittest.TestCase):
 def test_no_conflicting_greens_and_all_red(self):
  c=Actuated(min_green=3,max_green=5,clearance=2)
  for t in range(40):
   c.observe(t,{'A':2,'C':3})
   assert not (c.permits('A',t) and c.permits('C',t))
  for i,(t,phase) in enumerate(c.log):
   if phase=='ALL_RED':
    self.assertEqual(c.log[i+1][0]-t,2)
    self.assertNotEqual(c.log[i+1][1],'ALL_RED')
 def test_reject_skip_and_bad_observation(self):
  c=Actuated();c.observe(0,{'A':0,'C':0})
  with self.assertRaises(ValueError):c.observe(2,{'A':0,'C':0})
  with self.assertRaises(ValueError):Actuated(clearance=0)
 def test_model_gate_no_fixed_conflict(self):
  r={'A':Road('A',15,1,8)}
  with self.assertRaises(ValueError):run(r,[Vehicle('a',('A',),0)],controller=Actuated(),signals={'A':None})
 def test_paired_policy_court(self):
  rows,traces=compare(seeds=(101,),holdout=(211,),n=16)
  self.assertEqual(len(rows),8)
  self.assertTrue(all(x['collisions']==0 for x in rows))
  self.assertEqual({r['policy'] for r in rows},{'fixed6','fixed10','fixed14','actuated'})
  self.assertGreater(len(traces['holdout:211']),1)
 def test_cohort_disjoint(self):
  with self.assertRaises(ValueError): compare(seeds=(11,),holdout=(11,))
 def test_censor_not_optimistically_ranked(self):
  rows,_=compare(seeds=(101,),holdout=(211,),horizon=25,n=16)
  self.assertTrue(any(r['uncompleted'] for r in rows))
  self.assertTrue(all(r['mean_s'] is None for r in rows if r['uncompleted']))
  self.assertTrue(any(r['censored_scenarios'] for r in aggregate(rows)))

if __name__=='__main__':unittest.main()
