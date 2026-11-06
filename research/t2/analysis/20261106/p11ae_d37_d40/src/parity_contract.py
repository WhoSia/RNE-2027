"""Proof obligations before labeling a T2 vs SUMO experiment independent.

The contract is intentionally stricter than having two output CSVs.
"""
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

@dataclass(frozen=True)
class Evidence:
    source_sha256: str
    executable_version: str
    network_geometry_fingerprint: str
    demand_fingerprint: str
    signal_fingerprint: str
    time_unit: str
    distance_unit: str
    vehicle_id_semantics: str
    queue_definition: str
    completed_vehicle_count: int
    source_is_observed: bool


def evaluate_pair(t2: Evidence, sumo: Evidence, *, required_queue=True) -> dict:
    reasons = []
    for title, value in (
        ('SUMO executable version', sumo.executable_version),
        ('T2 executable version', t2.executable_version),
        ('SUMO raw source SHA256', sumo.source_sha256),
        ('T2 raw source SHA256', t2.source_sha256),
    ):
        if not value: reasons.append(f'missing {title}')
    for field in ('network_geometry_fingerprint','demand_fingerprint','signal_fingerprint',
                  'time_unit','distance_unit','vehicle_id_semantics'):
        if not getattr(t2,field) or getattr(t2,field)!=getattr(sumo,field):
            reasons.append(f'missing or conflicting {field}')
    if required_queue and (not t2.queue_definition or t2.queue_definition!=sumo.queue_definition):
        reasons.append('queue metric definition mismatch')
    if t2.completed_vehicle_count!=sumo.completed_vehicle_count:
        reasons.append('completed vehicles differ; right censoring / insertion delay')
    if not sumo.source_is_observed:
        reasons.append('SUMO raw output not observed; synthetic placeholder refused')
    return {'ready_for_metric_comparison':not reasons,'blocked_reasons':reasons,
            'claim_if_ready':'numerical comparison permitted, not validated real-world predictivity'}


def source_receipt(path: str|Path) -> dict:
    p=Path(path)
    if not p.is_file(): raise FileNotFoundError('missing original external evidence')
    b=p.read_bytes()
    if len(b)==0: raise ValueError('empty evidence')
    return {'filename':p.name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}


def audited_trip_rows(path: str|Path) -> list[dict]:
    """Only parse observed SUMO tripinfo. Never manufacture completion records."""
    from xml.etree import ElementTree as ET
    receipt=source_receipt(path)
    root=ET.parse(path).getroot()
    if root.tag!='tripinfos':raise ValueError('not tripinfo XML')
    result=[];ids=set()
    for trip in root.findall('tripinfo'):
        ident=trip.attrib.get('id');dep=trip.attrib.get('depart');arr=trip.attrib.get('arrival')
        if not ident or ident in ids or dep is None or arr is None:raise ValueError('invalid or duplicate trip')
        ids.add(ident)
        try: ds=float(dep);as_=float(arr)
        except ValueError as ex: raise ValueError('non-numeric trip times') from ex
        if ds>as_:raise ValueError('arrival before departure')
        result.append({'id':ident,'depart_s':ds,'arrival_s':as_})
    return result
