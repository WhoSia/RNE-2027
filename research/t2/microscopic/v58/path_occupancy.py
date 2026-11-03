"""Synthetic junction traversal-time proxy, NOT a swept-volume safety model.

Geometry is restricted to a square conflict-zone footprint around origin;
path centreline length is computed by exact piecewise linear clipping.
A vehicle's front must travel L_centerline + vehicle length to clear zone.
Constant speed proxy uses its measured pre-crossing longitudinal speed
bounded by a tunable floor. Results cannot certify real road safety.
"""
from dataclasses import dataclass
from math import hypot, ceil, isfinite
from geometry_v58 import Path


def clipped_length(path: Path, half_width_m: float = 8.0) -> float:
    if not isfinite(half_width_m) or half_width_m <= 0:
        raise ValueError('conflict-zone half-width must be finite and >0')
    total=0.0
    for (x0,y0),(x1,y1) in zip(path.points,path.points[1:]):
        dx,dy=x1-x0,y1-y0
        t0,t1=0.,1.
        for p,q in ((-dx,x0+half_width_m),(dx,half_width_m-x0),
                    (-dy,y0+half_width_m),(dy,half_width_m-y0)):
            if abs(p)<1e-14:
                if q<0: t0,t1=1.,0.;break
                continue
            r=q/p
            if p<0:t0=max(t0,r)
            else:t1=min(t1,r)
            if t0>t1:break
        if t1>t0:total+=hypot(dx,dy)*(t1-t0)
    return total

@dataclass(frozen=True)
class PathTimeModel:
    half_width_m: float=8.0
    vehicle_length_m: float=4.5
    minimum_cross_speed_mps: float=4.0
    maximum_cross_speed_mps: float=12.0
    response_buffer_s: float=0.0
    def __post_init__(self):
        vals=(self.half_width_m,self.vehicle_length_m,self.minimum_cross_speed_mps,self.maximum_cross_speed_mps,self.response_buffer_s)
        if not all(isfinite(v) for v in vals) or min(vals[:4])<=0 or vals[2]>vals[3] or vals[4]<0:
            raise ValueError('invalid path occupancy parameters')
    def duration(self,path:Path,entry_speed_mps:float,dt:float):
        if not isfinite(entry_speed_mps) or entry_speed_mps<0 or not isfinite(dt) or dt<=0:
            raise ValueError('invalid entry speed or timestep')
        speed=min(self.maximum_cross_speed_mps,max(self.minimum_cross_speed_mps,entry_speed_mps))
        length=clipped_length(path,self.half_width_m)+self.vehicle_length_m
        return ceil((length/speed+self.response_buffer_s)/dt-1e-12)*dt
