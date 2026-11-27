"""Historical aggregate count adapter; unknown availability never becomes causal input."""
import csv, hashlib, io, re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

UTC=timezone.utc
STAMP=re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\+00:00\Z')
MOVEMENT=re.compile(r'(?:East|West|North|South)\d+(?:East|West|North|South)\d+\Z')

def utc(t):
    if not isinstance(t,datetime) or t.tzinfo is None or t.utcoffset()!=timedelta(0):raise ValueError('explicit UTC required')
    return t.astimezone(UTC)

@dataclass(frozen=True)
class Window:
    source: str
    digest: str
    start: datetime
    seconds: int
    headers: tuple[str,...]
    rows: tuple[tuple[int,tuple[int,...]],...]
    # Publication/collection timestamp does not imply decision-time availability.
    available_at: datetime|None=None

    def bins(self,width,movement=None):
        if type(width) is not int or width<=0 or self.seconds%width:raise ValueError('invalid bin width')
        if movement is not None and movement not in self.headers:
            return [{'start':(self.start+timedelta(seconds=i)).isoformat(),'coverage_seconds':None,'observed_count':None,'status':'schema_absent'} for i in range(0,self.seconds,width)]
        index=self.headers.index(movement) if movement is not None else None
        coverage=[0]*(self.seconds//width);count=[0]*len(coverage)
        for t,v in self.rows:
            k=t//width;coverage[k]+=1;count[k]+=sum(v) if index is None else v[index]
        return [{'start':(self.start+timedelta(seconds=k*width)).isoformat(),'coverage_seconds':n,'observed_count':count[k] if n else None,'status':'complete' if n==width else 'partial' if n else 'unobserved'} for k,n in enumerate(coverage)]

    def decision_count(self,decision_at,movement=None):
        """Only an explicitly available, fully covered whole-window total. Not a queue/arrival estimate."""
        t=utc(decision_at)
        if self.available_at is None:raise ValueError('availability not independently established')
        if t<self.available_at or t<self.start+timedelta(seconds=self.seconds):raise ValueError('future window or unavailable data')
        row=self.bins(self.seconds,movement)[0]
        if row['status']!='complete':raise ValueError('incomplete or absent observation')
        return row['observed_count']

def read_counts(data,start,source,seconds=900,available_at=None):
    start=utc(start)
    if start.microsecond or type(seconds) is not int or seconds<=0 or not isinstance(source,str) or not source.strip():raise ValueError('invalid window/source')
    if available_at is not None:
        available_at=utc(available_at)
        if available_at<start+timedelta(seconds=seconds):raise ValueError('whole-window availability precedes end')
    try:records=csv.reader(io.StringIO(data.decode('utf-8-sig'),newline=''),strict=True);head=next(records)
    except (StopIteration,UnicodeError,csv.Error) as e:raise ValueError('invalid CSV') from e
    if len(head)<2 or head[0]!='timestamp' or len(set(head))!=len(head) or any(not MOVEMENT.fullmatch(h) for h in head[1:]):raise ValueError('invalid movement schema')
    rows=[];prev=-1
    try:
        for r in records:
            if len(r)!=len(head) or not STAMP.fullmatch(r[0]) or any(not re.fullmatch(r'[0-9]+',v) for v in r[1:]):raise ValueError('invalid timestamp or integer count')
            t=datetime.fromisoformat(r[0]);offset=int((t-start).total_seconds())
            if not prev<offset<seconds:raise ValueError('duplicate, unordered or out-of-window timestamp')
            rows.append((offset,tuple(map(int,r[1:]))));prev=offset
    except csv.Error as e:raise ValueError('invalid CSV') from e
    return Window(source,hashlib.sha256(data).hexdigest(),start,seconds,tuple(head[1:]),tuple(rows),available_at)
