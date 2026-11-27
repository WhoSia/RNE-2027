"""Frozen objective study, nondominated tested candidates only."""
from fractions import Fraction as F
from model import Model,Config,witness_belief
from planner import Planner
from objective import Objective,VectorDynamics,VectorPlanner,vector,dominates
import json
WEIGHTS=[(1,1,0,0,1),(1,1,1,0,1),(1,1,4,0,1),(1,1,0,2,1),(4,1,0,0,1),(1,4,0,0,1),(1,1,0,0,0),(1,1,0,0,4)]
CLASSES=[((2,2),'0001'),((2,0),'0011'),((0,2),'0011'),((1,1),'0011')]
POLICIES=[('free','free',4),('head','head',4),('full','full',4),('depth2','adaptive',2),('exact','adaptive',4)]
def run():
    results=[]
    for law,erasure,service in [('ideal',F(0),'fixed'),('broad',F(1,4),'random')]:
        m=Model(Config(schedule=(1,2,3,4),erasure=erasure,service=service,budget=4));d=VectorDynamics(m);base=VectorPlanner(d);r1=Planner(m);rr=[[] for _ in CLASSES]
        for weights in WEIGHTS:
            o=Objective(weights);ps={n:VectorPlanner(d,o,p,dep) for n,p,dep in POLICIES}
            for j,(q,w) in enumerate(CLASSES):
                b=witness_belief(q,w);reports={n:p.report(b) for n,p in ps.items()};v0=vector(base.report(b));opt=F(reports['exact']['objective']);old=o.cost(v0)
                for n,r in reports.items():
                    assert F(r['objective'])==o.cost(vector(r)) and F(r['objective'])>=opt and r['worst_credits']<=4
                    if n in ('depth2','exact'):assert F(r['lower'])<=opt
                assert old>=opt and F(reports['exact']['gap'])==0
                if weights==WEIGHTS[0]:
                    prior=r1.report(b);assert opt==F(prior['objective']) and v0[0]+v0[1]==F(prior['stock']) and v0[4]==F(prior['credits'])
                fixed=min(F(reports[n]['objective']) for n in ('free','head','full'))
                rr[j].append({'weights':weights,'policies':reports,'original_vector':[str(x) for x in v0],'original_cost':str(old),'gain_vs_original':str(old-opt),'gain_vs_fixed':str(fixed-opt)})
            print(law,weights,'complete',flush=True,file=__import__('sys').stderr)
        for (q,w),rows in zip(CLASSES,rr):
            vv=sorted(set(vector(r['policies'][n]) for r in rows for n in r['policies']));nd=[v for v in vv if not any(dominates(z,v) for z in vv)]
            results.append({'law':law,'q':q,'word':w,'rows':rows,'unique_candidate_vectors':len(vv),'nondominated_candidates':[[str(x) for x in v] for v in nd]})
    for law in ('ideal','broad'):
        a=next(x for x in results if x['law']==law and x['q']==(2,0));b=next(x for x in results if x['law']==law and x['q']==(0,2))
        for r in a['rows']:
            w=r['weights'];s=next(z for z in b['rows'] if z['weights']==(w[1],w[0],*w[2:]));assert r['policies']['exact']['objective']==s['policies']['exact']['objective']
    return results
if __name__=='__main__':print(json.dumps(run(),indent=2))
