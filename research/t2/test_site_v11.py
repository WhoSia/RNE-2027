import unittest,json,tempfile
from pathlib import Path
from site_v11 import read_site

FIXTURE=Path(__file__).parent/"fixtures"/"synthetic_dual_site_v11.json"

class SiteV11Tests(unittest.TestCase):
    def fixture(self):
        return json.loads(FIXTURE.read_text())
    def load(self,d):
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)/"site.json"
            p.write_text(json.dumps(d))
            return read_site(p)
    def test_synthetic_not_calibrated(self):
        y=self.load(self.fixture())
        self.assertEqual(y["calibration_status"],"NOT_CALIBRATED")
        self.assertEqual(y["input_status"],"SYNTHETIC")
    def test_observed_requires_source_note(self):
        d=self.fixture()
        d["parameters"]["pocket_length_m"]["source_type"]="map_estimate"
        d["parameters"]["pocket_length_m"]["source_note"]=""
        with self.assertRaises(ValueError):self.load(d)
    def test_source_does_not_establish_calibration(self):
        d=self.fixture()
        d["parameters"]["pocket_length_m"]["source_type"]="field_observed"
        d["parameters"]["pocket_length_m"]["source_note"]="asserted but unverified"
        self.assertEqual(self.load(d)["calibration_status"],"NOT_CALIBRATED")
    def test_missing_geometry_rejected(self):
        d=self.fixture()
        d["parameters"].pop("approach_length_m")
        with self.assertRaises(ValueError):self.load(d)
    def test_pocket_must_fit_approach(self):
        d=self.fixture()
        d["parameters"]["pocket_length_m"]["value"]=140
        with self.assertRaises(ValueError):self.load(d)
    def test_lane_split_range(self):
        d=self.fixture()
        d["parameters"]["through_B_share"]["value"]=1.5
        with self.assertRaises(ValueError):self.load(d)

if __name__=="__main__":
    unittest.main(verbosity=2)
