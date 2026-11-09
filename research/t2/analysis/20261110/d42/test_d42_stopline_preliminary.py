"""Contract tests. Synthetic geometry, not field agreement."""
import math,unittest,xml.etree.ElementTree as ET
from d42_stopline_preliminary import reference_pose, transitions

class CrossingContract(unittest.TestCase):
 def test_line(self):
  r=ET.fromstring('<road><planView><geometry s="0" x="1" y="2" hdg="0" length="10"><line/></geometry></planView></road>')
  self.assertEqual(reference_pose(r,3),(4.,2.,0.))
 def test_arc(self):
  r=ET.fromstring('<road><planView><geometry s="0" x="0" y="0" hdg="0" length="4"><arc curvature="0.5"/></geometry></planView></road>')
  x,y,h=reference_pose(r,math.pi)
  self.assertAlmostEqual(x,2);self.assertAlmostEqual(y,2);self.assertAlmostEqual(h,math.pi/2)
 def test_forward(self):
  self.assertEqual(transitions([('a',0,-.1,0,5,0),('a',.05,.15,0,5,0)],0,0,0),(1,0))
 def test_reverse(self):
  self.assertEqual(transitions([('a',0,.1,0,-5,0),('a',.05,-.15,0,-5,0)],0,0,0),(0,1))
 def test_gap_censored(self):
  self.assertEqual(transitions([('a',0,-.1,0,5,0),('a',.3,.15,0,5,0)],0,0,0),(0,0))
 def test_speed_rejected(self):
  self.assertEqual(transitions([('a',0,-.001,0,.02,0),('a',.05,.001,0,.02,0)],0,0,0),(0,0))
 def test_lateral_rejected(self):
  self.assertEqual(transitions([('a',0,-.1,18,5,0),('a',.05,.15,18,5,0)],0,0,0),(0,0))
 def test_spiral_rejected(self):
  r=ET.fromstring('<road><planView><geometry s="0" x="0" y="0" hdg="0" length="4"><spiral curvStart="0" curvEnd="0.5"/></geometry></planView></road>')
  with self.assertRaises(NotImplementedError):reference_pose(r,2)
if __name__=='__main__':unittest.main()
