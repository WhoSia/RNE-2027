from dataclasses import dataclass
@dataclass(frozen=True)
class World:
    storage:int=4
    arrivals_main:int=2
    arrivals_side:int=1
    main_service:int=2
    side_service:int=1
POLICIES=(2,3,4)
def simulate(w:World,main_green:int,horizon:int=80):
    if main_green not in POLICIES or horizon<1 or w.storage<1 or min(w.arrivals_main,w.arrivals_side)<0:raise ValueError('invalid')
    main=[0,0,0];side=[0,0,0];gen=done=blocked=lost=0;trace=[]
    for t in range(horizon):
        main[0]+=w.arrivals_main
        for j in range(3):side[j]+=w.arrivals_side
        gen+=w.arrivals_main+3*w.arrivals_side
        k=t%8
        if k<main_green:
            snapshot=main.copy();moves=[0,0,0]
            for j in (2,1,0):
                available=10**9 if j==2 else max(0,w.storage-main[j+1]-moves[j+1])
                moves[j]=min(snapshot[j],w.main_service,available)
                if j<2 and snapshot[j]>moves[j] and available==0:blocked+=1
            for j in range(3):main[j]-=moves[j]
            for j in range(2):main[j+1]+=moves[j]
            done+=moves[2]
        elif k==main_green or k==7:lost+=1
        else:
            for j in range(3):
                m=min(side[j],w.side_service);side[j]-=m;done+=m
        assert min(main+side)>=0 and max(main[1:])<=w.storage
        assert gen==done+sum(main)+sum(side)
        trace.append((t,gen,done,sum(main)+sum(side),blocked,lost))
    return dict(generated=gen,completed=done,remaining=gen-done,blocked=blocked,lost=lost,trace=trace)
def optima(w,horizon=80):
    outcomes={g:simulate(w,g,horizon)['completed'] for g in POLICIES}
    m=max(outcomes.values())
    return tuple(k for k,v in outcomes.items() if v==m),outcomes
