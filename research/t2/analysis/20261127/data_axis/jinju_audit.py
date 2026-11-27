"""Audit publisher aggregate fields without inferring traffic states or live availability."""
import csv
import hashlib
import io
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
import sys

HEADER = ['수집시작일시', '수집종료일시', '수집위치', '차선'] + [f'{i}차선 {field}' for i in range(1, 7) for field in ('교통량', '차량종류')]

def vector(s, width):
    cells = s.split('/')
    if len(cells) != width or any(not re.fullmatch(r'[0-9]+', v) for v in cells):
        raise ValueError('invalid vector')
    return tuple(map(int, cells))

def audit(raw):
    rows = csv.reader(io.StringIO(raw.decode('cp949'), newline=''), strict=True)
    if next(rows, None) != HEADER:
        raise ValueError('unexpected header')
    counts = Counter(); durations = Counter(); lanes = Counter(); sites = defaultdict(list)
    seen = set(); key_seen = set(); sums = Counter(); diff = Counter(); dates = Counter()
    earliest = latest = None
    for row in rows:
        if len(row) != len(HEADER): raise ValueError('unexpected width')
        a, b = [datetime.strptime(s, '%Y-%m-%d %H:%M:%S') for s in row[:2]]
        if b < a or not row[2] or not re.fullmatch(r'[1-6]', row[3]): raise ValueError('invalid time/site/lane')
        n = int(row[3]); counts['rows'] += 1; lanes[n] += 1; dates[a.date().isoformat()] += 1
        earliest = a if earliest is None else min(earliest,a); latest = b if latest is None else max(latest,b)
        duration = int((b-a).total_seconds()); durations[duration] += 1
        if tuple(row) in seen: counts['duplicate_rows'] += 1
        seen.add(tuple(row))
        key = (row[2],a,b)
        if key in key_seen: counts['duplicate_site_interval'] += 1
        key_seen.add(key); sites[row[2]].append((a,b,n))
        for i in range(6):
            x,y = row[4+2*i:6+2*i]
            if i >= n:
                counts['unused_slots'] += 1
                if x or y: counts['unexpected_populated_unused'] += 1
                continue
            counts['declared_slots'] += 1
            if not x or not y:
                counts['missing_declared_pair'] += 1
                continue
            u,v = vector(x,6),vector(y,7)
            counts['complete_declared_pair'] += 1
            if not any(u): counts['explicit_zero_volume_vectors'] += 1
            m = sum(u[:4]); c = sum(v); diff[m-c] += 1
            sums.update(movement_subtotal=m, remaining=u[4], waiting=u[5], vehicle_type_subtotal=c)
            if m == c: counts['movement_type_agree'] += 1
            if sum(u) == c: counts['all_six_type_agree'] += 1
            if u[4] or u[5]: counts['nonzero_remaining_or_waiting'] += 1
    if not counts['rows']: raise ValueError('no records')
    interval = Counter(); site_lane_variations = 0
    for seq in sites.values():
        site_lane_variations += len({n for _,_,n in seq}) > 1
        frontier = None
        for a,b,_ in sorted(seq):
            if a==b: interval['zero_duration'] += 1
            if frontier is not None:
                interval['overlap' if a<frontier else 'adjacent' if a==frontier else 'gap'] += 1
            frontier = b if frontier is None else max(frontier,b)
    ds=sorted(durations.items()); total=counts['rows']
    def percentile(p):
        target=(total*p+99)//100; acc=0
        for sec,n in ds:
            acc+=n
            if acc>=target:return sec
    return {'source':'Jinju public data 15152135; camera recognition; publisher field definitions', 'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'encoding':'cp949 (compatible with EUC-KR for this file)','timezone':'unverified; naive source timestamps','availability':'unverified; historical descriptive only','sites':len(sites),'sites_with_lane_count_variation':site_lane_variations,'start':str(earliest),'end':str(latest),'rows_by_start_date':dict(sorted(dates.items())),'counts':{k:counts[k] for k in ['rows','duplicate_rows','duplicate_site_interval','declared_slots','unused_slots','unexpected_populated_unused','missing_declared_pair','complete_declared_pair','explicit_zero_volume_vectors','movement_type_agree','all_six_type_agree','nonzero_remaining_or_waiting']},'lane_counts':dict(sorted(lanes.items())),'duration_seconds':{'min':ds[0][0],'p25':percentile(25),'p50':percentile(50),'p75':percentile(75),'p95':percentile(95),'max':ds[-1][0]},'same_site_interval_relations':dict(interval),'movement_minus_type_histogram':dict(sorted(diff.items())),'arithmetic_sums_not_unique_vehicle_counts':dict(sums),'interpretation':'Same-source arithmetic checks only; remaining/waiting timing and units unconfirmed; do not integrate or equate to R3 state. No raw locations exported.'}

if __name__=='__main__':
    print(json.dumps(audit(Path(sys.argv[1]).read_bytes()),ensure_ascii=False,indent=2))
