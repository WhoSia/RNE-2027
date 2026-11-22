"""P35 hard-fail source, interval, and exact P34-matcher timing tests."""
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from p35_observation_timing import (
    analyse, crossing_brackets, load_p34, read_signals, verify_bytes,
    P34_ARCHIVE_SHA, P34_EVENT_SHA, SIGNAL_SHA, VOLUME_SHA,
    GAP_START, GAP_END,
)

BASE = Path(__file__).resolve().parent
DATA = Path(os.environ.get('P35_SOURCE_DIR', '/mnt/data'))
ARCHIVE = Path(os.environ.get('P35_P34_ZIP', str(DATA / 'P34_OBS_20261122_REAL_DLR_STOPLINE_REPRO.zip')))
SIGNALS = DATA / 'traffic-lights_230924-233000_230924-234500.csv'
VOLUME = DATA / 'traffic-volume_230924-233000_230924-234500.csv'

class ObservationTimingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = analyse(ARCHIVE, SIGNALS, VOLUME)
        cls.p34 = load_p34(ARCHIVE)

    def test_locked_three_input_sources(self):
        for path, sha in [(ARCHIVE,P34_ARCHIVE_SHA),(SIGNALS,SIGNAL_SHA),(VOLUME,VOLUME_SHA)]:
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),sha)
        self.assertEqual(self.p34['sources_sha256']['traffic_volume'],VOLUME_SHA)

    def test_original_p34_counts_preserved(self):
        self.assertEqual(len(self.p34['crossings']),17)
        self.assertEqual(len(self.p34['matched_pairs']),16)
        self.assertEqual(self.results['crossings'],17)
        self.assertEqual(self.results['signal_ids'],30)
        self.assertEqual(self.results['signal_rows'],26970)

    def test_temporal_matching_tolerance_sensitive(self):
        v=self.results['matched_tolerance_sensitivity']
        self.assertEqual([x['matched'] for x in v],[4,7,10,16,16])
        self.assertEqual([x['matching_tolerance_s'] for x in v],[0.25,0.5,0.75,1.0,1.5])

    def test_causal_vs_nearest_hindsight(self):
        r=self.results
        self.assertEqual(r['crossings_with_nearest_hindsight_sample_future'],11)
        self.assertEqual(r['crossings_with_nearest_hindsight_sample_after_bracket'],10)
        self.assertTrue(all(x['causal_last_sample']<=x['bracket_start'] for x in r['event_records']))

    def test_sample_inside_vehicle_bracket_preserved(self):
        r=self.results
        self.assertEqual(r['crossing_brackets_containing_signal_sample'],1)
        self.assertEqual(sum(bool(x['signal_samples_inside_crossing_bracket']) for x in r['event_records']),1)

    def test_signal_state_cannot_be_extrapolated_from_group(self):
        r=self.results
        self.assertEqual(r['crossings_with_any_head_discordant_between_sample_bounds'],5)
        self.assertEqual(r['signal_head_event_pairs_with_discordant_samples'],8)
        self.assertTrue(all(x['status']=='UNMAPPED_SIGNAL_HEAD_TO_MOVEMENT' for x in r['event_records']))
        self.assertTrue(all(x['sampled_state_discordant_head_ids']==sorted(x['sampled_state_discordant_head_ids']) for x in r['event_records']))

    def test_freshness_is_based_on_bracket_end_not_estimate(self):
        self.assertEqual([self.results['freshness_at_bracket_end'][str(k)]['causally_fresh_crossings'] for k in (.25,.5,1.,1.5,2.5)],[3,6,16,17,17])
        self.assertEqual(self.results['age_at_bracket_end_s'],{'min':0.126482,'median':0.678482,'max':1.022482})

    def test_no_crossing_in_2s_common_signal_gap(self):
        self.assertEqual(self.results['crossings_overlapping_common_gap'],0)
        self.assertEqual(self.results['common_signal_gap'][0][2],2.004)
        self.assertEqual(tuple(self.results['common_signal_gap'][0][:2]),(GAP_START.isoformat(),GAP_END.isoformat()))

    def test_tampered_signal_bytes_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            file=Path(d)/'signal.csv'
            raw=SIGNALS.read_bytes()
            file.write_bytes(raw[:-1]+(b'X' if raw[-1:]!=b'X' else b'Y'))
            with self.assertRaisesRegex(ValueError,'SHA-256 mismatch'):
                read_signals(file)

    def test_tampered_zip_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            file=Path(d)/'a.zip'
            raw=ARCHIVE.read_bytes()
            file.write_bytes(raw[:-1]+(b'X' if raw[-1:]!=b'X' else b'Y'))
            with self.assertRaisesRegex(ValueError,'SHA-256 mismatch'):
                load_p34(file)

    def test_tampered_volume_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            file=Path(d)/'v.csv';file.write_bytes(VOLUME.read_bytes()+b' ')
            with self.assertRaisesRegex(ValueError,'SHA-256 mismatch'):
                analyse(ARCHIVE,SIGNALS,file)

    def test_bad_estimate_outside_bracket(self):
        tampered=copy.deepcopy(self.p34['crossings'])
        tampered[0]['crossing_time_utc']='2023-09-24T23:00:00+00:00'
        with self.assertRaises(ValueError):crossing_brackets(tampered)

    def test_fake_head_id_not_mapped(self):
        tampered=copy.deepcopy(self.p34['crossings']);tampered[0]['controlling_signal_id']=1
        with self.assertRaises(ValueError):crossing_brackets(tampered)

    def test_repeated_result_is_byte_deterministic(self):
        repeat=analyse(ARCHIVE,SIGNALS,VOLUME)
        self.assertEqual(repeat,self.results)
        on_disk=json.loads((BASE/'p35_result.json').read_text(encoding='utf-8'))
        self.assertEqual(on_disk,json.loads(json.dumps(self.results)))

    def test_p34_matcher_global_restored(self):
        import sys
        sys.path.insert(0, str(ARCHIVE))
        import p34_dlr_stopline_event_reconciliation as p34lib
        self.assertEqual(p34lib.MAX_MATCH_ERROR_S,1.0)

if __name__=='__main__':unittest.main()
