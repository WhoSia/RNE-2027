"""Offline GTFS Schedule audit / explicit service-date gate.

A planned timetable is not actual vehicle movement. The loader deliberately
rejects frequency-compressed feeds and unsupported timed-stop interpolation.
"""
import csv
import datetime as dt
import hashlib
import io
import zipfile
from collections import defaultdict
from pathlib import Path


WEEKDAYS = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')


def clock_seconds(value: str) -> int:
    parts = value.split(':')
    if len(parts) != 3 or any(not p.isdigit() for p in parts):
        raise ValueError('GTFS HH:MM:SS required')
    h, m, s = map(int, parts)
    if h < 0 or not 0 <= m < 60 or not 0 <= s < 60:
        raise ValueError('invalid GTFS time')
    return h * 3600 + m * 60 + s


def _table(zf, name, required=True):
    if name not in zf.namelist():
        if required:
            raise ValueError(f'missing {name}')
        return []
    with zf.open(name) as fp:
        text = io.TextIOWrapper(fp, encoding='utf-8-sig', newline='')
        return list(csv.DictReader(text))


def audit_zip(path, service_date: dt.date):
    if not isinstance(service_date, dt.date):
        raise ValueError('date is required')
    raw = Path(path).read_bytes()
    if not zipfile.is_zipfile(io.BytesIO(raw)):
        raise ValueError('not a ZIP')
    with zipfile.ZipFile(io.BytesIO(raw)) as zf:
        names = [x.filename for x in zf.infolist()]
        if len(names) != len(set(names)):
            raise ValueError('duplicate filename in GTFS archive')
        if any(x.filename.startswith('/') or '..' in Path(x.filename).parts for x in zf.infolist()):
            raise ValueError('unsafe file paths in ZIP')
        agency, routes, stops, trips, stop_times = (_table(zf, x) for x in ('agency.txt','routes.txt','stops.txt','trips.txt','stop_times.txt'))
        cal, exceptions = _table(zf,'calendar.txt',False), _table(zf,'calendar_dates.txt',False)
        transfers, frequencies, info = (_table(zf,x,False) for x in ('transfers.txt','frequencies.txt','feed_info.txt'))
        if not cal and not exceptions:
            raise ValueError('no service calendar')
        if frequencies:
            raise ValueError('frequencies.txt requires explicit expansion; no silent frequency-as-schedule assumption')
        if not agency or not routes or not stops or not trips or not stop_times:
            raise ValueError('missing base records')
        timezone={x.get('agency_timezone','') for x in agency}
        if len(timezone)!=1 or not next(iter(timezone)):
            raise ValueError('agency timezone needs unambiguous value')
        ymd=service_date.strftime('%Y%m%d')
        active=set()
        for c in cal:
            if c['start_date']<=ymd<=c['end_date'] and c[WEEKDAYS[service_date.weekday()]]=='1':
                active.add(c['service_id'])
        for exc in exceptions:
            if exc['date']!=ymd:continue
            if exc['exception_type']=='1':active.add(exc['service_id'])
            elif exc['exception_type']=='2':active.discard(exc['service_id'])
            else:raise ValueError('unsupported exception')
        known_stops={s['stop_id'] for s in stops}
        known_routes={r['route_id'] for r in routes}
        active_trip={t['trip_id']:t for t in trips if t['service_id'] in active}
        if len(active_trip)!=len([t for t in trips if t['service_id'] in active]):
            raise ValueError('duplicate active trip IDs')
        if any(t['route_id'] not in known_routes for t in active_trip.values()):
            raise ValueError('unknown route')
        by_trip=defaultdict(list)
        for row in stop_times:
            if row['trip_id'] not in active_trip:continue
            if row['stop_id'] not in known_stops:raise ValueError('unknown stop')
            if not row.get('arrival_time') or not row.get('departure_time'):
                raise ValueError('blank active stop time: interpolation not implemented')
            ar=clock_seconds(row['arrival_time'])
            dep=clock_seconds(row['departure_time'])
            if ar>dep:raise ValueError('departure before arrival')
            by_trip[row['trip_id']].append((int(row['stop_sequence']),row['stop_id'],ar,dep))
        if any(tid not in by_trip for tid in active_trip):
            raise ValueError('active trip missing stop_times')
        connections=[]
        for tid, rows in by_trip.items():
            if len(rows) < 2:
                raise ValueError('active trip requires at least two timed stops')
            ordered=sorted(rows)
            if len({r[0] for r in ordered})!=len(ordered):raise ValueError('duplicate stop_sequence')
            for a,b in zip(ordered,ordered[1:]):
                if b[2]<a[3]:raise ValueError('backwards trip timetable')
                if a[1]!=b[1]:
                    connections.append({'trip_id':tid,'from':a[1],'to':b[1],'depart_s':a[3],'arrive_s':b[2]})
        transfer_floor={}
        for row in transfers:
            if row.get('transfer_type')=='3':
                transfer_floor[(row['from_stop_id'],row['to_stop_id'])]=None
            elif row.get('transfer_type')=='2':
                transfer_floor[(row['from_stop_id'],row['to_stop_id'])]=int(row['min_transfer_time'])
        return {
            'sha256':hashlib.sha256(raw).hexdigest(), 'source_bytes':len(raw),
            'service_date':ymd,'timezone':next(iter(timezone)),
            'active_service_ids':sorted(active), 'active_trips':len(active_trip),
            'connections':connections, 'transfers':transfer_floor,
            'feed_info':info,
            'limitations':['not real-time vehicle tracking','no frequencies expansion','no interpolation','not a full GTFS validator','no platform pathways or walking graph']
        }
