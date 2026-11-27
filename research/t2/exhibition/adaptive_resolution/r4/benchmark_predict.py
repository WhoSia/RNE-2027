"""Exact differential comparison and randomized cold report benchmark."""
import json,random,time,statistics,sys,platform,cProfile,pstats,io
from pathlib import Path
from fractions import Fraction as F
from receiving import initial,Planner
from receiving_channel import ChannelModel,SystemPlanner
from fast_predict import FastChannelModel

SPECS=[('free',(0,)),('word',(0,1,2)),('receiving',(0,3)),('joint',(0,1,2,3))]
def parity():
    source=json.loads((Path(__file__).parent/'../r3/channel.json').read_text());n=0; pred=0
    for r in source:
        old=ChannelModel(F(r['error']));new=FastChannelModel(F(r['error']));b=initial(tuple(r['q']),r['word'])
        for obj,cls in [('upstream',Planner),('system',SystemPlanner)]:
            for name,modes in SPECS:
                p=cls(new,modes=modes)
                for row in r['rows']:
                    assert p.report(b,row['budget'])==row['policy'][obj][name],(r['q'],r['error'],obj,name,row['budget']);n+=1
        # Traverse a separate bounded set of feasible free and paid posterior histories.
        frontier={b}
        for h in range(2):
            nxt=set()
            for bb in sorted(frontier):
                for mode in range(4):
                    for _,_,bbb in old.partition(bb,mode):
                        for a in (0,1):
                            x=old.predict(bbb,a);y=new.predict(bbb,a);assert x==y;pred+=1
                            if h==0:nxt.update(b4 for _,b4 in x[1])
            frontier=nxt
    return {'stored_policy_reports':n,'per_predict_comparisons':pred}

def workload(cls,case):
    error,q,w,k,system=case
    m=cls(F(error));p=(SystemPlanner if system else Planner)(m)
    return p.report(initial(q,w),k)

def benchmark():
    cases=[('1/4',(2,2),'0001',4,False),('0',(2,0),'0011',2,False),('1/2',(2,2),'0001',4,True)]
    rng=random.Random(20261127);rows=[]
    for c in cases:
        expected=workload(ChannelModel,c); assert workload(FastChannelModel,c)==expected
        times={'baseline':[],'candidate':[]}
        for _ in range(9):
            order=[('baseline',ChannelModel),('candidate',FastChannelModel)];rng.shuffle(order)
            for name,cls in order:
                start=time.perf_counter_ns();actual=workload(cls,c);dt=(time.perf_counter_ns()-start)/1e6
                assert actual==expected;times[name].append(dt)
        med={k:statistics.median(v) for k,v in times.items()}
        rows.append({'case':c,'ms':times,'median_ms':med,'speedup':med['baseline']/med['candidate']})
    return rows
if __name__=='__main__':
    print(json.dumps({'python':sys.version,'platform':platform.platform(),'parity':parity(),'benchmark':benchmark()},indent=2))
