"""P11-J: source-declared 3D lane-boundary sampler and link seam audit.

This is an intentionally conservative geometric observer, not a legal road or
collision checker. It handles the restricted OpenDRIVE cross-section subset from
opendrive_lateral, with positive-width intervals audited separately.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from math import cos, sin, hypot, pi, isfinite
from bisect import bisect_right
from opendrive_lateral import parse_lateral
from road_integrity import audit_lane_widths


@dataclass(frozen=True)
class Boundary:
    road_id: str
    lane_id: int
    s_m: float
    inner_xyz_m: tuple[float, float, float]
    outer_xyz_m: tuple[float, float, float]
    center_xyz_m: tuple[float, float, float]
    heading_rad: float
    width_m: float
    status: str = 'COMPUTED_CONDITIONAL'


def _absolute(s: float, lane_offset: float, roll: float, ref: dict, lateral_m: float):
    t = lane_offset + lateral_m
    h = ref['hdg_rad']
    return (ref['x_m']-t*cos(roll)*sin(h),
            ref['y_m']+t*cos(roll)*cos(h),
            ref['z_m']+t*sin(roll))


def lane_boundaries(road, section, s: float, lane_id: int) -> Boundary | None:
    """Sample inner and outer edges for one lane at station s.

    UNKNOWN returned as None if any source geometry is absent. Width between
    profile knots is only accepted when the interval audit has already passed.
    """
    if lane_id == 0 or not 0 <= s <= road.length_m:
        return None
    ref=road.reference_at(s)
    offset=section.offset(s)
    roll=section.roll(s)
    if ref['z_m'] is None or offset is None or roll is None:
        return None
    sec_i=bisect_right([a for a,_ in road.sections],s)-1
    if sec_i<0: return None
    _, lanes=road.sections[sec_i]
    inner_lanes=sorted((l for l in lanes if l.lane_id*lane_id>0 and abs(l.lane_id)<=abs(lane_id)),key=lambda l:abs(l.lane_id))
    if len(inner_lanes)!=abs(lane_id):return None
    widths=[l.width_at(s) for l in inner_lanes]
    if any(w is None or not isfinite(w) or w<=0 for w in widths):return None
    sign=1 if lane_id>0 else -1
    inner=sign*sum(widths[:-1]);outer=sign*sum(widths)
    p=_absolute(s,offset,roll,ref,inner)
    q=_absolute(s,offset,roll,ref,outer)
    c=_absolute(s,offset,roll,ref,(inner+outer)/2)
    return Boundary(road.road_id,lane_id,s,p,q,c,ref['hdg_rad'],widths[-1])


def _distance3(a,b):
    return (sum((p-q)**2 for p,q in zip(a,b)))**.5


def _unsigned_heading_delta(a,b):
    return abs((a-b+pi)%(2*pi)-pi)


def audit_boundary_seams(xml: str, *, edge_tol_m: float = .15,
                         heading_tol_rad: float = .08,
                         width_tol_m: float = .15,
                         z_tol_m: float = .12):
    """Check declared junction link *candidate* seams and return structured findings.

    Note: incomingRoad travel endpoint not determined by reference orientation,
    so both endpoint hypotheses are examined but never grant travel legality.
    A source-declared gap is an evidence failure only if both candidate joins fail.
    Tolerances are explicit research thresholds, NOT any engineering standard.
    """
    if any(not isfinite(t) or t<=0 for t in (edge_tol_m,heading_tol_rad,width_tol_m,z_tol_m)):
        raise ValueError('all thresholds must be positive and finite')
    net,cross=parse_lateral(xml)
    width_results=audit_lane_widths(xml)
    if any(x.status=='FAIL' for x in width_results):
        return {'status':'BLOCKED_BAD_WIDTH','findings':[],
                'reason':'width interval or knot audit failed: no valid lane footprint'}
    roads={r.road_id:r for r in net.roads}
    findings=[]
    for link in net.junction_links:
        a=roads[link.incoming_road];b=roads[link.connecting_road]
        b_s=0.0 if link.contact_point=='start' else b.length_m
        target=lane_boundaries(b,cross[b.road_id],b_s,link.to_lane)
        entry={'junction':link.junction_id,'source':a.road_id,'source_lane':link.from_lane,
               'target':b.road_id,'target_lane':link.to_lane,'contact_point':link.contact_point}
        if target is None:
            findings.append({**entry,'status':'UNKNOWN','code':'TARGET_GEOMETRY_MISSING'});continue
        candidates=[]
        for a_s in (0.0,a.length_m):
            src=lane_boundaries(a,cross[a.road_id],a_s,link.from_lane)
            if src is None:continue
            # Left/right boundary correspondence may be reversed if direction
            # reverses; don't infer orientation by swapping edges. Record both.
            direct=max(_distance3(src.inner_xyz_m,target.inner_xyz_m),
                       _distance3(src.outer_xyz_m,target.outer_xyz_m))
            swapped=max(_distance3(src.inner_xyz_m,target.outer_xyz_m),
                        _distance3(src.outer_xyz_m,target.inner_xyz_m))
            cx=_distance3(src.center_xyz_m,target.center_xyz_m)
            zd=abs(src.center_xyz_m[2]-target.center_xyz_m[2])
            hd=_unsigned_heading_delta(src.heading_rad,target.heading_rad)
            wd=abs(src.width_m-target.width_m)
            candidates.append({'source_s_m':a_s,'boundary_direct_max_m':direct,
                               'boundary_swapped_max_m':swapped,'center_gap_3d_m':cx,
                               'height_gap_m':zd,'heading_delta_unsigned_rad':hd,
                               'width_gap_m':wd})
        if not candidates:
            findings.append({**entry,'status':'UNKNOWN','code':'SOURCE_GEOMETRY_MISSING'});continue
        # At most one end should geometrically connect; choose smallest center gap
        # as a reportable geometric hypothesis, never a traffic-direction decision.
        best=min(candidates,key=lambda v:v['center_gap_3d_m'])
        fail=[]
        if best['height_gap_m']>z_tol_m:fail.append('VERTICAL_GAP')
        if best['width_gap_m']>width_tol_m:fail.append('WIDTH_MISMATCH')
        if best['boundary_direct_max_m']>edge_tol_m:fail.append('BOUNDARY_GAP')
        if best['heading_delta_unsigned_rad']>heading_tol_rad:fail.append('HEADING_KINK_OR_REVERSE')
        if fail:
            # Even if a single candidate misses, this is source-declared geometry,
            # not a vehicle crash conclusion. Different 3D road alignments require
            # more precise full-road graph topology before legal rejection.
            status='FAIL';code='+'.join(fail)
        else:
            status='UNKNOWN';code='GEOMETRIC_SEAM_MATCH_ONLY'
        findings.append({**entry,'status':status,'code':code,
                         'chosen_geometry_hypothesis':best,
                         'candidate_count':len(candidates),
                         'travel_orientation_verified':False,
                         'legal_permission_verified':False})
    return {'status':'SOURCE_DECLARED_GEOMETRY_AUDIT',
            'research_thresholds_m':{'edge':edge_tol_m,'width':width_tol_m,'height':z_tol_m},
            'heading_tol_rad':heading_tol_rad,
            'source_width_findings':len(width_results),'findings':findings,
            'vehicle_motion_checked':False,'policy_executed':False}


def sample_lane_strip(xml: str, road_id: str, lane_id: int, *, n: int=25):
    """Finite sampled strip vertices for visualization, NOT certified polygon union.

    Reject multi-section roads: a geometry stitcher is needed to avoid a
    misleading strip crossing lane disappearances or interval discontinuities.
    """
    if n<2 or n>100000:raise ValueError('invalid station count')
    net,cross=parse_lateral(xml)
    road=next((r for r in net.roads if r.road_id==road_id),None)
    if road is None:raise ValueError('unknown road')
    if len(road.sections)!=1:raise ValueError('multiple laneSections not yet sampled')
    checks=audit_lane_widths(xml)
    if any(x.status!='PASS' for x in checks if x.subject.startswith(f'{road_id}:')):
        raise ValueError('lane widths not fully validated')
    inner=[];outer=[]
    for i in range(n):
        s=road.length_m*i/(n-1)
        b=lane_boundaries(road,cross[road_id],s,lane_id)
        if b is None:raise ValueError('missing lane surface data')
        inner.append(b.inner_xyz_m);outer.append(b.outer_xyz_m)
    return {'kind':'SAMPLED_STRIP_NOT_EXACT_SURFACE','road_id':road_id,
            'lane_id':lane_id,'station_count':n,'inner_xyz_m':inner,'outer_xyz_m':outer,
            'exact_3d_surface_certified':False}
