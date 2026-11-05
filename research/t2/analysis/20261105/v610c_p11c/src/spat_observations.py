"""Real-data SPaT validation, not an estimate of arrivals or vehicle queues.
Input: derived subset of public Utah UTC SPaT JSON; no secret credentials.
Treat absent signal groups as UNKNOWN, not red; irregular sampling must not be
used as if frames were equally spaced. Only observed transitions are counted.
"""
from collections import Counter
from datetime import datetime

def parse_utc_stamp(s):
    if not isinstance(s,str): raise ValueError('timestamp must be string')
    try:return datetime.fromisoformat(s.replace('Z','+00:00'))
    except (ValueError,TypeError) as e:raise ValueError('invalid timestamp') from e

def validate(rows,require_monotonic=False):
    if not isinstance(rows,list):raise ValueError('rows must be list')
    keys=['signalgroup'+str(i) for i in range(1,9)]
    allowed={'R','G','Y','r','g','y','D','F','U',''}
    ids=[];times=[];flags=[];pairs=[];states=[]
    for r in rows:
        if not isinstance(r,dict):raise ValueError('record not object')
        i=r.get('intersection_id')
        if i is None or not str(i):raise ValueError('no intersection_id')
        t=parse_utc_stamp(r.get('tmstp_utc'))
        state={k:r[k] for k in keys if k in r and r[k] not in (None,'')}
        if any(v not in allowed for v in state.values()):raise ValueError('invalid state')
        if not state:raise ValueError('no observed signal groups')
        ids.append(str(i));times.append(t);states.append(state)
        flags.append({k:r.get(k) for k in ('failure_flash','preempt_active','traffic_dependent_operation')})
        pairs.append(tuple(sorted(state.items())))
    if require_monotonic:
        if len(set(ids))>1:raise ValueError('must select one intersection')
        if times!=sorted(times):raise ValueError('timestamps unordered')
    return {'rows':len(rows),'intersections':len(set(ids)),'first_time':min(times).isoformat() if times else None,
            'last_time':max(times).isoformat() if times else None,
            'observed_transition_count':sum(pairs[i]!=pairs[i-1] for i in range(1,len(pairs))) if require_monotonic else None,
            'flags':{k:dict(Counter(str(f.get(k,'missing')) for f in flags)) for k in ('failure_flash','preempt_active','traffic_dependent_operation')},
            'groups_seen':sorted(set(x for d in states for x in d))}
