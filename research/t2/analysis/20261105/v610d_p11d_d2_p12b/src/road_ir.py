"""Loss-aware lane-level intermediate road graph, not a safety-certified network.

Adapters are strict: an unknown turn/conflict/signal mapping is never inferred as safe.
This IR is a topology data-contract; not a kinematic simulator or complete world map.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite
from xml.etree import ElementTree as ET

TURNS = {'left', 'right', 'straight', 'uturn', 'unknown'}

@dataclass(frozen=True)
class RoadLane:
    id: str
    length_m: float
    speed_mps: float
    permissions: tuple[str, ...] = ('passenger',)
    def __post_init__(self):
        if not self.id or not all(isfinite(v) and v>0 for v in (self.length_m,self.speed_mps)):
            raise ValueError('invalid road lane')

@dataclass(frozen=True)
class LaneConnection:
    id: str
    source: str
    destination: str
    junction: str
    direction: str = 'unknown'
    signal_id: str | None = None
    signal_index: int | None = None
    def __post_init__(self):
        if not self.id or self.direction not in TURNS or self.source==self.destination:
            raise ValueError('invalid lane connection')
        if self.signal_index is not None and (self.signal_id is None or self.signal_index<0):
            raise ValueError('unbound signal index')

@dataclass(frozen=True)
class RoadIR:
    lanes: tuple[RoadLane, ...]
    connections: tuple[LaneConnection, ...]
    provenance: str
    unresolved: tuple[str, ...] = ()
    def __post_init__(self):
        lids={l.id for l in self.lanes}; cids={c.id for c in self.connections}
        if len(lids)!=len(self.lanes) or len(cids)!=len(self.connections):
            raise ValueError('duplicate lane or movement')
        slots=set()
        for c in self.connections:
            if c.source not in lids or c.destination not in lids:
                raise ValueError(f'broken lane link: {c.id}')
            if c.signal_id is not None and c.signal_index is not None:
                key=(c.signal_id,c.signal_index)
                # SUMO can control >1 connections by one linkIndex, but that grouping
                # must be declared rather than silently treated as mutually exclusive.
                slots.add(key)
    def neighbors(self, lane):
        return tuple(c.destination for c in self.connections if c.source==lane)
    def route_exists(self, lanes):
        if not lanes or lanes[0] not in {l.id for l in self.lanes}:return False
        return all(b in self.neighbors(a) for a,b in zip(lanes,lanes[1:]))
    def summary(self):
        return {'lanes':len(self.lanes),'connections':len(self.connections),
                'junctions':len({c.junction for c in self.connections}),
                'signaled_links':sum(c.signal_id is not None for c in self.connections),
                'unresolved':list(self.unresolved),'provenance':self.provenance}

def import_cityflow(roadnet:dict, *, provenance:str='cityflow:provided') -> RoadIR:
    """Imports road/lanes/roadlinks/lanelinks; explicit traffic conflicts remain unresolved."""
    if not isinstance(roadnet,dict) or not isinstance(roadnet.get('roads'),list) or not isinstance(roadnet.get('intersections'),list):
        raise ValueError('bad CityFlow roadnet')
    lanes=[]; road_lanes={}; unresolved=['lane_conflicts_not_inferred','signal_phases_not_imported']
    for road in roadnet['roads']:
        rid=road['id']; pts=road.get('points',[])
        length=0.
        for a,b in zip(pts,pts[1:]):length+=((float(b['x'])-float(a['x']))**2+(float(b['y'])-float(a['y']))**2)**.5
        if length<=0:raise ValueError(f'road {rid} has no measurable length')
        indices=[]
        for i,l in enumerate(road['lanes']):
            lid=f'{rid}_{i}'; lanes.append(RoadLane(lid,length,float(l['maxSpeed'])));indices.append(lid)
        road_lanes[rid]=indices
    conns=[]
    turn={'turn_left':'left','turn_right':'right','go_straight':'straight'}
    for inter in roadnet['intersections']:
        if inter.get('virtual',False):continue
        for ri,link in enumerate(inter.get('roadLinks',[])):
            src=road_lanes[link['startRoad']];dst=road_lanes[link['endRoad']]
            for li,ll in enumerate(link['laneLinks']):
                a=int(ll['startLaneIndex']); b=int(ll['endLaneIndex'])
                if a<0 or a>=len(src) or b<0 or b>=len(dst):raise ValueError('invalid laneLink index')
                conns.append(LaneConnection(f'{inter["id"]}:{ri}:{li}',src[a],dst[b],inter['id'],turn.get(link.get('type'),'unknown')))
    return RoadIR(tuple(lanes),tuple(conns),provenance,tuple(unresolved))

def import_sumo_net(xml_text:str, *, provenance:str='sumo:provided') -> RoadIR:
    """Read-only SUMO .net.xml subset. Avoid XML external entities via stdlib ElementTree.
    Lane geometry may be internal to SUMO; no crossing conflict geometry inferred.
    """
    root=ET.fromstring(xml_text)
    if root.tag!='net':raise ValueError('expected SUMO net')
    lanes=[];edge_lanes={};unresolved=['geometric_conflicts_not_inferred','signal_state_program_not_bound']
    for e in root.findall('edge'):
        if e.attrib.get('function')=='internal':continue
        key=e.attrib['id']; edge_lanes[key]=[]
        for lane in e.findall('lane'):
            lid=lane.attrib['id'];edge_lanes[key].append(lid)
            lanes.append(RoadLane(lid,float(lane.attrib['length']),float(lane.attrib['speed'])))
    conns=[]
    for i,c in enumerate(root.findall('connection')):
        if c.attrib.get('from','').startswith(':') or c.attrib.get('to','').startswith(':'):continue
        a=edge_lanes[c.attrib['from']][int(c.attrib['fromLane'])]
        b=edge_lanes[c.attrib['to']][int(c.attrib['toLane'])]
        direction={'s':'straight','l':'left','r':'right','t':'uturn','L':'left','R':'right'}.get(c.attrib.get('dir'),'unknown')
        tl=c.attrib.get('tl');idx=int(c.attrib['linkIndex']) if 'linkIndex' in c.attrib else None
        conns.append(LaneConnection(f'conn:{i}',a,b,c.attrib.get('via','junction:unknown'),direction,tl,idx))
    if not conns:unresolved.append('no_explicit_connections')
    return RoadIR(tuple(lanes),tuple(conns),provenance,tuple(unresolved))

def import_osmnx_graph(graph, *, provenance='osmnx:provided') -> RoadIR:
    """Import directed OSMnx/NetworkX MultiDiGraph *road-segment skeleton*.

    Since segment geometry does not define permitted lane-to-lane turns, this
    deliberately returns NO authorized connections. It is not simulation-ready.
    Caller must supply regulatory turn restrictions and actual lane layout.
    """
    if not graph.is_directed() or not graph.is_multigraph():
        raise ValueError('expected directed MultiDiGraph from OSMnx')
    lanes=[]
    for u,v,key,attr in graph.edges(keys=True,data=True):
        dist=attr.get('length')
        speed=attr.get('speed_kph')
        if isinstance(speed,(tuple,list)):raise ValueError('ambiguous speed limit')
        if dist is None or speed is None:
            raise ValueError('missing road length or speed; no fabricated defaults')
        lanes.append(RoadLane(f'{u}>{v}:{key}',float(dist),float(speed)/3.6))
    return RoadIR(tuple(lanes),(),provenance,('lane_count_unverified','turn_restrictions_unverified',
                   'signal_groups_unverified','road_segment_only_not_simulation_ready'))
