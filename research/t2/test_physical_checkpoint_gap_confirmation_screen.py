"""PHYS-11 prospective result regression: known cohort, sign and accounting."""
import unittest
from physical_checkpoint_gap_confirmation_screen import (
    SEEDS, CONFIRMATIONS, POCKETS, B_SHARES, PLAN, experiment)


class GapConfirmationScreenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out=experiment()

    def test_locked_grid_and_all_expected_keys(self):
        self.assertEqual(SEEDS,tuple(range(80,88)))
        self.assertEqual(CONFIRMATIONS,(1,2,3))
        self.assertEqual(POCKETS,(14.,28.,70.))
        self.assertEqual(B_SHARES,(0.,.5))
        self.assertEqual(PLAN,((84,87,'-'),(87,91,'L'),(91,120,'-')))
        rows=self.out['pairs']
        self.assertEqual(len(rows),144)
        self.assertEqual(len({(r['confirmation_s'],r['seed'],r['pocket_m'],r['b_share'])
                             for r in rows}),144)
        self.assertTrue(all(r['matched_predecision'] for r in rows))

    def test_expected_admitted_changes_and_confirmation_waits(self):
        expected={1:(704,0),2:(593,1705),3:(578,2795)}
        for confirm,(changes,waits) in expected.items():
            with self.subTest(confirm=confirm):
                r=self.out['summary'][str(confirm)]
                self.assertEqual(r['baseline_changes'],changes)
                self.assertEqual(r['baseline_confirmation_wait_s'],waits)

    def test_null_strict_sign_reversals_reported(self):
        self.assertEqual(self.out['strict_sign_reversals'],[])
        self.assertEqual([(self.out['summary'][str(i)]['treat_better'],
                           self.out['summary'][str(i)]['baseline_better'],
                           self.out['summary'][str(i)]['ties']) for i in (1,2,3)],
                         [(15,0,33),(14,0,34),(21,0,27)])

    def test_costs_and_pair_accounting(self):
        for r in self.out['pairs']:
            self.assertEqual(r['delta'],r['treated_cost']-r['baseline_cost'])
            self.assertGreaterEqual(r['baseline_confirmation_wait_s'],0)
            self.assertGreaterEqual(r['treated_confirmation_wait_s'],0)
            self.assertTrue(r['baseline_remaining']>=0 and r['treated_remaining']>=0)


if __name__=='__main__':
    unittest.main()
