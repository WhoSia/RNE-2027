"""D47 exploratory within-ID speed residual by interpolation status.

Not independent ground truth: displacement/time is interval average speed, whereas
the publisher velocity is a point estimate. Do not infer causal interpolation error.
"""
import argparse,json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import binomtest

def audit(csv):
    frame=pd.read_csv(csv)
    frame['timestamp']=pd.to_datetime(frame.timestamp,utc=True,format='mixed',errors='raise')
    frame=frame.sort_values(['id','timestamp'])
    g=frame.groupby('id')
    dt=g.timestamp.diff().dt.total_seconds()
    speed=np.hypot(g.center_easting.diff(),g.center_northing.diff())/dt
    frame['abs_residual_mps']=(speed-frame.velocity_magnitude).abs()
    frame=frame.loc[dt.notna()&(dt>0)]
    strata={}
    for name,rows in [('all',frame),('interpolated_current',frame[frame.interpolated]),('not_interpolated_current',frame[~frame.interpolated])]:
        err=rows.abs_residual_mps
        strata[name]={'n':len(err),'median_mps':float(err.median()),'p95_mps':float(err.quantile(.95)),
                     'p99_mps':float(err.quantile(.99)),'gt_1_mps':int((err>1).sum())}
    paired=frame.groupby(['id','interpolated']).abs_residual_mps.mean().unstack().dropna()
    diff=paired[True]-paired[False]
    nonzero=int((diff!=0).sum())
    return {'strata':strata,'paired_ids':int(len(diff)),
            'positive_ids':int((diff>0).sum()),'negative_ids':int((diff<0).sum()),
            'median_within_id_mean_difference_mps':float(diff.median()),
            'exploratory_sign_test_p':float(binomtest(int((diff>0).sum()),nonzero,.5).pvalue) if nonzero else None,
            'limitations':'NOT independent truth, not a causal effect; positions are rounded and velocity types differ'}
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('csv',type=Path)
    p.add_argument('--out',type=Path,required=True)
    x=p.parse_args()
    result=audit(x.csv)
    x.out.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(result,indent=2,ensure_ascii=False))
