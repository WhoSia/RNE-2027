"""Independent one-vehicle numerical integrator. Not a refinement of micro_world.
Synthetic constant acceleration toward an always-green stopline. No car following.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class Config:
    road_m: float=40.0
    vehicle_m: float=4.5
    acceleration_mps2: float=1.5
    speed_limit_mps: float=8.0

def run(dt_s: float, cfg:Config=Config()):
    if not all(isfinite(v) for v in (dt_s,cfg.road_m,cfg.vehicle_m,cfg.acceleration_mps2,cfg.speed_limit_mps)):
        raise ValueError('nonfinite')
    if dt_s<=0 or dt_s>1 or cfg.road_m<=cfg.vehicle_m or cfg.acceleration_mps2<=0 or cfg.speed_limit_mps<=0:
        raise ValueError('invalid parameters')
    rear=0.; speed=0.; t=0.; trace=[(0.,rear,speed)]
    for i in range(10000):
        vnext=min(cfg.speed_limit_mps,speed+cfg.acceleration_mps2*dt_s)
        # End-of-step Euler, deterministic reference convention.
        dx=vnext*dt_s
        distance=(cfg.road_m-cfg.vehicle_m)-rear
        if dx>=distance:
            # Linear interpolation inside current cell; not an exact continuous dynamics solution.
            frac=distance/dx
            return {'exit_time_s':t+dt_s*frac,'steps':i+1,'trace':trace+[(t+dt_s*frac,cfg.road_m-cfg.vehicle_m,vnext)],'dt_s':dt_s}
        rear+=dx;speed=vnext;t+=dt_s;trace.append((t,rear,speed))
    raise RuntimeError('no exit')
