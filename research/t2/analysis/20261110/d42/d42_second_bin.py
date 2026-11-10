"""Exact integer-second bin intersections; preserve multiplicity, not vehicle identity.

Publisher time series has 1-s bins. Floor an interpolated trajectory crossing only
as a diagnostic hypothesis; publisher's actual timestamp convention unverified.
"""
import csv,math,collections,json,sys
from d42_temporal_gate import candidate_events,expand_events

LABELS=('East','South','West','North')

def bin_overlap(candidates,published,shift_s=0.):
    observed=collections.Counter(math.floor(t) for t in published)
    proposed=collections.Counter(math.floor(t+shift_s) for t,_,_ in candidates)
    return {'matched_bins':sum(min(proposed[t],observed[t]) for t in proposed|observed),
       'candidate_excess':sum(max(proposed[t]-observed[t],0) for t in proposed|observed),
       'publisher_excess':sum(max(observed[t]-proposed[t],0) for t in proposed|observed),
       'candidate_total':sum(proposed.values()),'publisher_total':sum(observed.values())}

def evaluate(events_csv,volume_csv):
    c=candidate_events(events_csv);p=expand_events(volume_csv)
    if set(c)!=set(LABELS) or set(p)!=set(LABELS):raise ValueError('unknown approach')
    return [{'approach':a,**bin_overlap(c[a],p[a],0.),
         'shift_plus_1s':bin_overlap(c[a],p[a],1.)['matched_bins'],
         'shift_plus_5s':bin_overlap(c[a],p[a],5.)['matched_bins']} for a in LABELS]

if __name__=='__main__':
    if len(sys.argv)!=4:raise SystemExit('d42_second_bin.py candidates.csv publisher.csv out.json')
    result=evaluate(sys.argv[1],sys.argv[2]);open(sys.argv[3],'w').write(json.dumps(result,indent=2)+'\n')
    print('same-second overlaps:',sum(x['matched_bins'] for x in result))
