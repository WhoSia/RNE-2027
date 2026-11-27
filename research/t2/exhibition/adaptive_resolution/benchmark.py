"""Local CPU wall time; cold caches, paired randomized policy ordering."""
import gc,json,random,time,statistics,platform
from fractions import Fraction as F
from model import Config,Model,witness_belief
from planner import Planner

def run(reps=7):
    rng=random.Random(271126);out=[];b=witness_belief()
    cases=[('ideal_first',Config()),('combined_all',Config(erasure=F(1,4),service='random',schedule=(1,2,3,4),budget=4)),('combined_zero_budget',Config(erasure=F(1,4),service='random',schedule=(1,2,3,4),budget=0))]
    for name,c in cases:
        values={1:[],2:[],4:[]};objectives={}
        for _ in range(reps):
            depths=[1,2,4];rng.shuffle(depths)
            for d in depths:
                gc.collect();start=time.perf_counter_ns();r=Planner(Model(c),depth=d).report(b);values[d].append((time.perf_counter_ns()-start)/1e6)
                if d in objectives:assert objectives[d]==r['objective']
                objectives[d]=r['objective']
        out.append({'case':name,'reps':reps,'objective':objectives,'ms':{d:{'raw':v,'median':statistics.median(v),'min':min(v),'max':max(v)} for d,v in values.items()}})
    return {'python':platform.python_version(),'platform':platform.platform(),'method':'fresh Model and Planner per evaluation, includes full-state tail, plan, replay; gc outside timing; randomized depth order; no startup or browser UI cost','cases':out}
if __name__=='__main__':print(json.dumps(run(),indent=2))
