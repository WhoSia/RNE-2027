"""RF11 schedule invariants; zero physical trials performed."""
import csv
import tempfile
import unittest
from pathlib import Path
from collections import Counter
from rf11_blind_trial_schedule import schedule,export,manifest_receipt


class TestSchedule(unittest.TestCase):
    def test_full_design_is_balanced_and_partitioned(self):
        rows=schedule()
        self.assertEqual(len(rows),300)
        c=Counter((r['session_id'],r['placement_id'],r['label']) for r in rows)
        self.assertEqual(set(c.values()),{10})
        self.assertEqual(Counter(r['partition'] for r in rows),{
            'train':100,'primary_blind_holdout':50,
            'secondary_holdout':100,'sealed_unused_reserve':50})
        self.assertTrue(all(r['trial_origin']=='planned_not_measured' for r in rows))

    def test_blind_analyst_never_receives_true_class(self):
        rows=schedule()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'blind.csv';export(rows,p,operator=False)
            with p.open(newline='') as f:
                rd=csv.DictReader(f)
                self.assertNotIn('label',rd.fieldnames)
                self.assertNotIn('ground_truth_source',rd.fieldnames)
                self.assertNotIn('trial_origin',rd.fieldnames)
                self.assertEqual(len(list(rd)),300)

    def test_replay_seed_and_bounds(self):
        self.assertEqual(manifest_receipt(schedule())['schedule_sha256'],
                         manifest_receipt(schedule())['schedule_sha256'])
        self.assertNotEqual(manifest_receipt(schedule(seed=1))['schedule_sha256'],
                            manifest_receipt(schedule(seed=2))['schedule_sha256'])
        with self.assertRaises(ValueError):schedule(reset_per_class=9)
        with self.assertRaises(ValueError):schedule(seed=-1)

if __name__=='__main__':unittest.main()
