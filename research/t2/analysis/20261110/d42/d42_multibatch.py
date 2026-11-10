"""D42 multi-window fixed-parameter validation of candidate crossings.

Uses prior, unaltered lane gate; no tuning on new-window publisher totals.
Publisher 5.1: files omit movement columns without observed crossings.
"""
import csv, json, sys, hashlib, pathlib
from collections import Counter
from d42_topology_gate import read_network, candidate_counts, INCOMING
from d42_temporal_gate import evaluate

ALLOWED=('East','South','West','North')

def volume_summary(path):
    with open(path,encoding='utf8',newline='') as f:
        r=csv.DictReader(f)
        assert r.fieldnames and r.fieldnames[0]=='timestamp'
        movement_names=r.fieldnames[1:]
        if not movement_names:raise ValueError('missing movement columns')
        if len(movement_names)!=len(set(movement_names)):raise ValueError('duplicate movement')
        if not all(any(name.startswith(a) for a in ALLOWED) for name in movement_names):
            raise ValueError('unknown origin')
        by=Counter({a:0 for a in ALLOWED}); rows=0
        for row in r:
            rows+=1
            for name in movement_names:
                v=int(row[name]);
                if v<0:raise ValueError('negative count')
                approach=next(a for a in ALLOWED if name.startswith(a))
                by[approach]+=v
    if rows!=900:raise ValueError('unexpected 15-min rows')
    return {'columns':len(movement_names),'seconds':rows,'counts':dict(by),'total':sum(by.values()),'column_names':movement_names}

def audit(map_path,events_csv,volume_csv):
    links=read_network(map_path)
    v=volume_summary(volume_csv)
    cand,byroad,unique,duplicate=candidate_counts(events_csv)
    matched,unmatched=evaluate(events_csv,volume_csv)
    approaches=[{'direction':name,'candidate':cand[road], 'published':v['counts'][name],
      'difference':cand[road]-v['counts'][name],**{k:rec[k] for k in ('matched_within_1s','candidate_unmatched_within_1s','publisher_unmatched_within_1s','matched_within_0p5s') }}
      for road,name in INCOMING.items() for rec in matched if rec['approach']==name]
    return {'volume':v,'network_routes':len(links),'network_lane_links':sum(len(l['lane_links']) for l in links),
      'candidate_approach':sum(cand.values()),'candidate_tracks':unique,
      'duplicate_approach_track_ids':duplicate,'approaches':approaches,
      'temporal_matched':sum(x['matched_within_1s'] for x in matched),
      'candidate_unmatched':sum(x['candidate_unmatched_within_1s'] for x in matched),
      'publisher_unmatched':sum(x['publisher_unmatched_within_1s'] for x in matched),
      'unmatched_events':unmatched,
      'status':'HOLD_INTERNAL_CONSISTENCY_NOT_INDEPENDENT_VALIDATION'}

if __name__=='__main__':
    if len(sys.argv)!=5:raise SystemExit('python d42_multibatch.py map.xodr candidate.csv volume.csv output.json')
    res=audit(*sys.argv[1:4]);pathlib.Path(sys.argv[4]).write_text(json.dumps(res,indent=2)+'\n')
    print(json.dumps({k:v for k,v in res.items() if k!='unmatched_events' and k!='volume'},indent=2))
    print('publisher columns',res['volume']['columns'],'published total',res['volume']['total'])
