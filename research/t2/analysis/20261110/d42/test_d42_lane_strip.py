"""Eight synthetic lane-strip validity tests. Not empirical validation."""
import unittest,xml.etree.ElementTree as ET
from d42_lane_strip import cubic_at,driving_lane_strips,scan_lane_crossings

class Lanes(unittest.TestCase):
 def test_polynomial_piece(self):
  x=ET.fromstring('<t><width sOffset="0" a="2" b="1"/><width sOffset="2" a="5"/></t>')
  self.assertAlmostEqual(cubic_at(x.findall('width'),1),3)
  self.assertAlmostEqual(cubic_at(x.findall('width'),3),5)
 def test_right_lane_widths(self):
  r=ET.fromstring('<road><lanes><laneSection s="0"><right><lane id="-1" type="driving"><width sOffset="0" a="3"/></lane><lane id="-2" type="shoulder"><width sOffset="0" a="2"/></lane><lane id="-3" type="driving"><width sOffset="0" a="4"/></lane></right></laneSection></lanes></road>')
  self.assertEqual(driving_lane_strips(r,0),[('-1',-3,0),('-3',-9,-5)])
 def test_forward_lane(self):
  self.assertEqual(len(scan_lane_crossings([('a',0,-.1,-1,4,0),('a',.05,.1,-1,4,0)],0,0,0,[('-1',-3,0)])),1)
 def test_outside_strip(self):
  self.assertEqual(len(scan_lane_crossings([('a',0,-.1,2,4,0),('a',.05,.1,2,4,0)],0,0,0,[('-1',-3,0)])),0)
 def test_boundary_ambiguous(self):
  self.assertEqual(len(scan_lane_crossings([('a',0,-.1,-3,4,0),('a',.05,.1,-3,4,0)],0,0,0,[('-1',-3,0),('-2',-6,-3)])),0)
 def test_gap_censored(self):
  self.assertEqual(len(scan_lane_crossings([('a',0,-.1,-1,4,0),('a',.25,.1,-1,4,0)],0,0,0,[('-1',-3,0)])),0)
 def test_wrong_direction(self):
  self.assertEqual(len(scan_lane_crossings([('a',0,-.1,-1,-4,0),('a',.05,.1,-1,-4,0)],0,0,0,[('-1',-3,0)])),0)
 def test_lane_offset_fails_closed(self):
  r=ET.fromstring('<road><lanes><laneOffset s="0" a="1"/><laneSection s="0"><right><lane id="-1" type="driving"><width sOffset="0" a="3"/></lane></right></laneSection></lanes></road>')
  with self.assertRaises(NotImplementedError):driving_lane_strips(r,0)
if __name__=='__main__':unittest.main()
