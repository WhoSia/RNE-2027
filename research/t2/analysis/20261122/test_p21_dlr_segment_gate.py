import os, unittest
from datetime import datetime
from pathlib import Path
from p21_dlr_segment_gate import ts,audit,execute,read_raw
T=Path(os.getenv('P21_TRAJECTORY','/mnt/data/trajectories_230924-233000_230924-234500.csv'))
S=Path(os.getenv('P21_SIGNAL','/mnt/data/traffic-lights_230924-233000_230924-234500.csv'))
C=('pedestrian','bicycle','motorbike','car','van','truck')
def track(id,when,speed=.1,cl='car'):
    return dict(id=id,timestamp=when,velocity_magnitude=str(speed),
        **{'classifications_'+x:str(int(x==cl)) for x in C})
def light(id,when,state):
    return dict(id=id,timestamp=when,state=state)
class P21Test(unittest.TestCase):
    def test_real_sha_locked_sources(self):
        if not T.is_file() or not S.is_file():self.skipTest('Two exact Drive CSVs required')
        x=execute(T,S)
        self.assertEqual((x['tracked_object_ids'],x['signal_ids']),(37,30))
        self.assertEqual(x['signal_code_changes'],869)
        self.assertEqual(x['signal_runs'],899)
        self.assertFalse(any(x['gates'].values()))
    def test_mixed_iso_timestamps(self):
        self.assertEqual(ts('2023-09-24 23:30:00+00:00'),
                         ts('2023-09-24 23:30:00.000000+00:00'))
    def test_naive_time_rejected(self):
        with self.assertRaises(ValueError):ts('2023-09-24 23:30:00')
    def test_censoring_and_change(self):
        t=[track('a','2023-09-24 23:30:00+00:00')]
        s=[light('1','2023-09-24 23:30:00+00:00','3'),
           light('1','2023-09-24 23:30:01+00:00','3'),
           light('1','2023-09-24 23:30:02+00:00','5')]
        x=audit(t,s)
        self.assertEqual(x['signal_code_changes'],1)
        self.assertEqual(x['signal_runs'],2)
        self.assertFalse(x['signal_runs_detail'][0]['right_censored'])
        self.assertTrue(x['signal_runs_detail'][1]['right_censored'])
        self.assertEqual(x['signal_runs_detail'][0]['observed_span_s'],1)
    def test_trajectory_gap_not_bridged(self):
        t=[track('a','2023-09-24 23:30:00+00:00'),
           track('a','2023-09-24 23:30:00.05+00:00'),
           track('a','2023-09-24 23:30:01+00:00')]
        s=[light('1','2023-09-24 23:30:00+00:00','3')]
        x=audit(t,s)
        self.assertEqual(x['low_speed_adjacent_intervals'],1)
        self.assertEqual(x['large_trajectory_gaps'],1)
        self.assertAlmostEqual(x['low_speed_observed_seconds'],.05)
    def test_duplicate_light_time_fails(self):
        t=[track('a','2023-09-24 23:30:00+00:00')]
        s=[light('1','2023-09-24 23:30:00+00:00','3')]*2
        with self.assertRaises(ValueError):audit(t,s)
    def test_missing_original_fails_sha(self):
        if not T.is_file():self.skipTest('source file missing')
        with self.assertRaises(ValueError):read_raw(T,'0'*64)
    def test_no_empirical_signal_phase_claim(self):
        t=[track('a','2023-09-24 23:30:00+00:00')]
        s=[light('1','2023-09-24 23:30:00+00:00','3')]
        self.assertFalse(any(audit(t,s)['gates'].values()))
if __name__=='__main__':unittest.main()
