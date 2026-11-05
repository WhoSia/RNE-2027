"""Explicit vehicle-to-road dimensional eligibility audit.

UNKNOWN is returned whenever a relevant clearance/dimension is absent. A
positive status is only relative to the declared thresholds, not evidence of
full road legality or dynamic safety.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class VehicleEnvelope:
    vehicle_id:str
    height_m:float
    width_m:float
    length_m:float
    gross_mass_t:float
    def __post_init__(self):
        if not self.vehicle_id or any(not isfinite(v) or v<=0 for v in
            (self.height_m,self.width_m,self.length_m,self.gross_mass_t)):
            raise ValueError('invalid vehicle envelope')

@dataclass(frozen=True)
class RoadLimits:
    lane_id:str
    max_height_m:float|None=None
    max_width_m:float|None=None
    max_length_m:float|None=None
    max_gross_mass_t:float|None=None
    provenance:str=''
    def __post_init__(self):
        if not self.lane_id or not self.provenance:
            raise ValueError('road limit requires source attribution')
        for v in (self.max_height_m,self.max_width_m,self.max_length_m,self.max_gross_mass_t):
            if v is not None and (not isfinite(v) or v<=0):
                raise ValueError('invalid road limit')

def audit(vehicle:VehicleEnvelope,road:RoadLimits):
    vals=(('height_m',road.max_height_m,vehicle.height_m),
          ('width_m',road.max_width_m,vehicle.width_m),
          ('length_m',road.max_length_m,vehicle.length_m),
          ('gross_mass_t',road.max_gross_mass_t,vehicle.gross_mass_t))
    violated=[name for name,limit,value in vals if limit is not None and value>limit+1e-10]
    unknown=[name for name,limit,_ in vals if limit is None]
    # Evidence that a vehicle is too tall still rejects it if other limits unknown.
    status='DENY' if violated else 'UNKNOWN' if unknown else 'PASS_DECLARED_ONLY'
    return {'lane_id':road.lane_id,'vehicle_id':vehicle.vehicle_id,'status':status,
            'violated':violated,'unknown':unknown,'evidence':road.provenance,
            'other_legality_not_certified':True}
