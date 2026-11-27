"""R3 finite receiving-storage laboratory abstraction; no road-control interface."""
from collections import Counter, defaultdict
from functools import lru_cache
from fractions import Fraction as F
from itertools import product, permutations
from math import gcd

COST=(0,1,4,1)
MODE=('none','head','word','receiving')
ZERO=(F(0),)*7  # upstream S,L, max, system stock, exits, credits, acquisitions

def norm(rows):
    c=Counter()
    for x,w in rows:
        if w<=0: raise ValueError('nonpositive belief weight')
        c[x]+=w
    if not c: raise ValueError('empty belief')
    d=gcd(*c.values())
    return tuple(sorted((x,w//d) for x,w in c.items()))
def mass(b):return sum(w for _,w in b)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def avg(rows):
    v=ZERO
    for p,x in rows:v=add(v,tuple(p*y for y in x))
    return v

def initial(q,word):
    return norm((((q[0],q[1],''.join(w),*r),1) for w in set(permutations(word)) for r in ((0,2),(2,0))))

class Model:
    def __init__(self,finite=True,horizon=3):
        self.finite=finite;self.H=horizon
        self.step=lru_cache(None)(self._step)
        self.predict=lru_cache(None)(self._predict)
        self.partition=lru_cache(None)(self._partition)
    def transition(self,x,a,drain,arrival):
        s,l,w,rs,rl=x;q=[s,l];r=[rs,rl]
        if a not in (0,1) or any(v not in range(3) for v in q+r) or set(w)-{'0','1'} or arrival not in '01' or len(arrival)!=1 or tuple(drain) not in tuple(product((0,1),repeat=2)):raise ValueError('invalid event/state')
        old=sum(q)+len(w)+sum(r)
        exits=sum(min(r[j],drain[j]) for j in (0,1));r=[max(0,r[j]-drain[j]) for j in (0,1)]
        d=min(q[a],2,2-r[a]) if self.finite else min(q[a],2)
        q[a]-=d
        if self.finite:r[a]+=d
        else:exits+=d
        for _ in range(2):
            if not w or q[int(w[0])]==2:break
            q[int(w[0])]+=1;w=w[1:]
        us=q[0]+w.count('0');ul=q[1]+w.count('1');system=us+ul+sum(r)
        assert system==old-exits and all(0<=v<=2 for v in q+r)
        return (*q,w+arrival,*r),(us,ul,max(us,ul),system,exits,0,0)
    def _step(self,x,a):return tuple(self.transition(x,a,d,z) for d in product((0,1),repeat=2) for z in '01')
    @staticmethod
    def observe(x,m):
        s,l,w,rs,rl=x
        return (s,l,w.count('0'),w.count('1')) if m==0 else w[:1] if m==1 else w if m==2 else (rs,rl)
    def _partition(self,b,m):
        c=defaultdict(list)
        for x,w in b:c[self.observe(x,m)].append((x,w))
        return tuple((o,F(sum(w for _,w in g),mass(b)),norm(g)) for o,g in sorted(c.items()))
    def _predict(self,b,a):
        c=Counter();v=[0]*7;den=8*mass(b)
        for x,w in b:
            for y,r in self.step(x,a):
                c[y]+=w
                for i,z in enumerate(r):v[i]+=w*z
        assert sum(c.values())==den
        return tuple(F(z,den) for z in v),tuple((p,bb) for _,p,bb in self.partition(norm(c.items()),0))

class Planner:
    def __init__(self,model,peak=0,modes=(0,1,2,3),calendar=None):
        self.m=model;self.peak=peak;self.allowed=modes;self.calendar=calendar
        self.sense=lru_cache(None)(self._sense);self.control=lru_cache(None)(self._control)
        self.evaluate=lru_cache(None)(self._evaluate);self.eval_action=lru_cache(None)(self._eval_action)
    def cost(self,v):return v[0]+v[1]+self.peak*v[2]
    def modes(self,b,h,k):
        if self.calendar is not None:
            m=self.calendar[self.m.H-h]
            return (m,) if m and COST[m]<=k and len(self.m.partition(b,m))>1 else (0,)
        return tuple(m for m in self.allowed if COST[m]<=k and (not m or len(self.m.partition(b,m))>1))
    def parts(self,b,m):return ((F(1),b),) if not m else tuple((p,bb) for _,p,bb in self.m.partition(b,m))
    def _sense(self,b,h,k):
        if not h:return F(0),0
        return min((sum(p*self.control(bb,h,k-COST[m])[0] for p,bb in self.parts(b,m)),m) for m in self.modes(b,h,k))
    def _control(self,b,h,k):
        candidates=[]
        for a in (0,1):
            v,parts=self.m.predict(b,a);r=self.cost(v)
            if h>1:r+=sum(p*self.sense(bb,h-1,k)[0] for p,bb in parts)
            candidates.append((r,a))
        return min(candidates)
    def _evaluate(self,b,h,k):
        if not h:return ZERO,0
        m=self.sense(b,h,k)[1];spent=COST[m]
        rows=[(p,self.eval_action(bb,h,k-spent)) for p,bb in self.parts(b,m)]
        v=add((0,0,0,0,0,spent,int(bool(m))),avg((p,r[0]) for p,r in rows));worst=spent+max(r[1] for _,r in rows)
        assert worst<=k
        return v,worst
    def _eval_action(self,b,h,k):
        a=self.control(b,h,k)[1];v,parts=self.m.predict(b,a)
        if h==1:return v,0
        rows=[(p,self.evaluate(bb,h-1,k)) for p,bb in parts]
        return add(v,avg((p,r[0]) for p,r in rows)),max(r[1] for _,r in rows)
    def report(self,b,k):
        v,worst=self.evaluate(b,self.m.H,k);opt,m=self.sense(b,self.m.H,k)
        assert opt==self.cost(v) and worst<=k
        return {'cost':str(opt),'vector':list(map(str,v)),'worst':worst,'first':MODE[m]}

def calendars(H,k):return [c for c in product(range(4),repeat=H) if sum(COST[m] for m in c)<=k]
