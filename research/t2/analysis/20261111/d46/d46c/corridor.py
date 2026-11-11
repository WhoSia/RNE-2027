"""Conservative synchronous two-link finite-storage experiment.

All flow/state units: vehicles per discrete step; no micromobility or real calibration.
Synchronous boundary: sink discharge and upstream-to-downstream transfer use
beginning-of-step inventory/space. Freed downstream room is available NEXT step.
New arrivals become eligible for upstream transfer NEXT step. This prevents
same-tick multi-link teleportation but is a modeling convention, not physics.
"""
from dataclasses import dataclass
from math import isfinite
from typing import Iterable

@dataclass(frozen=True)
class State:
    upstream: float
    downstream: float
    cumul_arrivals: float = 0.0
    cumul_exits: float = 0.0

@dataclass(frozen=True)
class Step:
    state: State
    transfer: float
    exit_flow: float
    blocked: float
    end_conservation_error: float

def advance(state: State, arrivals: float, transfer_cap: float,
            exit_cap: float, downstream_storage: float) -> Step:
    args=(state.upstream,state.downstream,state.cumul_arrivals,
          state.cumul_exits,arrivals,transfer_cap,exit_cap,downstream_storage)
    if any(not isfinite(float(x)) or float(x)<0 for x in args):
        raise ValueError('nonnegative finite physical quantities required')
    if state.downstream > downstream_storage+1e-9:
        raise ValueError('downstream occupancy exceeds storage')
    if abs((state.upstream+state.downstream)-(state.cumul_arrivals-state.cumul_exits))>1e-8:
        raise ValueError('invalid conservation initial state')
    free_space=max(0.,downstream_storage-state.downstream)
    move=min(state.upstream,transfer_cap,free_space)
    out=min(state.downstream,exit_cap)
    # Arrivals are added at the step END; no instantaneous advance to 2nd link.
    up=state.upstream+arrivals-move
    down=state.downstream+move-out
    nxt=State(up,down,state.cumul_arrivals+arrivals,state.cumul_exits+out)
    err=(nxt.cumul_arrivals-nxt.cumul_exits)-(nxt.upstream+nxt.downstream)
    if abs(err)>1e-8:raise AssertionError(f'conservation failure: {err}')
    if down>downstream_storage+1e-9:raise AssertionError('storage violation')
    return Step(nxt,move,out,max(0.,min(state.upstream,transfer_cap)-move),err)

def run(arrivals: Iterable[float], transfers: Iterable[float],
        exits: Iterable[float], downstream_storage: float,
        initial: State=State(0,0)) -> list[Step]:
    a,t,e=list(arrivals),list(transfers),list(exits)
    if not(len(a)==len(t)==len(e)):raise ValueError('schedule length mismatch')
    out=[];s=initial
    for aa,tt,ee in zip(a,t,e):
        z=advance(s,aa,tt,ee,downstream_storage)
        out.append(z);s=z.state
    return out
