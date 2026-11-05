"""Strict, research-only ASAM OpenDRIVE subset import and 3D reference-line sampling.

Unsupported geometries/junction features fail closed as unresolved, never approved
as real drivable turns. This IS NOT a standard-complete OpenDRIVE decoder.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import sin, cos, isfinite, fabs, ceil
from bisect import bisect_right
from xml.etree import ElementTree as ET

KINDS = {'line', 'arc', 'spiral'}

@dataclass(frozen=True)
class Geometry:
    s: float
    x: float
    y: float
    hdg: float
    length: float
    kind: str
    curvature: float = 0.0
    curvature_end: float | None = None
    def __post_init__(self):
        if (self.kind=='spiral' and self.curvature_end is None) or self.kind not in KINDS or not all(isfinite(v) for v in (self.s,self.x,self.y,self.hdg,self.length,self.curvature)) or (self.curvature_end is not None and not isfinite(self.curvature_end)) or self.s < 0 or self.length <= 0:
            raise ValueError('bad supported plan geometry')

def _simpson_clothoid(g:Geometry, ds:float):
    """Numerically integrate dxy/ds=[cos(theta),sin(theta)]; deterministic Simpson.

    Curvature k(s)=k0+(k1-k0)*s/L. This is a research reference;
    scipy Fresnel is used independently ONLY in tests, not runtime.
    """
    if ds<=0: return g.x,g.y,g.hdg
    k0=g.curvature; slope=(g.curvature_end-k0)/g.length
    def theta(t): return g.hdg+k0*t+0.5*slope*t*t
    # At least 64 intervals, and ~20 intervals per full radian of phase travel.
    span=abs(k0*ds+0.5*slope*ds*ds)
    n=max(64,2*ceil(ds*8),2*ceil((span+1)*100))
    h=ds/n; xc=cos(theta(0))+cos(theta(ds));yc=sin(theta(0))+sin(theta(ds))
    for i in range(1,n):
        t=i*h; w=4 if i%2 else 2
        xc+=w*cos(theta(t));yc+=w*sin(theta(t))
    return g.x+xc*h/3,g.y+yc*h/3,theta(ds)


@dataclass(frozen=True)
class Cubic:
    s: float
    a: float
    b: float
    c: float
    d: float
    def at(self, absolute_s):
        ds=absolute_s-self.s
        return ((self.d*ds+self.c)*ds+self.b)*ds+self.a

@dataclass(frozen=True)
class LaneDef:
    road: str
    section_s: float
    lane_id: int
    lane_type: str
    widths: tuple[Cubic,...]
    def width_at(self,absolute_s):
        if not self.widths:return None
        ds=absolute_s-self.section_s
        positions=[c.s for c in self.widths]
        i=bisect_right(positions,ds)-1
        if i<0:return None
        result=self.widths[i].at(ds)
        return result if result>=0 else None

@dataclass(frozen=True)
class RoadDef:
    road_id: str
    length_m: float
    geometries: tuple[Geometry,...]
    elevations: tuple[Cubic,...]
    sections: tuple[tuple[float,tuple[LaneDef,...]],...]
    unsupported: tuple[str,...]
    def reference_at(self,s):
        if not 0<=s<=self.length_m+1e-7:raise ValueError('road s beyond length')
        i=bisect_right([g.s for g in self.geometries],s)-1
        if i<0:raise ValueError('geometry start uncovered')
        g=self.geometries[i];ds=min(max(0.,s-g.s),g.length)
        if g.kind=='line':
            x,y=g.x+ds*cos(g.hdg),g.y+ds*sin(g.hdg);hdg=g.hdg
        elif g.kind=='spiral':
            x,y,hdg=_simpson_clothoid(g,ds)
        else:
            k=g.curvature
            if abs(k)<1e-12:x,y=g.x+ds*cos(g.hdg),g.y+ds*sin(g.hdg)
            else:x=g.x+(sin(g.hdg+k*ds)-sin(g.hdg))/k;y=g.y-(cos(g.hdg+k*ds)-cos(g.hdg))/k
            hdg=g.hdg+k*ds
        idx=bisect_right([v.s for v in self.elevations],s)-1
        z=self.elevations[idx].at(s) if idx>=0 else None
        return {'s_m':s,'x_m':x,'y_m':y,'z_m':z,'hdg_rad':hdg,'elevation_known':z is not None}
    def lane_at(self,s,lane_id):
        k=bisect_right([a for a,_ in self.sections],s)-1
        if k<0:return None
        return next((l for l in self.sections[k][1] if l.lane_id==lane_id),None)

@dataclass(frozen=True)
class JunctionLaneLink:
    junction_id:str
    incoming_road:str
    connecting_road:str
    contact_point:str
    from_lane:int
    to_lane:int

@dataclass(frozen=True)
class OpenDriveAudit:
    roads:tuple[RoadDef,...]
    junction_links:tuple[JunctionLaneLink,...]
    unresolved:tuple[str,...]
    def summary(self):
        return {'roads':len(self.roads),'lane_sections':sum(len(r.sections) for r in self.roads),
                'road_lane_sections':sum(len(lanes) for r in self.roads for _,lanes in r.sections),
                'explicit_junction_lane_links':len(self.junction_links),'unresolved':list(self.unresolved),
                'vehicle_simulation_ready':False,'policy_changed':False}

def _float(a,key,default=None):
    try:v=float(a[key]) if key in a else default
    except (TypeError,ValueError) as e:raise ValueError(f'invalid float {key}') from e
    if v is not None and not isfinite(v):raise ValueError(f'nonfinite {key}')
    return v

def _cubic(elem,tag,skey='s'):
    return tuple(Cubic(_float(x.attrib,skey),*(_float(x.attrib,k) for k in ('a','b','c','d'))) for x in elem.findall(tag))

def parse_xodr(xml:str, *, reject_unsupported_geometry=True)->OpenDriveAudit:
    if '<!DOCTYPE' in xml.upper() or '<!ENTITY' in xml.upper():raise ValueError('external entities/DOCTYPE prohibited')
    root=ET.fromstring(xml)
    if root.tag!='OpenDRIVE':raise ValueError('not OpenDRIVE')
    roads=[]; unresolved=[]; road_ids=set()
    for r in root.findall('road'):
        rid=r.attrib['id'];length=_float(r.attrib,'length')
        if rid in road_ids or length is None or length<=0:raise ValueError('invalid road identity/length')
        road_ids.add(rid); geom=[]; bad=[]
        for e in r.findall('./planView/geometry'):
            sub=list(e)
            if len(sub)!=1 or sub[0].tag not in KINDS:
                bad.append(f'{rid}:unsupported_planView:{sub[0].tag if sub else "none"}')
                continue
            typ=sub[0].tag
            k0=_float(sub[0].attrib,'curvature',0.) if typ=='arc' else _float(sub[0].attrib,'curvStart',0.) if typ=='spiral' else 0.
            k1=_float(sub[0].attrib,'curvEnd') if typ=='spiral' else None
            if typ=='spiral' and k1 is None:raise ValueError('spiral missing curvEnd')
            geom.append(Geometry(_float(e.attrib,'s'),_float(e.attrib,'x'),_float(e.attrib,'y'),
                           _float(e.attrib,'hdg'),_float(e.attrib,'length'),typ,k0,k1))
        if bad:raise ValueError('unsupported geometry cannot be safely sampled: '+';'.join(bad))
        unresolved.extend(bad)
        geom.sort(key=lambda g:g.s)
        if not geom or abs(geom[0].s)>1e-6:raise ValueError('missing first geometry')
        if any(abs(a.s+a.length-b.s)>1e-5 for a,b in zip(geom,geom[1:])):raise ValueError('geometry s gaps/overlap')
        if abs(geom[-1].s+geom[-1].length-length)>1e-4:raise ValueError('geometry does not cover road')
        # Neighboring pieces must join in position and heading. A spiral is
        # evaluated by the same independently tested numerical quadrature.
        for ga,gb in zip(geom,geom[1:]):
            if ga.kind=='line':
                xx=ga.x+ga.length*cos(ga.hdg); yy=ga.y+ga.length*sin(ga.hdg);heading=ga.hdg
            elif ga.kind=='spiral':
                xx,yy,heading=_simpson_clothoid(ga,ga.length)
            else:
                k=ga.curvature; d=ga.length
                xx=ga.x+d*cos(ga.hdg) if abs(k)<1e-12 else ga.x+(sin(ga.hdg+k*d)-sin(ga.hdg))/k
                yy=ga.y+d*sin(ga.hdg) if abs(k)<1e-12 else ga.y-(cos(ga.hdg+k*d)-cos(ga.hdg))/k
                heading=ga.hdg+k*d
            if (xx-gb.x)**2+(yy-gb.y)**2 > 1e-6 or abs(sin((heading-gb.hdg)/2)) > 1e-4:
                raise ValueError('geometry fragments are discontinuous')
        elev=_cubic(r,'./elevationProfile/elevation')
        if any(b.s<=a.s for a,b in zip(elev,elev[1:])) or (elev and elev[0].s!=0):raise ValueError('bad elevation intervals')
        if not elev:unresolved.append(f'{rid}:elevation_missing')
        if r.find('./lateralProfile/superelevation') is not None:unresolved.append(f'{rid}:superelevation_not_evaluated')
        if r.find('./lanes/laneOffset') is not None:unresolved.append(f'{rid}:lane_offset_not_evaluated')
        sections=[]
        for sec in r.findall('./lanes/laneSection'):
            sec_s=_float(sec.attrib,'s');lanes=[]
            for side in ('left','center','right'):
                for l in sec.findall(f'./{side}/lane'):
                    lid=int(l.attrib['id']); widths=_cubic(l,'width','sOffset')
                    if any(b.s<=a.s for a,b in zip(widths,widths[1:])):raise ValueError('unsorted lane widths')
                    if widths and widths[0].s!=0:raise ValueError('lane width starts late')
                    if lid and not widths:unresolved.append(f'{rid}:{sec_s}:{lid}:missing_width')
                    lanes.append(LaneDef(rid,sec_s,lid,l.attrib.get('type','unknown'),widths))
            if len({l.lane_id for l in lanes})!=len(lanes):raise ValueError('duplicate lane id within section')
            sections.append((sec_s,tuple(lanes)))
        if not sections:unresolved.append(f'{rid}:no_lane_sections')
        if any(b[0]<=a[0] for a,b in zip(sections,sections[1:])) or (sections and sections[0][0]!=0):raise ValueError('bad lane section s')
        roads.append(RoadDef(rid,length,tuple(geom),elev,tuple(sections),tuple(bad)))
    road_map={x.road_id:x for x in roads};junctions=[]
    for j in root.findall('junction'):
        jid=j.attrib['id']
        for c in j.findall('connection'):
            incoming=c.attrib.get('incomingRoad');connecting=c.attrib.get('connectingRoad');point=c.attrib.get('contactPoint')
            if incoming not in road_map or connecting not in road_map or point not in ('start','end'):
                raise ValueError('junction points to missing road or invalid contactPoint')
            links=c.findall('laneLink')
            if not links:unresolved.append(f'junction:{jid}:connection_without_laneLink')
            for link in links:
                a=int(link.attrib['from']);b=int(link.attrib['to'])
                incoming_s=road_map[incoming].length_m if point=='start' else 0.0
                # incoming road end depends on geometry/traffic orientation and connection type;
                # audit existence at either boundary, DO NOT assert legal orientation.
                if not any(road_map[incoming].lane_at(s,a) for s in (0,road_map[incoming].length_m)):
                    raise ValueError('junction incoming lane missing')
                if not road_map[connecting].lane_at(0 if point=='start' else road_map[connecting].length_m,b):
                    raise ValueError('junction connecting lane missing')
                junctions.append(JunctionLaneLink(jid,incoming,connecting,point,a,b))
                unresolved.append(f'junction:{jid}:connection_orientation_not_certified')
    if not roads:raise ValueError('empty roads')
    return OpenDriveAudit(tuple(roads),tuple(junctions),tuple(unresolved))
