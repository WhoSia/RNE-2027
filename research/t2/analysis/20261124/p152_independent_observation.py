"""P152: independent Python replay of P151, exploratory info ablation.
Same frozen six-vehicle cohort; not a new holdout or a field model.
"""
import itertools
import json
from collections import defaultdict, deque


def advance(q,p,d,exit_count,t,period,reuse,P,D,arrival):
    # Simultaneous old-state eligibility, then apply disjoint movements.
    green='S' if t%period<period//2 else 'L'
    release=bool(d) and t%4<2
    supply=D-len(d)+int(release and reuse)
    admit=bool(q) and q[0]=='L' and len(p)<P
    straight=bool(q) and q[0]=='S' and green=='S' and supply>0
    left=bool(p) and green=='L' and supply>0
    assert not (straight and left) and not (admit and straight)
    if release:
        d.popleft();exit_count+=1
    if straight:d.append(q.popleft())
    if left:d.append(p.popleft())
    if admit:p.append(q.popleft())
    if arrival is not None:q.append(arrival)
    assert len(p)<=P and len(d)<=D
    return exit_count


def cohort():
    for mask,interval,P,D in itertools.product(range(64),(1,2),(1,2),(1,2)):
        tape={interval*i:('L' if mask&(1<<i) else 'S') for i in range(6)}
        q,p,d=deque(),deque(),deque();z=0;cost=0
        for t in range(8):
            z=advance(q,p,d,z,t,4,False,P,D,tape.get(t));cost+=len(q)+len(p)+len(d)
            assert z+len(q)+len(p)+len(d)==sum(k<=t for k in tape)
        state=(tuple(q),len(p),len(d));future=tuple((t,l) for t,l in tape.items() if t>=8)
        costs={}
        for reuse,period in itertools.product((False,True),(4,8)):
            a,b,c=deque(q),deque(p),deque(d);out=z;total=cost
            for t in range(8,120):
                out=advance(a,b,c,out,t,period,reuse,P,D,tape.get(t));total+=len(a)+len(b)+len(c)
                assert out+len(a)+len(b)+len(c)==sum(k<=t for k in tape)
            assert out==6 and not(a or b or c)
            costs[reuse,period]=total
        yield (P,D,interval),state,future,costs


def score(worlds,feature):
    groups=defaultdict(list)
    for context,state,future,reuse,delta in worlds:
        groups[context+feature(state,future,reuse)].append(delta)
    worst=0;minimax_sum=0;mean_opt_sum=0;conflict=0
    for ds in groups.values():
        loss4=[max(0,x) for x in ds];loss8=[max(0,-x) for x in ds]
        a,b=max(loss4),max(loss8)
        worst=max(worst,min(a,b));conflict+=len(ds) if a and b else 0
        minimax_sum+=sum(loss4) if a<=b else sum(loss8)
        mean_opt_sum+=min(sum(loss4),sum(loss8))
    return dict(cells=len(groups),ambiguous_worlds=conflict,max_minimax_regret=worst,
                uniform_mean_minimax=minimax_sum/len(worlds),uniform_mean_optimal=mean_opt_sum/len(worlds))


def run():
    rows=list(cohort());worlds=[];decreased=tied=increased=reversed_count=tie_resolved=0
    for context,state,future,costs in rows:
        for period in (4,8):
            diff=costs[True,period]-costs[False,period]
            decreased+=diff<0;tied+=diff==0;increased+=diff>0
        a=costs[False,4]-costs[False,8];b=costs[True,4]-costs[True,8]
        reversed_count+=a*b<0;tie_resolved+=a==0 and b!=0
        for r,delta in ((False,a),(True,b)):worlds.append((context,state,future,r,delta))
    specs={
        'context':lambda s,f,r:(),
        'aggregate':lambda s,f,r:(len(s[0])+s[1]+s[2],),
        'separate_counts':lambda s,f,r:(len(s[0]),s[1],s[2]),
        'ordered_fifo':lambda s,f,r:s,
        'ordered_plus_rule':lambda s,f,r:s+(r,),
        'ordered_plus_future':lambda s,f,r:s+(f,),
        'oracle_both':lambda s,f,r:s+(f,r),
    }
    scores={k:score(worlds,v) for k,v in specs.items()}
    assert (decreased,tied,increased,reversed_count,tie_resolved)==(454,570,0,14,52)
    assert scores['ordered_fifo']['uniform_mean_minimax']==0.208984375
    assert scores['separate_counts']['uniform_mean_minimax']==0.662109375
    assert scores['oracle_both']['max_minimax_regret']==0
    return dict(status='SAME_COHORT_EXPLORATORY_PYTHON_REPLAY',unique_scenarios=len(rows),arms=4*len(rows),worlds=len(worlds),
                dominance=[decreased,tied,increased],strict_reversals=reversed_count,ties_resolved=tie_resolved,observations=scores)

if __name__=='__main__':print(json.dumps(run(),indent=2))
