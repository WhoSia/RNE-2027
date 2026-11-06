import sys,unittest,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from sumo_gate import prepare,run_if_available
from validation import sumo_tripinfo

class SumoGates(unittest.TestCase):
 def test_scenario_xml_deterministic(self):
  with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
   x=prepare(a);y=prepare(b)
   self.assertEqual({k:v['sha256'] for k,v in x.items()},{k:v['sha256'] for k,v in y.items()})
 def test_no_fabricated_tripinfo(self):
  with tempfile.TemporaryDirectory() as a:
   prepare(a)
   with self.assertRaises(FileNotFoundError):sumo_tripinfo(Path(a)/'tripinfo.xml')
 def test_local_status_does_not_claim_execution(self):
  with tempfile.TemporaryDirectory() as a:
   x=run_if_available(a)
   self.assertIn(x['independent_sumo_run'],('NOT_EXECUTED','EXECUTED'))
   if not x['sumo_installed'] or not x['netconvert_installed']:
    self.assertEqual(x['independent_sumo_run'],'NOT_EXECUTED')

if __name__=='__main__':unittest.main()
