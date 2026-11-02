"""T2 v4.0 independent field window validation; not real traffic data."""
import csv, math
from collections import defaultdict
KEY=('site_id','day','window','junction','approach','movement')
FIELDS=(*KEY,'start_s','end_s','arrivals','departures','queue_start','queue_end')
def read(path):
    seen=set(); rows=[]
    with open(path,encoding='utf-8-sig',newline='') as fh:
        rd=csv.DictReader(fh)
        if set(FIELDS)-set(rd.fieldnames or []):raise ValueError('schema')
        for n,r in enumerate(rd,2):
            k=tuple(r[x].strip() for x in KEY)
            if not all(k):raise ValueError(f'empty key {n}')
            try:z={x:int(r[x]) for x in FIELDS[len(KEY):]}
            except (ValueError,TypeError):raise ValueError(f'invalid integer {n}') from None
            if z['start_s']<0 or z['end_s']<=z['start_s'] or min(z[x] for x in ('arrivals','departures','queue_start','queue_end'))<0:raise ValueError(f'invalid values {n}')
            id_=(k,z['start_s'],z['end_s'])
            if id_ in seen:raise ValueError(f'duplicate {n}')
            seen.add(id_);rows.append({'key':k,**z})
    by=defaultdict(list)
    for r in rows:by[r['key']].append(r)
    discontinuities=[]
    for k,rs in by.items():
        rs.sort(key=lambda r:r['start_s'])
        for a,b in zip(rs,rs[1:]):
            if b['start_s']<a['end_s']:raise ValueError(f'overlap {k}')
            if b['start_s']==a['end_s'] and a['queue_end']!=b['queue_start']:
                discontinuities.append({'key':k,'boundary':a['end_s'],'left':a['queue_end'],'right':b['queue_start']})
    return rows,discontinuities
def audit(rows):
    return [{'key':r['key'],'start_s':r['start_s'],'end_s':r['end_s'],'queue_residual':r['queue_start']+r['arrivals']-r['departures']-r['queue_end']} for r in rows]
def holdout(predictions,observations,day):
    subset=[r for r in observations if r['key'][1]==day]
    if not subset:raise ValueError('empty holdout')
    err=[];actual=[];pred=[]
    for r in subset:
        key=(*r['key'],r['start_s'],r['end_s'])
        if key not in predictions:raise ValueError('missing prediction')
        x=predictions[key]
        if not isinstance(x,(float,int)) or not math.isfinite(x) or x<0:raise ValueError('invalid prediction')
        actual.append(r['departures']);pred.append(x);err.append(abs(x-r['departures']))
    return {'n':len(subset),'MAE_vehicles_per_window':sum(err)/len(err),'WAPE':sum(err)/sum(actual) if sum(actual)>0 else None,'total_observed':sum(actual),'total_predicted':sum(pred)}
