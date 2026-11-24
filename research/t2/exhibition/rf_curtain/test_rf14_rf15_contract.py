import unittest
from rf14_blind_contract import seal_predictions,score_sealed,availability
from rf15_active_only_evaluation import evaluate_active
from rf_pilot_evaluator import LABELS

def fixture():
    plan=[];rows=[]
    for s,p in (("S1","P1"),("S2","P1"),("S3","P2"),("S1","P2")):
        for i,label in enumerate(LABELS):
            r=dict(trial_id=f"{s}-{p}-{i}",session_id=s,placement_id=p)
            plan.append(r)
            rows.append(dict(r,label=label,trial_origin="synthetic_test_fixture",
                ground_truth_source="fixture",quality="ok",rssi_1_dbm=str(-90+i*10),
                rssi_2_dbm=str(-80+i*10),csi_1_amp_dispersion=str(i),
                csi_2_amp_dispersion=str(i)))
    return plan,rows

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.plan,self.rows=fixture()
        self.test=[r for r in self.rows if r["session_id"]=="S3"]
        self.pred=[dict(trial_id=r["trial_id"],prediction=r["label"]) for r in self.test]
        self.truth=[dict(trial_id=r["trial_id"],label=r["label"]) for r in self.test]
    def test_roundtrip(self):
        p,h=seal_predictions(self.plan,self.pred)
        self.assertEqual(score_sealed(self.plan,p,h,self.truth)["correct"],5)
    def test_missing_duplicate(self):
        for bad in (self.pred[:-1],self.pred+[self.pred[0]]):
            with self.assertRaises(ValueError):seal_predictions(self.plan,bad)
    def test_tamper(self):
        p,h=seal_predictions(self.plan,self.pred)
        with self.assertRaises(ValueError):score_sealed(self.plan,p+" ",h,self.truth)
    def test_truth_missing(self):
        p,h=seal_predictions(self.plan,self.pred)
        with self.assertRaises(ValueError):score_sealed(self.plan,p,h,self.truth[:-1])
    def test_reserve_isolation(self):
        rows=[r for r in self.rows if (r["session_id"],r["placement_id"])!=("S1","P2")]
        a=evaluate_active(self.plan,rows)
        plan=[r for r in self.plan if (r["session_id"],r["placement_id"])!=("S1","P2")]
        self.assertEqual(a,evaluate_active(plan,rows))
        with self.assertRaises(ValueError):evaluate_active(self.plan,self.rows)
    def test_availability(self):
        self.assertEqual(availability({"rssi_1_dbm":-60}),dict(rssi_one=True,rssi_both=False,csi_both=False,common=False))
    def test_abstention_denominator(self):
        self.pred[0]["prediction"]="abstain"
        p,h=seal_predictions(self.plan,self.pred)
        s=score_sealed(self.plan,p,h,self.truth)
        self.assertEqual((s["n"],s["correct"],s["abstain"]),(5,4,1))

if __name__=="__main__":unittest.main()
