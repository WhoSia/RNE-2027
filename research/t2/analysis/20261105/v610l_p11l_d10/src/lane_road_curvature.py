"""Research-only lane curvature from exact planar constant-normal offset.

k_lane = k_ref / (1 - t*k_ref) for a regular parallel planar curve;
refuses width / lateral offset changes, bank, missing lane geometry, and cusp.
This does NOT imply any speed or tire friction validation.
"""
from __future__ import annotations
from dataclasses import dataclass,asdict
from math import isfinite
from bisect import bisect_right
from opendrive_lateral import parse_lateral

@dataclass(frozen=True)
class OffsetCurvature:
    status:str
    road_id:str
    lane_id:int
    s_m:float
    k_ref_inv_m:float|None
    k_lane_planar_inv_m:float|None
    t_constant_m:float|None
    reason:str

def _is_constant(c):return c.b==0 and c.c==0 and c.d==0

def lane_curvature(xml:str,road_id:str,lane_id:int,s_m:float):
    net,cross=parse_lateral(xml)
    roads=[r for r in net.roads if r.road_id==road_id]
    if len(roads)!=1 or lane_id==0:raise ValueError('invalid road/lane')
    r=roads[0]
    if not isfinite(s_m) or not 0<=s_m<r.length_m:raise ValueError('invalid station')
    idx=bisect_right([v for v,_ in r.sections],s_m)-1
    if idx<0:return asdict(OffsetCurvature('UNKNOWN',road_id,lane_id,s_m,None,None,None,'MISSING_LANE_SECTION'))
    _,lanes=r.sections[idx]
    ls=sorted((l for l in lanes if l.lane_id*lane_id>0 and abs(l.lane_id)<=abs(lane_id)),key=lambda l:abs(l.lane_id))
    def unknown(reason,k=None,t=None):return asdict(OffsetCurvature('UNKNOWN',road_id,lane_id,s_m,k,None,t,reason))
    if len(ls)!=abs(lane_id):return unknown('MISSING_INNER_LANE')
    if len(r.sections)!=1 or any(len(l.widths)!=1 or not _is_constant(l.widths[0]) for l in ls):return unknown('VARIABLE_LANE_WIDTH_OR_SECTIONS')
    c=cross[road_id]
    if len(c.lane_offsets)>1 or (c.lane_offsets and not _is_constant(c.lane_offsets[0])):return unknown('VARIABLE_LANE_OFFSET')
    if len(c.superelevations)>1 or any(not _is_constant(v) or v.a!=0 for v in c.superelevations):return unknown('BANKED_OR_VARIABLE_CROSS_SECTION')
    if not r.elevations or len(r.elevations)>1 or any(abs(v.b)+abs(v.c)+abs(v.d)>1e-13 for v in r.elevations):return unknown('NONPLANAR_OR_UNKNOWN_ELEVATION')
    if any(l.widths[0].a<=0 for l in ls):return unknown('NONPOSITIVE_WIDTH')
    sgn=1 if lane_id>0 else -1
    t=(c.lane_offsets[0].a if c.lane_offsets else 0.)+sgn*(sum(l.widths[0].a for l in ls[:-1])+ls[-1].widths[0].a/2)
    i=bisect_right([g.s for g in r.geometries],s_m)-1
    if i<0:return unknown('MISSING_REFERENCE_GEOMETRY')
    geom=r.geometries[i]
    if geom.kind=='line':k=0.
    elif geom.kind=='arc':k=geom.curvature
    elif geom.kind=='spiral':k=geom.curvature+(geom.curvature_end-geom.curvature)*(s_m-geom.s)/geom.length
    else:return unknown('UNSUPPORTED_REFERENCE_GEOMETRY')
    d=1-t*k
    if d<=0 or abs(d)<1e-10:return unknown('OFFSET_CUSP_OR_DIRECTION_REVERSAL',k,t)
    return asdict(OffsetCurvature('PLANAR_GEOMETRIC_IDENTITY_ONLY',road_id,lane_id,s_m,k,k/d,t,'constant normal offset, not vehicle trajectory'))
