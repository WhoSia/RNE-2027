"""Finite-storage, discrete-time model of a protected-stage intersection.

All rates are service opportunities, measured in whole ticks. Movement IDs
are ET, EL, WT, WL, NT and ST, followed by a separate crossing stream (P).
"""
from bisect import bisect_left
from collections import deque
from dataclasses import dataclass
from functools import lru_cache

MOVES = ("ET", "EL", "WT", "WL", "NT", "ST", "P")
STAGES = ((0, 2), (1, 3), (4, 5), (6,))
APPROACH = (0, 0, 1, 1, 2, 3)


@dataclass(frozen=True, order=True)
class Plan:
    greens: tuple
    left_first: bool
    offset: int
    clearance: int = 3
    startup: int = 1

    @property
    def cycle(self):
        return sum(self.greens) + 4 * self.clearance

    def __post_init__(self):
        if (len(self.greens) != 4 or min(self.greens) <= self.startup
                or self.startup < 0 or self.clearance < 1 or not 0 <= self.offset < self.cycle):
            raise ValueError("invalid protected plan")


@dataclass(frozen=True)
class Scenario:
    name: str
    horizon: int
    arrivals: tuple
    bay: tuple = (8, 3, 8, 3, 10, 10)
    link: tuple = (6, 3, 6, 3, 6, 6)
    receive_cycle: int = 36
    receive_green: int = 23
    receive_offset: int = 0
    terminal: int = 60
    headway: tuple = (2, 2, 2, 2, 2, 2, 1)
    weights: tuple = (1, 1, 1, 1, 1, 1, 1)
    travel: tuple = (1, 1, 1, 1, 1, 1)

    def __post_init__(self):
        if (self.horizon < 1 or self.terminal < 0 or len(self.bay) != 6
                or len(self.link) != 6 or len(self.headway) != 7 or len(self.weights) != 7
                or len(self.travel) != 6 or any(type(v) is not int or v < 1 for v in self.travel)
                or min(*self.bay, *self.link, *self.headway, *self.weights) < 1
                or not 1 <= self.receive_green <= self.receive_cycle):
            raise ValueError("invalid scenario parameters")
        if tuple(sorted(self.arrivals, key=lambda row: row[0])) != self.arrivals or any(
                not (0 <= t < self.horizon and 0 <= m < 7) for t, m in self.arrivals):
            raise ValueError("arrivals must be time-ordered and inside the horizon")


@dataclass(frozen=True)
class Outcome:
    cost: int
    area: int
    completed: tuple
    remaining: tuple
    peak_link: tuple
    ticks: int


@lru_cache(maxsize=32768)
def calendar(plan, headway):
    order = (1, 0, 2, 3) if plan.left_first else (0, 1, 2, 3)
    service = [[] for _ in MOVES]
    start = 0
    for i in order:
        for m in STAGES[i]:
            service[m] = sorted((t + plan.offset) % plan.cycle for t in
                                range(start + plan.startup, start + plan.greens[i], headway[m]))
        start += plan.greens[i] + plan.clearance
    return tuple(tuple(s) for s in service)


def opportunity(t, cycle, slots):
    current_cycle, position = divmod(t, cycle)
    index = bisect_left(slots, position)
    if index == len(slots):
        return (current_cycle + 1) * cycle + slots[0]
    return current_cycle * cycle + slots[index]


@lru_cache(maxsize=32768)
def masks(cycle, opportunities):
    active = [[] for _ in range(cycle)]
    for m, opportunities_m in enumerate(opportunities):
        for t in opportunities_m:
            active[t].append(m)
    return tuple(tuple(x) for x in active)


@lru_cache(maxsize=128)
def receiving(cycle, green, offset):
    return tuple(tuple(sorted((t + offset + 3 * m) % cycle
                              for t in range(0, green, 2))) for m in range(6))


def run(plan, s, fast=False, limit=None, *, controller=None, observe=None):
    """Return None once queue area strictly exceeds a supplied cost limit."""
    if fast and (controller is not None or observe is not None):
        raise ValueError("a per-tick controller or observer requires tick mode")
    cycle = plan.cycle
    receive_cycle = s.receive_cycle
    service = calendar(plan, s.headway)
    receive = receiving(receive_cycle, s.receive_green, s.receive_offset)
    service_now = masks(cycle, service)
    receive_now = masks(receive_cycle, receive)
    source = [deque() for _ in range(4)]
    bay = [0] * 6
    link = [0] * 6
    release = None if s.travel == (1,) * 6 else [deque() for _ in range(6)]
    peak = [0] * 6
    active = [0] * 7
    completed = [0] * 7
    area = ped = i = t = visited = weight = 0
    demand = s.arrivals
    while t < s.horizon:
        if fast:
            upcoming = [demand[i][0] if i < len(demand) else s.horizon]
            if any(q and bay[q[0]] < s.bay[q[0]] for q in source):
                upcoming.append(t)
            if ped:
                upcoming.append(opportunity(t, cycle, service[6]))
            for m in range(6):
                if link[m]:
                    ready = t if release is None else max(t, release[m][0])
                    upcoming.append(opportunity(ready, receive_cycle, receive[m]))
                if bay[m] and link[m] < s.link[m]:
                    upcoming.append(opportunity(t, cycle, service[m]))
            next_t = min(upcoming)
            area += (next_t - t) * weight
            if limit is not None and area > limit:
                return None
            t = next_t
            if t == s.horizon:
                break
        visited += 1
        permitted = (service_now[t % cycle] if controller is None
                     else controller(t, tuple(bay), tuple(link), ped))
        first_arrival = i
        while i < len(demand) and demand[i][0] == t:
            m = demand[i][1]
            active[m] += 1
            weight += s.weights[m]
            if m == 6:
                ped += 1
            else:
                source[APPROACH[m]].append(m)
            i += 1
        pre_bay = tuple(bay)
        entry = tuple(m for m in permitted if m < 6 and bay[m] and link[m] < s.link[m])
        exit_now = tuple(m for m in receive_now[t % receive_cycle]
                         if link[m] and (release is None or release[m][0] <= t))
        if observe is not None:
            observe(t, demand[first_arrival:i], tuple(source), tuple(bay), tuple(link), ped,
                    permitted, entry, exit_now)
        for m in exit_now:
            if release is not None:
                release[m].popleft()
            link[m] -= 1
            completed[m] += 1
            active[m] -= 1
            weight -= s.weights[m]
        for m in entry:
            bay[m] -= 1
            link[m] += 1
            if release is not None:
                release[m].append(t + s.travel[m])
            peak[m] = max(peak[m], link[m])
        for q in source:
            if q and pre_bay[q[0]] < s.bay[q[0]]:
                bay[q.popleft()] += 1
        if ped and 6 in permitted:
            ped -= 1
            completed[6] += 1
            active[6] -= 1
            weight -= s.weights[6]
        area += weight
        if limit is not None and area > limit:
            return None
        t += 1
    remaining_weight = weight
    counts = [0] * 7
    for _, m in demand:
        counts[m] += 1
    assert tuple(a + b for a, b in zip(active, completed)) == tuple(counts)
    assert remaining_weight == sum(a*w for a,w in zip(active,s.weights))
    assert sum(active) == sum(map(len, source)) + sum(bay) + sum(link) + ped
    return Outcome(area + s.terminal * remaining_weight, area, tuple(completed),
                   tuple(active), tuple(peak), visited)


@lru_cache(maxsize=128)
def by_movement(s):
    arrivals = [[] for _ in MOVES]
    for t, m in s.arrivals:
        arrivals[m].append(t)
    return tuple(tuple(a) for a in arrivals)


@lru_cache(maxsize=65536)
def relaxed_cost(s, m, cycle, service, arrivals):
    """Earliest completion when each movement has an unlimited private bay/link."""
    receive = receiving(s.receive_cycle, s.receive_green, s.receive_offset)
    next_entry = next_exit = cost = 0
    for t in arrivals:
        entry = opportunity(max(next_entry, t + (m < 6)), cycle, service)
        next_entry = entry + 1
        if m < 6:
            out = opportunity(max(next_exit, entry + s.travel[m]), s.receive_cycle, receive[m])
            next_exit = out + 1
        else:
            out = entry
        cost += min(out, s.horizon) - t
        if out >= s.horizon:
            cost += s.terminal
    return cost * s.weights[m]


def lower_cost(plan, s):
    service = calendar(plan, s.headway)
    return sum(relaxed_cost(s, m, plan.cycle, service[m], arrivals)
               for m, arrivals in enumerate(by_movement(s)) if arrivals)
