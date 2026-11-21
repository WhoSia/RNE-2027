"""Unit-contract checks for strict reference comparator; no simulator invocation."""
import unittest
from compare_physical_checkpoint_reference import compare


def fixtures():
    ref=[]
    canonical=[]
    for cap in (2,4,8):
        rows=[]
        for seed in range(8):
            for pocket in (14.,28.,70.):
                for share in (0.,.5):
                    x=dict(seed=seed,pocket_m=pocket,b_share=share,
                           baseline_cost=100,treatment_cost=101,delta=1,
                           delta_p0=1,delta_p120=1,baseline_remaining=0,
                           treatment_remaining=0,baseline_out_S=1,
                           baseline_out_L=1,treatment_out_S=1,treatment_out_L=1,
                           baseline_lane_changes=0,treatment_lane_changes=0)
                    rows.append(x)
                    canonical.append(dict(capacity=cap,seed=seed,
                           pocket_m=pocket,b_share=share,
                           cost_baseline_p60=100,cost_treatment_p60=101,
                           delta_p60=1,delta_p0=1,delta_p120=1,
                           baseline_remaining=0,treatment_remaining=0,
                           baseline_out_S=1,baseline_out_L=1,
                           treatment_out_S=1,treatment_out_L=1,
                           baseline_bypass=0,treatment_bypass=0))
        ref.append(dict(capacity=cap,
             provenance='INDEPENDENT_REIMPLEMENTATION_NOT_CANONICAL_GITHUB_ENGINE',
             rows=rows))
    return {'pairs':canonical},ref


class ComparatorTests(unittest.TestCase):
    def test_matching_fixture(self):
        a,b=fixtures()
        self.assertEqual(compare(a,b),[])

    def test_mutated_cost_fails_comparison(self):
        a,b=fixtures()
        a['pairs'][0]['cost_baseline_p60']=111
        self.assertEqual(len(compare(a,b)),1)

    def test_missing_pair_fails_closed(self):
        a,b=fixtures()
        a['pairs'].pop()
        with self.assertRaisesRegex(AssertionError,'pair key set'):
            compare(a,b)

    def test_bad_reference_provenance_fails_closed(self):
        a,b=fixtures()
        b[0]['provenance']='CANONICAL_UNVERIFIED'
        with self.assertRaisesRegex(AssertionError,'provenance'):
            compare(a,b)


if __name__=='__main__':
    unittest.main()
