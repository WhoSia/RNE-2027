"""Research reference: finite-capacity time-ordered resource occupancy.

Uses integer ticks, hold-and-wait, atomic multi-zone handoff, and immutable
capacity limits. NOT a microscopic trajectory simulator or traffic controller.
"""
from collections import defaultdict
from dataclasses import dataclass, field
from heapq import heappop, heappush


@dataclass(frozen=True)
class Step:
    zones: tuple[str, ...]
    ticks: int


@dataclass(frozen=True)
class Movement:
    identity: str
    arrival: int
    lane: str
    kind: str
    steps: tuple[Step, ...]


class DeadlockError(RuntimeError):
    def __init__(self, blocked: dict, cycle: tuple[str, ...] = ()):
        self.blocked = blocked
        self.cycle = cycle
        super().__init__(f"blocked movements: {blocked}; cycle: {cycle}")


@dataclass(frozen=True)
class StorageGeometry:
    # Model-only 1D packing bound, NOT measured real driving headway.
    zone_lengths_mm: dict[str, int]
    vehicle_lengths_mm: dict[str, int]
    gap_mm: int = 0


@dataclass
class Result:
    starts: dict[str, int] = field(default_factory=dict)
    finishes: dict[str, int] = field(default_factory=dict)
    log: list[tuple[int, str, str, tuple[str, ...]]] = field(default_factory=list)
    max_occupancy: dict[str, int] = field(default_factory=dict)
    max_waiting: dict[str, int] = field(default_factory=dict)
    deadlock: dict | None = None


def _check(movements, capacity):
    if not capacity or any(not isinstance(k, str) or not k or type(v) is not int or v < 1 for k, v in capacity.items()):
        raise ValueError("capacities must have nonempty names and positive integers")
    ids = set()
    for m in movements:
        if not m.identity or m.identity in ids or type(m.arrival) is not int or m.arrival < 0 or not m.lane or not m.kind or not m.steps:
            raise ValueError("invalid movement")
        ids.add(m.identity)
        for s in m.steps:
            if type(s.ticks) is not int or s.ticks <= 0 or not s.zones or len(set(s.zones)) != len(s.zones) or any(z not in capacity for z in s.zones):
                raise ValueError("invalid step")


def _cycle(edges):
    color, stack = {}, []
    def visit(u):
        color[u] = 1
        stack.append(u)
        for v in sorted(edges.get(u, ())):
            if color.get(v) == 1:
                return tuple(stack[stack.index(v):] + [v])
            if not color.get(v):
                out = visit(v)
                if out:
                    return out
        stack.pop()
        color[u] = 2
        return ()
    for node in sorted(edges):
        if not color.get(node):
            result = visit(node)
            if result:
                return result
    return ()


def simulate(movements: list[Movement], capacity: dict[str, int], *, raise_deadlock=True, storage: StorageGeometry | None = None) -> Result:
    _check(movements, capacity)
    if storage is not None:
        if type(storage.gap_mm) is not int or storage.gap_mm < 0:
            raise ValueError('gap must be a nonnegative integer millimetre value')
        if set(storage.zone_lengths_mm) != set(capacity):
            raise ValueError('every zone needs exactly one physical length')
        if set(storage.vehicle_lengths_mm) != {m.identity for m in movements}:
            raise ValueError('every movement needs exactly one vehicle length')
        if any(type(x) is not int or x <= 0 for x in storage.zone_lengths_mm.values()):
            raise ValueError('zone lengths must be positive integer millimetres')
        if any(type(x) is not int or x <= 0 for x in storage.vehicle_lengths_mm.values()):
            raise ValueError('vehicle lengths must be positive integer millimetres')
        for m in movements:
            if any(storage.vehicle_lengths_mm[m.identity] > storage.zone_lengths_mm[z]
                   for step in m.steps for z in step.zones):
                raise ValueError('vehicle does not fit a requested zone')
    people = {m.identity: m for m in movements}
    owner = {z: set() for z in capacity}
    state = {m.identity: {"step": -1, "ready": False, "arrived": False} for m in movements}
    queues = defaultdict(list)
    result = Result(max_occupancy={z: 0 for z in capacity})
    heap = []
    seq = 0
    for m in movements:
        seq += 1
        heappush(heap, (m.arrival, 1, seq, m.identity))

    def zones(mid):
        ix = state[mid]["step"]
        return people[mid].steps[ix].zones if ix >= 0 else ()

    def next_zones(mid):
        return people[mid].steps[state[mid]["step"] + 1].zones

    def physical_room(zone, mid):
        if storage is None:
            return True
        inside = owner[zone] - {mid}
        occupied_mm = sum(storage.vehicle_lengths_mm[x] for x in inside)
        occupied_mm += max(0, len(inside) - 1) * storage.gap_mm
        required_mm = storage.vehicle_lengths_mm[mid] + (storage.gap_mm if inside else 0)
        return occupied_mm + required_mm <= storage.zone_lengths_mm[zone]

    def eligible(mid):
        desired = set(next_zones(mid))
        current = set(zones(mid))
        return all(len(owner[z] - {mid}) < capacity[z] and physical_room(z, mid)
                   for z in desired if z not in current) and all(
            len(owner[z]) <= capacity[z] for z in desired if z in current)

    def transition(mid, t):
        nonlocal seq
        s = state[mid]
        old = set(zones(mid))
        new_step = people[mid].steps[s['step'] + 1]
        new = set(new_step.zones)
        for z in sorted(old - new):
            owner[z].remove(mid)
        for z in sorted(new - old):
            owner[z].add(mid)
            result.max_occupancy[z] = max(result.max_occupancy[z], len(owner[z]))
        s['step'] += 1
        s['ready'] = False
        if mid not in result.starts:
            result.starts[mid] = t
        result.log.append((t, 'transition', mid, tuple(sorted(new))))
        seq += 1
        heappush(heap, (t + new_step.ticks, 0, seq, mid))

    while heap:
        t = heap[0][0]
        batch = []
        while heap and heap[0][0] == t:
            batch.append(heappop(heap))
        for _, kind, _, mid in batch:
            s = state[mid]
            if kind == 0:
                if s['step'] == len(people[mid].steps) - 1:
                    for z in zones(mid):
                        owner[z].remove(mid)
                    s['ready'] = False
                    result.finishes[mid] = t
                    result.log.append((t, 'exit', mid, ()))
                else:
                    s['ready'] = True
            else:
                s['ready'] = True
                s['arrived'] = True
                queues[people[mid].lane].append(mid)
        while True:
            heads = {q[0] for q in queues.values() if q}
            ready = [mid for mid,s in state.items() if s['ready'] and (s['step'] >= 0 or mid in heads)]
            possible = [mid for mid in ready if eligible(mid)]
            if not possible:
                break
            mid = min(possible, key=lambda x: (people[x].arrival, x))
            if state[mid]['step'] == -1:
                q = queues[people[mid].lane]
                assert q.pop(0) == mid
            transition(mid, t)
        for lane,q in queues.items():
            result.max_waiting[lane] = max(result.max_waiting.get(lane,0), len(q))
        assert all(len(held) <= capacity[z] for z,held in owner.items())
        assert set(result.finishes).issubset(set(result.starts))

    unfinished = sorted(set(people) - set(result.finishes))
    if unfinished:
        blocked = {}
        edges = {}
        for mid in unfinished:
            st = state[mid]
            if st['step'] < len(people[mid].steps) - 1:
                needed = next_zones(mid)
                blockers = sorted(set().union(*(owner[z] - {mid} for z in needed)))
                blocked[mid] = {'waiting_for': needed, 'held': zones(mid), 'owners': blockers}
                edges[mid] = set(blockers)
        cycle = _cycle(edges)
        if raise_deadlock:
            raise DeadlockError(blocked, cycle)
        result.deadlock = {'blocked': blocked, 'cycle': cycle}
    else:
        assert set(result.starts) == set(people) == set(result.finishes)
        assert all(not held for held in owner.values())
    return result
