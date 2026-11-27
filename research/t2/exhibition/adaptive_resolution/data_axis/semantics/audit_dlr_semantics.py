import json, sys
from pathlib import Path
from datetime import datetime, timezone
from dlr_recorded_counts import verified_collection
from data_contract import read_counts

root=Path(__file__).resolve().parents[2]
manifest=json.loads((root/'r4/data_audit_results.json').read_text())
base=Path(sys.argv[1]); windows=[]
for rec in manifest['windows']:
    start=datetime.strptime(rec['file'].split('_')[1],'%y%m%d-%H%M%S').replace(tzinfo=timezone.utc)
    w=read_counts((base/rec['file']).read_bytes(),start,manifest['source'])
    assert w.digest==rec['sha256']
    windows.append(w)
collection=verified_collection(windows,[r['sha256'] for r in manifest['windows']]); checks=0; results=[]
for adapter in collection:
    w=adapter.window; known=adapter.known_routes
    explicit=len(w.headers)*len(w.rows); implicit=(len(known)-len(w.headers))*len(w.rows); missing=(900-len(w.rows))*len(known)
    for j in range(len(w.headers)):
        assert sum(v[j] for _,v in w.rows)>0; checks+=1
    for width in (1,5,15,60,900):
        actual=w.bins(width)
        route_bins=[adapter.bins(width,r) for r in sorted(known)]
        for i,ref in enumerate(actual):
            group=[bins[i] for bins in route_bins]
            assert sum(x['observed_count'] or 0 for x in group)==(ref['observed_count'] or 0); checks+=1
            assert all(x['coverage_seconds']==ref['coverage_seconds'] and x['status']==ref['status'] for x in group); checks+=len(group)
            assert all(x['explicit_seconds']+x['implicit_zero_seconds']==x['coverage_seconds'] for x in group); checks+=len(group)
            assert all((x['observed_count'] is None)==(not ref['coverage_seconds']) for x in group); checks+=len(group)
        assert sum(sum(x['explicit_seconds'] for x in bins) for bins in route_bins)==explicit; checks+=1
        assert sum(sum(x['implicit_zero_seconds'] for x in bins) for bins in route_bins)==implicit; checks+=1
    try: w.decision_count(w.start)
    except ValueError: checks+=1
    else: raise AssertionError('causal gate opened')
    results.append(dict(start=w.start.isoformat(),sha256=w.digest,known_routes=len(known),supplied_routes=len(w.headers),explicit_cells=explicit,implicit_recorded_zero_cells=implicit,unknown_time_cells=missing,recorded_count=sum(sum(v) for _,v in w.rows)))
print(json.dumps(dict(source=manifest['source'],document_page=20,document_sha256='94fd9ebd32d04a9c35b02be526fbd11a8d5a613933d7961fde800386853b34f3',checks=checks,windows=results,totals={k:sum(r[k] for r in results) for k in ('explicit_cells','implicit_recorded_zero_cells','unknown_time_cells','recorded_count')}),indent=2))
