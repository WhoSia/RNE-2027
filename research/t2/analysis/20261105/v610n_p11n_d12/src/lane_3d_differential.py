"""Research-only local 3D differential geometry of a source-declared lane center.

No tire grip, actual driving-speed, physical clearance, legal movement or safety
claim is made. Finite differences are a diagnostic, not an error-bounded solver.
"""
from __future__ import annotations
from math import isfinite, sqrt
from bisect import bisect_left
from opendrive_lateral import parse_lateral


def _dot(a,b): return sum(x*y for x,y in zip(a,b))
def _cross(a,b): return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def _norm(a): return sqrt(_dot(a,a))
def _vec(*args): return tuple(sum(coeff*p[i] for coeff,p in args) for i in range(3))


def derivatives_3d(sample, station:float, h:float=0.025)->dict:
    """Five-point finite differences with separately declared sample function.

    The sample must return a 3-vector and be valid on [s-2h,s+2h].
    Results are mathematical geometry diagnostics only.
    """
    if not (isfinite(station) and isfinite(h) and h>0): raise ValueError('invalid station or step')
    p=[tuple(sample(station+k*h)) for k in (-2,-1,0,1,2)]
    if any(len(z)!=3 or not all(isfinite(v) for v in z) for z in p):raise ValueError('invalid point sample')
    a,b,c,d,e=p
    d1=_vec((-1/(12*h),e),(8/(12*h),d),(-8/(12*h),b),(1/(12*h),a))
    d2=_vec((-1/(12*h*h),e),(16/(12*h*h),d),(-30/(12*h*h),c),(16/(12*h*h),b),(-1/(12*h*h),a))
    d3=_vec((1/(2*h**3),e),(-2/(2*h**3),d),(2/(2*h**3),b),(-1/(2*h**3),a))
    cross=_cross(d1,d2);norm=_norm(cross);spd=_norm(d1)
    if spd<=1e-12:return {'status':'UNKNOWN','reason':'DEGENERATE_TANGENT'}
    k=norm/(spd**3)
    if norm<=1e-9:return {'status':'CURVATURE_ONLY','curvature_inv_m':k,'torsion_inv_m':None,'reason':'TORSION_UNDEFINED_NEAR_ZERO_CURVATURE','sample_step_m':h}
    tau=_dot(cross,d3)/(norm*norm)
    if not all(isfinite(x) for x in (k,tau)):return {'status':'UNKNOWN','reason':'NONFINITE_DERIVATIVE'}
    return {'status':'SAMPLED_3D_DIFFERENTIAL_GEOMETRY_ONLY','curvature_inv_m':k,'torsion_inv_m':tau,'sample_step_m':h,'sample_count':5,'field_validated':False,'safe_speed_mps':None}


def lane_3d_at(xml:str,road_id:str,lane_id:int,station:float,h:float=0.025)->dict:
    if not (isfinite(station) and isfinite(h) and h>0):raise ValueError('invalid sampling parameters')
    net,cross=parse_lateral(xml)
    matches=[r for r in net.roads if r.road_id==road_id]
    if len(matches)!=1 or lane_id==0:raise ValueError('invalid road/lane')
    road=matches[0]
    def unknown(reason):return {'status':'UNKNOWN','reason':reason,'road_id':road_id,'lane_id':lane_id,'station_m':station}
    if station-2*h<0 or station+2*h>=road.length_m:return unknown('STENCIL_OUTSIDE_ROAD')
    # No finite difference may cross a polynomial, geometry or lane-section knot.
    knots=set()
    knots.update(g.s for g in road.geometries)
    knots.update(x.s for x in road.elevations)
    knots.update(section_s for section_s,_ in road.sections)
    section=next(((ss,ls) for ss,ls in reversed(road.sections) if ss<=station),None)
    if section is None:return unknown('MISSING_SECTION')
    sec_s, lanes=section
    inner=[l for l in lanes if l.lane_id*lane_id>0 and abs(l.lane_id)<=abs(lane_id)]
    if len(inner)!=abs(lane_id):return unknown('MISSING_LANE')
    for l in inner:knots.update(sec_s+w.s for w in l.widths)
    knots.update(x.s for x in cross[road_id].lane_offsets)
    knots.update(x.s for x in cross[road_id].superelevations)
    for knot in knots:
        if station-2*h<=knot<=station+2*h and abs(knot-station)>1e-12:
            return unknown('FINITE_DIFFERENCE_CROSSES_SOURCE_KNOT')
        if abs(knot-station)<=1e-12:return unknown('FINITE_DIFFERENCE_ON_SOURCE_KNOT')
    def sample(s):
        r=cross[road_id].lane_center(road,s,lane_id)
        if r.get('status')!='COMPUTED_CONDITIONAL':raise ValueError('incomplete lane center profile')
        return (r['x_m'],r['y_m'],r['z_m'])
    try:return {**derivatives_3d(sample,station,h),'road_id':road_id,'lane_id':lane_id,'station_m':station}
    except (ValueError,ZeroDivisionError,OverflowError) as exc:return unknown('SOURCE_GEOMETRY_OR_NUMERICAL_FAILURE:'+type(exc).__name__)


def convergence_diagnostic(sample, station:float, h:float=0.04)->dict:
    """Compare two finite-difference stencil scales, without a certified bound."""
    coarse=derivatives_3d(sample,station,h)
    fine=derivatives_3d(sample,station,h/2)
    if coarse['status']=='UNKNOWN' or fine['status']=='UNKNOWN':
        return {'status':'UNKNOWN','reason':'DEGENERATE_STENCIL'}
    result={'status':'NUMERICAL_CONVERGENCE_DIAGNOSTIC_ONLY','step_coarse_m':h,'step_fine_m':h/2,
            'curvature_abs_difference_inv_m':abs(coarse['curvature_inv_m']-fine['curvature_inv_m']),
            'certified_error_bound':False}
    if coarse['torsion_inv_m'] is None or fine['torsion_inv_m'] is None:
        result['torsion_abs_difference_inv_m']=None
    else:result['torsion_abs_difference_inv_m']=abs(coarse['torsion_inv_m']-fine['torsion_inv_m'])
    return result
