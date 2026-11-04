"""T2 v6.10 independent typed intersection/movement/signal schema.

No claim of physical calibration or compatibility with old P2 objectives.
All times seconds; lengths metres; half-open signal intervals.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class Lane:
    id: str
    length_m: float
    storage_m: float
    def __post_init__(self):
        if not self.id or not all(map(isfinite,(self.length_m,self.storage_m))) or not 0 < self.storage_m <= self.length_m:
            raise ValueError('invalid lane dimensions')

@dataclass(frozen=True)
class Movement:
    id: str
    junction: str
    from_lane: str
    to_lane: str
    kind: str
    clearance_s: float
    conflicts: tuple[str,...]=()
    def __post_init__(self):
        if self.kind not in ('straight','left','right','uturn') or not isfinite(self.clearance_s) or self.clearance_s <= 0:
            raise ValueError('invalid movement')
        if self.id in self.conflicts or len(set(self.conflicts))!=len(self.conflicts):
            raise ValueError('self or duplicate conflict')

@dataclass(frozen=True)
class Phase:
    duration_s: float
    allowed: frozenset[str]
    name: str=''
    def __post_init__(self):
        if not isfinite(self.duration_s) or self.duration_s<=0: raise ValueError('invalid phase duration')

@dataclass(frozen=True)
class SignalPlan:
    junction: str
    phases: tuple[Phase,...]
    offset_s: float=0.
    def __post_init__(self):
        if not self.phases or not isfinite(self.offset_s): raise ValueError('invalid signal plan')
    @property
    def cycle_s(self):return sum(p.duration_s for p in self.phases)
    def at(self,t:float):
        if not isfinite(t) or t<0:raise ValueError('invalid time')
        local=(t-self.offset_s)%self.cycle_s
        for i,phase in enumerate(self.phases):
            if local<phase.duration_s-1e-10:return i,phase,phase.duration_s-local
            local-=phase.duration_s
        return 0,self.phases[0],self.phases[0].duration_s
    def permits(self,movement_id,t,clearance_s=0.):
        _,phase,remain=self.at(t)
        return movement_id in phase.allowed and remain+1e-9>=clearance_s

@dataclass(frozen=True)
class Network:
    lanes:tuple[Lane,...]
    movements:tuple[Movement,...]
    plans:tuple[SignalPlan,...]
    def __post_init__(self):
        lid={x.id:x for x in self.lanes}; mid={x.id:x for x in self.movements};pid={x.junction:x for x in self.plans}
        if len(lid)!=len(self.lanes) or len(mid)!=len(self.movements) or len(pid)!=len(self.plans):
            raise ValueError('duplicate identifiers')
        for m in self.movements:
            if m.from_lane not in lid or m.to_lane not in lid or m.junction not in pid or m.from_lane==m.to_lane:
                raise ValueError('missing lane or junction')
            for conflict in m.conflicts:
                if conflict not in mid or m.id not in mid[conflict].conflicts or mid[conflict].junction != m.junction:
                    raise ValueError('nonreciprocal or cross-junction conflict')
        for plan in self.plans:
            for phase in plan.phases:
                for x in phase.allowed:
                    if x not in mid or mid[x].junction!=plan.junction:raise ValueError('phase references unknown movement')
                for x in phase.allowed:
                    if set(mid[x].conflicts)&phase.allowed:raise ValueError('conflicting simultaneous movements')
    def lane(self,id): return next(x for x in self.lanes if x.id==id)
    def movement(self,id):return next(x for x in self.movements if x.id==id)
    def plan(self,j):return next(x for x in self.plans if x.junction==j)
