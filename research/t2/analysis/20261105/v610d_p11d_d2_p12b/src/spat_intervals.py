"""Irregularly sampled SPaT edge bracketing. Never assign exact transition time.

One intersection, strictly ordered timestamps and exactly named observed groups.
Data loaded from an independently retrieved official Socrata JSON series by caller.
"""
from datetime import datetime
from spat_observations import validate

def edges(rows, groups=('signalgroup2','signalgroup4')):
    validate(rows,require_monotonic=True)
    def stamp(x):return datetime.fromisoformat(x['tmstp_utc'].replace('Z','+00:00'))
    out=[]
    for a,b in zip(rows,rows[1:]):
        x=tuple(a.get(k) for k in groups); y=tuple(b.get(k) for k in groups)
        if any(z is None for z in (*x,*y)):
            continue # unknown is not red and is not an observable transition
        if x==y:continue
        lo,hi=stamp(a),stamp(b)
        delta=(hi-lo).total_seconds()
        if delta<0:raise ValueError('unsorted timestamps')
        out.append({'lower_exclusive_utc':a['tmstp_utc'],'upper_inclusive_utc':b['tmstp_utc'],
                    'time_uncertainty_s':delta,'old_state':list(x),'new_state':list(y)})
    return out
