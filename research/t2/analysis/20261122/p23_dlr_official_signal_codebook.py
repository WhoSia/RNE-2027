"""DLR UT 1.3.1 documented signal-code decoding; not lane-to-signal assignment.

Grounding: publisher documentation PDF, printed page 14 Table 4, and printed
page 12 Figure 1. Source time series is the exact 2023-09-24 23:30 UTC CSV.
"""
import csv
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import median

CSV_SHA='95802b0c00f1232572279fed62668dfb484d8ea2303c4d3eb4a88339d41a8f0c'
PDF_SHA='3c733b677ee63fd2cb282946f415f649d23954ac420d5bc37e0af545f7293849'
CODES={'0':'unavailable','1':'off','2':'stop_before_proceed','3':'red_stop_wait',
 '4':'red_and_yellow','5':'green','6':'green_protected_movement',
 '7':'yellow','8':'yellow_protected_movement','9':'yellow_flashing'}

def category(signal_id):
    if signal_id in range(1,10):return 'motor_vehicle_signal'
    if signal_id in range(10,30):return 'vulnerable_road_user_signal'
    if signal_id==30:return 'flashing_vru_warning'
    raise ValueError('signal identifier not represented in publisher Figure 1')

def analyze(csv_path, pdf_path):
    csv_path=Path(csv_path);pdf_path=Path(pdf_path)
    if hashlib.sha256(csv_path.read_bytes()).hexdigest()!=CSV_SHA:
        raise ValueError('wrong signal sample bytes')
    if hashlib.sha256(pdf_path.read_bytes()).hexdigest()!=PDF_SHA:
        raise ValueError('wrong publisher codebook bytes')
    with csv_path.open(encoding='utf-8',newline='') as f:
        rows=list(csv.DictReader(f))
    series=defaultdict(list)
    by_type=defaultdict(Counter)
    unknown=Counter()
    for row in rows:
        code=row['state']
        if code not in CODES:unknown[code]+=1;continue
        sid=int(row['id'])
        dt=datetime.fromisoformat(row['timestamp'])
        if dt.tzinfo is None:raise ValueError('naive time in source')
        series[sid].append((dt,code))
        by_type[category(sid)][code]+=1
    if unknown:raise ValueError('undocumented light code in source')
    if sorted(series)!=list(range(1,31)):
        raise ValueError('missing or unexpected source signal identifier')
    if any(len(v)!=899 for v in series.values()):
        raise ValueError('not the frozen matched 899-sample signal window')
    gaps=[]; changes=0; classifications={}
    for sid,seq in sorted(series.items()):
        seq=sorted(seq)
        for (t,a),(u,b) in zip(seq,seq[1:]):
            d=(u-t).total_seconds()
            if d<=0:raise ValueError('duplicate or nonascending timestamp')
            gaps.append(d)
            changes+=int(a!=b)
        classifications[str(sid)]=category(sid)
    if any(code not in ('1','9') for code in by_type['flashing_vru_warning']):
        raise ValueError('ID30 displays an unexpected code')
    return {'status':'OFFICIAL_CODEBOOK_DECODED_NO_STOPLINE_SIGNAL_MAPPING',
            'codebook_pdf_sha256':PDF_SHA,'original_traffic_signal_csv_sha256':CSV_SHA,
            'official_source':'DLR-UT v1.3.1 printed page14 Table4; page12 Figure1',
            'codebook':CODES,'source_rows':len(rows), 'signal_ids':len(series),
            'signal_code_changes':changes,
            'by_signal_purpose':{type_:dict(sorted(counts.items(),key=lambda x:int(x[0])))
                for type_,counts in sorted(by_type.items())},
            'signal_id_categories':classifications,
            'sampling_intervals_s':{'minimum':min(gaps),'maximum':max(gaps),
                'median':median(gaps),'gaps_over_1_5_s':sum(g>1.5 for g in gaps)},
            'gates':{'official_code_meaning_verified':True,'physical_signal_purpose_verified':True,
                'controlling_signal_to_movement_verified':False,'exact_stopline_vehicle_headway_verified':False,
                'real_world_policy_safety_verified':False,'independent_SUMO_validation':False}}

if __name__=='__main__':
    import argparse
    a=argparse.ArgumentParser()
    a.add_argument('signal_csv',type=Path);a.add_argument('official_pdf',type=Path);a.add_argument('result_json',type=Path)
    x=a.parse_args()
    x.result_json.write_text(json.dumps(analyze(x.signal_csv,x.official_pdf),sort_keys=True,indent=2)+'\n',encoding='utf-8')
