import unittest
from dual_lane_v11 import DualConfig,run
from spatial_v10 import Config,arrivals
from dataclasses import replace

class TimeGates(unittest.TestCase):
 def c(self,*,windows=(),allow=True,pocket=14.):
  return DualConfig(base=Config(duration_s=360,seed=0,demand_vph=1800,left_fraction=.5,pocket_length_m=pocket),through_B_share=0.,allow_lane_changes=allow,change_zone_m=70.,receiver_mode='cells',receiver_slots=4,lane_change_windows=windows)
 def test_invalid_windows_rejected(self):
  for w in (((4,4),),((-1,4),),((4,1000),),((30,40),(38,60)),((60,70),(5,10)),((2.5,3),)):
   with self.subTest(w=w),self.assertRaises(ValueError):run(self.c(windows=w))
 def test_no_gate_reproduces_legacy_engine(self):
  c=self.c()
  left=run(c)
  self.assertEqual(left['config']['lane_change_windows'],())
  self.assertGreater(left['changes_A_to_B'],0)
 def test_single_window_accepts_changes_only_inside_window(self):
  w=((20,35),(140,155),(260,275))
  r=run(self.c(windows=w),trace=True)
  self.assertEqual(len(r['lane_change_events']),r['changes_A_to_B'])
  self.assertTrue(all(any(a<=e['t']<b for a,b in w) for e in r['lane_change_events']))
 def test_permission_false_disables_windows(self):
  r=run(self.c(windows=((20,35),),allow=False),trace=True)
  self.assertEqual(r['changes_A_to_B'],0)
  self.assertEqual(r['lane_change_events'],[])
 def test_70m_pocket_is_outside_70m_change_zone(self):
  r=run(self.c(pocket=70.),trace=True)
  self.assertEqual(r['changes_A_to_B'],0)
 def test_trace_movement_events_are_real_lateral_one_dimension(self):
  r=run(self.c(),trace=True)
  self.assertGreater(len(r['lane_change_events']),0)
  prev={}
  for f in r['frames']:
   now={vid:(lane,x) for lane in ('A','B') for x,vid,route in f[lane]}
   for vid,(lane,x) in now.items():
    if vid in prev:
     oldlane,oldx=prev[vid]
     self.assertLessEqual(int(lane!=oldlane)+abs(x-oldx),1)
   prev=now
