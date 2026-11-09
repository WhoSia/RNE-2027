"""D46 strict original-data audit: one DLR UT 15-minute window (pandas/numpy).

No claimed head-to-movement correspondence or signal state meaning.
Run:
python raw_window_audit.py --input-dir PATH --output audit.json
"""
import argparse
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd

NAMES={
 'trajectory':'trajectories_230924-120000_230924-121500.csv',
 'signal':'traffic-lights_230924-120000_230924-121500.csv',
 'volume':'traffic-volume_230924-120000_230924-121500.csv'
}
def audit(input_dir):
    dfs={k:pd.read_csv(input_dir/v) for k,v in NAMES.items()}
    for frame in dfs.values():
        frame['timestamp']=pd.to_datetime(frame['timestamp'],utc=True,format='mixed',errors='raise')
    a,s,v=(dfs[k] for k in ('trajectory','signal','volume'))
    g=a.sort_values(['id','timestamp'],kind='stable').groupby('id')
    dt=g.timestamp.diff().dt.total_seconds()
    jumps=np.hypot(g.center_easting.diff(),g.center_northing.diff())
    times=s.timestamp.drop_duplicates().sort_values().reset_index(drop=True)
    time_gaps=times.diff().dt.total_seconds()
    cls=[c for c in a if c.startswith('classifications_')]
    movements=[c for c in v if c!='timestamp']
    counts=v[movements].sum().sort_values(ascending=False)
    return {
      'sha256':{k:hashlib.sha256((input_dir/n).read_bytes()).hexdigest() for k,n in NAMES.items()},
      'trajectory':{
        'rows':int(len(a)),'ids':int(a.id.nunique()),'unique_timestamps':int(a.timestamp.nunique()),
        'duplicate_id_time':int(a.duplicated(['id','timestamp']).sum()),'null_cells':int(a.isna().sum().sum()),
        'interpolated_rows':int(a.interpolated.sum()),'interpolated_share':float(a.interpolated.mean()),
        'median_id_timestep_s':float(dt.median()),'gaps_gt_0_1s':int((dt>.1).sum()),
        'jumps_gt_5m':int((jumps>5).sum()),'max_reported_speed_mps':float(a.velocity_magnitude.max()),
        'min_class_probability_sum':float(a[cls].sum(axis=1).min())},
      'signal':{
        'rows':int(len(s)),'heads':int(s.id.nunique()),'times':int(len(times)),
        'gaps_gt_1_5s':[{'start':str(times.iloc[i-1]),'end':str(times.iloc[i]),'s':float(time_gaps.iloc[i])}
          for i in np.where(time_gaps.to_numpy()>1.5)[0]],
        'raw_state_codes':{str(k):int(n) for k,n in s.state.value_counts().items()}},
      'volume':{
        'rows':int(len(v)),'movements':len(movements),'event_cell_sum':int(counts.sum()),
        'top_movements':{k:int(n) for k,n in counts.head(10).items()}}
    }
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input-dir',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    x=p.parse_args()
    result=audit(x.input_dir)
    x.output.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
