import unittest
from pathlib import Path
from run_site_v11 import execute

class SiteExecutionTests(unittest.TestCase):
    def test_provenance_preserved_for_all_interventions(self):
        path=Path(__file__).parent/"fixtures"/"synthetic_dual_site_v11.json"
        out=execute(path)
        self.assertEqual(out["input_status"],"SYNTHETIC")
        self.assertEqual(out["calibration_status"],"NOT_CALIBRATED")
        self.assertEqual([x["pocket_m"] for x in out["interventions"]],[14.,28.,42.,70.])
        self.assertTrue(all(x["through_exits"]>=0 for x in out["interventions"]))

if __name__=="__main__":
    unittest.main(verbosity=2)
