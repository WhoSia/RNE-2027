"""P5: One-step longitudinal reachability for experimental simulations only.

Not an operational vehicle controller. Assumes constant acceleration during dt,
no reaction delay and an already-known future obstacle position.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class StepResult:
    x_next_m: float
    v_next_mps: float
    accel_mps2: float
    feasible: bool
    limiting_constraint: str

def bounded_step(x_m: float,v_mps: float,desired_accel_mps2: float,dt_s: float,
                 accel_limit_mps2: float,brake_limit_mps2: float,
                 max_front_x_m: float|None=None)->StepResult:
    args=(x_m,v_mps,desired_accel_mps2,dt_s,accel_limit_mps2,brake_limit_mps2)
    if any(not isfinite(q) for q in args) or dt_s<=0 or accel_limit_mps2<=0 or brake_limit_mps2<=0 or v_mps<0:
        raise ValueError('invalid longitudinal parameters')
    if max_front_x_m is not None and not isfinite(max_front_x_m):
        raise ValueError('invalid obstacle')
    vlow=max(0.,v_mps-brake_limit_mps2*dt_s)
    vhigh=v_mps+accel_limit_mps2*dt_s
    desired=max(vlow,min(vhigh,v_mps+desired_accel_mps2*dt_s))
    if max_front_x_m is None:
        vnew=desired;feasible=True;limit='unconstrained'
    else:
        max_end_speed=2.*(max_front_x_m-x_m)/dt_s-v_mps
        feasible=max_end_speed>=vlow-1e-10
        vnew=max(vlow,min(vhigh,desired,max_end_speed)) if feasible else vlow
        limit=('obstacle' if vnew<desired-1e-10 else 'free') if feasible else 'infeasible_bound'
    xnew=x_m+.5*(v_mps+vnew)*dt_s
    return StepResult(xnew,vnew,(vnew-v_mps)/dt_s,feasible,limit)

def obstacle_from_leader(leader_front_next_m: float,leader_length_m: float,
                         follower_min_gap_m: float)->float:
    args=(leader_front_next_m,leader_length_m,follower_min_gap_m)
    if any(not isfinite(q) for q in args) or leader_length_m<=0 or follower_min_gap_m<0:
        raise ValueError('invalid leader geometry')
    return leader_front_next_m-leader_length_m-follower_min_gap_m
