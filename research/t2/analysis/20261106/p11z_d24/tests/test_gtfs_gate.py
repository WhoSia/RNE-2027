import csv
import datetime as dt
import io
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from gtfs_gate import clock_seconds,audit_zip

DATA={
'agency.txt':'agency_id,agency_name,agency_url,agency_timezone\n1,Fixture,https://example.org,Asia/Seoul\n',
'routes.txt':'route_id,route_short_name,route_type\nR,1,3\n',
'stops.txt':'stop_id,stop_name,stop_lat,stop_lon\nA,Alpha,37,127\nB,Beta,37.01,127.01\n',
'trips.txt':'route_id,service_id,trip_id\nR,WEEK,T1\nR,HOL,T2\n',
'stop_times.txt':'trip_id,arrival_time,departure_time,stop_id,stop_sequence\nT1,23:55:00,23:55:00,A,1\nT1,24:10:00,24:10:00,B,2\nT2,25:00:00,25:00:00,A,1\nT2,25:15:00,25:15:00,B,2\n',
'calendar.txt':'service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date\nWEEK,1,1,1,1,1,0,0,20261101,20261130\nHOL,0,0,0,0,0,0,0,20261101,20261130\n',
'calendar_dates.txt':'service_id,date,exception_type\nWEEK,20261106,2\nHOL,20261106,1\n',
'transfers.txt':'from_stop_id,to_stop_id,transfer_type,min_transfer_time\nA,B,2,180\n',
}


def fixture(path, data=None):
    with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for k,v in sorted((data or DATA).items()):
            meta=zipfile.ZipInfo(k,date_time=(2026,1,1,0,0,0))
            meta.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(meta,v)


class GTFSIntakeTests(unittest.TestCase):
    def test_overnight_and_bad_clock(self):
        self.assertEqual(clock_seconds('25:15:00'),90900)
        for bad in ('24:61:00','4:30','-1:03:00'):
            with self.assertRaises(ValueError):clock_seconds(bad)
    def test_calendar_exception_overrides_weekday(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'feed.zip';fixture(p)
            z=audit_zip(p,dt.date(2026,11,6))
            self.assertEqual(z['active_service_ids'],['HOL'])
            self.assertEqual(z['connections'][0]['trip_id'],'T2')
            self.assertEqual(z['connections'][0]['arrive_s'],90900)
            self.assertEqual(z['transfers'][('A','B')],180)
            self.assertEqual(len(z['sha256']),64)
    def test_weekday_without_exception(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'feed.zip';fixture(p)
            z=audit_zip(p,dt.date(2026,11,9))
            self.assertEqual(z['connections'][0]['trip_id'],'T1')
    def test_reject_frequency_as_exact_timetable(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'feed.zip'; fixture(p,{**DATA,'frequencies.txt':'trip_id,start_time,end_time,headway_secs,exact_times\nT1,05:00:00,06:00:00,300,0\n'})
            with self.assertRaisesRegex(ValueError,'frequencies'):audit_zip(p,dt.date(2026,11,6))
    def test_missing_calendar(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'feed.zip';fixture(p,{k:v for k,v in DATA.items() if k not in ('calendar.txt','calendar_dates.txt')})
            with self.assertRaisesRegex(ValueError,'calendar'):audit_zip(p,dt.date(2026,11,6))
    def test_unknown_stop(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'feed.zip';fixture(p,{**DATA,'stop_times.txt':DATA['stop_times.txt'].replace('T2,25:15:00,25:15:00,B,2','T2,25:15:00,25:15:00,NO_STOP,2')})
            with self.assertRaisesRegex(ValueError,'unknown stop'):audit_zip(p,dt.date(2026,11,6))

if __name__=='__main__':unittest.main()
