import csv
import tempfile
import unittest
from pathlib import Path
from rf17_feature_only_bridge import PLAN,WINDOW,WIRE,aggregate_holdout,export_features,read_exact,testing_plan


def fixture():
    plan=[dict(trial_id='T',session_id='S3',placement_id='P2',reset_index='1',partition='primary_blind_holdout')]
    windows=[dict(trial_id='T',session_id='S3',placement_id='P2',trial_origin='synthetic_test_fixture',link_id=lid,start_us='0',stop_us='5') for lid in ('1','2')]
    packets={lid:[dict(timestamp_us=t,rssi=-60,mean_amplitude=a) for t,a in ((1,10),(2,14),(5,999))] for lid in ('1','2')}
    return plan,windows,packets


class RF17Tests(unittest.TestCase):
    def test_features_and_half_open_window(self):
        row=aggregate_holdout(*fixture())[0]
        self.assertEqual(set(row),set(WIRE))
        self.assertEqual((row['quality'],row['rssi_1_dbm'],row['csi_1_amp_dispersion']),('ok',-60,2))
    def test_missing_link_preserves_trial(self):
        p,w,s=fixture();s['2']=[]
        row=aggregate_holdout(p,w,s)[0]
        self.assertEqual((row['quality'],row['rssi_2_dbm']),('missing',''))
    def test_leakage_rejected(self):
        for key in ('label','ground_truth_source','secret_truth'):
            p,w,s=fixture();w[0][key]='free'
            with self.assertRaises(ValueError):aggregate_holdout(p,w,s)
    def test_missing_duplicate_and_partition(self):
        p,w,s=fixture()
        for bad in (w[:1],w+w[:1]):
            with self.assertRaises(ValueError):aggregate_holdout(p,bad,s)
        p[0]['partition']='train'
        with self.assertRaises(ValueError):testing_plan(p)
    def test_clock_and_overlap(self):
        p,w,s=fixture();s['1'].reverse()
        with self.assertRaises(ValueError):aggregate_holdout(p,w,s)
        p,w,s=fixture();p.append(dict(p[0],trial_id='T2'))
        w.extend(dict(r,trial_id='T2') for r in list(w))
        with self.assertRaises(ValueError):aggregate_holdout(p,w,s)
    def test_csv_schema_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/'features.csv';rows=aggregate_holdout(*fixture())
            export_features(rows,f);self.assertEqual(set(read_exact(f,WIRE)[0]),set(WIRE))
            with self.assertRaises(FileExistsError):export_features(rows,f)
            with f.open('w',newline='') as out:
                csv.writer(out).writerow((*WIRE,'label'))
            with self.assertRaises(ValueError):read_exact(f,WIRE)
    def test_plan_truth_and_mixed_origin(self):
        p,w,s=fixture();p[0]['label']='free'
        with self.assertRaises(ValueError):aggregate_holdout(p,w,s)
        p,w,s=fixture();w[1]['trial_origin']='measured_authorized_lab'
        with self.assertRaises(ValueError):aggregate_holdout(p,w,s)

if __name__=='__main__':unittest.main()
