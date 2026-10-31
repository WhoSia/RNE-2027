"""Conservative frame-based spillback diagnosis, not causal proof.

Input is an existing dual_lane_v11.run(..., trace=True) result.
After-tick occupancy establishes simultaneous signatures, but cannot
by itself establish that a specific vehicle was denied service.
"""
from collections import Counter,defaultdict

def diagnose(result):
    frames=result.get("frames")
    if frames is None:raise ValueError("trace=True required")
    if result["config"]["receiver_mode"]!="cells":
        raise ValueError("physical receiving cells required")
    base=result["config"]["base"]
    k=int(base["pocket_length_m"]//base["cell_m"])
    signatures=Counter()
    trajectory={}
    transitions=Counter()
    stopped=Counter()
    for frame in frames:
        t=frame["t"]
        current={}
        for lane in ("A","B"):
            for cell,vid,route in frame[lane]:
                if vid in current:raise AssertionError("duplicate vehicle")
                current[vid]=(lane,cell,route)
        for cell,vid in frame["pocket"]:
            if vid in current:raise AssertionError("duplicate vehicle")
            current[vid]=("pocket",cell,"L")
        for cell,vid,route in frame["receiver"]:
            if vid in current:raise AssertionError("duplicate vehicle")
            current[vid]=("receiver",cell,route)
        for vid,loc in current.items():
            if vid in trajectory:
                old=trajectory[vid]
                if old[:2]==loc[:2]:stopped[vid]+=1
                if old[0]!=loc[0]:transitions[old[0]+"->"+loc[0]]+=1
        receiver0=any(cell==0 for cell,vid,route in frame["receiver"])
        stopline=any(cell==-1 and route=="S" for lane in ("A","B")
                     for cell,vid,route in frame[lane]) or any(
                     cell==-1 for cell,vid in frame["pocket"])
        fork=(k>0 and any(cell==-k for cell,vid in frame["pocket"])
              and any(cell==-k-1 and route=="L" for cell,vid,route in frame["A"]))
        if receiver0:
            signatures["receiver_entry_cell_occupied_frames"]+=1
            if stopline:signatures["receiver_occupied_and_stopline_waiting_frames"]+=1
        if fork:
            signatures["pocket_entry_block_signature_frames"]+=1
            if frame["signal"]=="S":
                signatures["fork_signature_through_green_frames"]+=1
        trajectory=current
    return {"world_status":"SYNTHETIC_DIAGNOSTIC_NOT_CAUSAL_PROOF",
       "frames":len(frames),"signatures":dict(signatures),
       "movement_transitions":dict(transitions),
       "stopped_vehicle_seconds_total":sum(stopped.values()),
       "model_denied_entry_counter":result["receiver_full_denied_s"],
       "model_fork_block_counter":result["pocket_block_seconds"],
       "warning":"After-tick co-occupancy is not a precise service-attempt event."}
