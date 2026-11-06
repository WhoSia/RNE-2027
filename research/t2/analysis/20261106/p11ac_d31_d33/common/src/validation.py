"""D29: explicit external-evidence reader. Never treats self-generated data as SUMO output."""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite
from pathlib import Path
from xml.etree import ElementTree as ET
import csv, hashlib

@dataclass(frozen=True)
class Trip:
    identity: str
    depart_s: float
    arrive_s: float
    depart_delay_s: float
    duration_s: float

def sumo_tripinfo(path: str|Path)->dict[str,Trip]:
    """Parse a *pre-existing* SUMO tripinfo XML; the simulator is not launched here."""
    path=Path(path)
    if not path.is_file():raise FileNotFoundError(f'no SUMO output: {path}')
    root=ET.parse(path).getroot()
    if root.tag!='tripinfos':raise ValueError('not SUMO tripinfos XML')
    records={}
    for row in root.findall('tripinfo'):
        key=row.get('id','')
        if not key or key in records:raise ValueError('duplicate or missing SUMO vehicle id')
        try:depart=float(row.attrib['depart']);arrive=float(row.attrib['arrival']);delay=float(row.attrib['departDelay']);duration=float(row.attrib['duration'])
        except (ValueError,KeyError) as exc:raise ValueError(f'invalid SUMO tripinfo for {key}') from exc
        if not all(isfinite(x) for x in (depart,arrive,delay,duration)) or depart<0 or delay<0 or duration<0 or arrive<depart:
            raise ValueError('nonfinite/negative SUMO trip')
        if abs((arrive-depart)-duration)>1e-3:raise ValueError('inconsistent SUMO duration')
        records[key]=Trip(key,depart,arrive,delay,duration)
    if not records:raise ValueError('no completed SUMO trips')
    return records

def compare_trips(model_admit:dict[str,int],model_finish:dict[str,int],reference:dict[str,Trip], *,max_missing_fraction=0.0)->dict:
    if not reference:raise ValueError('external reference required')
    matched=set(model_finish)&set(reference)
    mismatched=set(model_finish)^set(reference)
    if not 0<=max_missing_fraction<=1:raise ValueError('invalid missingness threshold')
    if len(mismatched)/len(set(model_finish)|set(reference))>max_missing_fraction:
        raise ValueError('vehicle cohort mismatch; no silently dropped ids')
    if not matched:raise ValueError('no matched vehicles')
    errs=[]
    for identity in sorted(matched):
        if identity not in model_admit or model_finish[identity]<model_admit[identity]:raise ValueError('invalid model trip')
        duration=model_finish[identity]-model_admit[identity]
        errs.append(duration-reference[identity].duration_s)
    return {'matched':len(matched),'unmatched':len(mismatched),
            'mae_duration_s':sum(abs(x) for x in errs)/len(errs),
            'mean_bias_duration_s':sum(errs)/len(errs),
            'max_abs_error_s':max(abs(x) for x in errs)}

def file_receipt(path):
    p=Path(path)
    if not p.is_file():raise FileNotFoundError(p)
    return {'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

def field_queue_csv(path, *,date_key='time_s',queue_key='queue_vehicles'):
    """Only explicit observed queue size; passing counts as queue size is a schema error."""
    with open(path,newline='',encoding='utf-8-sig') as handle:
        reader=csv.DictReader(handle)
        if not {date_key,queue_key}.issubset(set(reader.fieldnames or [])):
            raise ValueError('field observations require explicit queue size and time')
        rows=[]
        for row in reader:
            t=float(row[date_key]);q=float(row[queue_key])
            if not(isfinite(t) and isfinite(q)) or q<0:raise ValueError('invalid observation')
            rows.append((t,q))
    if not rows or any(a[0]>=b[0] for a,b in zip(rows,rows[1:])):
        raise ValueError('missing/nonmonotonic field timestamps')
    return rows
