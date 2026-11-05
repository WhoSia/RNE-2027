import datetime as dt
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
sys.path.insert(0,str(Path(__file__).parent))
from gtfs_gate import audit_zip
from test_gtfs_gate import DATA, fixture

class TestFailClosedGTFS(unittest.TestCase):
    def test_active_trip_with_missing_times_is_not_silently_ignored(self):
        new=dict(DATA)
        new['stop_times.txt']='\n'.join(x for x in DATA['stop_times.txt'].splitlines() if not x.startswith('T2,'))+'\n'
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'missing.zip';fixture(p,new)
            with self.assertRaisesRegex(ValueError,'missing stop_times'):
                audit_zip(p,dt.date(2026,11,6))
    def test_active_trip_with_one_stop_is_not_silently_ignored(self):
        new=dict(DATA)
        new['stop_times.txt']='\n'.join(x for x in DATA['stop_times.txt'].splitlines() if not x.startswith('T2,25:15:'))+'\n'
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'one_stop.zip';fixture(p,new)
            with self.assertRaisesRegex(ValueError,'at least two'):
                audit_zip(p,dt.date(2026,11,6))
    def test_duplicate_member_names_are_not_silently_shadowed(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'duplicate.zip';fixture(p)
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter('ignore',UserWarning)
                with zipfile.ZipFile(p,'a') as z:
                    z.writestr('stops.txt',DATA['stops.txt'])
            with self.assertRaisesRegex(ValueError,'duplicate filename'):
                audit_zip(p,dt.date(2026,11,6))
    def test_inactive_trip_without_times_not_conflated_with_active(self):
        new=dict(DATA)
        new['stop_times.txt']='\n'.join(x for x in DATA['stop_times.txt'].splitlines() if not x.startswith('T1,'))+'\n'
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'inactive.zip';fixture(p,new)
            z=audit_zip(p,dt.date(2026,11,6))
            self.assertEqual(z['connections'][0]['trip_id'],'T2')

if __name__=='__main__': unittest.main()
