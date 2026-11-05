"""K: differentiate C0/C1/G2 for consecutive OpenDRIVE planView pieces.

The source parser already gates C0/C1. This module diagnoses curvature jumps.
"""
from dataclasses import dataclass,asdict
from math import isfinite
from opendrive_ir import parse_xodr

@dataclass(frozen=True)
class CurvatureFinding:
    road_id:str
    station_m:float
    k_left_inv_m:float
    k_right_inv_m:float
    status:str

def audit_curvature(xml:str,*,tolerance_inv_m:float=1e-6):
    if not isfinite(tolerance_inv_m) or tolerance_inv_m<=0:raise ValueError('invalid tolerance')
    n=parse_xodr(xml)
    results=[]
    for road in n.roads:
        gs=road.geometries
        for a,b in zip(gs,gs[1:]):
            def k_start(x):return 0. if x.kind=='line' else x.curvature
            def k_end(x):return x.curvature_end if x.kind=='spiral' else k_start(x)
            left=k_end(a);right=k_start(b)
            results.append(asdict(CurvatureFinding(road.road_id,b.s,left,right,
                'G2_CURVATURE_CONTINUOUS' if abs(left-right)<=tolerance_inv_m else 'G2_CURVATURE_JUMP')))
    return {'findings':results,'traffic_safety_certified':False}
