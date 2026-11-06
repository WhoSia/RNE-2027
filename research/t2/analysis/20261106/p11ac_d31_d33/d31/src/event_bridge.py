"""D31 event-evidence bridge: common observable contract, not model equivalence."""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class Event:
    t:float
    actor:str
    action:str
    location:str


def from_micro(output):
    events=[Event(float(t),str(who),action,where) for t,action,who,where in output.events]
    validate_event_clock(events)
    return events


def from_p10(result):
    events=[Event(float(r['t']),str(r['id']),str(r['event']),f"junction:{r['j']}") for r in result['events']]
    validate_event_clock(events)
    return events


def validate_event_clock(events):
    for e in events:
        if not isfinite(e.t) or e.t<0 or not e.actor or not e.action or not e.location:
            raise ValueError('malformed physical event')
    if any(a.t>b.t+1e-8 for a,b in zip(events,events[1:])):
        raise ValueError('global event trace is not chronologically ordered')
    return len(events)


def capacity_witness(p10_trace):
    """Specialized audited P10 dependency: no generic inference from event types alone.

    Exactly the witness state where a vehicle link receipt funds another vehicle
    connector admission into a link of insufficient physical capacity.
    """
    m=p10_trace['mechanism']; case=p10_trace['source_case']
    if not (m['two_cars_storage_m']<=m['link_storage_m']<m['three_cars_storage_m']):
        raise ValueError('not the known P10 capacity-limited witness')
    if case['vehicle_1']!=1 or case['vehicle_8']!=8:
        raise ValueError('different source cohort')
    return [{'dt_s':r['dt_s'],'retroactive_seconds':max(0.0,r['link_receives_vehicle_1_at_s']-r['vehicle_8_enters_j0_at_s'])
             if r['vehicle_8_enters_j0_at_s'] < m['last_side_entry_s'] else 0.,
             'phase_boundary_s':m['last_side_entry_s'],
             'vehicle_8_entry_s':r['vehicle_8_enters_j0_at_s']} for r in p10_trace['runs']]
