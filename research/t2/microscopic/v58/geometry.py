"""Synthetic lane-centreline crossing graph. Geometry NOT a surveyed intersection.

Units metres. Crossing centreline / shared entry or exit lane generates a
conservative conflict; following headways, width, clearance times are NOT solved.
"""
from dataclasses import dataclass
from itertools import combinations

# Coordinates use right-hand traffic. Lane separation is 4 m.
ENTRY = {'N':(-2.,30.), 'S':(2.,-30.), 'E':(30.,2.), 'W':(-30.,-2.)}
EXIT  = {'N':(2.,30.), 'S':(-2.,-30.), 'E':(30.,-2.), 'W':(-30.,2.)}
OPPOSITE = {'N':'S','S':'N','E':'W','W':'E'}
RIGHT = {'N':'W','W':'S','S':'E','E':'N'}
LEFT = {'N':'E','E':'S','S':'W','W':'N'}

def movement_id(origin, destination):
    if origin not in ENTRY or destination not in EXIT or origin==destination:
        raise ValueError('invalid approach or destination')
    return f'{origin}>{destination}'

@dataclass(frozen=True)
class Path:
    name: str
    origin: str
    destination: str
    points: tuple[tuple[float,float], ...]


def path(origin,destination):
    name=movement_id(origin,destination)
    begin,end=ENTRY[origin],EXIT[destination]
    if destination==OPPOSITE[origin]:
        # Longitudinal travel at lane offset; two opposing through moves parallel.
        pts=(begin,end)
    elif destination==RIGHT[origin]:
        # Conservative cornering approximation through corner of entering and exit lanes.
        corner=(end[0],begin[1]) if origin in ('N','S') else (begin[0],end[1])
        pts=(begin,corner,end)
    else:
        # Protected left turn via center intersection. These are coarse centerlines.
        pts=(begin,(0.,0.),end)
    return Path(name,origin,destination,pts)

def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def point_on_segment(a,b,p,eps=1.e-9):
    return abs(orient(a,b,p))<=eps and min(a[0],b[0])-eps<=p[0]<=max(a[0],b[0])+eps and min(a[1],b[1])-eps<=p[1]<=max(a[1],b[1])+eps

def segments_intersect(a,b,c,d):
    o1,o2,o3,o4=orient(a,b,c),orient(a,b,d),orient(c,d,a),orient(c,d,b)
    if o1*o2<0 and o3*o4<0:return True
    return any((abs(o1)<1e-9 and point_on_segment(a,b,c),abs(o2)<1e-9 and point_on_segment(a,b,d),abs(o3)<1e-9 and point_on_segment(c,d,a),abs(o4)<1e-9 and point_on_segment(c,d,b)))

def conflict(a:Path,b:Path):
    if a.origin==b.origin or a.destination==b.destination:return True
    return any(segments_intersect(p,q,r,s)
               for p,q in zip(a.points,a.points[1:])
               for r,s in zip(b.points,b.points[1:]))

class GeometryGraph:
    def __init__(self, movements=None):
        self.paths={p.name:p for p in (movements if movements is not None else
                        (path(i,j) for i in ENTRY for j in EXIT if i!=j))}
        if len(self.paths)==0:raise ValueError('empty movements')
        self.incompatible=frozenset(frozenset((a,b)) for a,b in combinations(self.paths,2)
                                      if conflict(self.paths[a],self.paths[b]))
    def compatible(self,stage):
        s=list(stage)
        return len(s)==len(set(s)) and set(s)<=set(self.paths) and all(not p<=set(s) for p in self.incompatible)
    def maximal_stages(self):
        names=tuple(self.paths)
        valid=[frozenset(c) for n in range(1,len(names)+1) for c in combinations(names,n) if self.compatible(c)]
        return tuple(tuple(sorted(s)) for s in valid if not any(s<t for t in valid))


def audit_occupancy(events, graph,dt=0.5):
    """Checks discrete bin concurrency, NOT continuous swept envelopes."""
    if dt<=0:raise ValueError('dt')
    bins={}
    for e in events:
        key=(int(e['junction']),round(float(e['t_s'])/dt))
        bins.setdefault(key,[]).append(e['movement'])
    violations=[(key,m) for key,m in bins.items() if not graph.compatible(m)]
    return {'events':len(events),'slots':len(bins),'violations':violations}

def segment_distance(a,b,c,d):
    """Minimum planar distance in metres between two finite line segments."""
    if segments_intersect(a,b,c,d):return 0.0
    def point_dist(p,u,v):
        dx,dy=v[0]-u[0],v[1]-u[1]
        denom=dx*dx+dy*dy
        if denom==0:return ((p[0]-u[0])**2+(p[1]-u[1])**2)**.5
        f=max(0.,min(1.,((p[0]-u[0])*dx+(p[1]-u[1])*dy)/denom))
        return ((p[0]-u[0]-f*dx)**2+(p[1]-u[1]-f*dy)**2)**.5
    return min(point_dist(a,c,d),point_dist(b,c,d),point_dist(c,a,b),point_dist(d,a,b))

def clearance_conflict(a:Path,b:Path,required_centerline_separation=2.5):
    """Conservative swept-lane envelope test; not speed-dependent collision risk."""
    if required_centerline_separation<0:raise ValueError('separation')
    if a.origin==b.origin or a.destination==b.destination:return True
    return any(segment_distance(p,q,r,s)<=required_centerline_separation+1e-10
               for p,q in zip(a.points,a.points[1:])
               for r,s in zip(b.points,b.points[1:]))

class ClearanceGraph(GeometryGraph):
    def __init__(self, required_centerline_separation=2.5, movements=None):
        if required_centerline_separation<0:raise ValueError('separation')
        super().__init__(movements)
        self.separation=required_centerline_separation
        self.incompatible=frozenset(frozenset((a,b)) for a,b in combinations(self.paths,2)
                                      if clearance_conflict(self.paths[a],self.paths[b],self.separation))
