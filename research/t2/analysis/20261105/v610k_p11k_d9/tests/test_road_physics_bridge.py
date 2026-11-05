import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from road_physics_bridge import sample_road_physics
X='''<OpenDRIVE><road id="r" length="20"><planView><geometry s="0" x="0" y="0" hdg="0" length="20"><arc curvature="0.01"/></geometry></planView><elevationProfile><elevation s="0" a="0" b="0.02" c="0" d="0"/></elevationProfile><lateralProfile><superelevation s="0" a="0.05" b="0" c="0" d="0"/></lateralProfile><lanes><laneSection s="0"><right><lane id="-1" type="driving"><width sOffset="0" a="3.5" b="0" c="0" d="0"/><material sOffset="0" surface="asphalt" friction="0.8"/></lane></right></laneSection></lanes></road></OpenDRIVE>'''
class Bridge(unittest.TestCase):
 def test_curvature_from_xodr(self):self.assertAlmostEqual(sample_road_physics(X,'r',-1,10,speed_mps=10)['signed_curvature_inv_m'],.01)
 def test_grade_from_xodr(self):self.assertAlmostEqual(sample_road_physics(X,'r',-1,10,speed_mps=10)['grade_rad'],__import__('math').atan(.02))
 def test_bank_from_xodr(self):self.assertAlmostEqual(sample_road_physics(X,'r',-1,10,speed_mps=10)['bank_rad'],.05)
 def test_source_mu_not_effective(self):
  x=sample_road_physics(X,'r',-1,10,speed_mps=10)
  self.assertEqual(x['source_material']['mu_source'],.8)
  self.assertIsNone(x['friction_demand']['mu_effective_assumed'])
 def test_explicit_hypothesis(self):
  x=sample_road_physics(X,'r',-1,10,speed_mps=10,effective_mu_hypothesis=.35)
  self.assertEqual(x['friction_demand']['status'],'HYPOTHETICAL_COMPARISON')
 def test_missing_elevation(self):
  y=X.replace('<elevationProfile><elevation s="0" a="0" b="0.02" c="0" d="0"/></elevationProfile>','')
  self.assertEqual(sample_road_physics(y,'r',-1,10,speed_mps=10)['status'],'UNKNOWN')
 def test_geometry_seam_right_continuity(self):
  x=X.replace('length="20"><arc curvature="0.01"/>','length="10"><arc curvature="0.01"/>')
  # Exact seam endpoint belongs to the new segment, as in standard lane material knots.
  x=x.replace('<planView><geometry s="0" x="0" y="0" hdg="0" length="10"><arc curvature="0.01"/></geometry></planView>',
       '<planView><geometry s="0" x="0" y="0" hdg="0" length="10"><line/></geometry><geometry s="10" x="10" y="0" hdg="0" length="10"><arc curvature="0.01"/></geometry></planView>')
  self.assertAlmostEqual(sample_road_physics(x,'r',-1,10,speed_mps=10)['signed_curvature_inv_m'],.01)
  self.assertAlmostEqual(sample_road_physics(x,'r',-1,9.99,speed_mps=10)['signed_curvature_inv_m'],0)
 def test_bad_lane(self):
  with self.assertRaises(ValueError):sample_road_physics(X,'r',-2,10,speed_mps=10)
 def test_not_field_validated(self):self.assertFalse(sample_road_physics(X,'r',-1,10,speed_mps=10)['field_validated'])
if __name__=='__main__':unittest.main()
