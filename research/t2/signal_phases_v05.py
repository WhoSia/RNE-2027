"""Explicit protected left / through phase schedule for T2 research.

Independent specification component; NOT YET integrated into spatial_v04.
Times are integer seconds; clearance represented explicitly; no overlaps.
"""
from dataclasses import dataclass
from enum import Enum

class Phase(str, Enum):
    LEFT = "LEFT"
    THROUGH = "THROUGH"
    CLEARANCE = "CLEARANCE"
    RED = "RED"

@dataclass(frozen=True)
class PhaseConfig:
    cycle: int = 150
    green_left: int = 54
    green_through: int = 60
    clearance: int = 3
    order: str = "leading"

    def __post_init__(self):
        if self.order not in ("leading", "lagging"):
            raise ValueError("order must be leading or lagging")
        if self.cycle <= 0 or min(self.green_left, self.green_through, self.clearance) < 0:
            raise ValueError("negative or non-positive time")
        if self.green_left + self.green_through + 2*self.clearance > self.cycle:
            raise ValueError("phases exceed cycle")

def phase_at(time_s: int, c: PhaseConfig) -> Phase:
    if time_s < 0:
        raise ValueError("negative time")
    t = time_s % c.cycle
    first = (Phase.LEFT, c.green_left) if c.order == "leading" else (Phase.THROUGH, c.green_through)
    second = (Phase.THROUGH, c.green_through) if c.order == "leading" else (Phase.LEFT, c.green_left)
    if t < first[1]: return first[0]
    t -= first[1]
    if t < c.clearance: return Phase.CLEARANCE
    t -= c.clearance
    if t < second[1]: return second[0]
    t -= second[1]
    if t < c.clearance: return Phase.CLEARANCE
    return Phase.RED

def greens(time_s: int, c: PhaseConfig) -> tuple[bool, bool]:
    """(through_green, left_green), always mutually exclusive."""
    phase = phase_at(time_s, c)
    return phase == Phase.THROUGH, phase == Phase.LEFT

if __name__ == '__main__':
    from collections import Counter
    for order in ('leading','lagging'):
        c=PhaseConfig(order=order)
        print(order, Counter(phase_at(t,c) for t in range(c.cycle)))
