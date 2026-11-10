"""Time-matching probe for DLR candidate approach gates vs publisher volume.

NOT an independently validated stopline recount: movement assignment remains UNKNOWN.
This analysis reuses publisher-derived traffic volume (same sensor lineage).
"""
import csv
import datetime
import json
from collections import defaultdict
from pathlib import Path

ROAD_TO_APPROACH={'100000':'East','179000':'South','201000':'West','280000':'North'}

def expand_events(volume_csv):
    by=defaultdict(list)
    with open(volume_csv,encoding='utf8',newline='') as f:
        for row in csv.DictReader(f):
            t=datetime.datetime.fromisoformat(row['timestamp']).timestamp()
            for name,v in row.items():
                if name=='timestamp':continue
                approach=next((a for a in ROAD_TO_APPROACH.values() if name.startswith(a)),None)
                if approach is None:raise ValueError('unrecognized movement')
                count=int(v)
                if count<0:raise ValueError('negative traffic count')
                by[approach].extend([t]*count)
    return {a:sorted(by[a]) for a in ROAD_TO_APPROACH.values()}

def candidate_events(events_csv):
    by=defaultdict(list)
    with open(events_csv,encoding='utf8',newline='') as f:
        for row in csv.DictReader(f):
            if row['road_id'] in ROAD_TO_APPROACH:
                if row['direction']!='forward':raise ValueError('reverse approach event')
                by[ROAD_TO_APPROACH[row['road_id']]].append((float(row['epoch_s']),row['track_id'],row['lane_id']))
    return {a:sorted(by[a]) for a in ROAD_TO_APPROACH.values()}

def monotone_match(candidate,publisher,tolerance=1.,shift=0.):
    """Greedy maximum-cardinality matching on ordered 1-D timestamps with window.

    Returns matched and unmatched events, preserving repeated publisher counts.
    This has no vehicle identity truth and may match different real objects.
    """
    if tolerance<0:raise ValueError('negative tolerance')
    aa=sorted([(t+shift,tid,lane) for t,tid,lane in candidate]);bb=sorted(publisher)
    i=j=0;matches=[];unmatched_candidates=[];unmatched_publisher=[]
    while i<len(aa) and j<len(bb):
        t,tid,lane=aa[i];reference=bb[j]
        if abs(t-reference)<=tolerance+1e-9:
            matches.append({'candidate_epoch_s':t,'published_epoch_s':reference,
                'residual_s':t-reference,'track_id':tid,'lane_id':lane})
            i+=1;j+=1
        elif t<reference-tolerance:
            unmatched_candidates.append(aa[i]);i+=1
        else:
            unmatched_publisher.append(bb[j]);j+=1
    unmatched_candidates.extend(aa[i:]);unmatched_publisher.extend(bb[j:])
    assert len(matches)+len(unmatched_candidates)==len(aa)
    assert len(matches)+len(unmatched_publisher)==len(bb)
    return matches,unmatched_candidates,unmatched_publisher

def evaluate(events_csv,volume_csv):
    candidates=candidate_events(events_csv);reported=expand_events(volume_csv)
    results=[];unmatched=[]
    for label in ['East','South','West','North']:
        xs=candidates[label];ys=reported[label]
        m,extra,missing=monotone_match(xs,ys,1.,0.)
        m05,_,_=monotone_match(xs,ys,.5,0.)
        mshift,_,_=monotone_match(xs,ys,1.,1.)
        m5,_,_=monotone_match(xs,ys,1.,5.)
        results.append({'approach':label,'candidate_count':len(xs),'publisher_count':len(ys),
            'matched_within_1s':len(m),'candidate_unmatched_within_1s':len(extra),
            'publisher_unmatched_within_1s':len(missing),
            'matched_within_0p5s':len(m05),'matched_shift_candidate_plus_1s':len(mshift),
            'matched_shift_candidate_plus_5s':len(m5),'status':'EXPLORATORY_APPROACH_TIME_MATCH_NOT_LANE_VALIDATED'})
        for x in extra:
            unmatched.append({'approach':label,'kind':'candidate','epoch_s':x[0],'track_id':x[1]})
        for t in missing:
            unmatched.append({'approach':label,'kind':'publisher','epoch_s':t,'track_id':''})
    return results,unmatched

def main(events_csv,volume_csv,prefix):
    results,unmatched=evaluate(events_csv,volume_csv)
    Path(prefix+'.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf8')
    with open(prefix+'_summary.csv','w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
    with open(prefix+'_unmatched.csv','w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=['approach','kind','epoch_s','track_id']);w.writeheader();w.writerows(unmatched)
    print(json.dumps(results,indent=2))

if __name__=='__main__':
    import sys
    if len(sys.argv)!=4:raise SystemExit('usage: temporal_gate.py candidates.csv publisher_volume.csv output_prefix')
    main(*sys.argv[1:])
