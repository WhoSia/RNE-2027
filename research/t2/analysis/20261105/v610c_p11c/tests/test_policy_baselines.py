import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from policy_baselines import compare,evaluate,CANDIDATE_POLICIES
class PolicyBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.rows,cls.all=compare('balanced',6.5,6.5,5)
    def test_exact_candidates(self):
        self.assertEqual(CANDIDATE_POLICIES['oracle_all_8'],tuple(range(8)))
    def test_same_scenario_for_policy(self):
        self.assertEqual({t.total for t in self.all},{20})
    def test_all_complete(self):
        self.assertEqual({t.completed for t in self.all},{20})
    def test_oracle_regret_zero(self):
        self.assertEqual(next(x['regret_vs_oracle_veh_s'] for x in self.rows if x['policy_search']=='oracle_all_8'),0)
    def test_regret_never_negative(self):
        self.assertTrue(all(x['regret_vs_oracle_veh_s']>=0 for x in self.rows))
    def test_source_occupancy_limit(self):
        self.assertTrue(all(t.peak_source_m<=6.5+1e-9 for t in self.all))
    def test_determinism(self):
        self.assertEqual(evaluate('balanced',6.5,6.5,5,3),evaluate('balanced',6.5,6.5,5,3))
if __name__=='__main__':unittest.main()
