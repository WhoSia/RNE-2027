from fractions import Fraction as F
from model import Model,Config,witness_belief
from objective import Objective,VectorDynamics,VectorPlanner
from objective_certificate import select_vector
from objective_audit import enumerate_vector
import json

def run():
    refs=json.load(open('objective_results.json'));rows=[]
    for ctx in refs:
        broad=ctx['law']=='broad';m=Model(Config(schedule=(1,2,3,4),erasure=F(1,4) if broad else F(0),service='random' if broad else 'fixed'));d=VectorDynamics(m);b=witness_belief(tuple(ctx['q']),ctx['word'])
        for r in ctx['rows']:
            obj=Objective(tuple(r['weights']));exact=F(r['policies']['exact']['objective']);cases=[]
            for cap,eps in [(2,F(0)),(4,F(0)),(4,F(1,64))]:
                a,p=select_vector(d,obj,b,cap,eps);assert F(a['lower'])<=exact<=F(a['upper']) and a['policy']['worst_credits']<=4
                if cap==4:assert a['certified']
                if a['certified']:assert F(a['upper'])-exact<=eps
                cases.append(a)
            rows.append({'law':ctx['law'],'q':ctx['q'],'word':ctx['word'],'weights':r['weights'],'exact':str(exact),'cases':cases})
    d=VectorDynamics(Model(Config(schedule=(1,2,3,4),erasure=F(1,4),service='random')));b=witness_belief();o=Objective((1,1,4,0,1));aud=[]
    for depth in (2,4):
        p=VectorPlanner(d,o,depth=depth);v=enumerate_vector(p,b);r=p.report(b)
        assert all(v[k]==r[k] for k in ('vector','objective','worst_credits'));aud.append({'depth':depth,**v})
    return {'rows':rows,'event_audit':aud}
if __name__=='__main__':print(json.dumps(run(),indent=2))
