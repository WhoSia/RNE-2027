"""Frame-synchronized MARWIS source auditor.

Rows/frames are NOT independent traction measurements. This is a quality and
provenance tool; it does not infer road safety, speed or causal material effects.
"""
from __future__ import annotations
import csv
from io import StringIO
from math import isfinite

FIELDS=('timestamp_sec','marwis_friction','marwis_road_condition','marwis_surface_temp_c','marwis_water_film_height')

def audit_csv_text(csv_text:str, source_ref:str)->dict:
    if not source_ref.strip():raise ValueError('source ref required')
    reader=csv.DictReader(StringIO(csv_text))
    if not set(FIELDS).issubset(reader.fieldnames or ()):raise ValueError('missing sensor fields')
    count=0;valid=0;changes=0;blocks=[];states={};last_t=None;last_value=None;all_values=[]
    for row in reader:
        count+=1
        try:t=float(row['timestamp_sec'])
        except (TypeError,ValueError) as e:raise ValueError('bad timestamp') from e
        if not isfinite(t) or (last_t is not None and t<=last_t):raise ValueError('unordered/invalid timestamp')
        last_t=t
        val_text=(row['marwis_friction'] or '').strip()
        val=None
        if val_text:
            try:val=float(val_text)
            except ValueError as e:raise ValueError('bad instrument value') from e
            if not isfinite(val) or val<0:raise ValueError('invalid instrument value')
            valid+=1;all_values.append(val)
        if count==1 or val!=last_value:
            if count>1:changes+=1
            blocks.append({'start_row':count,'first_timestamp_epoch_s':t,'sensor_value':val})
        last_value=val
        condition=(row['marwis_road_condition'] or 'MISSING').strip()
        states[condition]=states.get(condition,0)+1
    if count==0:raise ValueError('empty CSV')
    sorted_vals=sorted(all_values)
    return {'status':'REAL_INSTRUMENT_FRAME_AUDIT_NOT_CALIBRATED_GRIP',
            'source':source_ref,'frame_rows':count,'instrument_value_rows':valid,
            'consecutive_sensor_constant_blocks':len(blocks),
            'between_row_sensor_value_changes':changes,
            'first_appearance_blocks':blocks,
            'distinct_sensor_values':len(set(all_values)),
            'sensor_value_range':[sorted_vals[0],sorted_vals[-1]] if valid else None,
            'sensor_value_median_frame_weighted':sorted_vals[len(sorted_vals)//2] if valid else None,
            'condition_frame_counts':states,
            'effective_independent_measurement_count':None,
            'device_measurement_rate_hz':None,
            'inference_warning':'Frame repeats and temporal dependence: never treat rows or runs as independent ground-truth friction measurements.'}
