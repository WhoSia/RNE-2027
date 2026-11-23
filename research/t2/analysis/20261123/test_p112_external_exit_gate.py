import unittest
import json
from pathlib import Path
from p112_external_exit_gate import audit

ROOT=Path(__file__).resolve().parent
class ExternalExitGateTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.manifest=json.loads((ROOT/'P111_RESULT.json').read_text())
  cls.reference=[]
  for arm in cls.manifest['arms_data']:
   tape=next(x for x in cls.manifest['tapes'] if x['seed']==arm['seed'] and x['family']==arm['family'])
   for evt in arm['terminal_exits']:
    arrival=tape['events'][evt['id']]
    cls.reference.append(dict(seed=str(arm['seed']),family=arm['family'],onset=arm['onset'],period_s=str(arm['period_s']),vehicle_id=str(evt['id']),movement=evt['movement'],arrival_second=str(arrival['enter_time_s']),exit_second=str(evt['t'])))

 def test_positive_adapter_fixture_not_independent_sumo(self):
  r=audit(self.manifest,self.reference)
  self.assertTrue(r['passed']);self.assertFalse(r['policy_comparison_allowed'])
  self.assertEqual(r['sign_agreement'],8)
  self.assertEqual(r['required_arms'],16)
  self.assertTrue(all(x['external_cost_delta_30_minus_60']==x['t2_cost_delta_30_minus_60'] for x in r['contrasts']))
 def test_missing_exit_rejected(self):
  r=audit(self.manifest,self.reference[:-1]);self.assertFalse(r['passed']);self.assertFalse(r['policy_comparison_allowed'])
 def test_wrong_route_rejected(self):
  rows=[dict(x) for x in self.reference];rows[0]['movement']='S' if rows[0]['movement']=='L' else 'L'
  self.assertFalse(audit(self.manifest,rows)['passed'])
 def test_duplicate_exit_rejected(self):
  self.assertFalse(audit(self.manifest,self.reference+[self.reference[0]])['passed'])
 def test_future_censor_rejected(self):
  rows=[dict(x) for x in self.reference];rows[0]['exit_second']='1440'
  self.assertFalse(audit(self.manifest,rows)['passed'])
 def test_arrival_mismatch_rejected(self):
  rows=[dict(x) for x in self.reference];rows[0]['arrival_second']=str(int(rows[0]['arrival_second'])+1)
  self.assertFalse(audit(self.manifest,rows)['passed'])
 def test_extra_arm_rejected(self):
  rows=[dict(x) for x in self.reference];rows[0]['seed']='999999'
  self.assertFalse(audit(self.manifest,rows)['passed'])

if __name__=='__main__':unittest.main()
