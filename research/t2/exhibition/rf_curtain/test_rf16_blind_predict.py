import unittest
from rf16_blind_predict import predict_blind
from rf14_blind_contract import score_sealed
from rf_pilot_evaluator import LABELS


def fixture():
    plan, train, test, truth = [], [], [], []
    for s in ('S1','S2','S3'):
        for p in ('P1','P2'):
            for i,label in enumerate(LABELS):
                for reset in range(10):
                    base = dict(trial_id=f'{s}-{p}-{i}-{reset}',session_id=s,placement_id=p)
                    plan.append(base)
                    row = dict(base,trial_origin='synthetic_test_fixture',quality='ok',
                               rssi_1_dbm=str(-90+10*i),rssi_2_dbm=str(-85+10*i),
                               csi_1_amp_dispersion=str(i),csi_2_amp_dispersion=str(i))
                    if (s,p) in (('S1','P1'),('S2','P1')):
                        train.append(dict(row,label=label,ground_truth_source='fixture'))
                    elif (s,p) != ('S1','P2'):
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

    def test_missing_duplicate_or_reserve(self):
        reserve=dict(self.test[0],**next(r for r in self.plan if (r['session_id'],r['placement_id'])==('S1','P2')))
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
