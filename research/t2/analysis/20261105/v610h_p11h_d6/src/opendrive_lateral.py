"""Research-only lateral OpenDRIVE cross-section reader.

Uses source-declared laneOffset and roll; refuses lane 3D point when elevation
or width is missing. Not complete OpenDRIVE (shape, CRG, lane height omitted).
"""
from dataclasses import dataclass
from math import sin,cos,isfinite
from xml.etree import ElementTree as ET
from bisect import bisect_right
from opendrive_ir import parse_xodr,Cubic

@dataclass(frozen=True)
class CrossSection:
    road_id: str
    length_m: float
    lane_offsets: tuple[Cubic,...]
    superelevations: tuple[Cubic,...]
    source_xml_present: bool

    def _at(self,seq,s,default):
        if not 0<=s<=self.length_m:raise ValueError('s out of range')
        if not seq:return default
        ix=bisect_right([c.s for c in seq],s)-1
        return seq[ix].at(s) if ix>=0 else None

    def offset(self,s):return self._at(self.lane_offsets,s,0.)
    def roll(self,s):return self._at(self.superelevations,s,0.)

    def lane_center(self,road,s,lane_id):
        """Sample center point (x,y,z) with the declared reference roll.

        This is deliberately a centerline approximation, no full surface or
        lateral shape. Positive t is to road's LEFT. For level=True lanes roll
        is not accounted for here; such lanes are blocked to avoid false truth.
        """
        p=road.reference_at(s);o=self.offset(s);r=self.roll(s)
        if p['z_m'] is None or o is None or r is None:
            return {'status':'UNKNOWN_GEOMETRY','reason':'missing elevation/offset/roll'}
        section_idx=bisect_right([v for v,_ in road.sections],s)-1
        if section_idx<0:return {'status':'UNKNOWN_GEOMETRY','reason':'no lane section'}
        section_s,ls=road.sections[section_idx]
        selected=next((v for v in ls if v.lane_id==lane_id),None)
        if selected is None or lane_id==0:return {'status':'UNKNOWN_GEOMETRY','reason':'missing target lane'}
        # Required lane widths for all inner lanes on the same side.
        inside=sorted((v for v in ls if v.lane_id*lane_id>0 and abs(v.lane_id)<=abs(lane_id)),key=lambda x:abs(x.lane_id))
        if len(inside)!=abs(lane_id):return {'status':'UNKNOWN_GEOMETRY','reason':'missing inner lane'}
        widths=[v.width_at(s) for v in inside]
        if any(w is None or w<=0 for w in widths):return {'status':'UNKNOWN_GEOMETRY','reason':'missing/nonpositive lane width'}
        t=o+(1 if lane_id>0 else -1)*(sum(widths[:-1])+widths[-1]/2)
        hdg=p['hdg_rad']; x=p['x_m']-t*cos(r)*sin(hdg);y=p['y_m']+t*cos(r)*cos(hdg)
        z=p['z_m']+t*sin(r)
        return {'status':'COMPUTED_CONDITIONAL','x_m':x,'y_m':y,'z_m':z,'t_m':t,
                'roll_rad':r,'not_surface_or_clearance_certified':True}

def parse_lateral(xml):
    if '<!DOCTYPE' in xml.upper() or '<!ENTITY' in xml.upper():raise ValueError('entities blocked')
    ref=parse_xodr(xml)
    root=ET.fromstring(xml);sections={}
    def extract(parent,tag):
        if parent is None:return ()
        out=[]
        for x in parent.findall(tag):
            nums=[float(x.attrib[k]) for k in ('s','a','b','c','d')]
            if not all(isfinite(v) for v in nums):raise ValueError('nonfinite lateral polynomial')
            out.append(Cubic(*nums))
        if any(x.s<0 or x.s>=r.length_m or (i and x.s<=out[i-1].s) for i,x in enumerate(out)):
            raise ValueError('invalid lateral intervals')
        return tuple(out)
    for road in root.findall('road'):
        r=next(v for v in ref.roads if v.road_id==road.attrib['id'])
        lanes=road.find('lanes');lateral=road.find('lateralProfile')
        offsets=extract(lanes,'laneOffset');rolls=extract(lateral,'superelevation')
        # Fail-closed: known unsupported per-lane leveling and alternate shapes.
        if road.find('.//lane[@level="true"]') is not None or road.find('.//shape') is not None:
            raise ValueError('levelled lanes/shape cross section not supported')
        sections[r.road_id]=CrossSection(r.road_id,r.length_m,offsets,rolls,lanes is not None)
    return ref,sections
