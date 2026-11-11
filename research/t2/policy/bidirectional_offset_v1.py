"""Two-intersection, two-way synthetic signal offset experiment.

Integer-time event model. Two opposite through streams run simultaneously
during each green; service rate one vehicle per second per direction.
Infinite point queues: NOT calibrated or physically spillback-capable.
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from statistics import mean
from typing import Iterable

@dataclass(frozen=True)
class Parameters:
    cycle_s: int = 60
    green_s: int = 20
    travel_s: int = 16
    horizon_s: int = 600
    offset_B_s: int = 0
    def __post_init__(self):
        if not isinstance(self.cycle_s, int) or self.cycle_s <= 0:
            raise ValueError("invalid cycle")
        if not isinstance(self.green_s, int) or not 1 <= self.green_s <= self.cycle_s:
            raise ValueError("invalid green")
        if not isinstance(self.travel_s, int) or self.travel_s <= 0:
            raise ValueError("invalid travel")
        if not isinstance(self.horizon_s, int) or self.horizon_s <= self.travel_s:
            raise ValueError("invalid horizon")
        if not isinstance(self.offset_B_s, int) or not 0 <= self.offset_B_s < self.cycle_s:
            raise ValueError("invalid offset")

@dataclass(frozen=True)
class DirectionResult:
    arrival_count: int
    completed: int
    unserved: int
    mean_trip_s: float | None
    mean_delay_s: float | None
    max_queue_up: int
    max_queue_down: int

@dataclass(frozen=True)
class ScenarioResult:
    offset_B_s: int
    eastbound: DirectionResult
    westbound: DirectionResult
    total_completed: int
    total_unserved: int
    network_mean_trip_s: float | None
    network_mean_delay_s: float | None
    worst_direction_mean_delay_s: float | None

def green(t: int, offset: int, p: Parameters) -> bool:
    return (t - offset) % p.cycle_s < p.green_s

def _check_arrivals(arrivals: tuple[int, ...], p: Parameters):
    if any(not isinstance(t, int) or t < 0 or t >= p.horizon_s for t in arrivals):
        raise ValueError("arrival outside horizon or noninteger")
    if tuple(sorted(arrivals)) != arrivals:
        raise ValueError("arrival sequence must be sorted")

def _simulate_direction(arrivals: tuple[int, ...], start_offset: int,
                        finish_offset: int, p: Parameters) -> DirectionResult:
    waiting: deque[tuple[int, int]] = deque()
    downstream: deque[tuple[int, int]] = deque()
    due: dict[int, list[tuple[int, int]]] = {}
    next_arrival = 0
    trips: list[int] = []
    max_up = max_down = 0
    for t in range(p.horizon_s):
        while next_arrival < len(arrivals) and arrivals[next_arrival] == t:
            waiting.append((next_arrival, t))
            next_arrival += 1
        downstream.extend(due.pop(t, ()))
        max_up = max(max_up, len(waiting))
        max_down = max(max_down, len(downstream))
        if waiting and green(t, start_offset, p):
            ident, source_t = waiting.popleft()
            due.setdefault(t + p.travel_s, []).append((ident, source_t))
        if downstream and green(t, finish_offset, p):
            _, source_t = downstream.popleft()
            trips.append(t - source_t)
    unserved = len(arrivals) - len(trips)
    assert unserved == len(waiting) + len(downstream) + sum(map(len, due.values()))
    avg = mean(trips) if trips else None
    return DirectionResult(len(arrivals), len(trips), unserved, avg,
                           avg - p.travel_s if avg is not None else None,
                           max_up, max_down)

def simulate(east_arrivals: Iterable[int], west_arrivals: Iterable[int],
             p: Parameters) -> ScenarioResult:
    east, west = tuple(east_arrivals), tuple(west_arrivals)
    _check_arrivals(east, p)
    _check_arrivals(west, p)
    e = _simulate_direction(east, 0, p.offset_B_s, p)
    w = _simulate_direction(west, p.offset_B_s, 0, p)
    n = e.completed + w.completed
    total_trip = sum((d.mean_trip_s or 0) * d.completed for d in (e, w))
    delays = [d.mean_delay_s for d in (e, w) if d.mean_delay_s is not None]
    return ScenarioResult(p.offset_B_s, e, w, n, e.unserved+w.unserved,
                          total_trip/n if n else None,
                          total_trip/n-p.travel_s if n else None,
                          max(delays) if delays else None)

def platoons(cycles: int, width: int, cycle_s: int = 60,
             phase_s: int = 0) -> tuple[int, ...]:
    if cycles <= 0 or width < 0 or width > cycle_s or phase_s < 0 or phase_s+width > cycle_s:
        raise ValueError("invalid platoon specification")
    return tuple(c*cycle_s + phase_s+i for c in range(cycles) for i in range(width))

def sweep(east: Iterable[int], west: Iterable[int], base: Parameters) -> list[ScenarioResult]:
    from dataclasses import replace
    e,w=tuple(east),tuple(west)
    return [simulate(e,w,replace(base,offset_B_s=k)) for k in range(base.cycle_s)]

def efficiency_key(r: ScenarioResult) -> tuple[int,float,int]:
    return (r.total_unserved,
            r.network_mean_delay_s if r.network_mean_delay_s is not None else float("inf"),
            r.offset_B_s)

def fairness_key(r: ScenarioResult) -> tuple[int,float,float,int]:
    return (r.total_unserved,
            r.worst_direction_mean_delay_s if r.worst_direction_mean_delay_s is not None else float("inf"),
            r.network_mean_delay_s if r.network_mean_delay_s is not None else float("inf"),
            r.offset_B_s)

if __name__ == "__main__":
    p=Parameters()
    for e_width,w_width in [(12,0),(0,12),(12,12),(18,6),(6,18),(16,16)]:
        results=sweep(platoons(6,e_width),platoons(6,w_width),p)
        best=min(results,key=efficiency_key)
        fair=min(results,key=fairness_key)
        baseline=results[0]
        print(f"e={e_width} w={w_width} baseline={baseline.network_mean_delay_s:.3f} "
              f"best={best.offset_B_s}:{best.network_mean_delay_s:.3f} "
              f"fair={fair.offset_B_s}:{fair.worst_direction_mean_delay_s:.3f} "
              f"unserved={best.total_unserved}")
