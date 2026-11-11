"""Exploratory two-intersection offset comparison (not a field calibrated model).

Deterministic, point-queue, single-direction corridor. One vehicle per second can
cross each intersection while green. All times are integer seconds. Vehicles
travel between signals for a constant number of seconds. Infinite queue storage,
no turns, pedestrian phases, actuated control or spillback.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from statistics import mean


@dataclass(frozen=True)
class Config:
    cycle_s: int = 60
    green_s: int = 20
    travel_s: int = 16
    horizon_s: int = 600
    downstream_offset_s: int = 0

    def __post_init__(self) -> None:
        if not (1 <= self.green_s <= self.cycle_s):
            raise ValueError("green_s must be in [1, cycle_s]")
        if self.travel_s < 1 or self.horizon_s <= self.travel_s:
            raise ValueError("travel_s and horizon_s must be positive")
        if not 0 <= self.downstream_offset_s < self.cycle_s:
            raise ValueError("offset must be in [0, cycle_s)")


@dataclass(frozen=True)
class Result:
    offset_s: int
    arrivals: int
    completed: int
    unserved: int
    mean_trip_s: float | None
    mean_queue_delay_s: float | None
    max_upstream_queue: int
    max_downstream_queue: int


def is_green(t: int, offset: int, cycle: int, green: int) -> bool:
    return ((t - offset) % cycle) < green


def simulate(arrivals_s: tuple[int, ...], cfg: Config) -> Result:
    """Return per-trip metrics; arrivals outside observation horizon are invalid."""
    if tuple(sorted(arrivals_s)) != arrivals_s:
        raise ValueError("arrivals_s must be sorted")
    if any(t < 0 or t >= cfg.horizon_s for t in arrivals_s):
        raise ValueError("all arrivals must be within the horizon")

    upstream: deque[tuple[int, int]] = deque()  # (vehicle id, source time)
    downstream: deque[tuple[int, int, int]] = deque()  # (id, source, arrival downstream)
    pending: dict[int, list[tuple[int, int]]] = {}
    trip_times: list[int] = []
    queue_delays: list[int] = []
    maximum_u = maximum_d = 0
    next_arrival = 0

    for t in range(cfg.horizon_s):
        # External arrivals are first admitted to the upstream queue.
        while next_arrival < len(arrivals_s) and arrivals_s[next_arrival] == t:
            upstream.append((next_arrival, t))
            next_arrival += 1
        for ident, source_t in pending.pop(t, []):
            downstream.append((ident, source_t, t))

        maximum_u = max(maximum_u, len(upstream))
        maximum_d = max(maximum_d, len(downstream))

        if upstream and is_green(t, 0, cfg.cycle_s, cfg.green_s):
            ident, source_t = upstream.popleft()
            arrival_t = t + cfg.travel_s
            pending.setdefault(arrival_t, []).append((ident, source_t))
            queue_delays.append(t - source_t)

        if downstream and is_green(t, cfg.downstream_offset_s, cfg.cycle_s, cfg.green_s):
            _, source_t, arrival_downstream_t = downstream.popleft()
            trip_times.append(t - source_t)
            queue_delays.append(t - arrival_downstream_t)

    completed = len(trip_times)
    unserved = len(arrivals_s) - completed
    assert unserved == len(upstream) + len(downstream) + sum(map(len, pending.values()))
    return Result(
        offset_s=cfg.downstream_offset_s,
        arrivals=len(arrivals_s),
        completed=completed,
        unserved=unserved,
        mean_trip_s=mean(trip_times) if trip_times else None,
        # This queue delay includes upstream service of even unfinished trips.
        mean_queue_delay_s=sum(queue_delays) / completed if completed and not unserved else None,
        max_upstream_queue=maximum_u,
        max_downstream_queue=maximum_d,
    )


def periodic_platoons(cycles: int = 6, cycle_s: int = 60, width_s: int = 12) -> tuple[int, ...]:
    if cycles < 1 or not (1 <= width_s <= cycle_s):
        raise ValueError("invalid platoon parameters")
    return tuple(c * cycle_s + i for c in range(cycles) for i in range(width_s))


def offset_sweep(arrivals_s: tuple[int, ...], cfg: Config) -> list[Result]:
    from dataclasses import replace
    return [simulate(arrivals_s, replace(cfg, downstream_offset_s=o)) for o in range(cfg.cycle_s)]


def rank_key(result: Result) -> tuple[int, float, int]:
    # Unserved first; never silently optimize travel time by omitting delayed trips.
    return (result.unserved, result.mean_trip_s if result.mean_trip_s is not None else float("inf"), result.offset_s)


if __name__ == "__main__":
    arrivals = periodic_platoons()
    results = offset_sweep(arrivals, Config())
    baseline = results[0]
    best = min(results, key=rank_key)
    print("SYNTHETIC, uncalibrated point queues; not field evidence")
    print("baseline:", baseline)
    print("best:", best)
