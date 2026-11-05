"""Time-indexed lane orientation. Transition to opposing direction requires external clearance evidence."""
from dataclasses import dataclass
from datetime import datetime
from road_rules import Window

@dataclass(frozen=True)
class LaneWindow:
    direction:str
    window:Window
    source_id:str
    def __post_init__(self):
        if self.direction not in {'forward','reverse','closed'} or not self.source_id:raise ValueError('bad rule')

class ReversibleLane:
    def __init__(self,lane_id,rules,timezone):
        from zoneinfo import ZoneInfo
        self.lane_id=lane_id;self.rules=tuple(rules);self.zone=ZoneInfo(timezone)
        if not lane_id or not self.rules:raise ValueError('missing reversible lane schedule')
    def state_at(self,instant:datetime):
        if instant.tzinfo is None:raise ValueError('timezone required')
        local=instant.astimezone(self.zone)
        hits=[x.direction for x in self.rules if x.window.active(local)]
        if len(hits)!=1:return {'status':'UNKNOWN' if not hits else 'CONFLICT', 'direction':None}
        if hits[0]=='closed':return {'status':'CLOSED','direction':None}
        return {'status':'DECLARED_DIRECTION_ONLY','direction':hits[0],
                'warning':'No occupancy/clearance verification: not operational authority'}
