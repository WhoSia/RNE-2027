import csv
import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from p34_official_volume_overlap import (
    SOURCE_HASHES, EXPECTED_MOVEMENTS, analyze, confusion,
    hash_guard, parse_utc, read_volume, read_tracks, read_signal_gap,
)

DATA=Path(os.environ.get('P34_SOURCE_DIR','/mnt/data'))
VOL=DATA/'traffic-volume_230924-233000_230924-234500.csv'
TRA=DATA/'trajectories_230924-233000_230924-234500.csv'
SIG=DATA/'traffic-lights_230924-233000_230924-234500.csv'


class P34Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=analyze(VOL, TRA, SIG)

    def test_real_sha_guard(self):
        for name,path in [('volume',VOL),('trajectories',TRA),('signals',SIG)]:
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),SOURCE_HASHES[name])

    def test_exact_published_bin_count(self):
        r=self.report
        self.assertEqual((r['volume_rows_1s'],r['volume_movement_channels']), (893,12))
        self.assertEqual((r['published_positive_unique_1s_bins'],r['published_positive_channel_bins']), (17,17))

    def test_exact_naive_confusion(self):
        r=self.report['naive_presence_classifier']
        self.assertEqual(tuple(r[k] for k in ('tp','fp','fn','tn')),(17,305,0,571))
        self.assertAlmostEqual(r['precision'],17/322)
        self.assertEqual(r['recall'],1)

    def test_multiple_candidate_ids_not_identity_match(self):
        self.assertEqual(self.report['positive_bins_with_more_than_one_candidate'],11)
        self.assertEqual(self.report['candidate_ids_at_official_positive_bins_histogram'],{1:6,2:7,3:1,5:2,6:1})

    def test_time_shifts_not_perfectly_invariant(self):
        r=self.report['shift_diagnostics']
        self.assertEqual([s['shift_seconds'] for s in r],[-2,-1,0,1,2])
        self.assertEqual([s['tp'] for s in r],[17,17,17,16,16])
        self.assertEqual([s['fn'] for s in r],[0,0,0,1,1])

    def test_common_signal_gap_exposure(self):
        r=self.report
        self.assertEqual(r['signal_sample_instants'],899)
        self.assertEqual(r['signal_heads_per_instant'],30)
        self.assertEqual(len(r['global_signal_observation_gaps_over_1_5s']),1)
        g=r['global_signal_observation_gaps_over_1_5s'][0]
        self.assertEqual(g['duration_ms'],2004)
        self.assertEqual(g['changed_endpoint_codes'],{'12':[5,7],'20':[5,3],'21':[5,3]})
        self.assertEqual((g['tracked_samples_strictly_inside'],g['distinct_tracked_ids_strictly_inside']),(40,1))
        self.assertEqual(len(g['official_1s_volume_intervals_intersecting_gap']),3)
        self.assertEqual(g['published_positive_bins_whose_intervals_intersect_gap'],0)

    def test_no_event_cannot_imply_no_objects(self):
        r=self.report['naive_presence_classifier']
        self.assertGreater(r['fp'],0)
        self.assertEqual(r['fp']+r['tn'],893-17)

    def test_hash_guard_fails_closed(self):
        with patch.dict('p34_official_volume_overlap.SOURCE_HASHES',{'volume':'0'*64}):
            with self.assertRaises(ValueError):hash_guard(VOL,'volume')

    def test_time_timezone_required(self):
        with self.assertRaises(ValueError):parse_utc('2023-09-24 23:35:05')
        with self.assertRaises(ValueError):parse_utc('invalid')
        self.assertEqual(parse_utc('2023-09-24 23:35:05+00:00').utcoffset().total_seconds(),0)

    def test_duplicate_bins_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'a.csv'
            with p.open('w',newline='') as f:
                w=csv.writer(f);w.writerow(['timestamp',*EXPECTED_MOVEMENTS])
                for _ in range(2):w.writerow(['2023-09-24 23:30:07+00:00',*([0]*12)])
            with self.assertRaisesRegex(ValueError,'duplicate'):read_volume(p,guard=False)

    def test_invalid_movement_indicator_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'a.csv'
            with p.open('w',newline='') as f:
                w=csv.writer(f);w.writerow(['timestamp',*EXPECTED_MOVEMENTS]);w.writerow(['2023-09-24 23:30:07+00:00',2,*([0]*11)])
            with self.assertRaisesRegex(ValueError,'indicator'):read_volume(p,guard=False)

    def test_duplicate_signal_head_time_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'s.csv'
            p.write_text('timestamp,id,state\n2023-09-24 23:30:07+00:00,1,3\n2023-09-24 23:30:07+00:00,1,5\n')
            with self.assertRaisesRegex(ValueError,'duplicate'):read_signal_gap(p,guard=False)

    def test_zero_predictions_not_division_by_zero(self):
        from datetime import datetime,timezone
        t=datetime(2023,9,24,23,30,7,tzinfo=timezone.utc)
        empty=confusion({t:(0,)*12},{})
        self.assertIsNone(empty['precision'])
        self.assertIsNone(empty['recall'])
        self.assertEqual(empty['tn'],1)

    def test_deterministic_full_report(self):
        self.assertEqual(self.report,analyze(VOL,TRA,SIG))

if __name__=='__main__':unittest.main()
