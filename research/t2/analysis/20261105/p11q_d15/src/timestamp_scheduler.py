"""Synthetic minimal event-causality witness. NOT legacy T2 P10 replay."""
from decimal import Decimal, ROUND_FLOOR
import heapq

def execute(request_time, release_time):
    if request_time < 0 or release_time < 0:
        raise ValueError("negative timestamp")
    heap=[(release_time,0,"release"),(request_time,1,"request")]
    heapq.heapify(heap)
    occupied=True
    waiting=False
    entry=None
    trace=[]
    while heap:
        t,_,kind=heapq.heappop(heap)
        trace.append((t,kind))
        if kind=="release":
            occupied=False
            if waiting:
                occupied=True
                entry=t
                trace.append((t,"entry_after_release"))
                waiting=False
        elif occupied:
            waiting=True
        else:
            occupied=True
            entry=t
            trace.append((t,"entry"))
    assert entry is not None
    assert entry >= request_time and entry >= release_time
    return entry,trace

def intentionally_flawed_tick(request_time,release_time,dt):
    if dt <= 0: raise ValueError("dt")
    q,r,h=(Decimal(str(z)) for z in (request_time,release_time,dt))
    start=(q/h).to_integral_value(rounding=ROUND_FLOOR)*h
    end=start+h
    return request_time if r<=end else max(request_time,release_time)
