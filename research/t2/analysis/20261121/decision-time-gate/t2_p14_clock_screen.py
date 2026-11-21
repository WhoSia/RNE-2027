"""P14 abstract two-queue timing screen; NOT the RNE PHYS engine or real signal control."""
from __future__ import annotations
from itertools import combinations_with_replacement, product
from collections import Counter
from hashlib import sha256
import json

HORIZON=4
SERVICE={"AABB": (0,0,1,1), "BBAA": (1,1,0,0)}


def tape_from_slots(slots):
    if len(slots)!=2 or any(type(x) is not int or x<0 or x>=HORIZON for x in slots):
        raise ValueError("two arrival ticks 0..3 required")
    return tuple(slots.count(t) for t in range(HORIZON))


def simulate(a, b, policy, *, capacity=2, loss_weight=5, terminal_weight=2):
    if policy not in SERVICE or len(a)!=HORIZON or len(b)!=HORIZON:
        raise ValueError("bad tape or policy")
    if any(type(x) is not int or x<0 for x in a+b):
        raise ValueError("nonnegative integer arrivals required")
    if type(capacity) is not int or capacity<1 or type(loss_weight) is not int or loss_weight<0 or type(terminal_weight) is not int or terminal_weight<0:
        raise ValueError("bad parameters")
    queue=[0,0]; lost=0; holding=0; served=0; log=[]
    for t, lane in enumerate(SERVICE[policy]):
        inbound=(a[t],b[t])
        for i in range(2):
            can_admit=min(inbound[i],max(0,capacity-queue[i]))
            lost+=inbound[i]-can_admit
            queue[i]+=can_admit
        if queue[lane]:
            queue[lane]-=1; served+=1
        holding+=sum(queue)
        log.append(tuple(queue))
    assert sum(a+b)==served+lost+sum(queue)
    cost=holding+loss_weight*lost+terminal_weight*sum(queue)
    return dict(cost=cost,holding=holding,lost=lost,served=served,
                terminal=sum(queue),trace=tuple(log))


def screen():
    slots=list(combinations_with_replacement(range(HORIZON),2))
    worlds=[]
    for sa,sb in product(slots,repeat=2):
        a,b=tape_from_slots(sa),tape_from_slots(sb)
        left=simulate(a,b,"AABB");right=simulate(a,b,"BBAA")
        worlds.append(dict(a=sa,b=sb,delta=left["cost"]-right["cost"],
                           a_cost=left["cost"],b_cost=right["cost"],
                           a_lost=left["lost"],b_lost=right["lost"]))
    neg=[w for w in worlds if w["delta"]<0]
    pos=[w for w in worlds if w["delta"]>0]
    ties=[w for w in worlds if w["delta"]==0]
    pair=None
    if neg and pos:
        # Entire same aggregate demand (two arrivals per lane), clocks differ.
        pair=(min(neg,key=lambda w:(abs(w["delta"]),w["a"],w["b"])),
              min(pos,key=lambda w:(abs(w["delta"]),w["a"],w["b"])))
    return {"world_count":len(worlds),"negative":len(neg),"positive":len(pos),
            "ties":len(ties),"delta_distribution":dict(sorted(Counter(w["delta"] for w in worlds).items())),
            "witness":pair,"scope":"ARTIFICIAL_FINITE_QUEUE_CLOCK_SCREEN_NOT_PHYS_OR_FIELD"}


def frozen_json():
    return json.dumps(screen(),sort_keys=True,indent=2)+"\n"

if __name__=="__main__":
    print(frozen_json(),end="")
