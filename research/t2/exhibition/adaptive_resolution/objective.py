"""Exact vector-cost extension of R1; no live controller."""
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from model import ACTIONS,CREDITS,PRICE,mass
from planner import Planner
NAMES=('straight','left','stage_max','terminal','credits')
ZERO=(F(0),)*5

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def weighted(rows):
    v=ZERO
    for p,x in rows:v=add(v,tuple(p*y for y in x))
    return v

def reward(y,h):
    s,l,w=y;w=w[:-1];s+=w.count('0');l+=w.count('1')
    return (F(s),F(l),F(max(s,l)),F(s+l if h==1 else 0),F(0))

@dataclass(frozen=True)
class Objective:
    weights:tuple=(1,1,0,0,1)
    def __post_init__(self):
        if len(self.weights)!=5 or any(not isinstance(w,(int,F)) or w<0 for w in self.weights) or not any(self.weights):raise ValueError('invalid weights')
    def cost(self,v):return sum(w*x*(PRICE if i==4 else 1) for i,(w,x) in enumerate(zip(self.weights,v)))

class VectorDynamics:
    def __init__(self,model):
        self.model=model;self.stage=lru_cache(None)(self._stage)
    def _stage(self,b,a,h):
        parts=self.model.predict(b,a)[1];rows=[]
        for x,w in b:
            z=self.model.step(x,a)
            for y,stock in z:
                v=reward(y,h)
                if v[0]+v[1]!=stock:raise AssertionError('stock parity')
                rows.append((F(w,mass(b)*len(z)),v))
        return weighted(rows),parts

class VectorPlanner(Planner):
    def __init__(self,dynamics,objective=Objective(),policy='adaptive',depth=None):
        self.dynamics=dynamics;self.obj=objective
        super().__init__(dynamics.model,policy,depth)
        self.tail=lru_cache(None)(self._tail_vector)
    def _tail_vector(self,x,h):
        if not h:return F(0)
        return min(sum((self.obj.cost(reward(y,h))+self.tail(y,h-1) for y,_ in self.model.step(x,a)),F(0))/len(self.model.step(x,a)) for a in ACTIONS)
    def _sense(self,b,h,k,d):
        if not h:return F(0),0
        return min((self.obj.cost((0,0,0,0,CREDITS[m]))+sum(p*self.control(bb,h,k-CREDITS[m],d)[0] for p,bb in self.parts(b,m)),m) for m in self.modes(b,h,k))
    def _control(self,b,h,k,d):
        out=[]
        for a in ACTIONS:
            v,parts=self.dynamics.stage(b,a,h);r=self.obj.cost(v)
            if h>1:
                if d>1:r+=sum(p*self.sense(bb,h-1,k,d-1)[0] for p,bb in parts.values())
                else:r+=sum(p*sum(F(w,mass(bb))*self.tail(x,h-1) for x,w in bb) for p,bb in parts.values())
            out.append((r,a))
        return min(out)
    def _evaluate(self,b,h,k):
        if not h:return ZERO,0,F(0)
        m=self.sense(b,h,k,min(h,self.depth))[1];spent=CREDITS[m]
        rows=[(p,self.evaluate_action(bb,h,k-spent)) for p,bb in self.parts(b,m)]
        v=add((0,0,0,0,F(spent)),weighted((p,x[0]) for p,x in rows));worst=spent+max(x[1] for _,x in rows)
        if worst>k:raise AssertionError('budget')
        return v,worst,F(m!=0)+sum(p*x[2] for p,x in rows)
    def _evaluate_action(self,b,h,k):
        a=self.control(b,h,k,min(h,self.depth))[1];v,parts=self.dynamics.stage(b,a,h)
        if h==1:return v,0,F(0)
        rows=[(p,self.evaluate(bb,h-1,k)) for p,bb in parts.values()]
        return add(v,weighted((p,x[0]) for p,x in rows)),max(x[1] for _,x in rows),sum(p*x[2] for p,x in rows)
    def report(self,b):
        h,k=self.model.c.horizon,self.model.c.budget
        for x,_ in b:self.model.validate(x)
        v,worst,acq=self.evaluate(b,h,k);lower,mode=self.sense(b,h,k,self.depth);cost=self.obj.cost(v)
        if lower>cost:raise AssertionError('bound')
        return {'vector':{n:str(x) for n,x in zip(NAMES,v)},'objective':str(cost),'lower':str(lower),'gap':str(cost-lower),'worst_credits':worst,'acquisitions':str(acq),'mode':mode}

def vector(report):return tuple(F(report['vector'][n]) for n in NAMES)
def dominates(a,b):return all(x<=y for x,y in zip(a,b)) and any(x<y for x,y in zip(a,b))
