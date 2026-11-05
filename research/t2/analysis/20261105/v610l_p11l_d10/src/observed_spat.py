"""Real-source Utah SPaT temporal evidence: transition intervals, never exact event instants."""
from datetime import datetime

def _ts(z):
    t=datetime.fromisoformat(z+'+00:00')
    return t.timestamp()

def audit_rows(rows):
    if not rows:raise ValueError('empty observation stream')
    ref=str(rows[0]['intersection_id']);out=[];prev=None
    for r in rows:
        if str(r.get('intersection_id'))!=ref:raise ValueError('mixed intersection')
        a=(r.get('signalgroup2'),r.get('signalgroup4'))
        if any(v not in ('R','Y','G') for v in a):raise ValueError('unknown state')
        t=_ts(r['tmstp_utc'])
        if prev is not None:
            if t<=prev[0]:raise ValueError('out-of-order or duplicate time')
            if a!=prev[1]:out.append({'after_utc':prev[2], 'no_later_than_utc':r['tmstp_utc'],
                                      'interval_width_s':round(t-prev[0],6),'from':''.join(prev[1]),'to':''.join(a)})
        prev=(t,a,r['tmstp_utc'])
    return {'kind':'OBSERVED_STATE_TRANSITION_BRACKETS_NOT_EXACT_EVENT_TIMES',
            'intersection':ref,'rows':len(rows),'transitions':out,
            'observations_not_vehicle_counts':True}
