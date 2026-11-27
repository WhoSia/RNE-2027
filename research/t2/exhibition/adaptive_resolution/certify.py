"""Anytime depth selection under exact model-based optimality certificates."""
from fractions import Fraction as F
from planner import Planner


def select(model,belief,max_depth=None,epsilon=F(0)):
    H=model.c.horizon;cap=H if max_depth is None else max_depth
    if not isinstance(cap,int) or not 1<=cap<=H or epsilon<0:raise ValueError('invalid depth/epsilon')
    lower=None;upper=None;best=None;history=[]
    for d in range(1,cap+1):
        p=Planner(model,depth=d);r=p.report(belief);ld,ud=F(r['lower']),F(r['objective'])
        if lower is not None and ld<lower:raise AssertionError('nonmonotone relaxation')
        lower=ld if lower is None else max(lower,ld)
        if upper is None or ud<upper:upper=ud;best=(d,p,r)
        if upper<lower:raise AssertionError('invalid bound')
        history.append({'depth':d,'lower':str(lower),'upper':str(upper),'gap':str(upper-lower),'policy_cost':str(ud)})
        if upper-lower<=epsilon:break
    d,p,r=best
    return {'selected_depth':d,'explored_depth':history[-1]['depth'],'lower':str(lower),'upper':str(upper),'gap':str(upper-lower),'certified':upper-lower<=epsilon,'exact':upper==lower,'epsilon':str(epsilon),'history':history,'policy':r},p
