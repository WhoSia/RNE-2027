import csv,json,hashlib,sys
from collections import defaultdict
from datetime import datetime
from bisect import bisect_right
from pathlib import Path
from statistics import median
EXPECTED='95802b0c00f1232572279fed62668dfb484d8ea2303c4d3eb4a88339d41a8f0c'
# Frozen P35 crossing brackets: seconds from 23:30 UTC; no object identifiers.
E=[(123.766482,123.816482,.826482),(136.466482,136.516482,.526482),(234.666482,234.716482,.724482),(305.866482,305.916482,.929482),(306.516482,306.566482,.579482),(392.066482,392.116482,.137482),(395.716482,395.766482,.786482),(626.816482,626.866482,.876482),(645.366482,645.416482,.414482),(647.066482,647.116482,.126482),(648.716482,648.766482,.775482),(651.766482,651.816482,.826482),(666.066482,666.116482,.126482),(686.216482,686.266482,.276482),(720.366482,720.416482,.425482),(802.966482,803.016482,1.022482),(884.616482,884.666482,.678482)]
BASE=datetime.fromisoformat('2023-09-24T23:30:00+00:00')
def us(t):
    d=datetime.fromisoformat(t)-BASE
    return (d.days*86400+d.seconds)*10**6+d.microseconds

def run(path):
    sha=hashlib.sha256(path.read_bytes()).hexdigest(); assert sha==EXPECTED,sha
    frames=defaultdict(dict)
    with path.open(newline='') as f:
        for r in csv.DictReader(f):
            t=us(r['timestamp']);h=int(r['id']);assert h not in frames[t];frames[t][h]=int(r['state'])
    times=sorted(frames);heads=set(frames[times[0]])
    assert len(times)==899 and len(heads)==30 and all(set(v)==heads for v in frames.values())
    events=[tuple(round(x*10**6) for x in e) for e in E]
    refs=[]
    for a,b,age in events:
        i=bisect_right(times,a)-1;assert i>=0 and b-times[i]==age,(i,b-times[i],age);refs.append(i)
    rows=[];nested={}
    for k in [1,2,3,5,10]:
        for phase in range(k):
            kept=times[phase::k];ages=[];dheads=0;devents=0;unknown=0;event_ages=[]
            for (a,b,_),ref in zip(events,refs):
                j=bisect_right(kept,a)-1
                if j<0:unknown+=1;event_ages.append(None);continue
                t=kept[j];assert t<=a
                age=b-t;ages.append(age);event_ages.append(age)
                d=sum(frames[t][h]!=frames[times[ref]][h] for h in heads)
                dheads+=d;devents+=d>0
            if phase==0:nested[k]=event_ages
            rows.append(dict(k=k,offset=phase,retained=len(kept),events=len(events),unknown=unknown,age_min_us=min(ages),age_median_us=median(ages),age_max_us=max(ages),fresh_1s=sum(a<=10**6 for a in ages),fresh_2s=sum(a<=2*10**6 for a in ages),fresh_5s=sum(a<=5*10**6 for a in ages),different_head_event=dheads,events_with_difference=devents,comparable_head_event=len(ages)*len(heads)))
    for ks in [(1,2,10),(1,5,10)]:
        for prev,nxt in zip(ks,ks[1:]):assert all(a<=b for a,b in zip(nested[prev],nested[nxt]))
    summary=[]
    for k in [1,2,3,5,10]:
        rr=[r for r in rows if r['k']==k];s={'k':k,'offsets':len(rr),'event_offset_pairs':17*k,'head_event_offset_pairs':sum(r['comparable_head_event'] for r in rr)}
        for key in ['fresh_1s','fresh_2s','fresh_5s','different_head_event','events_with_difference']:
            v=[r[key] for r in rr];s[key]={'sum':sum(v),'min':min(v),'max':max(v)}
        s['max_age_us']=max(r['age_max_us'] for r in rr);summary.append(s)
    return dict(source_sha256=sha,p35_git_blob='877c80866acb4c792d448e08007b19764068a88b',frames=len(times),heads=len(heads),events=len(E),full_stream_parity=True,nested_age_monotone=True,summary=summary,offsets=rows)
if __name__=='__main__':print(json.dumps(run(Path(sys.argv[1])),indent=2))
