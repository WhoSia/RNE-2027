"""Independent dimensioned IDM and finite receiving-space components. Uncalibrated."""
from dataclasses import dataclass
from math import sqrt,isfinite
@dataclass(frozen=True)
class Driver:
    desired_speed_mps:float=13.9
    min_gap_m:float=2.5
    time_headway_s:float=1.3
    max_accel_mps2:float=1.4
    comfort_decel_mps2:float=2.0
    exponent:float=4.0
    length_m:float=4.6
    def __post_init__(self):
        if any(not isfinite(v) or v<=0 for v in vars(self).values()):raise ValueError("invalid parameters")
def idm_acceleration(v_mps,gap_m,leader_v_mps,p:Driver):
    if any(not isfinite(x) for x in (v_mps,gap_m,leader_v_mps)) or min(v_mps,gap_m,leader_v_mps)<0:raise ValueError("invalid state")
    delta_v=v_mps-leader_v_mps
    s=p.min_gap_m+max(0,v_mps*p.time_headway_s+v_mps*delta_v/(2*sqrt(p.max_accel_mps2*p.comfort_decel_mps2)))
    return p.max_accel_mps2*(1-(v_mps/p.desired_speed_mps)**p.exponent-(s/max(gap_m,1e-6))**2)
def integrate_speed(v_mps,accel_mps2,delta_t_s,emergency_decel_mps2=8.0):
    if delta_t_s<=0 or emergency_decel_mps2<=0:raise ValueError("invalid timestep")
    return max(0,v_mps+max(accel_mps2,-emergency_decel_mps2)*delta_t_s)
def storage_capacity(length_m,average_vehicle_length_m,stopped_gap_m):
    if length_m<0 or average_vehicle_length_m<=0 or stopped_gap_m<0:raise ValueError("invalid geometry")
    return int(length_m//(average_vehicle_length_m+stopped_gap_m))
def receiving_supply(capacity,occupancy):
    if not isinstance(capacity,int) or not isinstance(occupancy,int) or not 0<=occupancy<=capacity:raise ValueError("invalid occupancy")
    return capacity-occupancy
