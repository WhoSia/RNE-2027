"""Exact rational planning and evaluation with pathwise acquisition credits."""
from dataclasses import dataclass
from functools import lru_cache
from fractions import Fraction as F
from model import ACTIONS,CREDITS,PRICE,mass

@dataclass(frozen=True)
class Metrics:
    stock:F=F(0)
    credits:F=F(0)
    acquisitions:F=F(0)
    worst:int=0
    @property
    def objective(self):return self.stock+PRICE*self.credits

class Planner:
    def __init__(self,model,policy='adaptive',depth=None):
        self.model=model;self.policy=policy;self.depth=model.c.horizon if depth is None else depth
        if policy not in ('adaptive','free','head','full') or not 1<=self.depth<=model.c.horizon:raise ValueError('policy/depth')
        self.sense=lru_cache(None)(self._sense);self.control=lru_cache(None)(self._control)
        self.evaluate=lru_cache(None)(self._evaluate);self.evaluate_action=lru_cache(None)(self._evaluate_action)
    def modes(self,b,h,k):
        if self.policy=='free' or self.model.c.horizon-h+1 not in self.model.c.schedule:return (0,)
        if self.policy in ('head','full'):
            m=1 if self.policy=='head' else 2
            return (m,) if CREDITS[m]<=k and len(self.model.partition(b,m))>1 else (0,)
        return tuple(m for m in range(3) if CREDITS[m]<=k)
    def parts(self,b,m):return [(F(1),b)] if not m else list(self.model.partition(b,m).values())
    def _sense(self,b,h,k,d):
        if h==0:return F(0),0
        return min((PRICE*CREDITS[m]+sum(p*self.control(bb,h,k-CREDITS[m],d)[0] for p,bb in self.parts(b,m)),m) for m in self.modes(b,h,k))
    def _control(self,b,h,k,d):
        candidates=[]
        for a in ACTIONS:
            r,parts=self.model.predict(b,a)
            if h>1:
                if d>1:r+=sum(p*self.sense(bb,h-1,k,d-1)[0] for p,bb in parts.values())
                else:r+=sum(p*sum(F(w,mass(bb))*self.model.tail(x,h-1) for x,w in bb) for p,bb in parts.values())
            candidates.append((r,a))
        return min(candidates)
    def _evaluate(self,b,h,k):
        if not h:return Metrics()
        m=self.sense(b,h,k,min(h,self.depth))[1];spent=CREDITS[m]
        if spent>k:raise AssertionError('budget')
        parts=[(p,self.evaluate_action(bb,h,k-spent)) for p,bb in self.parts(b,m)]
        out=Metrics(sum(p*x.stock for p,x in parts),F(spent)+sum(p*x.credits for p,x in parts),F(m!=0)+sum(p*x.acquisitions for p,x in parts),spent+max(x.worst for _,x in parts))
        if out.worst>k:raise AssertionError('path budget')
        return out
    def _evaluate_action(self,b,h,k):
        a=self.control(b,h,k,min(h,self.depth))[1];r,parts=self.model.predict(b,a)
        if h==1:return Metrics(r)
        xs=[(p,self.evaluate(bb,h-1,k)) for p,bb in parts.values()]
        return Metrics(r+sum(p*x.stock for p,x in xs),sum(p*x.credits for p,x in xs),sum(p*x.acquisitions for p,x in xs),max(x.worst for _,x in xs))
    def report(self,b):
        h,k=self.model.c.horizon,self.model.c.budget
        for x,_ in b:self.model.validate(x)
        lower,mode=self.sense(b,h,k,self.depth);m=self.evaluate(b,h,k)
        if lower>m.objective:raise AssertionError('invalid lower bound')
        return {'objective':str(m.objective),'stock':str(m.stock),'credits':str(m.credits),'acquisitions':str(m.acquisitions),'worst_credits':m.worst,'lower':str(lower),'gap':str(m.objective-lower),'mode':mode,'nodes':{n:getattr(self,n).cache_info().currsize for n in ('sense','control','evaluate','evaluate_action')},'tail_nodes':self.model.tail.cache_info().currsize}
