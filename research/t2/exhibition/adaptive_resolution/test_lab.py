import unittest
from fractions import Fraction as F
from model import Config,Model,witness_belief,normalize
from planner import Planner
from trace import replay,exhaustive

class LabTests(unittest.TestCase):
    def setUp(self):self.b=witness_belief()
    def test_parity(self):
        c=Config();f=Planner(Model(c),'free').report(self.b);a=Planner(Model(c)).report(self.b);q=Planner(Model(c),depth=1).report(self.b)
        self.assertEqual(F(f['objective'])-F(a['objective']),F(11,16));self.assertEqual(F(q['objective'])-F(a['objective']),F(13,64));self.assertEqual((a['mode'],q['mode']),(2,1))
    def test_exact_gap(self):
        c=Config(erasure=F(1,4),service='random',schedule=(1,2,3,4));a=Planner(Model(c)).report(self.b);d=Planner(Model(c),depth=2).report(self.b)
        self.assertEqual(a['objective'],d['objective']);self.assertEqual(d['gap'],'0')
    def test_budget(self):
        for k in range(5):
            c=Config(budget=k,schedule=(1,2,3,4));a=Planner(Model(c)).report(self.b);self.assertLessEqual(a['worst_credits'],k)
    def test_no_observation(self):
        c=Config(budget=0);self.assertEqual(Planner(Model(c)).report(self.b)['objective'],Planner(Model(c),'free').report(self.b)['objective'])
    def test_innovation(self):
        b=normalize([((0,0,''),1)]);m=Model(Config(erasure=F(1,4)));_,p=m.predict(b,0)
        self.assertEqual(len(p[(0,0,None,None)][1]),2)
        self.assertEqual(sum(x[0] for x in p.values()),1)
    def test_invalid_config(self):
        for kwargs in ({'budget':-1},{'erasure':F(5,4)},{'schedule':(0,)},{'capacity':(0,2)}):
            with self.assertRaises(ValueError):Config(**kwargs)
    def test_normalization(self):
        self.assertEqual(normalize([(x,7*w) for x,w in self.b]),self.b)
    def test_replay_no_truth_access(self):
        p=Planner(Model(Config(budget=1)),depth=2);events=[(2,'0',False)]*4
        traces=[replay(p,self.b,x,events) for x,_ in self.b]
        self.assertEqual(len({t['rows'][0]['mode'] for t in traces}),1)
        for a in traces:
            for b in traces:
                x,y=a['rows'][0],b['rows'][0]
                if x['paid_value']==y['paid_value']:self.assertEqual(x['action'],y['action'])
    def test_impossible_obs(self):
        p=Planner(Model(Config(budget=0)),depth=1)
        with self.assertRaisesRegex(ValueError,'OUT_OF_SUPPORT'):replay(p,self.b,(0,0,''),[(2,'0',False)]*4)
        with self.assertRaisesRegex(ValueError,'OUT_OF_SUPPORT'):replay(p,self.b,self.b[0][0],[(2,'0',True)]+[(2,'0',False)]*3)
    def test_event_tree(self):
        c=Config(erasure=F(1,4),service='random',schedule=(1,2,3,4));p=Planner(Model(c),depth=2)
        r=p.report(self.b);v=exhaustive(p,self.b)
        for k in ['objective','stock','credits','worst_credits']:self.assertEqual(r[k],v[k])
if __name__=='__main__':unittest.main()
