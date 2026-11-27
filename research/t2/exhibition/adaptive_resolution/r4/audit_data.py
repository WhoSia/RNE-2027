"""Audit the six previously selected public aggregate windows; never fill unknowns."""
import json, sys
from pathlib import Path
from datetime import datetime, timezone
from data_contract import read_counts
WINDOWS=[('230924-230000_230924-231500',900,16),('230924-231500_230924-233000',857,2),('230924-233000_230924-234500',893,17),('230924-234500_230925-000000',868,17),('230924-121500_230924-123000',900,475),('230924-123000_230924-124500',900,498)]
def audit(root):
    out=[]; checks=0
    for stem,n,count in WINDOWS:
        path=root/f'traffic-volume_{stem}.csv'
        if not path.is_file():out.append({'file':path.name,'status':'unavailable'});continue
        start=datetime.strptime(stem.split('_')[0],'%y%m%d-%H%M%S').replace(tzinfo=timezone.utc)
        raw=path.read_bytes();w=read_counts(raw,start,'DLR UT v1.3.1 publisher aggregate counts')
        assert len(w.rows)==n;checks+=1
        assert w.bins(900)[0]['observed_count']==count;checks+=1
        bins={}
        for width in (1,5,15,60,900):
            v=w.bins(width);assert sum(r['observed_count'] or 0 for r in v)==count;checks+=1
            assert sum(r['coverage_seconds'] for r in v)==n;checks+=1
            bins[str(width)]={s:sum(r['status']==s for r in v) for s in ('complete','partial','unobserved')}
        try:w.decision_count(start)
        except ValueError:checks+=1
        else:raise AssertionError('unknown available_at must block decision input')
        out.append({'file':path.name,'status':'verified','sha256':w.digest,'bytes':len(raw),'seconds':n,'observed_count':count,'columns':len(w.headers),'bins':bins,'decision_availability':None})
    return {'source':'https://doi.org/10.5281/zenodo.20919480','license':'CC BY-NC-SA 4.0','checks':checks,'windows':out,'scope':'historical aggregate counts only; availability and independent labels not established'}
if __name__=='__main__': print(json.dumps(audit(Path(sys.argv[1])),indent=2))
