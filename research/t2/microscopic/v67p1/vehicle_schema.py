"""Single immutable vehicle-class contract shared by micro and macro mechanisms.

Dimensions are metres; dynamics m/s and m/s²; times seconds.  The class
fields encode assumptions, not measured fleet statistics.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class VehicleSpec:
    name: str
    length_m: float
    width_m: float
    min_gap_m: float
    acceleration_mps2: float
    braking_mps2: float
    time_headway_s: float
    discharge_headway_s: float
    connector_clearance_buffer_s: float = 0.0

    def __post_init__(self):
        if not self.name: raise ValueError('vehicle class needs a name')
        positive = (self.length_m,self.width_m,self.min_gap_m,self.acceleration_mps2,
                    self.braking_mps2,self.time_headway_s,self.discharge_headway_s)
        if any(not isfinite(v) or v<=0 for v in positive):
            raise ValueError('nonpositive/nonfinite vehicle parameter')
        if not isfinite(self.connector_clearance_buffer_s) or self.connector_clearance_buffer_s<0:
            raise ValueError('invalid connector buffer')

    @property
    def storage_footprint_m(self):
        return self.length_m+self.min_gap_m

CAR=VehicleSpec('car',4.5,1.8,2.0,1.5,3.0,1.3,2.0)
TRUCK=VehicleSpec('truck',11.0,2.5,3.0,0.95,2.2,1.9,3.5)
VEHICLE_CLASSES={s.name:s for s in (CAR,TRUCK)}


def get_vehicle_spec(name:str)->VehicleSpec:
    try:return VEHICLE_CLASSES[name]
    except KeyError as e:raise ValueError('unknown vehicle class: '+str(name)) from e
