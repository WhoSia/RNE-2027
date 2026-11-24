import unittest
from rf16_blind_predict import predict_blind
from rf14_blind_contract import score_sealed
from rf_pilot_evaluator import LABELS


def fixture():
    plan, train, test, truth = [], [], [], []
    from rf11_blind_trial_schedule import schedule
    for r in schedule(seed=16001):
        label=r['label']
        i=LABELS.index(label)
        base={k:r[k] for k in ('trial_id','session_id','placement_id')}
        plan.append(dict(base,reset_index=r['reset_index'],partition=r['partition']))
        row = dict(base,trial_origin='synthetic_test_fixture',quality='ok',
                   rssi_1_dbm=str(-90+10*i),rssi_2_dbm=str(-85+10*i),
                   csi_1_amp_dispersion=str(i),csi_2_amp_dispersion=str(i))
        if r['partition']=='train':
            train.append(dict(row,label=label,ground_truth_source='fixture'))
        elif r['partition']!='sealed_unused_reserve':
            test.append(row)
            truth.append(dict(trial_id=row['trial_id'],label=label))
    return plan,train,test,truth


class BlindPredictTests(unittest.TestCase):
    def setUp(self):
        self.plan,self.train,self.test,self.truth = fixture()

    def test_full_plan_and_later_truth(self):
        result=predict_blind(self.plan,self.train,self.test)
        self.assertEqual((result['train_n'],result['test_n']),(100,150))
        m=result['models']['csi_both']
        self.assertEqual(score_sealed(self.plan,m['payload'],m['sha256'],self.truth)['correct'],150)

    def test_reject_truth_or_extra_field(self):
        for extra in ({'label':'free'}, {'ground_truth_source':'fixture'}, {'secret_truth':'free'}):
            rows=[dict(self.test[0],**extra)]+self.test[1:]
            with self.assertRaises(ValueError):predict_blind(self.plan,self.train,rows)

    def test_plan_truth_rejected(self):
        plan=[dict(self.plan[0],label='free')]+self.plan[1:]
        with self.assertRaises(ValueError):predict_blind(plan,self.train,self.test)

    def test_missing_duplicate_or_reserve(self):
        reserve=dict(self.test[0],**{k:v for k,v in next(r for r in self.plan if (r['session_id'],r['placement_id'])==('S1','P2')).items() if k in ('trial_id','session_id','placement_id')})
        for rows in (self.test[:-1],self.test+[self.test[0]],self.test+[reserve]):
            with self.assertRaises(ValueError):predict_blind(self.plan,self.train,rows)

    def test_abstain_preserved(self):
        self.test[0]['quality']='missing'
        m=predict_blind(self.plan,self.train,self.test)['models']['csi_both']
        report=score_sealed(self.plan,m['payload'],m['sha256'],self.truth)
        self.assertEqual((report['n'],report['correct'],report['abstain']),(150,149,1))

    def test_invalid_cell_and_telemetry(self):
        for extra in ({'session_id':'S1'}, {'csi_1_amp_dispersion':'nan'}, {'quality':'unknown'}):
            rows=[dict(self.test[0],**extra)]+self.test[1:]
            with self.assertRaises(ValueError):predict_blind(self.plan,self.train,rows)

    def test_reserve_plan_independence(self):
        reduced=[r for r in self.plan if (r['session_id'],r['placement_id'])!=('S1','P2')]
        self.assertEqual(predict_blind(self.plan,self.train,self.test),predict_blind(reduced,self.train,self.test))

if __name__=='__main__':unittest.main()
