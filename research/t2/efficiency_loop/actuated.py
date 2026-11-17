"""Causal ring controllers with common green and clearance constraints."""
from collections import deque
from dataclasses import dataclass
from random import Random

from signal_model import STAGES

MIN_GREEN = (10, 6, 10, 8)
MAX_GREEN = (36, 16, 32, 12)
EXTENSION = (3, 3, 3, 3)


@dataclass(frozen=True)
class Observation:
    delay: int = 0
    miss: float = 0.0
    seed: int = 0

    def __post_init__(self):
        if self.delay < 0 or not 0 <= self.miss <= 1:
            raise ValueError("invalid detector observation")


class Ring:
    """Visit all phases in a fixed ring, adjusting their green lengths online.

    The controller sees only bays, receiving occupancy, and pedestrian queue
    at the end of a prior tick. True queues remain inside the plant.
    """

    def __init__(self, plan, scenario, kind, detector=Observation(), start_stage=None):
        if kind not in ("queue", "receiving", "confirmed"):
            raise ValueError("unknown actuation mode")
        self.plan, self.scenario, self.kind = plan, scenario, kind
        self.detector = detector
        self.order = (1, 0, 2, 3) if plan.left_first else (0, 1, 2, 3)
        self.history = deque(maxlen=detector.delay + 1)
        self.index = 0 if start_stage is None else self.order.index(start_stage)
        self.start, self.end = 0, None
        self.next_tick = 0
        self.empty_checks = 0
        self.periods = []
        self.rng = Random(detector.seed)

    def _detected(self, counts):
        if not self.detector.miss:
            return counts
        return tuple(sum(self.rng.random() >= self.detector.miss for _ in range(n)) for n in counts)

    def __call__(self, t, bay, link, ped):
        if t != self.next_tick:
            raise ValueError("controller requires consecutive ticks")
        self.next_tick += 1
        self.history.append((self._detected(bay + (ped,)), self._detected(link)))
        if self.end is not None:
            if t < self.end:
                return ()
            self.index = (self.index + 1) % len(self.order)
            self.start, self.end = t, None
            self.empty_checks = 0
        stage = self.order[self.index]
        elapsed = t - self.start
        if elapsed >= MIN_GREEN[stage]:
            q, down = (self.history[0] if len(self.history) == self.history.maxlen
                       else ((0,) * 7, (0,) * 6))
            remaining = sum(q[m] for m in STAGES[stage])
            if self.kind in ("receiving", "confirmed"):
                remaining = sum(q[m] for m in STAGES[stage]
                                if m == 6 or down[m] < self.scenario.link[m])
            maxed = elapsed >= MAX_GREEN[stage]
            should_check = (elapsed - MIN_GREEN[stage]) % EXTENSION[stage] == 0
            if should_check:
                self.empty_checks = 0 if remaining else self.empty_checks + 1
            confirmation = 2 if self.kind == "confirmed" else 1
            if maxed or self.empty_checks >= confirmation:
                self.periods.append((stage, self.start, t, "max" if maxed else "gap"))
                self.end = t + self.plan.clearance
                return ()
        return tuple(m for m in STAGES[stage]
                     if elapsed >= self.plan.startup
                     and (elapsed - self.plan.startup) % self.scenario.headway[m] == 0)
