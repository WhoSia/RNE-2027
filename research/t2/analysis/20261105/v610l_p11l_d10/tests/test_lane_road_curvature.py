import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from lane_road_curvature import lane_curvature

def x(k=.02,w=4.,offset='',roll='',elev='<elevationProfile><elevation s="0" a="0" b="0" c="0" d="0"/></elevationProfile>'):
 return f'<OpenDRIVE><road id="a" length="20"><planView><geometry s="0" x="0" y="0" hdg="0" length="20"><arc curvature="{k}"/></geometry></planView>{elev}<lateralProfile>{roll}</lateralProfile><lanes>{offset}<laneSection s="0"><right><lane id="-1" type="driving"><width sOffset="0" a="{w}" b="0" c="0" d="0"/></lane></right></laneSection></lanes></road></OpenDRIVE>'
class T(unittest.TestCase):
 def test_right_lane_expands_radius(self):self.assertAlmostEqual(lane_curvature(x(), 'a',-1,10)['k_lane_planar_inv_m'],.02/(1+.04))
 def test_left_and_right_differ(self):self.assertLess(lane_curvature(x(), 'a',-1,10)['k_lane_planar_inv_m'],.02)
 def test_straight(self):self.assertEqual(lane_curvature(x(k=0), 'a',-1,10)['k_lane_planar_inv_m'],0)
 def test_variable_offset_unknown(self):self.assertEqual(lane_curvature(x(offset='<laneOffset s="0" a="0" b=".1" c="0" d="0"/>'), 'a',-1,10)['status'],'UNKNOWN')
 def test_nonzero_roll_unknown(self):self.assertEqual(lane_curvature(x(roll='<superelevation s="0" a=".1" b="0" c="0" d="0"/>'),'a',-1,10)['status'],'UNKNOWN')
 def test_nonplanar_unknown(self):self.assertEqual(lane_curvature(x(elev='<elevationProfile><elevation s="0" a="0" b=".01" c="0" d="0"/></elevationProfile>'),'a',-1,10)['status'],'UNKNOWN')
 def test_zero_width_unknown(self):self.assertEqual(lane_curvature(x(w=0),'a',-1,10)['status'],'UNKNOWN')
 def test_unknown_lane(self):self.assertEqual(lane_curvature(x(),'a',-2,10)['status'],'UNKNOWN')
 def test_speed_not_calculated(self):self.assertNotIn('safe_speed',lane_curvature(x(),'a',-1,10))
if __name__=='__main__':unittest.main()
