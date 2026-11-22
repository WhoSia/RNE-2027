"""P24 tests: actual publisher originals and explicit fail-closed signal mapping."""
import os, math, unittest, xml.etree.ElementTree as ET
from pathlib import Path
from p24_xodr_static_signal_audit import audit, pose, MAP_SHA, PDF_SHA
M=Path(os.getenv("P24_MAP","/mnt/data/bs-inner-ring-road-ut.xodr.xml"))
P=Path(os.getenv("P24_PDF","/mnt/data/DLR-Urban-Traffic-dataset_v1-3-1_documentation.pdf"))
class TestP24(unittest.TestCase):
 @classmethod
 def setUpClass(cls): cls.result=audit(M,P)
 def test_originals_sha(self):
  self.assertEqual(self.result["map_sha256"],MAP_SHA)
  self.assertEqual(self.result["documentation_sha256"],PDF_SHA)
 def test_xodr_counts(self):
  self.assertEqual((self.result["roads"],self.result["junctions"],len(self.result["static_signals"])),(28,1,7))
  self.assertEqual(len(self.result["unique_static_ids"]),6)
 def test_static_only_not_control_ids(self):
  self.assertTrue(all(x["dynamic"]=="no" for x in self.result["static_signals"]))
  self.assertTrue(all(int(x)>30 for x in self.result["unique_static_ids"]))
 def test_18_official_head_coordinates(self):
  self.assertEqual(self.result["original_motor_vehicle_heads"],18)
  self.assertEqual(set(x["observed_light_id"] for x in self.result["candidates"]),set(range(1,10)))
 def test_nearest_is_not_signal_lane_mapping(self):
  for x in self.result["candidates"]:
   self.assertIsNone(x["controlling_lane"])
   self.assertIsNone(x["movement"])
   self.assertEqual(x["verdict"],"UNVERIFIED_NEAR_NEIGHBOR_ONLY")
   self.assertEqual([a["distance_m"] for a in x["nearest_static_map_features"]],sorted(a["distance_m"] for a in x["nearest_static_map_features"]))
  self.assertFalse(self.result["gates"]["signal_movements_verified"])
 def test_projection_regression(self):
  p=self.result["candidates"][0]["local_xy"]
  self.assertAlmostEqual(p[0],-7.52,places=2)
  self.assertAlmostEqual(p[1],19.102,places=2)
 def test_wrong_map_fails(self):
  with self.assertRaises(ValueError):audit(P,P)
 def test_wrong_doc_fails(self):
  with self.assertRaises(ValueError):audit(M,M)
 def test_analytical_arc_and_line(self):
  road=ET.fromstring('<road length="15"><planView><geometry s="0" x="2" y="3" hdg="0" length="5"><line/></geometry><geometry s="5" x="7" y="3" hdg="0" length="10"><arc curvature="0.1"/></geometry></planView></road>')
  self.assertEqual(pose(road,5)[:2],(7.,3.))
  x,y,h=pose(road,15)
  self.assertAlmostEqual(x,7+math.sin(1)/.1)
  self.assertAlmostEqual(y,3+(1-math.cos(1))/.1)
  self.assertAlmostEqual(h,1.)
  with self.assertRaises(ValueError):pose(road,16)
if __name__=="__main__":unittest.main()
