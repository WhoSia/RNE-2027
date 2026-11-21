import unittest
from pathlib import Path
from p20_dlr_observed_window_gate import run, describe, read

TRAJ=Path('/mnt/data/trajectories_230924-233000_230924-234500.csv')
SIGNALS=Path('/mnt/data/traffic-lights_230924-233000_230924-234500.csv')

class DLRWindowTests(unittest.TestCase):
    def test_actual_sha_sealed_15min_window(self):
        if not TRAJ.exists() or not SIGNALS.exists():
            self.skipTest('Two exact original DLR-UT Drive files are required')
        r=run(TRAJ,SIGNALS)
        self.assertEqual(r['datasets']['trajectories']['rows'],8624)
        self.assertEqual(r['datasets']['traffic_lights']['rows'],26970)
        self.assertEqual(r['datasets']['trajectories']['unique_ids'],37)
        self.assertEqual(r['datasets']['traffic_lights']['unique_ids'],30)
        self.assertEqual(r['datasets']['traffic_lights']['total_within_id_state_code_transitions'],869)
    def test_sha_mismatch_fail_closed(self):
        if not TRAJ.exists():self.skipTest('missing original')
        with self.assertRaises(ValueError):read(TRAJ,'0'*64)
    def test_mixed_fractional_timestamps(self):
        t=[{'id':'1','timestamp':'2023-09-24 23:30:00+00:00',
            'classifications_car':'1','velocity_magnitude':'7'},
           {'id':'1','timestamp':'2023-09-24 23:30:00.050000+00:00',
            'classifications_car':'1','velocity_magnitude':'3'}]
        s=[{'id':'1','timestamp':'2023-09-24 23:30:00.992+00:00','state':'3'},
           {'id':'1','timestamp':'2023-09-24 23:30:01+00:00','state':'5'}]
        o=describe(t,s)
        self.assertEqual(o['datasets']['trajectories']['within_id_sample_interval_median_s'],.05)
        self.assertEqual(o['datasets']['traffic_lights']['total_within_id_state_code_transitions'],1)
    def test_no_empty_observation(self):
        with self.assertRaises(ValueError):describe([],[])
    def test_missing_id_rejected(self):
        with self.assertRaises(ValueError):describe([{'id':'','timestamp':'2023-09-24 00:00:00+00:00'}],
           [{'id':'1','timestamp':'2023-09-24 00:00:00+00:00'}])

if __name__=='__main__':unittest.main()
