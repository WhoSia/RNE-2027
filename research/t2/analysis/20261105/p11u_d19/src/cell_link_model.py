"""Research-only three-cell conservative CTM reference; not an operational controller.

Conserved quantities are continuous vehicle-equivalents, NOT individual vehicles.
The gate is externally fixed, and not optimized. Spatial cells have finite jam storage,
CFL-bounded forward/backwards propagation, and simultaneous sending/receiving fluxes.
"""
from dataclasses import dataclass, asdict
from math import isfinite

@dataclass(frozen=True)
class Config:
    lengths_m: tuple[float, ...] = (30., 15., 7.5)
    jam_spacing_m: float = 7.5
    free_speed_mps: float = 7.5
    backward_wave_mps: float = 7.5
    saturation_veh_per_s: float = 1.
    dt_s: float = 1.
    horizon_s: float = 24.
    arrival_veh_per_s: float = 0.5
    downstream_closed_until_s: float = 12.
    infinite_storage_baseline: bool = False


def validate(c:Config):
    nums=[*c.lengths_m,c.jam_spacing_m,c.free_speed_mps,c.backward_wave_mps,
          c.saturation_veh_per_s,c.dt_s,c.horizon_s,c.arrival_veh_per_s,
          c.downstream_closed_until_s]
    if not all(isfinite(v) for v in nums): raise ValueError('nonfinite')
    if len(c.lengths_m)<2 or min(c.lengths_m)<=0: raise ValueError('links')
    if min(c.jam_spacing_m,c.free_speed_mps,c.backward_wave_mps,c.saturation_veh_per_s,c.dt_s,c.horizon_s)<=0: raise ValueError('positive parameters')
    if c.arrival_veh_per_s<0 or c.downstream_closed_until_s<0: raise ValueError('negative demand/gate')
    if c.free_speed_mps*c.dt_s > min(c.lengths_m)+1e-12 or c.backward_wave_mps*c.dt_s > min(c.lengths_m)+1e-12:
        raise ValueError('CFL: dt exceeds cell length / speed')
    if abs(c.horizon_s/c.dt_s-round(c.horizon_s/c.dt_s))>1e-10: raise ValueError('horizon must be integer number of steps')
    if abs(c.downstream_closed_until_s/c.dt_s-round(c.downstream_closed_until_s/c.dt_s))>1e-10:
        raise ValueError('gate must coincide with grid for unambiguous experiment')


def simulate(c:Config)->dict:
    validate(c)
    N=[L/c.jam_spacing_m for L in c.lengths_m]
    if c.infinite_storage_baseline:
        # Counterfactual removes jam-storage constraint; all other rates identical.
        N=[float('inf') for _ in N]
    q=c.saturation_veh_per_s*c.dt_s
    n=[0. for _ in N]
    source=0.
    arrivals=admitted=departed=0.
    states=[]
    rows=[]
    for k in range(round(c.horizon_s/c.dt_s)):
        t=k*c.dt_s
        incoming=c.arrival_veh_per_s*c.dt_s
        source+=incoming
        arrivals+=incoming
        send=[min(ni,q,c.free_speed_mps*c.dt_s/c.lengths_m[i]*ni) for i,ni in enumerate(n)]
        receive=[min(q,c.backward_wave_mps*c.dt_s/c.lengths_m[i]*(N[i]-n[i])) for i in range(len(n))]
        transfers=[min(send[i],receive[i+1]) for i in range(len(n)-1)]
        outgoing=min(send[-1],q if t+1e-12 >= c.downstream_closed_until_s else 0.)
        entry=min(source,receive[0])
        flows=[entry,*transfers,outgoing]
        newn=[n[i]+flows[i]-flows[i+1] for i in range(len(n))]
        if any(v < -1e-9 or (v>N[i]+1e-9 if isfinite(N[i]) else False) for i,v in enumerate(newn)):
            raise AssertionError('capacity or nonnegativity violated')
        n=newn
        source-=entry
        admitted+=entry
        departed+=outgoing
        if abs((source+sum(n)+departed)-arrivals)>1e-8:
            raise AssertionError('conservation violated')
        if any(v<-1e-10 for v in flows): raise AssertionError('negative flux')
        row={'t_end_s':round(t+c.dt_s,10),'source_queue_veh':source,
             'in_network_veh':sum(n),'cumulative_arrivals_veh':arrivals,
             'cumulative_admitted_veh':admitted,'cumulative_departed_veh':departed,
             'flows_veh':flows,'cells_veh':list(n),'full_flags':[n[i]>=N[i]-1e-8 for i in range(len(n))]}
        rows.append(row)
    first_blocked=next((r['t_end_s'] for r in rows if r['source_queue_veh']>1e-8), None)
    first_all_full=next((r['t_end_s'] for r in rows if all(r['full_flags'])),None) if not c.infinite_storage_baseline else None
    first_upstream_full=next((r['t_end_s'] for r in rows if r['full_flags'][0]),None) if not c.infinite_storage_baseline else None
    return {'config':asdict(c),'capacities_veh':N,'rows':rows,
            'summary':{'first_source_blocked_end_s':first_blocked,'first_upstream_full_end_s':first_upstream_full,
                       'first_all_full_end_s':first_all_full,'max_source_queue_veh':max(r['source_queue_veh'] for r in rows),
                       'final_departures_veh':departed,'final_source_queue_veh':source,
                       'max_conservation_abs_error':max(abs(r['cumulative_arrivals_veh']-r['cumulative_departed_veh']-r['source_queue_veh']-r['in_network_veh']) for r in rows)}}
