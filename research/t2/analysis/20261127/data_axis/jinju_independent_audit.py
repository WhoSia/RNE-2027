"""Independent pandas aggregate comparison; same source, not independent sensor."""
import pandas as pd
from pathlib import Path
import json, hashlib, sys
from collections import Counter
p=Path(sys.argv[1]); x=pd.read_csv(p,encoding='euc-kr',dtype=str,keep_default_na=False); r=json.loads(Path('jinju_audit_results.json').read_text()); c=r['counts']; checks={}
checks['raw_digest']=hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']; checks['rows']=len(x)==c['rows'];checks['site_count']=x.iloc[:,2].nunique()==r['sites']; checks['duplicate_rows']=int(x.duplicated().sum())==c['duplicate_rows'];checks['duplicate_key']=int(x.iloc[:,[2,0,1]].duplicated().sum())==c['duplicate_site_interval']; n=x.iloc[:,3].astype(int); checks['declared_slots']=int(n.sum())==c['declared_slots']; checks['unused_slots']=int(6*len(n)-n.sum())==c['unused_slots']
hist=Counter(); sums=Counter(); used=unused=0
for k in range(6):
    unused+=int((x.loc[n<=k].iloc[:,4+2*k:6+2*k]=='').all(axis=1).sum())
    f=x.loc[n>k].iloc[:,4+2*k:6+2*k]
    if f.empty: continue
    u=f.iloc[:,0].str.split('/',expand=True).astype(int);v=f.iloc[:,1].str.split('/',expand=True).astype(int);m=u.iloc[:,:4].sum(axis=1);t=v.sum(axis=1);hist.update((m-t).tolist());sums.update(movement_subtotal=int(m.sum()),remaining=int(u.iloc[:,4].sum()),waiting=int(u.iloc[:,5].sum()),vehicle_type_subtotal=int(t.sum()));used+=len(f)
checks['vectors']=used==c['complete_declared_pair'];checks['unused_empty']=unused==c['unused_slots'];checks['diff_hist']=dict(hist)=={int(k):v for k,v in r['movement_minus_type_histogram'].items()};checks['all_sums']=dict(sums)==r['arithmetic_sums_not_unique_vehicle_counts'];d=(pd.to_datetime(x.iloc[:,1])-pd.to_datetime(x.iloc[:,0])).dt.total_seconds();checks['duration_bounds']=[int(d.min()),int(d.max())]==[r['duration_seconds']['min'],r['duration_seconds']['max']];checks['zero_duration']=int((d==0).sum())==r['same_site_interval_relations']['zero_duration'];checks['date_count']={str(k):int(v) for k,v in x.iloc[:,0].str[:10].value_counts().items()}==r['rows_by_start_date'];checks['lane_count_variation']=int((x.groupby(x.columns[2])[x.columns[3]].nunique()>1).sum())==r['sites_with_lane_count_variation']; assert all(checks.values()),checks
print(json.dumps({'method':'independent pandas vectorized aggregate, same publisher and raw file, no independent sensor','pandas':pd.__version__,'checks':{k:bool(v) for k,v in checks.items()},'passed':int(sum(checks.values())),'total':len(checks)},indent=2))
