"""Reproduction gates and exact definitions for separate observed/model data."""
from math import sqrt
from statistics import mean
from hashlib import sha256
from pathlib import Path
import csv


def manifest(path: str):
    data=Path(path).read_bytes()
    return {'sha256':sha256(data).hexdigest(),'bytes':len(data),'source':str(path)}


def validate_trajectories(rows):
    """Each row is [id, t_s, x_m, v_mps, link]; no merging across IDs."""
    last={}
    for row in rows:
        vid=row['id'];t=float(row['t_s']);x=float(row['x_m']);v=float(row['v_mps'])
        if v<0:raise ValueError('negative longitudinal speed requires sign convention review')
        if vid in last and t<=last[vid]:raise ValueError('nonincreasing trajectory timestamp')
        last[vid]=t
    return len(last)


def score_pair(pred,obs,units):
    if len(pred)!=len(obs) or not pred:raise ValueError('matched independent observations required')
    if units not in ('m','s','m/s','vehicles','vehicle_seconds'):
        raise ValueError('unknown comparison unit')
    err=[float(x)-float(y) for x,y in zip(pred,obs)]
    return {'units':units,'n':len(err),'bias':mean(err),'mae':mean(map(abs,err)),
            'rmse':sqrt(mean(e*e for e in err))}


def split_dates(records,holdout_dates):
    train=[r for r in records if r['date'] not in holdout_dates]
    test=[r for r in records if r['date'] in holdout_dates]
    if not train or not test:raise ValueError('nonempty date-disjoint holdout required')
    assert not ({r['date'] for r in train}&{r['date'] for r in test})
    return train,test


def emission_conservation(total,queued,active,finished):
    assert total==queued+active+finished, 'vehicle conservation violation'
