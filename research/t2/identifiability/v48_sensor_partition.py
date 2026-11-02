"""T2 v4.8 sensor-policy identifiability experiment; synthetic only."""
from dataclasses import dataclass
from itertools import product
from collections import defaultdict
@dataclass(frozen=True)
class World:
    storage:int
    main:int
    side:int
def simulate(w,split,horizon=50):
    q=[0,0,0];side=[0,0,0];total=0;major=0;minor=0
    for t in range(horizon):
        q[0]+=w.main
        for j in range(3):side[j]+=w.side
        if t%5<split:
            for j in (2,1,0):
                n=min(q[j],2,10**9 if j==2 else max(0,w.storage-q[j+1]))
                q[j]-=n
                if j==2:major+=n;total+=n
                else:q[j+1]+=n
        else:
            for j in range(3):
                n=min(side[j],1);side[j]-=n;minor+=n;total+=n
    return (total,major,minor,tuple(q),tuple(side))
def optima(w):
    values={g:simulate(w,g)[0] for g in (1,2,3,4)}
    return {g for g,n in values.items() if n==max(values.values())}
def sensor(w,name,baseline):
    total,major,minor,q,side=simulate(w,baseline)
    if name=="aggregate":return (total,)
    if name=="directional":return major,minor
    if name=="queues":return (major,minor,*q,*side)
    if name=="demand":return w.main,w.side
    raise ValueError(name)
def audit():
    worlds=[World(c,m,s) for c,m,s in product((2,4,8,16),(1,2,3),(0,1,2,3))]
    rows=[]
    for baseline in (3,5):
        for name in ("aggregate","directional","queues","demand"):
            groups=defaultdict(list)
            for w in worlds:groups[sensor(w,name,baseline)].append(w)
            ambiguous=sum(not set.intersection(*(optima(w) for w in group)) for group in groups.values())
            rows.append((baseline,name,len(groups),ambiguous))
    return rows
if __name__=="__main__":
    for row in audit():print(*row)
