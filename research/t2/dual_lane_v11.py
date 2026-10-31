"""T2 v1.1 two through lanes and a finite physical turn pocket.

L cars preposition in lane A; straight cars route to A/B before approach.
Optional A->B lateral move requires empty target, front and rear cells
and an upstream zone. No simultaneous forward move during lane-change.
This is a synthetic minimal mesoscopic approximation, not real gap acceptance.
"""
from dataclasses import dataclass,asdict
from collections import deque,Counter
from math import floor
import random
from spatial_v10 import Config,validate,phase,arrivals

@dataclass(frozen=True)
class DualConfig:
    base:Config=Config()
    through_B_share:float=.5
    allow_lane_changes:bool=False
    change_zone_m:float=100.
    downstream_conflict_gap_s:int=0 # optional shared exit conflict; 0 disables
    receiver_slots:int=0 # zero disables finite receiving buffer
    receiver_headway_s:int=2

def run(c:DualConfig=DualConfig(),events=None,*,trace=False):
    n,k=validate(c.base)
    if not 0<=c.through_B_share<=1 or not 0<=c.change_zone_m<=c.base.approach_length_m:
        raise ValueError("invalid lane settings")
    if not isinstance(c.downstream_conflict_gap_s,int) or c.downstream_conflict_gap_s<0:
        raise ValueError("invalid common exit headway")
    if not isinstance(c.receiver_slots,int) or c.receiver_slots<0 or not isinstance(c.receiver_headway_s,int) or c.receiver_headway_s<1:
        raise ValueError("invalid downstream receiver")
    if events is None:events=arrivals(c.base)
    if any(not isinstance(t,int) or not 0<=t<c.base.duration_s or r not in ("L","S")
           for t,r in events) or any(events[i][0]>events[i+1][0] for i in range(len(events)-1)):
        raise ValueError("invalid arrival events")
    rng=random.Random(c.base.seed+193)
    outside={"A":deque(),"B":deque()}
    A={};B={};pocket={};index=0
    count=Counter();last={"A":-999999,"B":-999999,"L":-999999}
    admission={"A":-999999,"B":-999999};cycles=[];frames=[]
    last_common_exit=-999999
    receiver=deque();last_receiver_service=-999999
    for t in range(c.base.duration_s):
        while index<len(events) and events[index][0]==t:
            route=events[index][1]
            lane="A" if route=="L" or rng.random()>=c.through_B_share else "B"
            outside[lane].append((index,route,t));index+=1
        if receiver and t-last_receiver_service>=c.receiver_headway_s:
            vehicle=receiver.popleft();count["network_out_"+vehicle[1]]+=1
            last_receiver_service=t
        light=phase(c.base,t)
        if light=="S":
            for lane,occ in (("A",A),("B",B)):
                if -1 in occ and occ[-1][1]=="S" and t-last[lane]>=c.base.departure_headway_s:
                    if c.downstream_conflict_gap_s and t-last_common_exit<c.downstream_conflict_gap_s:
                        count["common_exit_denied_s"]+=1
                    elif c.receiver_slots and len(receiver)>=c.receiver_slots:
                        count["receiver_full_denied_s"]+=1
                    else:
                        v=occ.pop(-1);count["exit_S"]+=1
                        if c.receiver_slots:receiver.append(v)
                        else:count["network_out_S"]+=1
                        count["time_S_s"]+=t-v[2];last[lane]=t;last_common_exit=t
        elif light=="L" and -1 in pocket and t-last["L"]>=c.base.departure_headway_s:
            if c.downstream_conflict_gap_s and t-last_common_exit<c.downstream_conflict_gap_s:
                count["common_exit_denied_s"]+=1
            elif c.receiver_slots and len(receiver)>=c.receiver_slots:
                count["receiver_full_denied_s"]+=1
            else:
                v=pocket.pop(-1);count["exit_L"]+=1
                if c.receiver_slots:receiver.append(v)
                else:count["network_out_L"]+=1
                count["time_L_s"]+=t-v[2];last["L"]=t;last_common_exit=t
        for x in sorted(tuple(pocket),reverse=True):
            if x< -1 and x+1 not in pocket:pocket[x+1]=pocket.pop(x)
        for lane,occ in (("A",A),("B",B)):
            for x in sorted(tuple(occ),reverse=True):
                if x not in occ:continue
                v=occ[x]
                if lane=="A" and v[1]=="L" and k>0 and x==-k-1:
                    if -k not in pocket:
                        pocket[-k]=occ.pop(x);count["merges"]+=1
                    else:count["pocket_block_seconds"]+=1
                elif lane=="A" and v[1]=="L" and k==0 and x==-1:
                    count["pocket_block_seconds"]+=1
                elif x< -1 and x+1 not in occ and not(lane=="A" and v[1]=="L" and x>=-k-1):
                    occ[x+1]=occ.pop(x)
        if c.allow_lane_changes:
            zone=floor(c.change_zone_m/c.base.cell_m+1e-9)
            for x in sorted(tuple(A),reverse=True):
                if x not in A or A[x][1]!="S" or x>=-k or x< -zone:continue
                if x not in B and x-1 not in B and x+1 not in B:
                    if x+1 in A and (A[x+1][1]=="L" or x+2 in A):
                        B[x]=A.pop(x);count["changes_A_to_B"]+=1
        for lane,occ in (("A",A),("B",B)):
            if outside[lane] and -n not in occ and t-admission[lane]>=c.base.entry_headway_s:
                occ[-n]=outside[lane].popleft();count["admitted"]+=1;admission[lane]=t
        out=len(outside["A"])+len(outside["B"])
        count["max_receiver"]=max(count["max_receiver"],len(receiver))
        if index!=count["network_out_S"]+count["network_out_L"]+out+len(A)+len(B)+len(pocket)+len(receiver):
            raise AssertionError(("conservation",t))
        if any(len(occ)>n or any(x< -n or x>-1 for x in occ) for occ in (A,B)) or len(pocket)>k or (c.receiver_slots and len(receiver)>c.receiver_slots):
            raise AssertionError(("road geometry",t))
        ids=[v[0] for occ in (A,B,pocket) for v in occ.values()]+[v[0] for v in receiver]
        if len(ids)!=len(set(ids)):raise AssertionError(("duplicate vehicle",t))
        if trace:
            frames.append({"t":t,"signal":light,
                "A":sorted((x,v[0],v[1]) for x,v in A.items()),
                "B":sorted((x,v[0],v[1]) for x,v in B.items()),
                "pocket":sorted((x,v[0]) for x,v in pocket.items()),"outside":out,
                "receiver":[v[0] for v in receiver]})
        if (t+1)%c.base.cycle_s==0 or t==c.base.duration_s-1:
            cycles.append({"end_s":t+1,"exit_S":count["exit_S"],"exit_L":count["exit_L"],
                "A":len(A),"B":len(B),"pocket":len(pocket),"outside":out,
                "receiver":len(receiver),"network_out_S":count["network_out_S"],
                "network_out_L":count["network_out_L"]})
    outside_total=len(outside["A"])+len(outside["B"])
    result={"status":"SYNTHETIC_UNCALIBRATED",
        "config":{"base":asdict(c.base),"through_B_share":c.through_B_share,
                  "allow_lane_changes":c.allow_lane_changes,"change_zone_m":c.change_zone_m,
                  "downstream_conflict_gap_s":c.downstream_conflict_gap_s,
                  "receiver_slots":c.receiver_slots,"receiver_headway_s":c.receiver_headway_s},
        "generated":len(events),"admitted":count["admitted"],
        "exit_S":count["exit_S"],"exit_L":count["exit_L"],
        "remaining":outside_total+len(A)+len(B)+len(pocket)+len(receiver),
        "network_out_S":count["network_out_S"],"network_out_L":count["network_out_L"],
        "receiver_final":len(receiver),"max_receiver":count["max_receiver"],
        "receiver_full_denied_s":count["receiver_full_denied_s"],
        "outside":outside_total,"pocket_slots":k,"through_slots_per_lane":n,
        "pocket_block_seconds":count["pocket_block_seconds"],
        "changes_A_to_B":count["changes_A_to_B"],
        "common_exit_denied_s":count["common_exit_denied_s"],
        "mean_time_S_s":count["time_S_s"]/count["exit_S"] if count["exit_S"] else None,
        "mean_time_L_s":count["time_L_s"]/count["exit_L"] if count["exit_L"] else None,
        "cycles":cycles}
    if trace:result["frames"]=frames
    return result
