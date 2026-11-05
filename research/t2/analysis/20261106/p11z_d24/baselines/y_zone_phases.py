"""Deterministic phased resource occupancy, using integer time ticks.

Synthetic dependency-free counterexample, NOT a driving controller.
Each movement holds its old zone until the next zone becomes available.
Deadlock is detected and reported, NOT resolved with an invented policy.
"""
from collections import defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush


class DeadlockError(RuntimeError):
    pass


@dataclass(frozen=True)
class Movement:
    identity: str
    at: int
    phases: tuple  # tuples of (resource-zone, strictly positive duration ticks)


def simulate(movements):
    identifiers = [m.identity for m in movements]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError('duplicate movement identifier')
    for m in movements:
        if not m.identity or type(m.at) is not int or m.at < 0 or not m.phases:
            raise ValueError('invalid movement')
        for zone, duration in m.phases:
            if not isinstance(zone, str) or not zone or type(duration) is not int or duration <= 0:
                raise ValueError('invalid phase')
    # event: (time, event type [0=end,1=arrival], sequence, movement identifier)
    events = []
    owner = {}
    states = {m.identity: {'phase': -1, 'ready': False} for m in movements}
    requests = {m.identity: m for m in movements}
    arrivals = {}
    released = {}
    log = []
    sequence = 0
    for m in movements:
        sequence += 1
        heappush(events, (m.at, 1, sequence, m.identity))
    def phase_zone(mid, ix):
        return requests[mid].phases[ix][0]
    def can_start(mid):
        st = states[mid]
        ix = st['phase'] + 1
        if ix >= len(requests[mid].phases):
            return False
        next_zone = phase_zone(mid, ix)
        return next_zone not in owner or owner[next_zone] == mid
    def enter(mid, t):
        nonlocal sequence
        st = states[mid]
        next_ix = st['phase'] + 1
        old_zone = phase_zone(mid, st['phase']) if st['phase'] >= 0 else None
        new_zone, duration = requests[mid].phases[next_ix]
        if old_zone != new_zone and old_zone is not None:
            del owner[old_zone]
            log.append((t, 'release', mid, old_zone))
        owner[new_zone] = mid
        st['phase'] = next_ix
        st['ready'] = False
        if mid not in arrivals:
            arrivals[mid] = t
        log.append((t, 'enter', mid, new_zone))
        sequence += 1
        heappush(events, (t + duration, 0, sequence, mid))
    while events:
        t = events[0][0]
        batch = []
        while events and events[0][0] == t:
            batch.append(heappop(events))
        for _, typ, _, mid in batch:
            if typ == 0:
                st = states[mid]
                if st['phase'] == len(requests[mid].phases) - 1:
                    zone = phase_zone(mid, st['phase'])
                    del owner[zone]
                    log.append((t, 'release', mid, zone))
                    released[mid] = t
                else:
                    st['ready'] = True
            else:
                states[mid]['ready'] = True
        # Request ordering is deterministic and fixed per timestamp.
        while True:
            eligible = [mid for mid, st in states.items()
                        if st['ready'] and can_start(mid)]
            if not eligible:
                break
            eligible.sort(key=lambda mid: (requests[mid].at, mid))
            enter(eligible[0], t)
        assert len(set(owner)) == len(owner)
    unfinished = set(requests) - set(released)
    if unfinished:
        raise DeadlockError(f'no future release events; blocked movements: {sorted(unfinished)}')
    return {'starts': arrivals, 'finishes': released, 'log': log}
