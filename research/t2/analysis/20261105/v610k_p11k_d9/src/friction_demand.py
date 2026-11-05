"""Simplified tire/road friction-demand budget for synthetic comparison only.

NOT an actual safe-speed calculator, vehicle dynamics solver, crash predictor,
road-safety certification, or a recommendation to operate a real vehicle.
The inputs are externally supplied effective friction hypotheses (not inferred
from asphalt/concrete labels or source XODR `friction`).
"""
from dataclasses import dataclass
from math import sin,cos,sqrt,isfinite

G=9.80665
@dataclass(frozen=True)
class PhysicsPoint:
    speed_mps: float
    curvature_inv_m: float  # signed relative to +road s and bank direction
    bank_rad: float         # positive bank contributes inward force for +curvature
    grade_rad: float        # positive uphill in travel direction
    longitudinal_accel_mps2: float=0.0  # +accelerating, -braking

@dataclass(frozen=True)
class FrictionResult:
    status: str
    mu_required: float | None
    mu_effective_assumed: float | None
    margin: float | None
    lateral_force_per_mass_mps2: float | None
    longitudinal_force_per_mass_mps2: float | None
    normal_force_per_mass_mps2: float | None
    note: str = 'SIMPLIFIED_QUASI_STATIC_NOT_SAFETY_CERTIFICATION'

def demand(pt:PhysicsPoint, *, effective_mu:float | None=None)->FrictionResult:
    nums=(pt.speed_mps,pt.curvature_inv_m,pt.bank_rad,pt.grade_rad,pt.longitudinal_accel_mps2)
    if any(not isfinite(x) for x in nums) or pt.speed_mps<0 or abs(pt.bank_rad)>=1.3 or abs(pt.grade_rad)>=1.3:
        raise ValueError('unsupported physical input')
    if effective_mu is not None and (not isfinite(effective_mu) or effective_mu<0):
        raise ValueError('invalid assumed friction')
    # Local-road-frame quasi-static projection; ignores suspension/tire dynamics.
    turn_accel=pt.speed_mps**2*pt.curvature_inv_m
    gravity_normal=G*cos(pt.grade_rad)
    lat=turn_accel*cos(pt.bank_rad)-gravity_normal*sin(pt.bank_rad)
    normal=gravity_normal*cos(pt.bank_rad)+turn_accel*sin(pt.bank_rad)
    longitudinal=pt.longitudinal_accel_mps2+G*sin(pt.grade_rad)
    if normal<=0:
        return FrictionResult('UNKNOWN_NONPOSITIVE_NORMAL',None,effective_mu,None,lat,longitudinal,normal)
    mu_req=sqrt(lat*lat+longitudinal*longitudinal)/normal
    return FrictionResult('DEMAND_ONLY' if effective_mu is None else 'HYPOTHETICAL_COMPARISON',
                          mu_req,effective_mu,None if effective_mu is None else effective_mu-mu_req,
                          lat,longitudinal,normal)
