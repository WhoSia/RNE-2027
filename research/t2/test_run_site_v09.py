import unittest
from pathlib import Path
from run_site_v09 import execute

class SiteRunTests(unittest.TestCase):
    def test_four_paired_interventions(self):
        p=Path(__file__).parent/"fixtures"/"hypothetical_signalized_approach_v09.json"
        x=execute(p)
        self.assertEqual(len(x["paired_interventions"]),4)
        self.assertFalse(x["field_calibrated"])
        self.assertEqual(x["world_contact_status"],"SYNTHETIC_ONLY")
        self.assertEqual([r["bay_length_m"] for r in x["paired_interventions"]],[14,28,42,70])
        self.assertTrue(all(r["through_exits"]<=375 for r in x["paired_interventions"]))
if __name__=="__main__":
    unittest.main(verbosity=2)
