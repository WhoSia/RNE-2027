"""T2 empirical observation checker (not a simulation, no real field data included)."""
import csv

FIELDS=('site_id','day','window','junction','approach','movement','arrivals','departures','queue_start','queue_end','green_seconds','cycles','mean_headway_s')

def read_observations(path):
    records=[]; seen=set()
    with open(path,encoding='utf-8-sig',newline='') as fh:
        rd=csv.DictReader(fh)
        if set(FIELDS)-set(rd.fieldnames or []):
            raise ValueError('missing schema fields')
        for i,row in enumerate(rd,2):
            key=tuple(row[k].strip() for k in FIELDS[:6])
            if not all(key) or key in seen:raise ValueError(f'empty or duplicate key at {i}')
            seen.add(key)
            try:
                vals={k:int(row[k]) for k in ('arrivals','departures','queue_start','queue_end','cycles')}
                vals.update({k:float(row[k]) for k in ('green_seconds','mean_headway_s')})
            except (ValueError,TypeError):
                raise ValueError(f'bad numeric field at {i}') from None
            if min(vals.values())<0 or vals['mean_headway_s']<=0:raise ValueError(f'invalid measurement at {i}')
            records.append({'key':key,**vals})
    return records

def audit(records):
    report=[]
    for row in records:
        residual=row['queue_start']+row['arrivals']-row['departures']-row['queue_end']
        capacity=row['green_seconds']/row['mean_headway_s']
        report.append({'key':'|'.join(row['key']),'conservation_residual':residual,
                       'served_per_green_s':row['departures']/row['green_seconds'] if row['green_seconds'] else None,
                       'ideal_service_reference':capacity,
                       'departures_above_reference':row['departures']>capacity+1e-9})
    return report

def evaluate(predictions, observations, split_day):
    selected=[r for r in observations if r['key'][1]==split_day]
    if not selected:raise ValueError('empty holdout')
    if any(r['key'] not in predictions for r in selected):raise ValueError('missing predictions')
    errors=[abs(float(predictions[r['key']])-r['departures']) for r in selected]
    return {'holdout_day':split_day,'n':len(selected),'mae_departures':sum(errors)/len(errors),
            'total_observed':sum(r['departures'] for r in selected),
            'total_predicted':sum(float(predictions[r['key']]) for r in selected)}
