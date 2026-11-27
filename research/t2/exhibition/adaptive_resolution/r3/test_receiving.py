"""Independent per-token transition oracle and exhaustive finite path audit."""
import unittest
from collections import deque
from itertools import product
from fractions import Fraction as F
from receiving import *

def oracle(x,a,drain,arrival,finite):
    pockets=[deque([str(j)]*x[j]) for j in range(2)]
    down=[deque([str(j)]*x[3+j]) for j in range(2)];up=deque(x[2]);exits=0
    for j in range(2):
        if drain[j] and down[j]:down[j].popleft();exits+=1
    for _ in range(2):
        if not pockets[a] or finite and len(down[a])==2:break
        tok=pockets[a].popleft()
        if finite:down[a].append(tok)
        else:exits+=1
    for _ in range(2):
        if not up or len(pockets[int(up[0])])==2:break
        pockets[int(up[0])].append(up.popleft())
    s=len(pockets[0])+up.count('0');l=len(pockets[1])+up.count('1')
    y=(len(pockets[0]),len(pockets[1]),''.join(up)+arrival,len(down[0]),len(down[1]))
    return y,(s,l,max(s,l),s+l+sum(map(len,down)),exits,0,0)

def path_audit(m,p,b,k):
    n=0;v=[F(0)]*7;worst=0
    def walk(x,belief,h,budget,prob,acc):
        nonlocal n,worst
        mode=p.sense(belief,h,budget)[1];cost=COST[mode]
        if mode:
            o=m.observe(x,mode);belief=next(bb for oo,_,bb in m.partition(belief,mode) if oo==o)
        action=p.control(belief,h,budget-cost)[1];parts=m.predict(belief,action)[1]
        for drain,arrival in product(product((0,1),repeat=2),'01'):
            y,r=oracle(x,action,drain,arrival,m.finite)
            nxt=add(acc,add(r,(0,0,0,0,0,cost,int(bool(mode)))))
            if h==1:
                n+=1;worst=max(worst,nxt[5])
                for i,z in enumerate(nxt):v[i]+=prob*z/8
            else:
                bb=next(bb for _,bb in parts if any(y==z for z,_ in bb));walk(y,bb,h-1,budget-cost,prob/8,nxt)
    for x,w in b:walk(x,b,m.H,k,F(w,mass(b)),ZERO)
    return n,tuple(v),worst

class TestReceiving(unittest.TestCase):
    def test_oracle(self):
        words=[''.join(w) for h in range(5) for w in product('01',repeat=h)]
        count=0
        for finite in (False,True):
            m=Model(finite)
            for s,l,rs,rl,w,a,d,z in product(range(3),range(3),range(3),range(3),words,range(2),product((0,1),repeat=2),'01'):
                x=(s,l,w,rs,rl);self.assertEqual(m.transition(x,a,d,z),oracle(x,a,d,z,finite));count+=1
        self.assertEqual(count,80352)
    def test_infinite_r2_parity(self):
        import sys;sys.path.insert(0,'..')
        from model import Model as Old,Config
        old=Old(Config(horizon=3));m=Model(False);count=0
        for s,l,w,a,z in product(range(3),range(3),['','0','1','01','10','0001'],range(2),'01'):
            y,v=m.transition((s,l,w,0,0),a,(0,0),z);yy,stock=old.transition((s,l,w),a,2,z)
            self.assertEqual(y[:3],yy);self.assertEqual(v[0]+v[1],stock);count+=1
        self.assertEqual(count,216)
    def test_path(self):
        m=Model(True);b=initial((2,2),'0001')
        for peak in (0,4):
            p=Planner(m,peak);n,v,w=path_audit(m,p,b,4);self.assertEqual(n,4096);self.assertEqual((v,w),p.evaluate(b,3,4))
    def test_budget_and_calendar(self):
        import json
        for name in ('finite','infinite'):
            for c in json.load(open(name+'.json')):
                old=None
                for r in c['rows']:
                    opt=F(r['policies']['joint']['cost']);self.assertTrue(old is None or opt<=old);old=opt
                    self.assertTrue(all(F(v['cost'])>=opt and v['worst']<=r['budget'] for v in r['policies'].values()))
                    self.assertEqual(F(r['calendar_gain']),0)
if __name__=='__main__':unittest.main()
