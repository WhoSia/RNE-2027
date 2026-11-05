"""Offline research demonstration: earliest arrival in immutable transit timetables.

No live service, transit feed, H3 geometry or signal-control optimization.
Times are integer minutes from a common service-day origin.
"""
from collections import defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush
from math import inf


@dataclass(frozen=True)
class Connection:
    trip: str
    origin: str
    destination: str
    depart: int
    arrive: int
    distance_km: float


def validate(connections):
    if not connections:
        raise ValueError('empty timetable')
    by_trip = defaultdict(list)
    for c in connections:
        if not c.trip or not c.origin or not c.destination or c.origin == c.destination:
            raise ValueError('invalid trip/stop')
        if type(c.depart) is not int or type(c.arrive) is not int or c.depart < 0 or c.arrive <= c.depart:
            raise ValueError('invalid timetable times')
        if not 0 < c.distance_km < inf:
            raise ValueError('invalid distance')
        by_trip[c.trip].append(c)
    for legs in by_trip.values():
        legs.sort(key=lambda c: c.depart)
        for a, b in zip(legs, legs[1:]):
            if a.destination != b.origin or a.arrive > b.depart:
                raise ValueError('discontinuous trip')


def shortest_distance(connections, origin, dest):
    """Topological lower bound on travelled distance, *ignoring schedule*."""
    validate(connections)
    graph = defaultdict(dict)
    for c in connections:
        graph[c.origin][c.destination] = min(c.distance_km, graph[c.origin].get(c.destination, inf))
    queue = [(0.0, origin, (origin,))]
    best = {origin: 0.0}
    while queue:
        distance, stop, path = heappop(queue)
        if distance != best[stop]:
            continue
        if stop == dest:
            return distance, path
        for nxt, length in graph[stop].items():
            nd = distance + length
            if nd < best.get(nxt, inf):
                best[nxt] = nd
                heappush(queue, (nd, nxt, path + (nxt,)))
    return inf, ()


def earliest_arrival(connections, origin, dest, start, transfer_min=1, max_transfers=4):
    """Label-setting earliest arrival with scheduled boardings and trip continuity.

    Search state tracks last trip and number of transfers. This intentionally
    favors earliest arrival; it does not optimize frequency or change schedules.
    """
    validate(connections)
    if type(start) is not int or start < 0 or type(transfer_min) is not int or transfer_min < 0:
        raise ValueError('invalid query time')
    if type(max_transfers) is not int or max_transfers < 0:
        raise ValueError('invalid transfer limit')
    by_stop = defaultdict(list)
    for c in connections:
        by_stop[c.origin].append(c)
    for cs in by_stop.values():
        cs.sort(key=lambda c: (c.depart, c.arrive, c.trip))
    # (arrival, sequence, stop, last_trip, transfers, itinerary)
    pq = [(start, 0, origin, None, 0, ())]
    best = {(origin, None, 0): start}
    sequence = 0
    while pq:
        at, _, stop, last, changes, route = heappop(pq)
        if at != best[(stop, last, changes)]:
            continue
        if stop == dest:
            return {'arrival': at, 'travel_minutes': at - start,
                    'transfers': changes, 'legs': route,
                    'distance_km': sum(c.distance_km for c in route)}
        for c in by_stop[stop]:
            change = int(last is not None and last != c.trip)
            nc = changes + change
            if nc > max_transfers:
                continue
            earliest_board = at + (transfer_min if change else 0)
            if c.depart < earliest_board:
                continue
            key = (c.destination, c.trip, nc)
            if c.arrive < best.get(key, inf):
                best[key] = c.arrive
                sequence += 1
                heappush(pq, (c.arrive, sequence, c.destination, c.trip, nc, route + (c,)))
    return None


def scenario():
    """Synthetic 1-hour periodic service plus time-offset variation, not GTFS."""
    result = []
    for t in range(0, 120, 15):
        result.append(Connection(f'near_feed_{t}', 'O', 'N', t, t + 4, 2.0))
    for t in range(28, 150, 30):
        result.append(Connection(f'near_connector_{t}', 'N', 'D', t, t + 4, 1.0))
    for t in range(1, 120, 6):
        result.append(Connection(f'far_feed_{t}', 'O', 'F', t, t + 6, 4.0))
    for t in range(8, 150, 6):
        result.append(Connection(f'far_connector_{t}', 'F', 'D', t, t + 6, 4.0))
    validate(result)
    return result
