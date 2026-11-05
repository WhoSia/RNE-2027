import unittest,sys
from pathlib import Path
from datetime import datetime
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from road_rules import Window
from variable_lanes import ReversibleLane,LaneWindow
D=lambda a,b: Window(a*60,b*60,frozenset({0,1,2,3,4}))
T=lambda s: datetime.fromisoformat('2026-11-02T'+s+'+09:00')
class ReversibleTests(unittest.TestCase):
 def test_forward(self):
  l=ReversibleLane('c',(LaneWindow('forward',D(7,9),'sign'),),'Asia/Seoul')
  self.assertEqual(l.state_at(T('08:00:00'))['direction'],'forward')
 def test_unlisted_time_unknown(self):
  l=ReversibleLane('c',(LaneWindow('forward',D(7,9),'sign'),),'Asia/Seoul')
  self.assertEqual(l.state_at(T('10:00:00'))['status'],'UNKNOWN')
 def test_gap_for_clearance(self):
  l=ReversibleLane('c',(LaneWindow('forward',D(7,9),'sign'),LaneWindow('closed',D(9,10),'sign'),LaneWindow('reverse',D(10,12),'sign')),'Asia/Seoul')
  self.assertEqual(l.state_at(T('09:30:00'))['status'],'CLOSED')
  self.assertEqual(l.state_at(T('10:30:00'))['direction'],'reverse')
 def test_overlap_detected(self):
  l=ReversibleLane('c',(LaneWindow('forward',D(7,10),'a'),LaneWindow('reverse',D(9,12),'b')),'Asia/Seoul')
  self.assertEqual(l.state_at(T('09:30:00'))['status'],'CONFLICT')
 def test_no_occupancy_certificate(self):
  l=ReversibleLane('c',(LaneWindow('reverse',D(7,9),'sign'),),'Asia/Seoul')
  self.assertIn('No occupancy',l.state_at(T('08:00:00'))['warning'])
 def test_naive_rejected(self):
  l=ReversibleLane('c',(LaneWindow('forward',D(7,9),'a'),),'Asia/Seoul')
  with self.assertRaises(ValueError):l.state_at(datetime(2026,11,2,8))
if __name__=='__main__':unittest.main()
