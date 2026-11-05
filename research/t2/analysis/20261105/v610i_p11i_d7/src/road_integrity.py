"""P11-I: conservative OpenDRIVE lane-width and junction-geometry audit.

This module checks mathematical assertions about *reported* XML geometry.
It never declares a permitted movement, crash-free route, or an operational signal plan.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from math import sqrt, isfinite, hypot

from opendrive_ir import Cubic
from opendrive_lateral import parse_lateral


@dataclass(frozen=True)
class AuditFinding:
    subject: str
    status: str
    code: str
    detail: str


def _critical_points(p: Cubic, interval: float):
    """Stationary points of a + b*u + c*u^2 + d*u^3 on [0, interval]."""
    if not isfinite(interval) or interval < 0:
        raise ValueError('invalid polynomial interval')
    out=[0.0, interval]
    a=3*p.d; b=2*p.c; c=p.b
    if abs(a)<1e-14:
        if abs(b)>1e-14:
            u=-c/b
            if 0<u<interval:out.append(u)
    else:
        disc=b*b-4*a*c
        if disc>=0:
            root=sqrt(disc)
            for u in ((-b-root)/(2*a),(-b+root)/(2*a)):
                if 0<u<interval:out.append(u)
    return out


def polynomial_range(p:Cubic, begin:float, end:float):
    """Analytic polynomial extrema over *absolute* s interval."""
    if not begin<=end or begin<p.s-1e-12:
        raise ValueError('outside polynomial support')
    shift=begin-p.s
    shifted=Cubic(begin,p.at(begin),p.b+2*p.c*shift+3*p.d*shift*shift,p.c+3*p.d*shift,p.d)
    us=_critical_points(shifted,end-begin)
    vals=[p.at(begin+u) for u in us]
    if any(not isfinite(v) for v in vals):raise ValueError('nonfinite polynomial')
    return min(vals),max(vals)


def audit_lane_widths(xml:str, *, min_width_m:float=1e-6, continuity_tol_m:float=1e-6):
    """Check complete lane-width polynomials rather than sampling stations only.

    A width knot belongs to the next polynomial. The left limit must agree with
    the next value. No requirement that physical lane width be constant.
    """
    net,_=parse_lateral(xml)
    findings=[]
    for road in net.roads:
        for idx,(section_start,lanes) in enumerate(road.sections):
            section_end=road.sections[idx+1][0] if idx+1<len(road.sections) else road.length_m
            for lane in lanes:
                if lane.lane_id==0:continue
                tag=f'{road.road_id}:{section_start:g}:lane{lane.lane_id}'
                if not lane.widths:
                    findings.append(AuditFinding(tag,'UNKNOWN','NO_WIDTH','No explicit width profile'))
                    continue
                for k,p in enumerate(lane.widths):
                    begin=section_start+p.s
                    end=section_start+lane.widths[k+1].s if k+1<len(lane.widths) else section_end
                    if end<begin or end>road.length_m+1e-8:
                        findings.append(AuditFinding(tag,'FAIL','WIDTH_INTERVAL','Knot outside lane section'))
                        continue
                    low,high=polynomial_range(p,begin,end)
                    if low<=min_width_m:
                        findings.append(AuditFinding(tag,'FAIL','WIDTH_NONPOSITIVE',f'minimum={low:.9g}m at some s in [{begin:g},{end:g}]'))
                    if k+1<len(lane.widths):
                        next_p=lane.widths[k+1]
                        left=p.at(end); right=next_p.at(end)
                        if abs(left-right)>continuity_tol_m:
                            findings.append(AuditFinding(tag,'FAIL','WIDTH_KNOT_JUMP',f'jump={right-left:.9g}m at s={end:g}'))
                if not any(f.subject==tag for f in findings):
                    findings.append(AuditFinding(tag,'PASS','WIDTH_INTERVALS_CERTIFIED',f'{len(lane.widths)} polynomial width segment(s)'))
    return findings


def audit_explicit_junctions(xml:str, *, join_max_gap_m:float=0.05, lane_center_max_gap_m:float=2.0):
    """Report *geometric* gaps of explicit links only, not vehicle permission.

    Incoming endpoint is unknown without validated traveling direction. We
    compare BOTH endpoint hypotheses, flag distant endpoints, and report the
    chosen hypothesis as UNRESOLVED rather than granting connectivity.
    """
    net,sections=parse_lateral(xml)
    by_id={road.road_id:road for road in net.roads}
    out=[]
    for link in net.junction_links:
        src=by_id[link.incoming_road]; dst=by_id[link.connecting_road]
        d_s=0.0 if link.contact_point=='start' else dst.length_m
        dst_ref=dst.reference_at(d_s)
        candidates=[]
        for s in (0.,src.length_m):
            p=src.reference_at(s)
            gap=hypot(dst_ref['x_m']-p['x_m'],dst_ref['y_m']-p['y_m'])
            candidates.append((gap,s))
        candidates.sort()
        subject=f'{link.junction_id}:{link.incoming_road}:{link.from_lane}->{link.connecting_road}:{link.to_lane}'
        min_gap,s_src=candidates[0]
        if min_gap>join_max_gap_m:
            out.append(AuditFinding(subject,'FAIL','ROAD_REFERENCE_GAP',f'nearest XY gap {min_gap:.6g}m'))
            continue
        a=sections[src.road_id].lane_center(src,s_src,link.from_lane)
        b=sections[dst.road_id].lane_center(dst,d_s,link.to_lane)
        if a.get('status')!='COMPUTED_CONDITIONAL' or b.get('status')!='COMPUTED_CONDITIONAL':
            out.append(AuditFinding(subject,'UNKNOWN','LANE_GEOMETRY_UNKNOWN','Missing actual lane geometry for gap test'))
            continue
        distance=hypot(a['x_m']-b['x_m'],a['y_m']-b['y_m'])
        if distance>lane_center_max_gap_m:
            out.append(AuditFinding(subject,'FAIL','LANE_CENTER_GAP',f'XY gap {distance:.6g}m'))
        else:
            out.append(AuditFinding(subject,'UNKNOWN','LINK_GEOMETRY_ONLY',f'XY center gap {distance:.6g}m; travel orientation/legality unverified'))
    return out


def full_audit(xml:str):
    widths=audit_lane_widths(xml)
    links=audit_explicit_junctions(xml)
    return {'scope':'synthetic_or_source_declared_geometry_only',
            'policy_ran':False,'vehicle_simulated':False,
            'width_findings':[asdict(a) for a in widths],
            'link_findings':[asdict(a) for a in links],
            'fail_count':sum(a.status=='FAIL' for a in widths+links),
            'unknown_count':sum(a.status=='UNKNOWN' for a in widths+links)}
