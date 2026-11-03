"""Movement occupancy interval validation for a SYNTHETIC junction (not a road safety certificate).

Conflict is determined by the fixed v5.5 centreline-clearance graph. Any
intersection occupation overlaps [start_s,end_s) on conflicting movements.
For the SAME movement, discharge spacing is governed separately by network
headway; occupancy audit checks distinct movements and geometric incompatibility.
"""
from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Occupancy:
    junction: int
    movement: str
    start_s: float
    end_s: float
    vehicle_id: int

    def __post_init__(self):
        if self.junction not in range(3) or not self.movement or not all(math.isfinite(x) for x in (self.start_s,self.end_s)) or self.end_s<=self.start_s:
            raise ValueError('invalid junction occupancy event')

def overlap(a: Occupancy,b: Occupancy,tol=1.e-9):
    return a.start_s<b.end_s-tol and b.start_s<a.end_s-tol

def movement_conflict(graph, a: str, b: str):
    if a not in graph.paths or b not in graph.paths:
        raise ValueError('unknown lane-to-lane geometry movement')
    # Same-stream following time headways are enforced separately by the engine.
    return a!=b and not graph.compatible((a,b))

def can_enter(j: int, movement: str, start_s: float, duration_s: float, prior: list[Occupancy], graph):
    if j not in range(3) or not math.isfinite(start_s) or not math.isfinite(duration_s) or duration_s<0:
        raise ValueError('invalid admission query')
    if movement not in graph.paths:raise ValueError('unknown geometry movement')
    if duration_s==0:return True
    proposed=Occupancy(j,movement,start_s,start_s+duration_s,-1)
    return all(not (q.junction==j and movement_conflict(graph,movement,q.movement) and overlap(q,proposed)) for q in prior)

def audit(events: list[Occupancy],graph):
    """Independent interval auditor, O(E^2) per junction; returns conflicting pairs."""
    by_junction={j:[] for j in range(3)}
    for e in events:
        if e.movement not in graph.paths:raise ValueError('unknown movement')
        by_junction[e.junction].append(e)
    failures=[]
    for j,rows in by_junction.items():
        rows.sort(key=lambda e:e.start_s)
        for i,a in enumerate(rows):
            for b in rows[i+1:]:
                if b.start_s>=a.end_s-1.e-9:break
                if movement_conflict(graph,a.movement,b.movement) and overlap(a,b):
                    failures.append((a.vehicle_id,b.vehicle_id,j))
    return dict(events=len(events),conflicting_intervals=len(failures),failures=failures)
