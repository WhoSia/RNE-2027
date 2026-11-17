"""D50: approach divergence with a finite protected-left pocket.

Synthetic, integer-second, *point-queue* network, not physical car-following.
Compare (a) one FIFO shared feeder feeding distinct finite through and left
storage bays, with (b) two independent feeders. Source vehicles arrive with
IDs and movement labels, preserving the same external input across scenarios.

One crossing per second per movement phase; admissions use storage occupancy
at the beginning of the tick, so downstream discharge does not create an
immediately usable space in the same tick. This choice is explicit and testable.
"""
from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from statistics import mean
from typing import Iterable

@dataclass(frozen=True)
class Vehicle:
    arrival_s: int
    movement: str
    ident: int

@dataclass(frozen=True)
class Config:
    cycle_s: int = 60
    through_green_s: int = 24
    left_green_s: int = 12
    horizon_s: int = 600
    through_capacity: int = 12
    left_capacity: int = 4
    mode: str = "shared"
    def __post_init__(self):
        scalars = (self.cycle_s, self.through_green_s, self.left_green_s,
                   self.horizon_s, self.through_capacity, self.left_capacity)
        if any(type(v) is not int for v in scalars):
            raise ValueError("integer times and capacities required")
        if not 0 < self.through_green_s or not 0 < self.left_green_s:
            raise ValueError("both movement greens must be positive")
        if self.through_green_s + self.left_green_s > self.cycle_s:
            raise ValueError("movement greens exceed cycle")
        if self.horizon_s <= 0 or self.through_capacity < 1 or self.left_capacity < 1:
            raise ValueError("invalid horizon/storage")
        if self.mode not in ("shared", "independent"):
            raise ValueError("mode must be shared or independent")

@dataclass(frozen=True)
class Result:
    mode: str
    left_capacity: int
    total_arrivals: int
    arrivals_through: int
    arrivals_left: int
    completed_through: int
    completed_left: int
    unserved_through: int
    unserved_left: int
    mean_through_delay_s: float | None
    mean_left_delay_s: float | None
    worst_through_delay_s: int | None
    maximum_source_queue: int
    maximum_left_pocket: int
    maximum_through_bay: int
    blocked_left_head_seconds: int
    blocked_through_head_seconds: int
    blocked_through_behind_left_seconds: int


def validate_vehicles(vehicles: tuple[Vehicle, ...], cfg: Config) -> None:
    if any(type(v.arrival_s) is not int or not (0 <= v.arrival_s < cfg.horizon_s)
           or type(v.ident) is not int or v.movement not in ("T", "L")
           for v in vehicles):
        raise ValueError("invalid external vehicle")
    if tuple(v.arrival_s for v in vehicles) != tuple(sorted(v.arrival_s for v in vehicles)):
        raise ValueError("vehicles must be ordered by arrival time")
    if len(set(v.ident for v in vehicles)) != len(vehicles):
        raise ValueError("vehicle identifiers must be unique")


def simulate(vehicles: Iterable[Vehicle], cfg: Config = Config()) -> Result:
    xs = tuple(vehicles)
    validate_vehicles(xs, cfg)
    source_shared = deque()
    source_t = deque()
    source_l = deque()
    bay_t = deque()
    pocket_l = deque()
    finished_t, finished_l = [], []
    index = max_source = max_t = max_l = 0
    blocked_l = blocked_t = trapped_t = 0
    expected_t = sum(v.movement == "T" for v in xs)
    expected_l = len(xs) - expected_t

    for second in range(cfg.horizon_s):
        while index < len(xs) and xs[index].arrival_s == second:
            v = xs[index]
            if cfg.mode == "shared":
                source_shared.append(v)
            elif v.movement == "T":
                source_t.append(v)
            else:
                source_l.append(v)
            index += 1
        pre_t, pre_l = len(bay_t), len(pocket_l)
        phase = second % cfg.cycle_s
        if phase < cfg.through_green_s and bay_t:
            v = bay_t.popleft()
            finished_t.append(second - v.arrival_s)
        if cfg.through_green_s <= phase < cfg.through_green_s + cfg.left_green_s and pocket_l:
            v = pocket_l.popleft()
            finished_l.append(second - v.arrival_s)

        if cfg.mode == "shared":
            if source_shared:
                v = source_shared[0]
                if v.movement == "L":
                    if pre_l < cfg.left_capacity:
                        pocket_l.append(source_shared.popleft())
                    else:
                        blocked_l += 1
                        # A through vehicle trapped behind the leading left-turner
                        # in the common feeder cannot enter its own through bay.
                        if any(x.movement == "T" for x in source_shared):
                            trapped_t += 1
                elif pre_t < cfg.through_capacity:
                    bay_t.append(source_shared.popleft())
                else:
                    blocked_t += 1
        else:
            if source_l:
                if pre_l < cfg.left_capacity:
                    pocket_l.append(source_l.popleft())
                else:
                    blocked_l += 1
            if source_t:
                if pre_t < cfg.through_capacity:
                    bay_t.append(source_t.popleft())
                else:
                    blocked_t += 1
        sources = (source_shared, source_t, source_l)
        max_source = max(max_source, sum(map(len, sources)))
        max_t = max(max_t, len(bay_t))
        max_l = max(max_l, len(pocket_l))
        assert len(bay_t) <= cfg.through_capacity and len(pocket_l) <= cfg.left_capacity
        assert index == (sum(map(len, sources)) + len(bay_t) + len(pocket_l)
                         + len(finished_t) + len(finished_l)), "vehicle conservation"
    unserved_t = expected_t - len(finished_t)
    unserved_l = expected_l - len(finished_l)
    assert unserved_t + unserved_l == sum(map(len,(source_shared,source_t,source_l,bay_t,pocket_l)))
    return Result(cfg.mode,cfg.left_capacity,len(xs),expected_t,expected_l,
                  len(finished_t),len(finished_l),unserved_t,unserved_l,
                  mean(finished_t) if finished_t else None,
                  mean(finished_l) if finished_l else None,
                  max(finished_t) if finished_t else None,
                  max_source,max_l,max_t,blocked_l,blocked_t,trapped_t)


def periodic_arrivals(ncycles: int = 6, per_cycle: int = 18,
                      left_every: int = 3, cycle_s: int = 60,
                      phase_s: int = 0) -> tuple[Vehicle, ...]:
    """One new vehicle/second, left for positions divisible by left_every."""
    if (not all(type(x) is int for x in (ncycles,per_cycle,left_every,cycle_s,phase_s))
        or ncycles < 1 or per_cycle < 1 or left_every < 1 or phase_s < 0
        or phase_s + per_cycle > cycle_s):
        raise ValueError("invalid periodic demand")
    return tuple(Vehicle(k * cycle_s + phase_s + j,
                         "L" if j % left_every == 0 else "T", k*per_cycle+j)
                 for k in range(ncycles) for j in range(per_cycle))


def sweep(vehicles: Iterable[Vehicle], capacities=(1,2,3,4,6,8,12,20),
          cfg: Config = Config()) -> list[Result]:
    from dataclasses import replace
    xs=tuple(vehicles)
    return [simulate(xs, replace(cfg,left_capacity=cap,mode=mode))
            for cap in capacities for mode in ("shared","independent")]

if __name__ == "__main__":
    for cap in (1,2,3,4,6,8,12,20):
        r=sweep(periodic_arrivals(),capacities=(cap,))
        for x in r:
            print(cap,x.mode,'T',x.completed_through,'L',x.completed_left,
                  'T_delay',x.mean_through_delay_s,
                  'blocked_behind_L',x.blocked_through_behind_left_seconds)
