"""P9b: falsification gates for the proposed one-tick release constraint."""
import sys,unittest
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE/'code'))
import tick_order_ablation as ab
from dt_convergence import SCENARIOS,PLANS,arrivals_for

class TickReleaseAblationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=next(s for s in SCENARIOS if s.name=='upstream_peak')
  cls.p=next(p for p in PLANS if p.key==(24.,24.,24.))
  cls.arr=arrivals_for(cls.s,223)
 def test_original_trace_contains_an_earlier_timestamp(self):
  value,n=ab.eval_run(ab.original_run,self.p,self.arr,18.,.25)
  self.assertEqual(value,19661.5)
  self.assertEqual(n,56)
 def test_one_tick_release_gate_removes_timestamp_overlap(self):
  value,n=ab.eval_run(ab.mod.run,self.p,self.arr,18.,.25)
  self.assertEqual(n,0)
  self.assertEqual(value,19679.5)
 def test_grid_resonance_persists_after_release_gate(self):
  v0,n0=ab.eval_run(ab.mod.run,self.p,self.arr,18.,.25)
  v1,n1=ab.eval_run(ab.mod.run,self.p,self.arr,18.,.125)
  self.assertEqual(n0,0);self.assertEqual(n1,0)
  self.assertGreater(abs(v1-v0),1000)
 def test_original_unmodified_via_sealed_hash(self):
  import hashlib,json
  original=HERE/'reference/T2_v69_P2/corridor.py'
  info=json.loads((HERE/'source_receipts/original_P2_hashes.json').read_text())
  self.assertEqual(hashlib.sha256(original.read_bytes()).hexdigest(),info['members_sha256']['T2_v69_P2/corridor.py'])
if __name__=='__main__':unittest.main()
