import gc,json,random,time,statistics
from fractions import Fraction as F
from pathlib import Path
from model import Config,Model,witness_belief
from planner import Planner
from certify import select

def run():
    b=witness_belief();rows=[];src=json.loads((Path(__file__).parent/'results.json').read_text())
    for case in src:
        c=Config(erasure=F(case['erasure']),service=case['service'],schedule=tuple(case['schedule']),budget=case['budget']);opt=F(case['policies']['exact']['objective'])
        for eps in (F(0),F(1,64)):
            for cap in (1,4):
                r,_=select(Model(c),b,cap,eps);assert F(r['lower'])<=opt<=F(r['upper']);assert r['policy']['worst_credits']<=c.budget
                assert r['certified']==(F(r['gap'])<=eps)
                if r['certified']:assert F(r['upper'])-opt<=eps
                rows.append({'erasure':case['erasure'],'service':case['service'],'schedule':case['schedule'],'budget':case['budget'],'cap':cap,**r})
    rng=random.Random(271126);times=[]
    for name,c in [('ideal_first',Config()),('combined_all',Config(erasure=F(1,4),service='random',schedule=(1,2,3,4),budget=4)),('combined_zero_budget',Config(erasure=F(1,4),service='random',schedule=(1,2,3,4),budget=0))]:
        vals={k:[] for k in ('auto','depth2','exact')};costs={}
        for _ in range(7):
            order=list(vals);rng.shuffle(order)
            for k in order:
                gc.collect();t=time.perf_counter_ns();m=Model(c)
                value=select(m,b)[0]['upper'] if k=='auto' else Planner(m,depth=2 if k=='depth2' else 4).report(b)['objective'];vals[k].append((time.perf_counter_ns()-t)/1e6)
                costs[k]=value
        assert len(set(costs.values()))==1
        times.append({'case':name,'costs':costs,'ms':{k:{'raw':v,'median':statistics.median(v),'min':min(v),'max':max(v)} for k,v in vals.items()}})
    return {'rows':rows,'timing':times,'timing_method':'7 paired randomized repeats, fresh model, planning and evaluation, gc excluded, no process startup or UI'}
if __name__=='__main__':print(json.dumps(run(),indent=2))
