import unittest,sys
from pathlib import Path
from datetime import datetime, timezone
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from osm_relations import ingest,evaluate

def R(kind='no_left_turn',via_type='node',tags=None):
 return {'id':123,'tags':tags or {'type':'restriction','restriction':kind},
         'members':[{'type':'way','role':'from','ref':10},{'type':via_type,'role':'via','ref':20},
                    {'type':'way','role':'to','ref':30}]}
def at(x='2026-11-02T08:30:00+09:00'):return datetime.fromisoformat(x)
def ev(rr,to=30,mode='passenger',turn='left',time=None):return evaluate(rr,'10','20',str(to),mode,turn,time or at(),'Asia/Seoul')
class RelationsTests(unittest.TestCase):
 def test_no_left_turn_deny(self):self.assertEqual(ev(ingest([R()]).relations)['status'],'DENY')
 def test_other_path_is_unknown_not_allow(self):self.assertEqual(ev(ingest([R()]).relations,31)['status'],'UNKNOWN')
 def test_only_right_turn_denies_other_destination(self):self.assertEqual(ev(ingest([R('only_right_turn')]).relations,31,turn='straight')['status'],'DENY')
 def test_only_target_unknown_not_explicit_permission(self):self.assertEqual(ev(ingest([R('only_right_turn')]).relations,30,turn='right')['status'],'UNKNOWN')
 def test_exception_bicycle(self):
  r=R(tags={'type':'restriction','restriction':'no_left_turn','except':'bicycle;psv'})
  rel=ingest([r]).relations
  self.assertEqual(ev(rel,mode='bicycle')['status'],'UNKNOWN');self.assertEqual(ev(rel,mode='passenger')['status'],'DENY')
 def test_mode_specific(self):
  rel=ingest([R(tags={'type':'restriction','restriction:hgv':'no_left_turn'})]).relations
  self.assertEqual(ev(rel,mode='passenger')['status'],'UNKNOWN');self.assertEqual(ev(rel,mode='hgv')['status'],'DENY')
 def test_conditional_peak(self):
  rel=ingest([R(tags={'type':'restriction','restriction:conditional':'no_left_turn @ (Mo-Fr 07:00-09:00)'})]).relations
  self.assertEqual(ev(rel)['status'],'DENY')
  self.assertEqual(ev(rel,time=at('2026-11-02T09:00:00+09:00'))['status'],'UNKNOWN')
 def test_overnight_conditions(self):
  rel=ingest([R(tags={'type':'restriction','restriction:conditional':'no_left_turn @ (Mo 22:00-06:00)'})]).relations
  self.assertEqual(ev(rel,time=at('2026-11-03T03:00:00+09:00'))['status'],'DENY')
 def test_via_way_unresolved(self):self.assertIn('via',ingest([R(via_type='way')]).unresolved[0]['reason'])
 def test_solar_condition_unresolved(self):self.assertEqual(len(ingest([R(tags={'type':'restriction','restriction:conditional':'no_left_turn @ (sunrise-sunset)'})]).relations),0)
 def test_unknown_except_unresolved(self):self.assertEqual(len(ingest([R(tags={'type':'restriction','restriction':'no_left_turn','except':'spacecraft'})]).unresolved),1)
 def test_ambiguous_restriction_unresolved(self):self.assertEqual(len(ingest([R(tags={'type':'restriction','restriction':'no_left_turn','restriction:conditional':'no_left_turn @ (Mo 07:00-09:00)'})]).unresolved),1)
 def test_wrong_turn_metadata_flagged(self):self.assertEqual(ev(ingest([R()]).relations,turn='right')['status'],'UNKNOWN')
 def test_naive_time_rejected(self):
  with self.assertRaises(ValueError):ev(ingest([R()]).relations,time=datetime(2026,11,2,8))
 def test_invalid_only_target_never_allow(self):self.assertNotEqual(ev(ingest([R('only_left_turn')]).relations)['status'],'ALLOW')
if __name__=='__main__':unittest.main()
