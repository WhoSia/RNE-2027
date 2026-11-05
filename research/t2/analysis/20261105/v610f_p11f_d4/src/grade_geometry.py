"""Loss-aware level/height-aware crossing and turn-pocket geometry contract."""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class WayGeometry:
    id:str
    points:tuple[tuple[float,float],...]
    layer:int|None=None
    elevation_m:float|None=None
    kind:str='road'
    def __post_init__(self):
        if not self.id or len(self.points)<2 or self.kind not in {'road','bridge','tunnel','footway','rail','cycleway'}:raise ValueError('bad way')
        if any(not all(isfinite(v) for v in p) for p in self.points):raise ValueError('bad coordinates')
        if self.elevation_m is not None and not isfinite(self.elevation_m):raise ValueError('bad elevation')

@dataclass(frozen=True)
class TurnPocket:
    parent_lane:str
    pocket_lane:str
    length_m:float
    permitted_turns:frozenset[str]
    source_id:str
    def __post_init__(self):
        if not self.parent_lane or not self.pocket_lane or self.parent_lane==self.pocket_lane or not self.source_id:raise ValueError('invalid pocket')
        if self.length_m<=0 or not isfinite(self.length_m) or not self.permitted_turns or not self.permitted_turns<={'left','right','uturn','straight'}:raise ValueError('bad pocket')
    def capacity_upper_bound(self,footprint_m):
        if footprint_m<=0 or not isfinite(footprint_m):raise ValueError('bad footprint')
        return int(self.length_m//footprint_m)  # upper bound, not dynamic queue length

def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def strict_cross(a,b,c,d):
    vals=(orient(a,b,c),orient(a,b,d),orient(c,d,a),orient(c,d,b))
    return vals[0]*vals[1]<0 and vals[2]*vals[3]<0

def audit_crossing(w1:WayGeometry,w2:WayGeometry):
    crosses=[(i,j) for i,(a,b) in enumerate(zip(w1.points,w1.points[1:]))
             for j,(c,d) in enumerate(zip(w2.points,w2.points[1:])) if strict_cross(a,b,c,d)]
    if not crosses:return {'status':'NO_STRICT_PLANAR_CROSSING','intersections':0,'evidence':'computed geometry only'}
    if w1.layer is None or w2.layer is None:
        return {'status':'UNKNOWN_3D_RELATION','intersections':len(crosses),'evidence':'missing explicit layer'}
    if w1.layer!=w2.layer:
        return {'status':'GRADE_SEPARATED_DECLARED','intersections':len(crosses),'evidence':'different sourced levels required'}
    return {'status':'SAME_LEVEL_CONFLICT_POSSIBLE','intersections':len(crosses),'evidence':'planar crossing at same declared layer; not automatic junction'}
