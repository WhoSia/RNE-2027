"""T2 v6.3-P0 theoretical viability envelope (20261103).

Idealized diagnostic, NOT an operational traffic-signal controller.
Units: m, s, m/s, m/s^2. No claims of real-world traffic safety.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class Envelope:
    speed_mps: float
    brake_mps2: float
    reaction_s: float
    buffer_m: float
    green_remaining_s: float
    clearance_s: float

    def __post_init__(self):
        vals=(self.speed_mps,self.brake_mps2,self.reaction_s,
              self.buffer_m,self.green_remaining_s,self.clearance_s)
        if any(not isfinite(v) for v in vals): raise ValueError('nonfinite')
        if self.speed_mps<0 or self.brake_mps2<=0 or any(v<0 for v in vals[2:]):
            raise ValueError('invalid domain')

    @property
    def stop_distance_m(self):
        v=self.speed_mps
        return self.buffer_m+v*self.reaction_s+v*v/(2*self.brake_mps2)

    @property
    def pass_distance_m(self):
        return self.speed_mps*max(0.,self.green_remaining_s-self.clearance_s)

    @property
    def dilemma_interval_m(self):
        return ((self.pass_distance_m,self.stop_distance_m)
                if self.pass_distance_m<self.stop_distance_m else None)

    def classification(self,distance_m):
        if not isfinite(distance_m) or distance_m<0:
            raise ValueError('invalid distance')
        stop=distance_m>=self.stop_distance_m-1e-10
        advance=distance_m<=self.pass_distance_m+1e-10
        if stop and advance:return 'either_idealized'
        if stop:return 'stop_feasible'
        if advance:return 'pass_feasible_idealized'
        return 'dilemma_no_feasible_idealized_action'
