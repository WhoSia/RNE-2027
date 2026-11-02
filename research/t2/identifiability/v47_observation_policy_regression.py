"""T2 v4.7 historical observation-policy regression. Synthetic model, not field validation."""
from dataclasses import dataclass
from itertools import product
@dataclass(frozen=True)
class World:
    capacity:int
    main:int
    side:int
def run(w,split,cycle=5,lost=0,snapshot=False,horizon=50):
    if not 0<=split<=cycle-lost:raise ValueError("split")
    q=[0,0,0];side=[0,0,0];created=completed=0
    for t in range(horizon):
        q[0]+=w.main
        for i in range(3):side[i]+=w.side
        created+=w.main+3*w.side
        phase=t%cycle
        if phase<split:
            before=q.copy()
            for i in (2,1,0):
                capacity=10**9 if i==2 else max(0,w.capacity-q[i+1])
                n=min((before if snapshot else q)[i],2,capacity)
                q[i]-=n
                if i==2:completed+=n
                else:q[i+1]+=n
        elif phase<cycle-lost:
            for i in range(3):
                n=min(side[i],1);side[i]-=n;completed+=n
        assert created==completed+sum(q)+sum(side)
        assert 0<=q[1]<=w.capacity and 0<=q[2]<=w.capacity
    return completed
def witness_count(cycle=5,lost=0,snapshot=False,min_green=0,baseline=None):
    splits=[i for i in range(cycle-lost) if i>=min_green and cycle-lost-i>=min_green]
    if baseline is None:baseline=cycle-lost
    count=0
    for capacity,main in product((2,4,8,16),(1,2,3)):
        a,b=World(capacity,main,0),World(capacity,main,2)
        if run(a,baseline,cycle,lost,snapshot)!=run(b,baseline,cycle,lost,snapshot):continue
        outcomes=[{g:run(w,g,cycle,lost,snapshot) for g in splits} for w in (a,b)]
        sets=[{k for k,v in d.items() if v==max(d.values())} for d in outcomes]
        count+=sets[0].isdisjoint(sets[1])
    return count
if __name__=="__main__":
    for name,kwargs in (("historical",{}),("baseline_3",{"baseline":3}),("snapshot",{"snapshot":True}),("min_green_1",{"min_green":1}),("lost_1",{"lost":1}),("cycle_8",{"cycle":8}),("cycle8_baseline3",{"cycle":8,"baseline":3})):
        print(name,witness_count(**kwargs))
