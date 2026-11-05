import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from grade_geometry import WayGeometry,audit_crossing,TurnPocket
A=((0.,0.),(10.,10.));B=((0.,10.),(10.,0.))
class GradeTests(unittest.TestCase):
 def test_unresolved_crossing(self):self.assertEqual(audit_crossing(WayGeometry('a',A),WayGeometry('b',B))['status'],'UNKNOWN_3D_RELATION')
 def test_bridge_separation(self):self.assertEqual(audit_crossing(WayGeometry('a',A,1),WayGeometry('b',B,0))['status'],'GRADE_SEPARATED_DECLARED')
 def test_tunnel_separation(self):self.assertEqual(audit_crossing(WayGeometry('a',A,-1),WayGeometry('b',B,0))['status'],'GRADE_SEPARATED_DECLARED')
 def test_same_level_not_automatically_junction(self):self.assertEqual(audit_crossing(WayGeometry('a',A,0),WayGeometry('b',B,0))['status'],'SAME_LEVEL_CONFLICT_POSSIBLE')
 def test_parallel(self):self.assertEqual(audit_crossing(WayGeometry('a',A,0),WayGeometry('b',((0,12),(10,22)),0))['status'],'NO_STRICT_PLANAR_CROSSING')
 def test_pocket_capacity_bound(self):self.assertEqual(TurnPocket('main','left',19.5,frozenset({'left'}),'survey').capacity_upper_bound(6.5),3)
 def test_missing_pocket_evidence(self):
  with self.assertRaises(ValueError):TurnPocket('main','left',30,frozenset({'left'}),'')
 def test_pocket_invalid_turn(self):
  with self.assertRaises(ValueError):TurnPocket('main','left',30,frozenset({'helicopter'}),'sign')
 def test_pocket_not_real_flow(self):self.assertEqual(TurnPocket('main','left',10,frozenset({'left'}),'sign').capacity_upper_bound(6.5),1)
 def test_collinear_caution(self):self.assertEqual(audit_crossing(WayGeometry('a',A,0),WayGeometry('b',((2,2),(8,8)),0))['status'],'NO_STRICT_PLANAR_CROSSING')
if __name__=='__main__':unittest.main()
