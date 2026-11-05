"""Research-only planar variable-offset lane curvature for a restricted OpenDRIVE subset.

This module calculates geometric curvature (not a tyre/traction limit, safe
speed or traffic policy). It fails closed on nonplanar/unsupported definitions.
"""
from __future__ import annotations
from bisect import bisect_right
from math import isfinite
from opendrive_lateral import parse_lateral


def _poly_derivs(c, s):
    d = s-c.s
    return c.at(s),c.b+2*c.c*d+3*c.d*d*d,2*c.c+6*c.d*d


def lane_curvature_variable(xml:str, road_id:str, lane_id:int, s_m:float)->dict:
    net, crosses=parse_lateral(xml)
    rr=[r for r in net.roads if r.road_id==road_id]
    if len(rr)!=1 or lane_id==0 or not isfinite(s_m):raise ValueError('road, lane, or station invalid')
    r=rr[0]
    if not 0<=s_m<r.length_m:raise ValueError('station out of range')
    def unknown(reason):return {'status':'UNKNOWN','reason':reason,'road_id':road_id,'lane_id':lane_id,'s_m':s_m,'field_validated':False}
    section_i=bisect_right([v for v,_ in r.sections],s_m)-1
    if section_i<0:return unknown('MISSING_LANE_SECTION')
    section_s,lanes=r.sections[section_i]
    within=sorted((l for l in lanes if l.lane_id*lane_id>0 and abs(l.lane_id)<=abs(lane_id)),key=lambda l:abs(l.lane_id))
    if len(within)!=abs(lane_id):return unknown('MISSING_INNER_LANES')
    cross=crosses[road_id]
    if cross.superelevations and any(abs(c.at(s_m))>1e-12 or abs(c.b)+abs(c.c)+abs(c.d)>1e-12 for c in cross.superelevations):return unknown('BANKED_LANE_NOT_PLANAR')
    if not r.elevations or len(r.elevations)!=1 or any(abs(x)>1e-12 for x in (r.elevations[0].b,r.elevations[0].c,r.elevations[0].d)):
        return unknown('NONPLANAR_OR_MISSING_ELEVATION')
    o=(0.,0.,0.)
    if cross.lane_offsets:
        i=bisect_right([p.s for p in cross.lane_offsets],s_m)-1
        if i<0:return unknown('LANE_OFFSET_NOT_DEFINED_AT_STATION')
        o=_poly_derivs(cross.lane_offsets[i],s_m)
    t,tp,tpp=o
    sign=1 if lane_id>0 else -1
    for i,l in enumerate(within):
        local_s=s_m-section_s
        j=bisect_right([v.s for v in l.widths],local_s)-1
        if j<0:return unknown('LANE_WIDTH_NOT_DEFINED')
        w,wp,wpp=_poly_derivs(l.widths[j],local_s)
        if not isfinite(w) or w<=0:return unknown('NONPOSITIVE_WIDTH')
        factor=sign*(0.5 if i==len(within)-1 else 1.)
        t+=factor*w;tp+=factor*wp;tpp+=factor*wpp
    g_i=bisect_right([g.s for g in r.geometries],s_m)-1
    if g_i<0:return unknown('MISSING_REFERENCE')
    g=r.geometries[g_i]
    if g.kind=='line':k,kp=0.,0.
    elif g.kind=='arc':k,kp=g.curvature,0.
    elif g.kind=='spiral':k=g.curvature+(g.curvature_end-g.curvature)*(s_m-g.s)/g.length;kp=(g.curvature_end-g.curvature)/g.length
    else:return unknown('UNSUPPORTED_REFERENCE')
    a=1-t*k;b=tp
    speed2=a*a+b*b
    if not isfinite(speed2) or speed2<1e-16 or a<=0:return unknown('OFFSET_CUSP_OR_DIRECTION_REVERSAL')
    # r_lane' = (1 - tk)T + t' N; its derivative uses T'=kN and N'=-kT.
    numerator=a*a*k+a*tpp+2*tp*tp*k+t*tp*kp
    k_lane=numerator/(speed2**1.5)
    if not isfinite(k_lane):return unknown('NUMERICAL_OVERFLOW')
    return {'status':'PLANAR_DIFFERENTIAL_GEOMETRY_ONLY','road_id':road_id,'lane_id':lane_id,'s_m':s_m,
            'k_ref_inv_m':k,'dk_ref_ds_inv_m2':kp,'t_m':t,'dt_ds':tp,'d2t_ds2_inv_m':tpp,
            'k_lane_inv_m':k_lane,'planar_tangent_speed_per_reference_m':speed2**0.5,
            'field_validated':False,'safe_speed_mps':None}
