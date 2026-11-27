import unittest
from fractions import Fraction as F
from model import Model,Config,witness_belief
from planner import Planner
from objective import Objective,VectorDynamics,VectorPlanner,vector,reward,dominates
from objective_certificate import select_vector
from session import DecisionSession
from trace import advance

class TestObjective(unittest.TestCase):
    def setUp(self):self.b=witness_belief();self.d=VectorDynamics(Model(Config(schedule=(1,2,3,4))))
    def test_stock_parity(self):
        p=Planner(self.d.model).report(self.b);q=VectorPlanner(self.d).report(self.b);v=vector(q)
        self.assertEqual(F(p['objective']),F(q['objective']));self.assertEqual(v[0]+v[1],F(p['stock']));self.assertEqual(v[4],F(p['credits']))
    def test_reward_excludes_arrival(self):self.assertEqual(reward((1,2,'001'),1),(3,2,3,5,0))
    def test_weights(self):
        for w in [(0,)*5,(-1,1,0,0,0),(1.,1,0,0,0)]:
            with self.assertRaises(ValueError):Objective(w)
        self.assertEqual(Objective((1,1,0,0,4)).cost((1,2,3,4,4)),F(13,4))
    def test_objective_failure_and_certificate(self):
        d=VectorDynamics(Model(Config(schedule=(1,2,3,4),erasure=F(1,4),service='random')));o=Objective((1,1,4,0,1));r=VectorPlanner(d,o,depth=2).report(self.b);e=VectorPlanner(d,o).report(self.b)
        self.assertEqual(F(r['objective'])-F(e['objective']),F(1131,131072));a,_=select_vector(d,o,self.b,2);self.assertFalse(a['certified']);a,_=select_vector(d,o,self.b);self.assertTrue(a['exact']);self.assertEqual(a['upper'],e['objective'])
    def test_session_compatibility(self):
        p=VectorPlanner(self.d,Objective((1,1,4,0,1)));s=DecisionSession(p,self.b);b=self.b;k=4;x=b[0][0]
        for h in (4,3,2,1):
            stage=5-h;nb,nk,y,row=advance(p,b,h,k,x,2,'0',False);req=s.request(stage);self.assertEqual(req['mode'],row['mode'])
            if req['mode']:s.supply(stage,row['paid_value'])
            self.assertEqual(s.decide(stage)['action'],row['action']);s.receive_next(stage,row['free_next']);self.assertEqual(s.remaining,nk);b,k,x=nb,nk,y
        self.assertEqual(s.status()['status'],'DONE')
    def test_dominance(self):self.assertTrue(dominates((1,2,3),(1,3,3)));self.assertFalse(dominates((1,2,3),(1,2,3)))
if __name__=='__main__':unittest.main()
