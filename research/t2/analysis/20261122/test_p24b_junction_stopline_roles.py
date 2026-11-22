import os,unittest
from pathlib import Path
from p24b_junction_stopline_roles import structural_roles
M=Path(os.getenv("P24_MAP","/mnt/data/bs-inner-ring-road-ut.xodr.xml"))
D=Path(os.getenv("P24_PDF","/mnt/data/DLR-Urban-Traffic-dataset_v1-3-1_documentation.pdf"))
class P24bTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.result=structural_roles(M,D)
 def test_exact_role_counts(self):
  self.assertEqual(self.result["roles"],{"INBOUND_ROAD_APPROACH_END":4,
   "OUTBOUND_ROAD_JUNCTION_START":1,"WITHIN_JUNCTION_CONNECTOR":2,"UNDETERMINED":0})
 def test_candidate_roads(self):
  self.assertEqual(self.result["inbound_candidate_road_ids"],["100000","179000","201000","280000"])
 def test_outbound_marker_road(self):
  x=[r for r in self.result["features"] if r["role"]=="OUTBOUND_ROAD_JUNCTION_START"]
  self.assertEqual([(a["road_id"],a["marker_id"]) for a in x],[("101000","300607")])
 def test_connector_markers(self):
  x=[r for r in self.result["features"] if r["role"]=="WITHIN_JUNCTION_CONNECTOR"]
  self.assertEqual({a["road_id"] for a in x},{"300013","300018"})
 def test_duplicate_id_not_unique_place(self):
  pairs=[(r["road_id"],r["marker_id"]) for r in self.result["features"]]
  self.assertEqual(len(set(pairs)),7)
  self.assertEqual(len(set(r["marker_id"] for r in self.result["features"])),6)
 def test_explicit_lane_ranges_do_not_prove_controller(self):
  self.assertTrue(self.result["gates"]["stopline_lane_validity_explicit"])
  self.assertFalse(self.result["gates"]["lane_ranges_current_2023_and_counting_validated"])
  self.assertTrue(all(x["explicit_lane_validity_count"]==1 for x in self.result["features"]))
  self.assertEqual(next(x["declared_lane_ranges"] for x in self.result["features"] if x["road_id"]=="100000"),[{"fromLane":-1,"toLane":-5}])
  self.assertFalse(self.result["gates"]["observed_light_id_crosswalk"])
  self.assertTrue(all(r["controller_id"] is None and not r["right_of_way_verified"] for r in self.result["features"]))
 def test_pdf_wrong_bytes(self):
  with self.assertRaises(ValueError):structural_roles(M,M)
if __name__=="__main__":unittest.main()
