"""D44 offline kinematic feasibility prototype, NOT calibrated road control."""
from dataclasses import dataclass
from math import isfinite

class InfeasibleStop(ValueError): pass

@dataclass(frozen=True)
class Sample:
    t_s: float
    rear_m: float
    v_mps: float
    mode: str

def simulate(stop_rear_m=7.5, acceleration=1.5, max_decel=.25,
             dt=1., steps=8, green_until_s=1.):
    numbers=(stop_rear_m,acceleration,max_decel,dt,green_until_s)
    if not all(map(isfinite,numbers)) or min(stop_rear_m,acceleration,max_decel,dt)<=0:
        raise ValueError("invalid kinematic input")
    if not isinstance(steps,int) or steps<1: raise ValueError("invalid steps")
    x=v=0.
    result=[Sample(0.,x,v,"initial")]
    for step in range(steps):
        t=step*dt
        green=t<green_until_s
        next_v=(v+acceleration*dt) if green else max(0.,v-max_decel*dt)
        next_x=x+(v+next_v)*dt/2
        if next_x>stop_rear_m+1e-9: raise InfeasibleStop("stopline overshoot")
        d=max(0.,stop_rear_m-next_x)
        if t+dt>=green_until_s and next_v**2/(2*max_decel)>d+1e-9:
            raise InfeasibleStop("insufficient remaining stopping distance")
        x,v=next_x,next_v
        result.append(Sample((step+1)*dt,x,v,"green" if green else "red"))
    return result
