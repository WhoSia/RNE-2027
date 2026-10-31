import unittest
from separation_court_v11 import court

class IndependentLaneProofTests(unittest.TestCase):
    def test_all_30_seed_ratio_cases_at_five_pocket_lengths(self):
        result=court()
        self.assertEqual(result["status"],"PASS_SYNTHETIC_CONDITIONAL")
        self.assertEqual(result["independent_cases"],30)
        self.assertEqual(len(result["records"]),30)

if __name__=="__main__":
    unittest.main(verbosity=2)
