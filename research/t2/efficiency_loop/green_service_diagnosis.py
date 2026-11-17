"""Distinguish synthetic missed through-service opportunities from no demand."""
from collections import Counter
from dataclasses import dataclass

from signal_model import APPROACH, run

THROUGH = (0, 2)


@dataclass(frozen=True)
class Opportunity:
    tick: int
    movement: int
    through_ready: int
    through_upstream: int
    left_bay: int
    left_capacity: int
    shared_head_is_left: bool
    downstream_space: int
    entered: bool

    @property
    def pocket_signature(self):
        return (self.shared_head_is_left and
                self.left_bay == self.left_capacity and
                self.through_upstream > 0)

    @property
    def diagnosis(self):
        if self.entered:
            return "served"
        if self.through_ready and self.downstream_space == 0:
            return "joint_signature" if self.pocket_signature else "downstream_blocked"
        if self.pocket_signature:
            return "joint_signature" if self.downstream_space == 0 else "pocket_signature"
        if self.through_ready or self.through_upstream:
            return "upstream_pending"
        return "no_through_demand"


def measure(plan, scenario):
    counts = Counter()
    examples = {}

    def observe(tick, arrivals, source, bay, link, pedestrians, permitted, entry, exit_now):
        for movement in THROUGH:
            if movement not in permitted:
                continue
            left = movement + 1
            queue = source[APPROACH[movement]]
            row = Opportunity(tick, movement, bay[movement], queue.count(movement),
                              bay[left], scenario.bay[left], bool(queue and queue[0] == left),
                              scenario.link[movement] - link[movement], movement in entry)
            if row.entered != bool(row.through_ready and row.downstream_space):
                raise AssertionError("through admission disagrees with the pre-service frame")
            diagnosis = row.diagnosis
            counts[diagnosis] += 1
            examples.setdefault(diagnosis, row)

    outcome = run(plan, scenario, observe=observe)
    return outcome, counts, examples
