"""DLR UT: conservative as-of timestamp join. Does not map head IDs to lanes.

NO interpolation across unknown intervals; no assumed traffic light state semantics.
Source raw CSV: traffic-lights_230924-120000_230924-121500.csv.
"""
from bisect import bisect_right
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class AsOfResult:
    raw_state: int | None
    age_s: float | None
    reason: str

def asof_state(times, states, query, max_age_s=1.05):
    """Strictly earlier or same observation only; old samples return UNKNOWN."""
    if not isfinite(max_age_s) or max_age_s < 0:
        raise ValueError("max_age_s must be finite and nonnegative")
    if len(times) != len(states) or not times:
        raise ValueError("nonempty matching timestamp/state series required")
    if any(t1 <= t0 for t0,t1 in zip(times,times[1:])):
        raise ValueError("strictly increasing signal source timestamps required")
    i = bisect_right(times, query)-1
    if i < 0:
        return AsOfResult(None,None,"no_prior_sample")
    age=(query-times[i]).total_seconds()
    if age>max_age_s:
        return AsOfResult(None,age,"stale")
    return AsOfResult(int(states[i]),age,"observed_prior")
