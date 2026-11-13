import csv
from datetime import datetime, timezone, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from dlr_documented_signal_baseline import (
  utc, source_table3, source_table4, read_signals, signal_bracket,
  signal_block_summary, candidate_brackets, STATE_SEMANTICS,
  VEHICULAR_APPROACH_HEADS)

ROOT=Path(__file__).parent
class SourceSemanticsTests(unittest.TestCase):
    def test_all_ten_source_states(self):
        with open(ROOT/'documented_signal_states.csv',encoding='utf8') as f: rows=list(csv.DictReader(f))
        self.assertEqual({int(x['state_code']) for x in rows},set(range(10)))
        self.assertEqual(rows[3]['short_code'],'red')
        self.assertEqual(rows[4]['short_code'],'red_yellow')
        self.assertEqual(rows[5]['short_code'],'green')
    def test_source_coordinate_duplicate_physical_heads(self):
        with open(ROOT/'documented_signal_positions.csv',encoding='utf8') as f: rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),35)
        self.assertEqual(len({int(x['head_id']) for x in rows}),26)
        self.assertEqual(set(range(1,31))-{int(x['head_id']) for x in rows},{10,11,12,13})
        self.assertEqual(sum(int(x['head_id'])==3 for x in rows),3)
    def test_vehicular_approach_heads_are_disjoint(self):
        h=[i for ids in VEHICULAR_APPROACH_HEADS.values() for i in ids]
        self.assertEqual(sorted(h),list(range(1,10)))
    def test_source_table3_rejects_missing(self):
        with self.assertRaises(ValueError):source_table3('nothing')
    def test_source_table4_rejects_incomplete(self):
        with self.assertRaises(ValueError):source_table4('Table 4: Traffic light states\n3 red\n4.3.')
    def test_utc_requires_offset(self):
        with self.assertRaises(ValueError):utc('2023-09-24T23:30:00')
        self.assertEqual(utc('2023-09-24T23:30:00Z').tzinfo,timezone.utc)
    def test_bracket_stable_and_transition(self):
        a=utc('2023-09-24T23:30:00Z');seq=[(a,3),(a+timedelta(seconds=1),3),(a+timedelta(seconds=2),5)]
        self.assertEqual(signal_bracket(seq,a+timedelta(seconds=.4))['status'],'bracket_stable')
        self.assertEqual(signal_bracket(seq,a+timedelta(seconds=1.4))['status'],'transition_within_bracket')
    def test_bracket_rejects_unobserved_extrapolation(self):
        a=utc('2023-09-24T23:30:00Z');seq=[(a,3),(a+timedelta(seconds=1),3)]
        self.assertEqual(signal_bracket(seq,a+timedelta(seconds=20))['status'],'censored_or_gap')
    def test_signal_csv_requires_full_30_heads_per_instant(self):
        with TemporaryDirectory() as d:
            f=Path(d)/'s.csv';f.write_text('timestamp,id,state\n2023-09-24T23:30:00Z,1,5\n')
            with self.assertRaises(ValueError):read_signals(f)
    def test_signal_csv_rejects_undocumented_state(self):
        with TemporaryDirectory() as d:
            f=Path(d)/'s.csv';f.write_text('timestamp,id,state\n2023-09-24T23:30:00Z,1,10\n')
            with self.assertRaises(ValueError):read_signals(f)
    def test_synthetic_vehicle_head_join_remains_unknown(self):
        a=utc('2023-09-24T23:30:00Z')
        series={i:[(a,3),(a+timedelta(seconds=1),3)] for i in range(1,31)}
        events=[{'road_id':'100000','object_id':'x','center_utc':(a+timedelta(seconds=.1)).isoformat(),
                 'front_utc':(a+timedelta(seconds=.05)).isoformat()}]
        r=candidate_brackets(series,events)
        self.assertEqual(len(r),4)
        self.assertTrue(all(row['movement_mapping']=='UNKNOWN' for row in r))
        self.assertTrue(all(row['legal_signal_compliance']=='NOT_EVALUATED' for row in r))
    def test_derived_run_summary(self):
        a=utc('2023-09-24T23:30:00Z')
        series={i:[(a,3),(a+timedelta(seconds=1),5)] for i in range(1,31)}
        r=signal_block_summary(series,'test')
        self.assertEqual(len(r),9)
        self.assertTrue(all(abs(row['sampled_green_fraction']-.5)<1e-8 for row in r))

if __name__ == '__main__':unittest.main()
