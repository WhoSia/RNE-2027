"""DLR-UT v1.3.1: source-document signal state and approach-level baseline.

Non-commercial research reuse. Source: DLR-Urban-Traffic-dataset_v1-3-1_documentation.pdf,
pp. 12–14 (Figure 1 and Tables 3–4), © DLR, CC BY-NC-SA 4.0 dataset.

A signal head ID is not a road marking ID. Approach group is explicitly transcribed
from Figure 1, NOT a certified lane/movement controller association.
"""
from __future__ import annotations
import argparse
import bisect
import csv
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import median

# Carefully transcribed FROM DLR-UT v1.3.1 PDF Figure 1 p.12.
VEHICULAR_APPROACH_HEADS = {
    "north": (1, 2), "east": (3, 4), "south": (5, 6, 7), "west": (8, 9)
}
# Four approach-to-road matches are geometric inference checked against Figure 1,
# NOT a signed declaration of the specific lane movement controlled by each head.
ROAD_APPROACH_CANDIDATE = {"100000": "east", "179000": "south",
                           "201000": "west", "280000": "north"}
# Match semantics of DLR-UT documentation Table 4, page 14.
STATE_SEMANTICS = {
    0: "unavailable", 1: "off", 2: "stop_required", 3: "red",
    4: "red_yellow", 5: "green", 6: "green_protected",
    7: "yellow", 8: "yellow_protected", 9: "yellow_flashing"
}
GREEN = frozenset({5, 6})

def utc(v: str) -> datetime:
    dt = datetime.fromisoformat(v.replace('Z', '+00:00'))
    if dt.tzinfo is None: raise ValueError('timezone required')
    return dt.astimezone(timezone.utc)

def source_table3(text: str):
    """Extract 35 coordinate placements, preserving repeated IDs (1, 3...)."""
    anchor = text.rfind('Table 3: Traffic light coordinates')
    if anchor == -1: raise ValueError('source Table 3 not present')
    end = text.find('4.2.3. Traffic Light States', anchor)
    if end == -1: raise ValueError('Table 3 boundary missing')
    part = text[anchor:end]
    rows = re.findall(r'^\s*(\d{1,2})\s+(604\d{3}\.\d+)\s+(5792\d{3}\.\d+)\s*$', part, flags=re.M)
    out = [(int(i), float(e), float(n)) for i, e, n in rows]
    if len(out)!=35 or {a for a,_,_ in out}!={*range(1,10),*range(14,31)}:
        raise ValueError('documentation coordinate table differs from verified source layout')
    return out

def source_table4(text: str):
    anchor = text.rfind('Table 4: Traffic light states')
    if anchor == -1: raise ValueError('source Table 4 missing')
    end=text.find('4.3.', anchor)
    part=text[anchor:end if end!=-1 else None]
    p=re.findall(r'^\s*([0-9])\s+(.*?)(?=\n)',part,flags=re.M)
    codes={int(i) for i,_ in p}
    if codes!=set(range(10)):
        raise ValueError(f'signal state table incomplete: {codes}')
    return {int(i):desc.strip() for i,desc in p}

def read_signals(path: str | Path):
    by_id=defaultdict(list); moment_ids=defaultdict(set)
    with open(path, newline='', encoding='utf-8-sig') as f:
        reader=csv.DictReader(f)
        if reader.fieldnames != ['timestamp','id','state']: raise ValueError('unexpected signal columns')
        for r in reader:
            t=utc(r['timestamp']); i=int(r['id']); state=int(r['state'])
            if i not in range(1,31) or state not in STATE_SEMANTICS:
                raise ValueError('head ID or state outside documentation range')
            if i in moment_ids[t]: raise ValueError('duplicate head ID at identical timestamp')
            moment_ids[t].add(i)
            by_id[i].append((t,state))
    if set(by_id)!=set(range(1,31)) or any(set(ids)!=set(range(1,31)) for ids in moment_ids.values()):
        raise ValueError('source file has missing head at an observation instant')
    for seq in by_id.values():
        seq.sort()
        if len({t for t,_ in seq}) != len(seq):raise ValueError('duplicate timestamp in signal head')
    return dict(by_id)

def signal_bracket(seq, time:datetime, max_age_s=2.):
    """No interpolation across a state transition; return uncertainty explicitly."""
    times = [t for t,_ in seq]
    pos=bisect.bisect_right(times,time)
    previous=seq[pos-1] if pos>0 else None
    following=seq[pos] if pos<len(seq) else None
    prev_age=(time-previous[0]).total_seconds() if previous else float('inf')
    next_age=(following[0]-time).total_seconds() if following else float('inf')
    prev_state=previous[1] if prev_age<=max_age_s else None
    next_state=following[1] if next_age<=max_age_s else None
    if prev_state is None or next_state is None:
        verdict='censored_or_gap'
    elif prev_state!=next_state:
        verdict='transition_within_bracket'
    else:
        verdict='bracket_stable'
    return {'prev_code':prev_state,'next_code':next_state,
            'prev_age_s':round(prev_age,3) if prev_state is not None else None,
            'next_age_s':round(next_age,3) if next_state is not None else None,
            'status':verdict}

def signal_block_summary(by_id,window_label):
    rows=[]
    for i in range(1,10):
        seq=by_id[i]
        counts=Counter(v for _,v in seq)
        transitions=sum(a[1]!=b[1] for a,b in zip(seq,seq[1:]))
        green_fraction=sum(counts[s] for s in GREEN)/len(seq)
        # Observed sample fraction, NOT actual time-weighted green fraction.
        rows.append({'window':window_label,'head_id':i,
                     'documented_approach': next(n for n,ids in VEHICULAR_APPROACH_HEADS.items() if i in ids),
                     'observed_samples':len(seq),'sampled_green_fraction':round(green_fraction,6),
                     'red_samples':counts[3],'red_yellow_samples':counts[4],
                     'green_samples':counts[5],'protected_green_samples':counts[6],
                     'yellow_samples':counts[7], 'other_samples':len(seq)-sum(counts[j] for j in (3,4,5,6,7)),
                     'observed_changes':transitions})
    return rows

def candidate_brackets(by_id,events):
    out=[]
    for event in events:
        road=event['road_id']
        if road not in ROAD_APPROACH_CANDIDATE: raise ValueError('unrecognized approach road')
        approach=ROAD_APPROACH_CANDIDATE[road]
        for head in VEHICULAR_APPROACH_HEADS[approach]:
            for location in ('center','front'):
                ts=utc(event[f'{location}_utc'])
                b=signal_bracket(by_id[head],ts)
                out.append({'road_id':road,'object_id':event['object_id'],
                  'documented_approach':approach,'candidate_head_id':head,
                  'geometry_point':location,'crossing_utc':ts.isoformat(),
                  **b, 'movement_mapping':'UNKNOWN',
                  'legal_signal_compliance':'NOT_EVALUATED'})
    return out

def load_events(path):
    with open(path,newline='',encoding='utf8') as f:return list(csv.DictReader(f))

def save_csv(path, rows):
    if not rows:raise ValueError('empty rows')
    with open(path,'w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--documentation-text',required=True)
    ap.add_argument('--signal-2330',required=True)
    ap.add_argument('--signal-1230',required=True)
    ap.add_argument('--paired-v4',required=True)
    ap.add_argument('--out',required=True)
    args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    doc=Path(args.documentation_text).read_text(encoding='utf8')
    placements=source_table3(doc);descriptions=source_table4(doc)
    save_csv(out/'documented_signal_positions.csv', [
        {'head_id':i,'utm32_easting_m':e,'utm32_northing_m':n,
         'figure1_approach':next((a for a,ids in VEHICULAR_APPROACH_HEADS.items() if i in ids),'pedestrian_bicycle_or_other'),
         'source':'DLR UT 1.3.1 documentation Table 3 pp12-13'}
        for i,e,n in placements])
    save_csv(out/'documented_signal_states.csv', [
        {'state_code':j,'official_description':desc,'short_code':STATE_SEMANTICS[j]}
        for j,desc in descriptions.items()])
    a=read_signals(args.signal_2330);b=read_signals(args.signal_1230)
    blocks=signal_block_summary(a,'2023-09-24T23:30_23:45Z')+signal_block_summary(b,'2023-09-24T12:30_12:45Z')
    save_csv(out/'observed_head_phase_samples.csv',blocks)
    candidate=candidate_brackets(a,load_events(args.paired_v4))
    save_csv(out/'v4_candidate_signal_brackets.csv',candidate)
    verdicts=Counter(r['status'] for r in candidate)
    d={'source':'DLR-UT v1.3.1 official documentation, Figure 1, Tables 3–4 and §5.1',
       'coords_placements':len(placements),'coordinate_ids':len(set(i for i,_,_ in placements)),
       'ids_without_coordinate_rows':sorted(set(range(1,31))-set(i for i,_,_ in placements)),
       'samples_2330_per_head':len(a[1]),'samples_1230_per_head':len(b[1]),
       'pair_events':len(load_events(args.paired_v4)),
       'head_location_brackets':len(candidate), 'bracket_quality_counts':dict(verdicts),
       'caution':'Approach-level candidate head associations only, no lane-turn or signal compliance conclusions. Publisher volume derived from the same trajectories and is NOT independent ground truth.'}
    (out/'g1v5_summary.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(d,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
