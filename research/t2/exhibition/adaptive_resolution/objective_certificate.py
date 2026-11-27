"""Incumbent-first certification for the same objective used by the planner."""
from fractions import Fraction as F
from objective import VectorPlanner

def select_vector(dynamics,objective,belief,max_depth=None,epsilon=F(0)):
    c=dynamics.model.c;cap=c.horizon if max_depth is None else max_depth
    if not isinstance(cap,int) or not 1<=cap<=c.horizon or epsilon<0:raise ValueError('cap/epsilon')
    lower=upper=best=None;history=[]
    for d in range(1,cap+1):
        p=VectorPlanner(dynamics,objective,depth=d);ld=p.sense(belief,c.horizon,c.budget,d)[0]
        if lower is not None and ld<lower:raise AssertionError('relaxation monotonicity')
        lower=ld
        if upper is not None and upper<lower:raise AssertionError('invalid bound')
        if upper is not None and upper-lower<=epsilon:
            history.append({'depth':d,'lower':str(lower),'upper':str(upper),'evaluated':False});break
        r=p.report(belief);ud=F(r['objective'])
        if upper is None or ud<upper:upper=ud;best=(d,p,r)
        if upper<lower:raise AssertionError('invalid bound')
        history.append({'depth':d,'lower':str(lower),'upper':str(upper),'evaluated':True})
        if upper-lower<=epsilon:break
    d,p,r=best
    return {'selected_depth':d,'explored_depth':history[-1]['depth'],'lower':str(lower),'upper':str(upper),'gap':str(upper-lower),'certified':upper-lower<=epsilon,'exact':upper==lower,'epsilon':str(epsilon),'history':history,'policy':r},p
