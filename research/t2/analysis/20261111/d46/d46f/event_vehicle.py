"""D46-F independent exact-rational event-calendar, finite-buffer, discrete vehicles.

Events at rational time points, NOT a finite-difference stepper. Arrivals 3 veh per
physical time unit, admission and internal transfer max 4 veh/unit, downstream exit
slots 1 or 4 veh/unit. Link FIFO and positive minimum time in each link.
At a simultaneous timestamp exit -> transfer -> entry to make reuse causal.

Travel-time delay tau>=0 is time from link admission to its *eligible* next service;
service capacities are reserved by their own calendars, with no teleportation before
admission. Model differs from event_fluid and cannot be identified from publisher DLR
volume alone. Queue/buffer capacities are integer vehicles, not physical meters.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from collections import deque

@dataclass(frozen=True)
class Result:
    arrivals:int
    admitted:int
    exits:int
    outside:int
    upstream:int
    downstream:int
    max_outside:int
    max_upstream:int
    max_downstream:int
    first_external_queue_time: str | None
    first_downstream_full_time: str | None
    first_upstream_full_time: str | None
    first_exited_time: str | None
    last_exited_time: str | None
    outflow_times: tuple[str,...]


def make_events(horizon=F(40), arrival_rate=3, gate_rate=4, transfer_rate=4):
    """Service slots are completions at k/r (k>=1); schedule changes at 10,30."""
    events={}
    def add(t,name):
        if t>horizon:return
        events.setdefault(t, set()).add(name)
    for k in range(1,25*arrival_rate+1):add(F(k,arrival_rate),'arrival')
    for k in range(1,int(horizon*gate_rate)+1):add(F(k,gate_rate),'gate')
    for k in range(1,int(horizon*transfer_rate)+1):add(F(k,transfer_rate),'transfer')
    for k in range(1,21):add(F(10+k,1),'exit')
    for k in range(1,41):add(F(30,1)+F(k,4),'exit')
    return sorted(events.items())


def simulate(ku:int, kd:int=6, tau_up=F(0),tau_down=F(0)) -> Result:
    if isinstance(ku,bool) or isinstance(kd,bool) or not isinstance(ku,int) or not isinstance(kd,int) or ku<=0 or kd<=0:
        raise ValueError('finite positive integer capacities required')
    tau_up,tau_down=F(tau_up),F(tau_down)
    if tau_up<0 or tau_down<0:raise ValueError('nonnegative delays required')
    outside=0
    up=deque();down=deque()
    n_arr=n_admitted=n_exit=0
    max_b=max_u=max_d=0
    first_b=first_u=first_d=first_out=last_out=None
    outs=[]
    for t,types in make_events():
        if 'arrival' in types:
            outside+=1;n_arr+=1
        # downstream service frees physical room first, not before this timestamp.
        if 'exit' in types and down and down[0]+tau_down<=t:
            down.popleft();n_exit+=1;outs.append(str(t))
            if first_out is None:first_out=str(t)
            last_out=str(t)
        if 'transfer' in types and up and up[0]+tau_up<=t and len(down)<kd:
            up.popleft();down.append(t)
        if 'gate' in types and outside and len(up)<ku:
            outside-=1;n_admitted+=1;up.append(t)
        if len(down)==kd and first_d is None:first_d=str(t)
        if len(up)==ku and first_u is None:first_u=str(t)
        if outside and first_b is None:first_b=str(t)
        max_b=max(max_b,outside);max_u=max(max_u,len(up));max_d=max(max_d,len(down))
        if n_arr-n_exit != outside+len(up)+len(down):
            raise AssertionError('vehicle conservation violated')
        if n_admitted < n_exit or n_admitted>n_arr:
            raise AssertionError('invalid cumulative boundary counts')
        if len(up)>ku or len(down)>kd:raise AssertionError('storage violation')
    return Result(n_arr,n_admitted,n_exit,outside,len(up),len(down),max_b,max_u,max_d,
                  first_b,first_d,first_u,first_out,last_out,tuple(outs))
