import copy
import csv
import tempfile
import unittest
from pathlib import Path
from rf_pilot_evaluator import LABELS, MODELS, REQUIRED, validate, read_trials, evaluate, fit_predict


def fixture():
    rows=[]
    for place in ('P1','P2'):
        for session in ('S1','S2','S3'):
            for label_id,label in enumerate(LABELS):
                for i in range(10):
                    rows.append(dict(trial_id=f'{place}-{session}-{label}-{i}',
                        session_id=session,placement_id=place,
                        trial_origin='synthetic_test_fixture',label=label,
                        quality='ok',ground_truth_source='synthetic_test_fixture',
                        rssi_1_dbm=str(-50+.01*i),rssi_2_dbm=str(-50+.02*i),
                        csi_1_amp_dispersion=str(label_id*2+.01*i),
                        csi_2_amp_dispersion=str(label_id*3+.01*i)))
    return rows

class EvaluatorContracts(unittest.TestCase):
    def test_heldout_split_and_no_class_leakage_into_features(self):
        data=fixture(); result=evaluate(data)
        self.assertEqual(result['train_n'],100)
        self.assertEqual(result['test_n'],50)
        self.assertEqual(result['unused_n'],150)
        self.assertEqual(result['pilot_gate'],'NOT_APPLICABLE_SYNTHETIC_FIXTURE')
        self.assertEqual(result['models']['csi_both']['macro_f1'],1.)
        self.assertEqual(result['status'],'SYNTHETIC_PIPELINE_TEST_NOT_RF_EVIDENCE')
        self.assertLess(result['models']['rssi_both']['macro_f1'],result['models']['csi_both']['macro_f1'])
        self.assertTrue(all(not set(features)&{'label','session_id','placement_id'}
                            for features in MODELS.values()))
    def test_missing_measurement_stays_in_denominator_as_abstention(self):
        data=fixture()
        for row in data:
            if row['placement_id']=='P2' and row['session_id']=='S3' and row['label']=='both':
                row['quality']='missing';row['csi_1_amp_dispersion']=''
        r=evaluate(data)
        self.assertEqual(r['models']['csi_both']['abstain_rate'],.2)
        self.assertEqual(r['models']['csi_both']['per_class']['both']['recall'],0.)
        self.assertEqual(r['pilot_gate'],'NOT_APPLICABLE_SYNTHETIC_FIXTURE')
        self.assertEqual(r['test_n'],50)
    def test_validation_rejects_duplicate_mixed_origin_and_nan(self):
        data=fixture()
        with self.assertRaisesRegex(ValueError,'duplicate'):
            validate(data+[dict(data[0])])
        a=copy.deepcopy(data);a[0]['trial_origin']='measured_authorized_lab';a[0]['ground_truth_source']='manual_model_state'
        with self.assertRaisesRegex(ValueError,'mixed'):
            validate(a)
        a=copy.deepcopy(data);a[0]['rssi_1_dbm']='NaN'
        with self.assertRaisesRegex(ValueError,'nonfinite'):
            validate(a)
    def test_unrepresented_class_causes_split_error(self):
        data=[r for r in fixture() if not (r['placement_id']=='P1' and r['label']=='pocket')]
        with self.assertRaisesRegex(ValueError,'lacks'):
            evaluate(data)
    def test_real_origin_does_not_magically_verify_real_sensor(self):
        data=fixture()
        for row in data:
            row['trial_origin']='measured_authorized_lab'
            row['ground_truth_source']='manual_model_state'
        r=evaluate(data)
        self.assertEqual(r['status'],'LAB_TRIAL_ANALYSIS_REQUIRES_SOURCE_AUDIT')
    def test_csv_loading_and_header_checks(self):
        data=fixture()
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'trials.csv'
            with p.open('w',encoding='utf-8',newline='') as f:
                writer=csv.DictWriter(f,fieldnames=REQUIRED);writer.writeheader();writer.writerows(data)
            self.assertEqual(len(read_trials(p)),300)
            with p.open('w',encoding='utf-8',newline='') as f:f.write('bad,headers\n1,2\n')
            with self.assertRaisesRegex(ValueError,'required columns'):
                read_trials(p)
    def test_fit_all_missing_is_abstaining_not_silent_drop(self):
        data=fixture()
        train=[r for r in data if r['placement_id']=='P1' and r['session_id']=='S1']
        test=[r for r in data if r['placement_id']=='P2' and r['session_id']=='S3']
        for row in train:row['csi_1_amp_dispersion']=''
        preds,meta=fit_predict(train,test,MODELS['csi_both'])
        self.assertEqual(set(preds),{'abstain'})
        self.assertFalse(meta['fit_possible'])

if __name__=='__main__':unittest.main()
