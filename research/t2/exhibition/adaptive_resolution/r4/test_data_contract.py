import unittest
from datetime import datetime,timedelta,timezone
from data_contract import read_counts
S=datetime(2023,9,24,tzinfo=timezone.utc)
HEAD='timestamp,East2West0\n'
def data(*rows):return (HEAD+''.join(f'2023-09-24 00:00:{s:02d}+00:00,{v}\n' for s,v in rows)).encode()
class TestContract(unittest.TestCase):
    def test_distinguish(self):
        w=read_counts(data((0,0),(2,2)),S,'synthetic',3)
        self.assertEqual([(r['status'],r['observed_count']) for r in w.bins(1)],[('complete',0),('unobserved',None),('complete',2)])
        self.assertEqual(w.bins(3)[0]['observed_count'],2)
        self.assertEqual(w.bins(3,'North1South0')[0]['status'],'schema_absent')
    def test_availability(self):
        b=data((0,0),(1,2));end=S+timedelta(seconds=2);w=read_counts(b,S,'synthetic',2)
        with self.assertRaises(ValueError):w.decision_count(end)
        w=read_counts(b,S,'synthetic',2,available_at=end+timedelta(seconds=1))
        with self.assertRaises(ValueError):w.decision_count(end)
        self.assertEqual(w.decision_count(end+timedelta(seconds=1)),2)
        with self.assertRaises(ValueError):w.decision_count(end+timedelta(seconds=1),'North1South0')
        with self.assertRaises(ValueError):read_counts(b,S,'synthetic',2,available_at=S)
    def test_incomplete_decision(self):
        end=S+timedelta(seconds=2);w=read_counts(data((0,0)),S,'synthetic',2,available_at=end)
        with self.assertRaises(ValueError):w.decision_count(end)
    def test_invalid(self):
        for b in [data((0,1),(0,2)),data((1,1),(0,2)),data((2,1)),data((0,-1)),data((0,'1.0')),b'timestamp,East2West0,East2West0\n',b'timestamp,bad\n',b'\xff',b'timestamp,East2West0\n2023-09-24 00:00:00,1\n']:
            with self.subTest(b=b),self.assertRaises(ValueError):read_counts(b,S,'synthetic',2)
    def test_empty_window(self):
        w=read_counts(HEAD.encode(),S,'synthetic',2)
        self.assertEqual(w.bins(2)[0]['status'],'unobserved')
        self.assertIsNone(w.bins(2)[0]['observed_count'])
if __name__=='__main__':unittest.main()
