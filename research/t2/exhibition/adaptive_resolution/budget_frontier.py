"""Exact hard-cap frontier; shared model caches, no credit price or equal realized usage claim."""
from fractions import Fraction as F
from model import Model,Config,witness_belief
from objective import Objective,VectorDynamics,VectorPlanner,NAMES
from run_objective import CLASSES
import json, argparse

def run(law):
    out=[];erasure,service=(F(0),'fixed') if law=='ideal' else (F(1,4),'random')
    for weights in [(1,1,0,0,0),(1,1,4,0,0)]:
        o=Objective(weights);d=VectorDynamics(Model(Config(schedule=(1,2,3,4),erasure=erasure,service=service,budget=8)))
        ps={p:VectorPlanner(d,o,p) for p in ('adaptive','free','head','full')}
        for q,w in CLASSES:
            b=witness_belief(q,w);rows=[];prev=None
            for k in (0,1,2,3,4,8):
                rr={}
                for name,p in ps.items():
                    v,worst,acq=p.evaluate(b,4,k);cost=o.cost(v);lower,mode=p.sense(b,4,k,4)
                    assert lower==cost
                    rr[name]={'vector':{n:str(x) for n,x in zip(NAMES,v)},'objective':str(cost),'worst_credits':worst,'acquisitions':str(acq),'mode':mode}
                cost=F(rr['adaptive']['objective']);fixed=min(F(rr[p]['objective']) for p in ('free','head','full'))
                assert prev is None or cost<=prev;assert cost<=fixed and all(x['worst_credits']<=k for x in rr.values());prev=cost
                rows.append({'budget':k,'policy':rr,'gain_vs_fixed':str(fixed-cost)})
            out.append({'law':law,'q':q,'word':w,'weights':weights,'rows':rows})
            print(law,q,weights,flush=True,file=__import__('sys').stderr)
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--law',choices=['ideal','broad']);a=p.parse_args();print(json.dumps(run(a.law) if a.law else run('ideal')+run('broad'),indent=2))
