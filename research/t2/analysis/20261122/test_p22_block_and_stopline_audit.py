import os
import unittest
from pathlib import Path
from p22_block_and_stopline_audit import produce, audit_p19, source_volume, SOURCES

BASE=Path(os.environ.get('P22_DLR_DIR','/mnt/data'))
RESULT=Path(os.environ.get('P22_P19_RESULT','/mnt/data/t2_p18_canonical/p19_receiver_service_opportunity_results.json'))

class P22Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if RESULT.is_file() and all((BASE/name).is_file() for name,_ in SOURCES.values()):
            cls.out=produce(RESULT,BASE)
        else:
            cls.out=None

    def test_preregistered_3_real_windows(self):
        if self.out is None:self.skipTest('full original inputs unavailable')
        s=self.out['observed_stopline']
        self.assertEqual([s[k]['recorded_crossing_bins'] for k in SOURCES],[436,192,17])
        self.assertEqual([s[k]['movement_columns'] for k in SOURCES],[32,27,12])
        self.assertEqual([s[k]['seconds_observed'] for k in SOURCES],[900,900,893])

    def test_no_vehicle_headway_claims(self):
        if self.out is None:self.skipTest('full original inputs unavailable')
        for val in self.out['observed_stopline'].values():
            self.assertIn('one-second',val['unit'])
            self.assertNotIn('headway',str(val))

    def test_16_not_128_independent_blocks(self):
        if self.out is None:self.skipTest('full original inputs unavailable')
        x=self.out['p19']
        self.assertEqual((x['worlds'],x['unique_full_tape_hashes'],x['matched_offset_geometry_pairs']),(256,16,128))
        self.assertEqual(x['effects']['15']['positive_cost_delta'],0)
        self.assertEqual(x['effects']['15']['tape_blocks_with_any_positive'],0)
        self.assertTrue(.17 < x['iid_block_based_zero_of_16_one_sided_95pct_upper_probability'] < .171)

    def test_seed_115_removal_flips_aggregate_sign(self):
        if self.out is None:self.skipTest('full original inputs unavailable')
        x=self.out['p19']['effects']['0']
        self.assertEqual(x['sum_model_delta_over_reused_worlds'],5108)
        self.assertEqual(x['leave_one_seed_out_total_by_seed']['115'],-2248)
        self.assertEqual(x['leave_one_seed_out_total_by_seed']['118'],-2230)

    def test_sha_mismatch_fail_closed(self):
        name,_=next(iter(SOURCES.values()))
        if not (BASE/name).exists():self.skipTest('original absent')
        with self.assertRaises(ValueError):source_volume(BASE/name,'0'*64)

    def test_no_fake_block_independence(self):
        with self.assertRaises(ValueError):audit_p19([])

    def test_missing_columns_not_imputed(self):
        if self.out is None:self.skipTest('full original inputs unavailable')
        s=self.out['observed_stopline']
        self.assertNotEqual(set(s['12:00-12:15']['movement_names']),set(s['23:30-23:45']['movement_names']))
        self.assertGreater(len(s['12:00-12:15']['movement_names']),len(s['23:30-23:45']['movement_names']))

if __name__=='__main__':unittest.main()
