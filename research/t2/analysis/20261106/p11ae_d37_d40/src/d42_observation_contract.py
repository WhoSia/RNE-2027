"""D42 offline data-alignment audit. No claims about real-field results."""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class Sample:
    t_s: float
    object_id: str
    lane_id: str
    center_m: float
    speed_mps: float

@dataclass(frozen=True)
class SignalSample:
    t_s: float
    head_id: str
    state: str

def audit_trajectories(records, max_step_s=0.050001):
    issues = []
    prev = {}
    for r in records:
        if not r.object_id or not r.lane_id or not all(map(isfinite, (r.t_s, r.center_m, r.speed_mps))):
            issues.append(("invalid_record", r.object_id))
            continue
        if r.object_id in prev:
            old = prev[r.object_id]
            if r.t_s <= old.t_s:
                issues.append(("non_increasing_timestamp", r.object_id))
            if r.t_s - old.t_s > max_step_s:
                issues.append(("tracking_gap", r.object_id))
            if (r.lane_id == old.lane_id and
                abs(r.center_m - old.center_m) >
                    max(r.t_s - old.t_s, 0) * max(r.speed_mps, old.speed_mps, 0) + 2):
                issues.append(("position_jump", r.object_id))
        prev[r.object_id] = r
    return issues

def align_signal_at_event(t_s, signal_samples, *, head_id, max_age_s=1.0):
    """A sampled indication is NOT event-time truth between observations."""
    if not isfinite(t_s):
        raise ValueError("nonfinite event time")
    rows = sorted((s for s in signal_samples if s.head_id == head_id and isfinite(s.t_s)),
                  key=lambda s: s.t_s)
    prior = [s for s in rows if s.t_s <= t_s]
    if not prior:
        return {"state": None, "status": "UNKNOWN", "reason": "no_preceding_sample"}
    s = prior[-1]
    if t_s - s.t_s > max_age_s:
        return {"state": None, "status": "UNKNOWN", "reason": "stale_sample"}
    if s.state not in {"RED", "YELLOW", "GREEN"}:
        return {"state": None, "status": "UNKNOWN", "reason": "ambiguous_state"}
    return {"state": s.state, "status": "LAST_OBSERVED_NOT_EVENT_TRUTH",
            "age_s": round(t_s - s.t_s, 6)}

def crossing_event(before, after, stopline_m):
    """Return interval for center crossing; do not invent exact event time."""
    if before.object_id != after.object_id or before.lane_id != after.lane_id:
        return None
    if not (isfinite(stopline_m) and before.t_s < after.t_s):
        return None
    if before.center_m < stopline_m <= after.center_m:
        return {"vehicle": after.object_id, "lane": after.lane_id,
                "t_lower_s": before.t_s, "t_upper_s": after.t_s,
                "status": "INTERVAL_CENSORED_CROSSING"}
    return None
