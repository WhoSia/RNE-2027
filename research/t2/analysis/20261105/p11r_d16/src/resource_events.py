"""Synthetic resource occupancy event model; no field/safety or policy claims."""
from dataclasses import dataclass
import heapq
@dataclass(frozen=True)
class Request:
    at:float
    identity:str
    resources:tuple
    duration:float
    group:str
def run(requests, capacities, incompatible=frozenset()):
    if any(c<1 for c in capacities.values()): raise ValueError("capacity")
    if len(set(q.identity for q in requests))!=len(requests): raise ValueError("duplicate id")
    if any(q.at<0 or q.duration<=0 or not q.resources or any(r not in capacities for r in q.resources) for q in requests):
        raise ValueError("invalid request")
    event=[(q.at,1,i,"request",q) for i,q in enumerate(requests)]
    heapq.heapify(event)
    occupied={k:set() for k in capacities}
    active={}
    waiting=[]
    entries={}
    exits={}
    log=[]
    serial=len(event)
    def possible(q):
        return all(len(occupied[r])<capacities[r] for r in q.resources) and all(
            frozenset((q.group,a.group)) not in incompatible for a in active.values())
    def grant(q,t):
        nonlocal serial
        assert t>=q.at
        for r in q.resources: occupied[r].add(q.identity)
        active[q.identity]=q
        entries[q.identity]=t
        log.append((t,"enter",q.identity))
        serial+=1
        heapq.heappush(event,(t+q.duration,0,serial,"exit",q))
    last=-1.
    while event:
        t,_,_,kind,q=heapq.heappop(event)
        assert t>=last
        last=t
        if kind=="exit":
            for r in q.resources: occupied[r].remove(q.identity)
            del active[q.identity]
            exits[q.identity]=t
            log.append((t,"exit",q.identity))
            while waiting and possible(waiting[0]):
                grant(waiting.pop(0),t)
        elif waiting or not possible(q):
            waiting.append(q)
        else:
            grant(q,t)
        assert all(len(v)<=capacities[k] for k,v in occupied.items())
    assert entries.keys()==exits.keys()==set(q.identity for q in requests)
    return {"entries":entries,"exits":exits,"log":log}
