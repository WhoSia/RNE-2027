import unittest,json,csv
from fractions import Fraction as F
from receiving_channel import *
from calibration import audit,read
class TestChannel(unittest.TestCase):
    def test_initial_partition(self):
        b=initial((2,2),'0001')
        for e in (F(0),F(1,4),F(1,2)):
            m=ChannelModel(e);parts=m.partition(b,3);self.assertEqual(sum(p for _,p,_ in parts),1)
            for o,p,bb in parts:
                self.assertEqual(p,F(1,2));self.assertEqual(sum(F(w,mass(bb)) for x,w in bb if x[3:]==o),1-e)
        self.assertTrue(all(bb==b for _,_,bb in ChannelModel(F(1,2)).partition(b,3)))
    def test_zero_error_parity(self):
        b=initial((2,2),'0001');m=Model();c=ChannelModel()
        self.assertEqual(m.partition(b,3),c.partition(b,3))
        for k in (0,1,2,4):self.assertEqual(Planner(m).report(b,k),Planner(c).report(b,k))
    def test_mismatch_receipt(self):
        with open('mismatch.json') as f:a=json.load(f)
        self.assertEqual(len(a),18)
        for r in a:
            self.assertEqual(F(r['complete_mass'])+F(r['abort_mass']),1);self.assertLessEqual(r['worst'],2)
            if r['nominal']==r['actual']:self.assertEqual(r['excess_if_no_abort'],'0')
            if F(r['abort_mass']):self.assertIsNone(r['excess_if_no_abort'])
    def test_calibration_fixture(self):
        r=read('calibration_fixture.csv');a=r['splits']['calibration'];v=r['splits']['validation'];self.assertEqual(a['swap_only_fit_candidate'],'1/4');self.assertIsNone(v['swap_only_fit_candidate']);self.assertEqual(v['counts']['nonswap'],1);self.assertEqual(v['counts']['missing'],1)
    def test_reject_split_leak(self):
        with open('calibration_fixture.csv') as f:r=list(csv.DictReader(f))
        r[-1]['block_id']='B1'
        with self.assertRaises(ValueError):audit(r)
    def test_reject_duplicate(self):
        with open('calibration_fixture.csv') as f:r=list(csv.DictReader(f))
        with self.assertRaises(ValueError):audit(r+[r[0]])
    def test_reject_personal_id(self):
        with open('calibration_fixture.csv') as f:r=list(csv.DictReader(f))
        r[0]['block_id']='Alice'
        with self.assertRaises(ValueError):audit(r)
if __name__=='__main__':unittest.main()
