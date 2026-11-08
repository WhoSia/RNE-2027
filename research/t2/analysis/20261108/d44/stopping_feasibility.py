"""D44 physical feasibility oracle; diagnostic only, not a signal-controller algorithm.

A vehicle at speed v with remaining stopping distance d needs
mean constant deceleration magnitude v**2 / (2*d), for v>=0, d>0.
This is a lower-bound check under simplified constant deceleration,
not a proof of collision safety with reaction time.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class StoppingAudit:
    speed_mps: float
    remaining_m: float
    configured_decel_mps2: float
    required_decel_mps2: float
    feasible_without_reaction: bool

def evaluate_stopping(speed_mps:float, remaining_m:float, max_decel_mps2:float)->StoppingAudit:
    if not all(isfinite(z) for z in (speed_mps,remaining_m,max_decel_mps2)):
        raise ValueError("nonfinite input")
    if speed_mps<0 or remaining_m<0 or max_decel_mps2<=0:
        raise ValueError("invalid kinematic constraint")
    required=(speed_mps**2/(2*remaining_m)) if remaining_m>0 else (float("inf") if speed_mps>0 else 0.0)
    return StoppingAudit(speed_mps,remaining_m,max_decel_mps2,
                         required,required<=max_decel_mps2)

if __name__=="__main__":
    case=evaluate_stopping(3,3,0.25)
    print(case)
    assert not case.feasible_without_reaction
    assert abs(case.required_decel_mps2-1.5)<1e-12
