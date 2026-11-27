import unittest
from fractions import Fraction as F
from model import Config,Model,witness_belief,CREDITS
from planner import Planner
from session import DecisionSession
from trace import replay

class SessionTests(unittest.TestCase):
    def setUp(self):self.b=witness_belief()
    def test_truth_free_api_matches_replay(self):
        for config in [Config(),Config(erasure=F(1,4),service='random',schedule=(1,2,3,4))]:
            for d in (1,2,4):
                p=Planner(Model(config),depth=d)
                for truth,_ in self.b:
                    events=[(2,'0',False),(1 if config.service=='random' else 2,'1',bool(config.erasure)),(2,'0',False),(2,'1',False)]
                    expected=replay(p,self.b,truth,events);s=DecisionSession(p,self.b)
                    for j,(ev,row) in enumerate(zip(events,expected['rows']),1):
                        r=s.request(j);self.assertEqual(r['mode'],row['mode']);m=r['mode']
                        if m:self.assertEqual(s.supply(j,row['paid_value'])['status'],'CAN_DECIDE')
                        self.assertEqual(s.decide(j)['action'],row['action']);self.assertEqual(s.remaining,row['remaining_budget'])
                        self.assertIn(s.receive_next(j,row['free_next'])['status'],('READY','DONE'))
                    self.assertEqual(s.phase,'DONE')
    def test_future_or_duplicate_request(self):
        for wrong in (0,2):
            s=DecisionSession(Planner(Model(Config())),self.b);self.assertEqual(s.request(wrong)['status'],'ABSTAINED');self.assertNotIn('action',s.decide(1))
        s=DecisionSession(Planner(Model(Config())),self.b);s.request(1);self.assertEqual(s.request(1)['status'],'ABSTAINED');self.assertNotIn('action',s.decide(1))
    def test_bad_paid_observation_spends_reserved_budget(self):
        s=DecisionSession(Planner(Model(Config())),self.b);r=s.request(1);self.assertEqual(r['mode'],2);self.assertEqual(s.remaining,0)
        self.assertEqual(s.supply(1,'1111')['status'],'ABSTAINED');self.assertEqual(s.remaining,0);self.assertNotIn('action',s.decide(1))
    def test_unknown_free_observation(self):
        s=DecisionSession(Planner(Model(Config(budget=0))),self.b);s.request(1);s.decide(1);r=s.receive_next(1,(100,100,0,0));self.assertEqual(r['status'],'ABSTAINED');self.assertNotIn('action',s.decide(2))
    def test_decide_without_measurement(self):
        s=DecisionSession(Planner(Model(Config())),self.b);s.request(1);self.assertEqual(s.decide(1)['status'],'ABSTAINED')
    def test_no_post_completion_action(self):
        c=Config(horizon=1,budget=0);s=DecisionSession(Planner(Model(c)),self.b);s.request(1);s.decide(1);s.receive_next(1,None);self.assertEqual(s.request(2)['status'],'DONE');self.assertNotIn('action',s.decide(2))
if __name__=='__main__':unittest.main()
