from dataclasses import dataclass
@dataclass(frozen=True)
class World:
    storage:int=8
    main_service:int=2
    side_service:int=1
    arrivals_main:int=2
    arrivals_side:int=1

def simulate(w:World, split:int, horizon:int=24):
    if not 0<=split<=5 or horizon<1 or w.storage<1:raise ValueError("invalid")
    main=[0,0,0];side=[0,0,0];done=0;gen=0;blocked=0
    traces=[]
    for t in range(horizon):
        main[0]+=w.arrivals_main
        for j in range(3):side[j]+=w.arrivals_side
        gen+=w.arrivals_main+3*w.arrivals_side
        if t%5<split:
            for j in (2,1,0):
                supply=(10**10 if j==2 else w.storage-main[j+1])
                quantity=min(main[j],w.main_service,supply)
                if j<2:main[j+1]+=quantity
                else:done+=quantity
                main[j]-=quantity
                if quantity<min(main[j]+quantity,w.main_service) and supply==0:blocked+=1
        else:
            for j in range(3):
                quantity=min(side[j],w.side_service)
                side[j]-=quantity;done+=quantity
        remaining=sum(main)+sum(side)
        assert main[1]<=w.storage and main[2]<=w.storage
        assert gen==done+remaining
        traces.append((t,gen,done,remaining,blocked))
    return {'generated':gen,'completed':done,'remaining':gen-done,'blocked_events':blocked,'trace':traces}

def optimum(w,horizon=50):
    outcomes={g:simulate(w,g,horizon)['completed'] for g in range(6)}
    best=max(outcomes.values())
    return [g for g,v in outcomes.items() if v==best],outcomes
