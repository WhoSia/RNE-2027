"""Signal service accounting and per-movement exposure on the same tick engine."""
from collections import deque
from dataclasses import asdict

from actuated import Ring, Observation
from signal_model import MOVES, run


class Ledger:
    def __init__(self, s):
        self.capacity = s.link
        self.bay_capacity = s.bay
        self.active = [deque() for _ in MOVES]
        self.opportunity = [[0, 0, 0] for _ in MOVES]
        self.stopline = [0] * len(MOVES)
        self.area = [0] * len(MOVES)
        self.maximum_observed_wait = [0] * len(MOVES)
        self.source_left_blocks_through = 0
        self.trace = None

    def __call__(self, tick, arrivals, source, bay, link, ped, permitted, entry, exits):
        for _, movement in arrivals:
            self.active[movement].append(tick)
        for m in permitted:
            if m == 6:
                kind = 0 if ped else 1
            elif not bay[m]:
                kind = 1
            else:
                kind = 2 if link[m] == self.capacity[m] else 0
            self.opportunity[m][kind] += 1
        crossing = entry + ((6,) if ped and 6 in permitted else ())
        for m in crossing:
            self.stopline[m] += 1
        for m in exits + ((6,) if ped and 6 in permitted else ()):
            assert self.active[m]
            lag = tick - self.active[m].popleft()
            self.maximum_observed_wait[m] = max(self.maximum_observed_wait[m], lag)
        for m, q in enumerate(self.active):
            self.area[m] += len(q)
        for q in source[:2]:
            if q and q[0] in (1,3) and bay[q[0]] == self.bay_capacity[q[0]] and q[0]-1 in q:
                self.source_left_blocks_through += 1
        if self.trace is not None:
            self.trace.append((tick, tuple(map(len, self.active)), permitted, crossing, exits, link))

    def summary(self, s, result):
        assert sum(x*w for x,w in zip(self.area,s.weights)) == result.area
        assert all(self.stopline[m] == kinds[0] for m,kinds in enumerate(self.opportunity))
        assert tuple(map(len,self.active)) == result.remaining
        return {"opportunity": dict(zip(MOVES, self.opportunity)),
                "stopline": self.stopline, "area_by_movement": self.area,
                "maximum_observed_wait": [max(w, s.horizon - q[0]) if q else w
                                          for w,q in zip(self.maximum_observed_wait,self.active)],
                "source_left_blocks_through_approach_ticks": self.source_left_blocks_through}


def evaluate(plan, s, policy, detector=Observation(), trace=False, *, start_stage=None):
    ledger = Ledger(s)
    if trace:
        ledger.trace = []
    control = None if policy == "fixed" else Ring(plan, s, policy, detector, start_stage)
    result = run(plan, s, controller=control, observe=ledger)
    values = asdict(result) | ledger.summary(s, result)
    values["gaps"] = sum(p[3] == "gap" for p in control.periods) if control else 0
    values["maxouts"] = sum(p[3] == "max" for p in control.periods) if control else 0
    if trace:
        values["trace"] = ledger.trace
        values["phases"] = control.periods if control else []
    return values
