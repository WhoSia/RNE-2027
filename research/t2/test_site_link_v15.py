import json,tempfile,unittest
from pathlib import Path
from site_link_v15 import read_link_site

FIXTURE=Path(__file__).parent/"fixtures"/"synthetic_two_signals_v15.json"
class SiteLinkTests(unittest.TestCase):
    def load(self,doc):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"site.json"
            p.write_text(json.dumps(doc))
            return read_link_site(p)
    def test_valid_synthetic_link_is_not_calibrated(self):
        y=read_link_site(FIXTURE)
        self.assertEqual(y["downstream_mode"],"CELLULAR_LINK_UNCALIBRATED")
        self.assertEqual(y["calibration_status"],"NOT_CALIBRATED")
        self.assertEqual(y["config"].receiver_slots,4)
    def test_invalid_green_rejected(self):
        x=json.loads(FIXTURE.read_text())
        x["spatial_downstream"]["downstream_green_s"]["value"]=90
        with self.assertRaises(ValueError):self.load(x)
    def test_external_source_requires_note_and_stays_unverified(self):
        x=json.loads(FIXTURE.read_text())
        x["spatial_downstream"]["receiver_slots"]["source_type"]="field_observed"
        with self.assertRaises(ValueError):self.load(x)
        x["spatial_downstream"]["receiver_slots"]["source_note"]="asserted map measurement"
        y=self.load(x)
        self.assertEqual(y["calibration_status"],"NOT_CALIBRATED")
        self.assertEqual(y["input_status"],"SOURCE_ASSERTED_NOT_VALIDATED")

if __name__=="__main__":unittest.main(verbosity=2)
