"""Conservative definition of an observed stopped-vehicle queue.

This is an estimator when lane-local positions, vehicle identity and a measured
stop line are available. It explicitly does not synthesize field observations.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class LaneMeasurement:
    lane_id: str
    stopline_s_m: float
    upstream_limit_m: float
    stationary_threshold_mps: float = 0.5

    def __post_init__(self):
        if not self.lane_id or not all(isfinite(x) for x in
            (self.stopline_s_m, self.upstream_limit_m, self.stationary_threshold_mps)):
            raise ValueError('lane-specific calibrated stopline required')
        if self.upstream_limit_m <= 0 or self.stationary_threshold_mps <= 0:
            raise ValueError('invalid measurement envelope')

@dataclass(frozen=True)
class Track:
    vehicle_id: str
    time_s: float
    lane_id: str
    front_s_m: float
    speed_mps: float


def count_stopped_approach(tracks: list[Track], lane: LaneMeasurement, time_s: float) -> dict:
    """Count stationary vehicles within an audited upstream observation window.

    front_s_m is calibrated curvilinear position in lane coordinates, increasing
    in the driving direction. This counts *stopped vehicles within a window*,
    not necessarily a contiguous physical queue. No queue length is inferred.
    """
    if not isfinite(time_s): raise ValueError('nonfinite requested time')
    chosen=[x for x in tracks if x.lane_id==lane.lane_id and x.time_s==time_s]
    ids=[x.vehicle_id for x in chosen]
    if len(set(ids))!=len(ids): raise ValueError('duplicate vehicle/time records')
    if any(not all(isfinite(z) for z in (x.front_s_m,x.speed_mps)) or x.speed_mps<-0.5 for x in chosen):
        raise ValueError('invalid observed track')
    stopped=[x for x in chosen if 0<=lane.stopline_s_m-x.front_s_m<=lane.upstream_limit_m
             and x.speed_mps<lane.stationary_threshold_mps]
    return {'lane_id':lane.lane_id,'time_s':time_s,
            'observed_vehicles_in_window':len([x for x in chosen if 0<=lane.stopline_s_m-x.front_s_m<=lane.upstream_limit_m]),
            'stationary_count':len(stopped),'measurement':'stopped vehicles in calibrated lane window; not queue length or spillback distance'}
