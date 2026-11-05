import unittest,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from variable_lane_curvature import lane_curvature_variable

def xml(kind='<arc curvature="0.02"/>',width='a="4" b="0" c="0" d="0"',offset='',elev='a="0" b="0" c="0" d="0"',roll=''):
 return f'<OpenDRIVE><road id="a" length="20"><planView><geometry s="0" x="0" y="0" hdg="0" length="20">{kind}</geometry></planView><elevationProfile><elevation s="0" {elev}/></elevationProfile><lateralProfile>{roll}</lateralProfile><lanes>{offset}<laneSection s="0"><right><lane id="-1" type="driving"><width sOffset="0" {width}/></lane></right></laneSection></lanes></road></OpenDRIVE>'

class VariableLane(unittest.TestCase):
 def test_constant_curved(self):self.assertAlmostEqual(lane_curvature_variable(xml(),'a',-1,10)['k_lane_inv_m'],.02/1.04)
 def test_straight_constant(self):self.assertEqual(lane_curvature_variable(xml(kind='<line/>'),'a',-1,10)['k_lane_inv_m'],0)
 def test_variable_linear_straight(self):
  x=xml(kind='<line/>',offset='<laneOffset s="0" a="0" b=".1" c="0" d="0"/>')
  self.assertAlmostEqual(lane_curvature_variable(x,'a',-1,10)['k_lane_inv_m'],0)
 def test_variable_quadratic_straight(self):
  x=xml(kind='<line/>',offset='<laneOffset s="0" a="0" b="0" c=".01" d="0"/>')
  k=lane_curvature_variable(x,'a',-1,10)['k_lane_inv_m'];self.assertAlmostEqual(k,.02/(1+.2**2)**1.5)
 def test_spiral_with_variable_offset(self):
  x=xml(kind='<spiral curvStart="0" curvEnd=".1"/>',offset='<laneOffset s="0" a="0" b=".01" c="0" d="0"/>')
  z=lane_curvature_variable(x,'a',-1,10);self.assertEqual(z['status'],'PLANAR_DIFFERENTIAL_GEOMETRY_ONLY');self.assertTrue(math.isfinite(z['k_lane_inv_m']))
 def test_nonplanar_unknown(self):self.assertEqual(lane_curvature_variable(xml(elev='a="0" b=".02" c="0" d="0"'),'a',-1,10)['status'],'UNKNOWN')
 def test_roll_unknown(self):self.assertEqual(lane_curvature_variable(xml(roll='<superelevation s="0" a=".1" b="0" c="0" d="0"/>'),'a',-1,10)['status'],'UNKNOWN')
 def test_negative_width_unknown(self):self.assertEqual(lane_curvature_variable(xml(width='a="-2" b="0" c="0" d="0"'),'a',-1,10)['status'],'UNKNOWN')
 def test_offset_cusp(self):
  x=xml(kind='<arc curvature=".1"/>',offset='<laneOffset s="0" a="12" b="0" c="0" d="0"/>')
  self.assertEqual(lane_curvature_variable(x,'a',-1,10)['reason'],'OFFSET_CUSP_OR_DIRECTION_REVERSAL')
 def test_no_safe_speed(self):self.assertIsNone(lane_curvature_variable(xml(),'a',-1,5)['safe_speed_mps'])
 def test_bad_road(self):
  with self.assertRaises(ValueError):lane_curvature_variable(xml(),'not',-1,5)
 def test_bad_station(self):
  with self.assertRaises(ValueError):lane_curvature_variable(xml(),'a',-1,20)
if __name__=='__main__':unittest.main()
