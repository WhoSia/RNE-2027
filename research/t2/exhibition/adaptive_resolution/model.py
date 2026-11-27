"""Finite FIFO laboratory model; abstract slots, not road-signal control."""
from dataclasses import dataclass
from collections import Counter, defaultdict
from functools import lru_cache
from fractions import Fraction as F
from math import gcd
from itertools import product, permutations

ACTIONS=(0,1)
CREDITS=(0,1,4)
PRICE=F(1,64)

def normalize(weights):
    c=Counter()
    for x,w in weights:
        if not isinstance(w,int) or w<=0: raise ValueError('positive integer weights required')
        c[x]+=w
    if not c: raise ValueError('empty belief')
    g=gcd(*c.values())
    return tuple(sorted((x,w//g) for x,w in c.items()))
def mass(b): return sum(w for _,w in b)
def witness_belief(q=(2,2),word='0001'):
    return normalize(((q[0],q[1],''.join(w)),1) for w in sorted(set(permutations(word))))

@dataclass(frozen=True)
class Config:
    capacity: tuple[int,int]=(2,2)
    horizon: int=4
    schedule: tuple[int,...]=(1,)
    erasure: F=F(0)
    service: str='fixed'
    budget: int=4
    def __post_init__(self):
        if len(self.capacity)!=2 or min(self.capacity)<1 or not 1<=self.horizon<=6: raise ValueError('geometry/horizon')
        if not 0<=self.erasure<=1 or self.service not in ('fixed','random'): raise ValueError('channel/service')
        if self.budget<0 or any(not 1<=t<=self.horizon for t in self.schedule) or len(set(self.schedule))!=len(self.schedule): raise ValueError('budget/schedule')

class Model:
    def __init__(self,config):
        self.c=config
        self.step=lru_cache(None)(self._step)
        self.predict=lru_cache(None)(self._predict)
        self.tail=lru_cache(None)(self._tail)
    def validate(self,x):
        s,l,w=x
        if not 0<=s<=self.c.capacity[0] or not 0<=l<=self.c.capacity[1] or set(w)-{'0','1'}: raise ValueError('state')
    def transition(self,x,a,service,arrival):
        self.validate(x)
        if a not in ACTIONS or service not in (1,2) or arrival not in ('0','1'): raise ValueError('event')
        q,w=list(x[:2]),x[2]; d=min(q[a],service); q[a]-=d
        for _ in range(2):
            if not w or q[int(w[0])]>=self.c.capacity[int(w[0])]: break
            q[int(w[0])]+=1; w=w[1:]
        stock=sum(q)+len(w)
        if stock!=sum(x[:2])+len(x[2])-d: raise AssertionError('conservation')
        return (*q,w+arrival),stock
    def _step(self,x,a):
        services=(2,) if self.c.service=='fixed' else (1,2)
        return tuple(self.transition(x,a,s,z) for s,z in product(services,('0','1')))
    @staticmethod
    def observe(x,m,erased=False):
        s,l,w=x
        if m==0:return (s,l,None,None) if erased else (s,l,w.count('0'),w.count('1'))
        if m==1:return w[:1]
        if m==2:return w
        raise ValueError('mode')
    def partition(self,b,m):
        groups=defaultdict(list)
        for x,w in b:groups[self.observe(x,m)].append((x,w))
        return {o:(F(sum(w for _,w in g),mass(b)),normalize(g)) for o,g in groups.items()}
    def _predict(self,b,a):
        prior=Counter();stock=den=0
        for x,w in b:
            for y,r in self.step(x,a):prior[y]+=w;stock+=w*r;den+=w
        groups=defaultdict(Counter);p=self.c.erasure
        for y,w in prior.items():
            for erased,mult in ((False,p.denominator-p.numerator),(True,p.numerator)):
                if mult:groups[self.observe(y,0,erased)][y]+=w*mult
        outcomes={o:(F(sum(g.values()),den*p.denominator),normalize(g.items())) for o,g in groups.items()}
        if sum(v[0] for v in outcomes.values())!=1:raise AssertionError('posterior mass')
        return F(stock,den),outcomes
    def _tail(self,x,h):
        if not h:return F(0)
        return min(sum((r+self.tail(y,h-1) for y,r in self.step(x,a)),F(0))/len(self.step(x,a)) for a in ACTIONS)
