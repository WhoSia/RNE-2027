import sys,unittest
from datetime import datetime,timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from road_ir import RoadLane,LaneConnection,RoadIR
from road_rules import Rule,Window,RoadRules,readiness

NET=RoadIR((RoadLane('a',30,10),RoadLane('b',30,10),RoadLane('c',30,10)),
           (LaneConnection('ab','a','b','J','left'),LaneConnection('bc','b','c','J2','straight')),
           'synthetic',('turn_restrictions_unverified',))
def now(d='2026-11-02T08:20:00+09:00'):return datetime.fromisoformat(d)
class TestRegulatory(unittest.TestCase):
 def test_default_unknown_not_permitted(self):
  self.assertEqual(RoadRules(NET,(),'Asia/Seoul').evaluate('ab','passenger',now()).status,'UNKNOWN')
 def test_mode_specific(self):
  a=RoadRules(NET,(Rule('ab','bus','allow','declaration:1'),),'Asia/Seoul')
  self.assertEqual(a.evaluate('ab','bus',now()).status,'ALLOW')
  self.assertEqual(a.evaluate('ab','passenger',now()).status,'UNKNOWN')
 def test_explicit_denial(self):
  a=RoadRules(NET,(Rule('ab','passenger','allow','source:a'),Rule('ab','passenger','deny','source:b')),'Asia/Seoul')
  self.assertEqual(a.evaluate('ab','passenger',now()).status,'DENY')
 def test_weekday_time_window(self):
  a=RoadRules(NET,(Rule('ab','passenger','deny','sign',Window(7*60,9*60,frozenset({0,1,2,3,4}))),),'Asia/Seoul')
  self.assertEqual(a.evaluate('ab','passenger',now()).status,'DENY')
  self.assertEqual(a.evaluate('ab','passenger',now('2026-11-02T09:00:00+09:00')).status,'UNKNOWN')
  self.assertEqual(a.evaluate('ab','passenger',now('2026-11-01T08:20:00+09:00')).status,'UNKNOWN')
 def test_overnight_weekday_anchor(self):
  a=RoadRules(NET,(Rule('ab','passenger','deny','sign',Window(22*60,6*60,frozenset({0}))),),'Asia/Seoul')
  self.assertEqual(a.evaluate('ab','passenger',now('2026-11-03T03:00:00+09:00')).status,'DENY')
  self.assertEqual(a.evaluate('ab','passenger',now('2026-11-03T06:00:00+09:00')).status,'UNKNOWN')
 def test_timezone_conversion(self):
  a=RoadRules(NET,(Rule('ab','passenger','allow','sign',Window(8*60,9*60,frozenset({0}))),),'Asia/Seoul')
  self.assertEqual(a.evaluate('ab','passenger',now('2026-11-01T23:20:00+00:00')).status,'ALLOW')
 def test_no_naive_clock(self):
  with self.assertRaises(ValueError):RoadRules(NET,(),'Asia/Seoul').evaluate('ab','passenger',datetime(2026,11,2,8))
 def test_invalid_rule_reference(self):
  with self.assertRaises(ValueError):RoadRules(NET,(Rule('x','passenger','allow','sign'),),'Asia/Seoul')
 def test_route_all_links_required(self):
  a=RoadRules(NET,(Rule('ab','passenger','allow','sign'),),'Asia/Seoul')
  self.assertEqual([r.status for r in a.verified_route(('a','b','c'),'passenger',now())],['ALLOW','UNKNOWN'])
 def test_broken_route(self):
  with self.assertRaises(ValueError):RoadRules(NET,(),'Asia/Seoul').verified_route(('a','c'),'passenger',now())
 def test_unresolved_audit(self):
  v=readiness(NET,RoadRules(NET,(),'Asia/Seoul'),'passenger',now())
  self.assertEqual(v['unknown'],2)
  self.assertTrue(v['research_only'])
 def test_bad_window(self):
  with self.assertRaises(ValueError):Window(1440,0)
 def test_full_day(self):
  self.assertTrue(Window(0,0,frozenset({0})).active(now()))
if __name__=='__main__':unittest.main()
