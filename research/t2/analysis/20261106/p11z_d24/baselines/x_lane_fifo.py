"""Synthetic lane FIFO events with scoped movement conflicts.

Each demand may specify one or more conflict zones. Scalar 'global' preserves
legacy P11-W behavior. Shared zones trigger conflict only for forbidden kinds.
Zones are locked atomically for the full fixed duration: this is NOT a
trajectory-following model or an operational traffic-light controller.
"""
from dataclasses import dataclass, field
from collections import deque
from heapq import heappush, heappop
from math import isfinite

@dataclass(frozen=True)
class Demand:
    at: float
    identity: str
    lane: str
    resources: tuple[str, ...]
    duration: float
    kind: str = "vehicle"
    conflict_zone: str | tuple[str, ...] = "global"

@dataclass
class Audit:
    entries: dict[str, float] = field(default_factory=dict)
    exits: dict[str, float] = field(default_factory=dict)
    log: list[tuple[float,str,str]] = field(default_factory=list)
    max_occupation: dict[str,int] = field(default_factory=dict)
    max_waiting: dict[str,int] = field(default_factory=dict)


def simulate(demands: list[Demand], capacity: dict[str,int],
             conflicts: set[frozenset[str]] | None = None) -> Audit:
    conflicts = conflicts or set()
    if not capacity or any(type(v) is not int or v < 1 for v in capacity.values()):
        raise ValueError("positive integer capacities are required")
    ids=set()
    zones: dict[str, frozenset[str]] = {}
    for d in demands:
        if not d.identity or d.identity in ids:
            raise ValueError("duplicate/empty identity")
        ids.add(d.identity)
        if not d.lane or not d.kind or not isfinite(d.at) or d.at<0 or not isfinite(d.duration) or d.duration<=0:
            raise ValueError("invalid lane/kind/times")
        labels = (d.conflict_zone,) if isinstance(d.conflict_zone, str) else d.conflict_zone
        if not isinstance(labels, tuple) or not labels or any(not isinstance(z, str) or not z for z in labels) or len(set(labels)) != len(labels):
            raise ValueError("zone must be a nonempty string or tuple of unique nonempty strings")
        zones[d.identity] = frozenset(labels)
        if not d.resources or len(set(d.resources)) != len(d.resources) or any(x not in capacity for x in d.resources):
            raise ValueError("unknown/duplicate/empty resources")
    events=[]
    for i,d in enumerate(demands): heappush(events,(d.at, 1, i, "arrival", d))
    queues: dict[str,deque[Demand]]={}
    occupiers={k:set() for k in capacity}
    active: dict[str,Demand]={}
    out=Audit(max_occupation={k:0 for k in capacity})
    seq=len(events)
    previous=-float('inf')

    def eligible(d: Demand) -> bool:
        return all(len(occupiers[x]) < capacity[x] for x in d.resources) and all(
            not (zones[d.identity] & zones[a.identity]) or
            frozenset((d.kind, a.kind)) not in conflicts for a in active.values())

    def grant(d: Demand,t:float) -> None:
        nonlocal seq
        assert t >= d.at and d.identity not in active
        # Check time validity before mutating occupancy so failed calls do not
        # partially modify audit state (the failure is still terminal).
        end=t+d.duration
        if not isfinite(end) or end<=t:
            raise ValueError("exit time is not representable after entry; rescale clock or use integer time ticks")
        active[d.identity]=d
        for r in d.resources:
            occupiers[r].add(d.identity)
            out.max_occupation[r]=max(out.max_occupation[r], len(occupiers[r]))
        out.entries[d.identity]=t
        out.log.append((t,'enter',d.identity))
        seq+=1
        heappush(events,(end,0,seq,'exit',d))

    while events:
        t=events[0][0]
        assert t>=previous
        previous=t
        batch=[]
        while events and events[0][0]==t:batch.append(heappop(events))
        for _,_,_,action,d in batch:
            if action=='exit':
                assert d.identity in active
                for r in d.resources: occupiers[r].remove(d.identity)
                del active[d.identity]
                out.exits[d.identity]=t
                out.log.append((t,'exit',d.identity))
        for _,_,_,action,d in batch:
            if action=='arrival':
                queues.setdefault(d.lane,deque()).append(d)
        while True:
            heads=sorted((q[0] for q in queues.values() if q),key=lambda d:(d.at,d.identity,d.lane))
            chosen=next((d for d in heads if eligible(d)),None)
            if chosen is None: break
            assert queues[chosen.lane].popleft() == chosen
            grant(chosen,t)
        for lane,queue in queues.items():
            out.max_waiting[lane]=max(out.max_waiting.get(lane,0),len(queue))
        for r,inside in occupiers.items(): assert len(inside)<=capacity[r]
        assert all(d.identity in out.entries for d in active.values())
    assert set(out.entries)==ids==set(out.exits)
    assert all(not q for q in queues.values())
    return out
