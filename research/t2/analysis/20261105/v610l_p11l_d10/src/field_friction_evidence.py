"""Field-measurement contract for incompatible pavement metrics.
No SN->mu or source XODR friction->measured grip conversion is implemented.
"""
from __future__ import annotations
from dataclasses import dataclass,asdict
from math import isfinite
from datetime import datetime

METRICS={
 'LTPP_SKID_NUMBER':('dimensionless_skid_number','LTPP_MON_FRICTION'),
 'CPFM_REPORTED_FRICTION':('device_reported_dimensionless','FHWA_INFOMATERIALS_CPFM'),
 'MEAN_PROFILE_DEPTH':('millimetre','FHWA_TEXTURE'),
 'DFT_FRICTION':('device_reported_dimensionless','DFT_DEVICE'),
}
@dataclass(frozen=True)
class Measurement:
 source:str; source_record_id:str; metric:str; value:float; unit:str
 station_or_section:str; time_utc:str|None; device:str|None; test_speed_mps:float|None
 weather:str|None; reference_url:str

def validate(record:dict)->dict:
    # Fail closed on absent source and ambiguity; do not automatically infer location, date, or tire-grip physics.
    try:m=Measurement(**record)
    except TypeError as e:raise ValueError('missing or extra provenance fields') from e
    if m.metric not in METRICS:raise ValueError('unrecognized friction/texture metric')
    expected,source=METRICS[m.metric]
    if m.unit!=expected:raise ValueError('unit mismatch')
    if not m.source or not m.source_record_id or not m.station_or_section or not m.reference_url.startswith('https://'):raise ValueError('missing provenance')
    if m.source!=source:raise ValueError('wrong data authority for metric')
    if not isfinite(m.value) or m.value<0:raise ValueError('invalid value')
    if m.test_speed_mps is not None and (not isfinite(m.test_speed_mps) or m.test_speed_mps<=0):raise ValueError('invalid measurement speed')
    if m.time_utc:
        try:
            z=datetime.fromisoformat(m.time_utc.replace('Z','+00:00'))
            if z.tzinfo is None or z.utcoffset().total_seconds()!=0:raise ValueError('must be UTC')
        except (ValueError,AttributeError) as e:raise ValueError('bad UTC timestamp') from e
    return {'status':'MEASUREMENT_PROVENANCE_VALIDATED_NOT_PHYSICS_CALIBRATED','measurement':asdict(m),
            'effective_vehicle_tire_mu':None,'converted_to_tire_mu':False,
            'missing_context':[k for k in ('time_utc','device','test_speed_mps','weather') if getattr(m,k) is None]}
