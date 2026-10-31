"""Backward-compatible provenance for optional shared downstream models."""
import unittest,json,tempfile
from pathlib import Path
from site_v11 import read_site

FIXTURE=Path(__file__).parent/"fixtures"/"synthetic_dual_site_v11.json"

class DownstreamSiteTests(unittest.TestCase):
    def read_case(self,obj):
        with tempfile.TemporaryDirectory() as root:
            f=Path(root)/"site.json";f.write_text(json.dumps(obj))
            return read_site(f)
    def fixture(self):
        return json.loads(FIXTURE.read_text())
    def test_v11_fixture_still_works_with_defaults(self):
        r=self.read_case(self.fixture())
        self.assertEqual(r["downstream_mode"],"INDEPENDENT")
        self.assertEqual(r["config"].receiver_slots,0)
    def test_finite_receiver_is_not_field_calibrated(self):
        x=self.fixture()
        x["parameters"]["receiver_slots"]={"value":2,"source_type":"synthetic"}
        x["parameters"]["receiver_headway_s"]={"value":4,"source_type":"synthetic"}
        r=self.read_case(x)
        self.assertEqual(r["downstream_mode"],"FINITE_RECEIVER")
        self.assertEqual(r["calibration_status"],"NOT_CALIBRATED")
    def test_unverified_field_value_requires_source(self):
        x=self.fixture()
        x["parameters"]["receiver_slots"]={"value":2,"source_type":"field_observed"}
        with self.assertRaises(ValueError):self.read_case(x)
    def test_zero_headway_rejected(self):
        x=self.fixture()
        x["parameters"]["receiver_headway_s"]={"value":0,"source_type":"synthetic"}
        with self.assertRaises(ValueError):self.read_case(x)

if __name__=="__main__":
    unittest.main(verbosity=2)
