import gc,json,random,time,statistics
from fractions import Fraction as F
from pathlib import Path
from model import Config,Model,witness_belief
from planner import Planner
from certify import select
from lazy_certificate import select_lazy

def run():
    b=witness_belief();base=json.loads((Path(__file__).parent/'auto_results.json').read_text())['rows'];rows=[]
    for x in base:
        c=Config(erasure=F(x['erasure']),service=x['service'],schedule=tuple(x['schedule']),budget=x['budget']);r,_=select_lazy(Model(c),b,x['cap'],F(x['epsilon']))
        assert F(r['lower'])==F(x['lower']);assert r['certified']==x['certified'];assert r['policy']['worst_credits']<=c.budget
        if not r['certified']:assert F(r['upper'])==F(x['upper'])
        if r['certified']:assert F(r['upper'])-F(x['lower'])<=F(x['epsilon'])
        rows.append({k:x[k] for k in ('erasure','service','schedule','budget','cap','epsilon')}|{'eager_upper':x['upper'],'eager_evaluations':len(x['history']),**r})
    rng=random.Random(271126);times=[]
    for name,c in [('ideal_first',Config()),('combined_all',Config(erasure=F(1,4),service='random',schedule=(1,2,3,4),budget=4)),('combined_zero_budget',Config(erasure=F(1,4),service='random',schedule=(1,2,3,4),budget=0))]:
        vals={k:[] for k in ('lazy','eager','exact')};costs={}
        for _ in range(7):
            order=list(vals);rng.shuffle(order)
            for k in order:
                gc.collect();t=time.perf_counter_ns();m=Model(c)
                value=select_lazy(m,b)[0]['upper'] if k=='lazy' else select(m,b)[0]['upper'] if k=='eager' else Planner(m,depth=4).report(b)['objective'];vals[k].append((time.perf_counter_ns()-t)/1e6);costs[k]=value
        assert len(set(costs.values()))==1
        times.append({'case':name,'costs':costs,'ms':{k:{'raw':v,'median':statistics.median(v),'min':min(v),'max':max(v)} for k,v in vals.items()}})
    return {'rows':rows,'timing':times,'timing_method':'7 paired randomized repeats; fresh model, lower/upper and evaluation work, gc excluded, no startup/UI'}
if __name__=='__main__':print(json.dumps(run(),indent=2))
