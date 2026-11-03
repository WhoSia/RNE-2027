"""T2 v5.9 standalone synthetic 2-D Bezier speed profile; NOT calibrated or integrated."""
from dataclasses import dataclass
from math import sqrt, hypot, isfinite, ceil

@dataclass(frozen=True)
class Cubic:
    controls:tuple[tuple[float,float],...]
    def __post_init__(self):
        if len(self.controls)!=4 or any(len(p)!=2 or not all(isfinite(v) for v in p) for p in self.controls):raise ValueError('four finite points required')
    def at(self,t):
        if not 0<=t<=1:raise ValueError('bad parameter')
        u=1-t;a,b,c,d=self.controls
        return tuple(u**3*a[j]+3*u*u*t*b[j]+3*u*t*t*c[j]+t**3*d[j] for j in range(2))
    def derivatives(self,t):
        a,b,c,d=self.controls;u=1-t
        first=tuple(3*u*u*(b[j]-a[j])+6*u*t*(c[j]-b[j])+3*t*t*(d[j]-c[j]) for j in range(2))
        second=tuple(6*u*(c[j]-2*b[j]+a[j])+6*t*(d[j]-2*c[j]+b[j]) for j in range(2))
        return first,second
    def curvature(self,t):
        v,a=self.derivatives(t);norm=hypot(*v)
        return 0. if norm<1e-10 else abs(v[0]*a[1]-v[1]*a[0])/norm**3

@dataclass(frozen=True)
class Dynamics:
    max_speed:float=13.
    lateral_accel:float=1.8
    accel:float=1.5
    braking:float=2.5
    vehicle_length:float=4.5
    n:int=240
    dt:float=.5
    def __post_init__(self):
        if not all(isfinite(v) and v>0 for v in (self.max_speed,self.lateral_accel,self.accel,self.braking,self.vehicle_length,self.dt)) or self.n<4:raise ValueError('bad parameters')

def make_profile(curve:Cubic,cfg:Dynamics,entry_speed:float=7.):
    if not isfinite(entry_speed) or entry_speed<0:raise ValueError('entry speed')
    ts=[i/cfg.n for i in range(cfg.n+1)]
    xy=[curve.at(t) for t in ts]
    ds=[hypot(xy[i+1][0]-xy[i][0],xy[i+1][1]-xy[i][1]) for i in range(cfg.n)]
    limits=[min(cfg.max_speed,sqrt(cfg.lateral_accel/max(curve.curvature(t),1e-12))) for t in ts]
    speeds=limits.copy();speeds[0]=min(entry_speed,limits[0])
    for i in range(cfg.n-1,-1,-1):speeds[i]=min(speeds[i],sqrt(speeds[i+1]**2+2*cfg.braking*ds[i]))
    for i in range(cfg.n):speeds[i+1]=min(speeds[i+1],sqrt(speeds[i]**2+2*cfg.accel*ds[i]))
    clocks=[0.];distance=0.;out=[]
    for i in range(cfg.n+1):
        if i:
            mean=(speeds[i-1]+speeds[i])/2
            if mean<=0:raise ValueError('nonmoving path')
            clocks.append(clocks[-1]+ds[i-1]/mean);distance+=ds[i-1]
        out.append(dict(t_s=clocks[i],x_m=xy[i][0],y_m=xy[i][1],s_m=distance,v_mps=speeds[i],curvature_inv_m=curve.curvature(ts[i]),a_lat_mps2=speeds[i]**2*curve.curvature(ts[i])))
    return tuple(out)

def crossing_occupancy(profile,half_width=8.,vehicle_length=4.5,dt=.5):
    if not all(isfinite(v) and v>0 for v in (half_width,vehicle_length,dt)):raise ValueError('bad clearance')
    inside=[i for i,p in enumerate(profile) if abs(p['x_m'])<=half_width and abs(p['y_m'])<=half_width]
    if not inside:raise ValueError('path misses conflict zone')
    first,last=inside[0],inside[-1]
    entry=profile[first]['t_s'];clear=profile[last]['s_m']+vehicle_length
    for k in range(last+1,len(profile)):
        if profile[k]['s_m']>=clear:
            prev=profile[k-1];now=profile[k];ds=now['s_m']-prev['s_m']
            f=min(1.,max(0.,(clear-prev['s_m'])/ds)) if ds>0 else 1.
            exit_t=prev['t_s']+f*(now['t_s']-prev['t_s'])
            return dict(entry_s=entry,exit_s=exit_t,duration_s=ceil((exit_t-entry)/dt-1e-12)*dt,exact_duration_s=exit_t-entry)
    raise ValueError('too little exit length')

def example_turn():
    return Cubic(((-2.,30.),(-2.,-5.),(5.,2.),(-30.,2.)))
def example_through():
    return Cubic(((-2.,30.),(-2.,10.),(-2.,-10.),(-2.,-30.)))
