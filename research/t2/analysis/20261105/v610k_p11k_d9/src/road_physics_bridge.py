"""Bridge geometry -> simplified demand without converting source material into real grip.

Outputs are synthetic engineering model diagnostics only. No driving advice.
"""
from math import atan,isfinite
from opendrive_ir import parse_xodr
from opendrive_lateral import parse_lateral
from pavement_material import MaterialMap
from friction_demand import PhysicsPoint,demand

def sample_road_physics(xml:str,road_id:str,lane_id:int,s_m:float,*,speed_mps:float,
                        longitudinal_accel_mps2:float=0., effective_mu_hypothesis:float|None=None):
    net,sections=parse_lateral(xml)
    roads=[r for r in net.roads if r.road_id==road_id]
    if len(roads)!=1:raise ValueError('road not unique')
    r=roads[0]
    if not 0<=s_m<r.length_m:raise ValueError('station out of road length')
    if r.lane_at(s_m,lane_id) is None:raise ValueError('lane absent')
    ref=r.reference_at(s_m)
    if ref['z_m'] is None:
        return {'status':'UNKNOWN','reason':'MISSING_ELEVATION','source_material':MaterialMap(xml).at(road_id,s_m,lane_id)}
    g=next(x for x in r.geometries if x.s<=s_m<x.s+x.length+1e-9)
    if g.kind=='line':curvature=0.
    elif g.kind=='arc':curvature=g.curvature
    elif g.kind=='spiral':curvature=g.curvature+(g.curvature_end-g.curvature)*(s_m-g.s)/g.length
    else:raise ValueError('unsupported geometry')
    elevations=[e for e in r.elevations if e.s<=s_m]
    if not elevations:return {'status':'UNKNOWN','reason':'MISSING_ELEVATION_POLYNOMIAL'}
    e=elevations[-1];ds=s_m-e.s
    grade=atan(e.b+2*e.c*ds+3*e.d*ds*ds)
    bank=sections[road_id].roll(s_m)
    if bank is None or not isfinite(bank):return {'status':'UNKNOWN','reason':'MISSING_BANK'}
    p=PhysicsPoint(speed_mps,curvature,bank,grade,longitudinal_accel_mps2)
    f=demand(p,effective_mu=effective_mu_hypothesis)
    return {'status':'RESEARCH_ONLY','road_id':road_id,'lane_id':lane_id,'s_m':s_m,
            'signed_curvature_inv_m':curvature,'bank_rad':bank,'grade_rad':grade,
            'source_material':MaterialMap(xml).at(road_id,s_m,lane_id),
            'effective_grip_assumed_by_analyst':effective_mu_hypothesis,
            'friction_demand':f.__dict__,'field_validated':False,
            'notice':'Measured grip and detailed tire dynamics not available; never convert source material into effective grip'}
