"""Independent two-movement receiving-supply queue model, exploratory T2 v1.9.

No real intersection calibration; not a Daganzo CTM implementation.
Each movement has independent finite downstream storage and an upstream
infinite backlog. FIFO within each movement; downstream service is bounded
by a phase gate and headway. One tick: departures, admission from queue,
then exogenous arrivals. Initial queue is explicit, no hidden warmup.
"""
from dataclasses import dataclass
from collections import deque

@dataclass(frozen=True)
class ReceivingPolicy:
    capacity_S: int = 4
    capacity_L: int = 4
    headway_S: int = 3
    headway_L: int = 3
    cycle_s: int = 60
    green_S: int = 30
    green_L: int = 30
    offset_L: int = 0
    shared_receiver: bool = False
    admission_priority: str = "S_first"  # S_first | L_first | alternate

class TwoMovementLink:
    def __init__(self, policy: ReceivingPolicy, initial_S=0, initial_L=0):
        p=policy
        if any(type(v) is not int or v<0 for v in (initial_S, initial_L,p.capacity_S,p.capacity_L)):
            raise ValueError('invalid queue sizes or storage')
        if not p.capacity_S or not p.capacity_L or any(type(v) is not int or v<1 for v in
               (p.headway_S,p.headway_L,p.cycle_s)):
            raise ValueError('invalid positive headways or cell lengths')
        if any(type(v) is not int for v in (p.green_S,p.green_L,p.offset_L)) or not 0<=p.green_S<=p.cycle_s or not 0<=p.green_L<=p.cycle_s:
            raise ValueError('invalid signal phase')
        if p.admission_priority not in ('S_first','L_first','alternate'):
            raise ValueError('invalid merge priority')
        self.p=p
        self.up={'S':deque(('initial',j) for j in range(initial_S)),
                 'L':deque(('initial',j) for j in range(initial_L))}
        self.down={'S':deque(),'L':deque()}
        self.finished={'S':0,'L':0}
        self.departures=[]
        self.blocked={'S':0,'L':0}
        self.generated={'S':initial_S,'L':initial_L}
        self.last={'S':-10**9,'L':-10**9}
        self.clock=-1
    def tick(self,t,arriving_S=0,arriving_L=0):
        if type(t) is not int or t!=self.clock+1:raise ValueError('must advance sequential seconds')
        if type(arriving_S) is not int or type(arriving_L) is not int or min(arriving_S,arriving_L)<0:
            raise ValueError('invalid arrivals')
        self.clock=t
        p=self.p
        # downstream service: independent red/green receiving signals
        for m,g,offset,h in [('S',p.green_S,0,p.headway_S),('L',p.green_L,p.offset_L,p.headway_L)]:
            if self.down[m] and (t+offset)%p.cycle_s<g and t-self.last[m]>=h:
                self.down[m].popleft();self.finished[m]+=1;self.departures.append((t,m));self.last[m]=t
        # shared_receiver is a physical competition for the same *common* storage budget.
        # The separate source queues retain movement identity and deterministic S-first tie-break.
        order=('L','S') if p.admission_priority=='L_first' or (p.admission_priority=='alternate' and t%2) else ('S','L')
        for m in order:
            capacity=p.capacity_S if m=='S' else p.capacity_L
            if not self.up[m]:continue
            occupied=sum(map(len,self.down.values())) if p.shared_receiver else len(self.down[m])
            space=min(p.capacity_S,p.capacity_L) if p.shared_receiver else capacity
            if occupied<space:self.down[m].append(self.up[m].popleft())
            else:self.blocked[m]+=1
        for m,count in [('S',arriving_S),('L',arriving_L)]:
            self.up[m].extend((t,j) for j in range(count))
            self.generated[m]+=count
        self.assert_invariants()
    def assert_invariants(self):
        p=self.p
        for m in ('S','L'):
            if self.generated[m]!=self.finished[m]+len(self.up[m])+len(self.down[m]):
                raise AssertionError('vehicle mass not conserved')
            if len(self.down[m])>(p.capacity_S if m=='S' else p.capacity_L):
                raise AssertionError('receiver lane overflow')
        if p.shared_receiver and len(self.down['S'])+len(self.down['L'])>min(p.capacity_S,p.capacity_L):
            raise AssertionError('shared receiving storage overflow')
    def result(self):
        return {'generated':dict(self.generated),'completed':dict(self.finished),
                'upstream':{m:len(self.up[m]) for m in self.up},
                'downstream':{m:len(self.down[m]) for m in self.down},
                'blocked_attempts':dict(self.blocked), 'departures':list(self.departures)}
