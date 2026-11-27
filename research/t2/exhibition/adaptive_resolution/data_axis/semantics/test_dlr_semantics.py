import unittest
from datetime import datetime, timezone
from data_contract import read_counts
from dlr_recorded_counts import verified_collection

class ContractTest(unittest.TestCase):
    def setUp(self):
        self.start=datetime(2023,9,24,tzinfo=timezone.utc)
        self.a=read_counts(b'timestamp,East1West0\n2023-09-24 00:00:00+00:00,2\n',self.start,'synthetic')
        self.b=read_counts(b'timestamp,North1South0\n2023-09-24 00:15:00+00:00,1\n',self.start.replace(minute=15),'synthetic')
    def test_missing_route_and_time(self):
        a,_=verified_collection([self.a,self.b],[self.a.digest,self.b.digest])
        rows=a.bins(1,'North1South0')
        self.assertEqual((rows[0]['observed_count'],rows[0]['implicit_zero_seconds']), (0,1))
        self.assertEqual((rows[1]['observed_count'],rows[1]['implicit_zero_seconds']), (None,0))
        self.assertEqual(a.bins(900,'North1South0')[0]['status'],'partial')
        self.assertEqual(a.bins(1,'East1West0')[0]['explicit_seconds'],1)
    def test_unknown_route(self):
        a,_=verified_collection([self.a,self.b],[self.a.digest,self.b.digest])
        self.assertEqual(a.bins(900,'West9East9')[0]['status'],'schema_absent')
    def test_source_gate(self):
        with self.assertRaises(ValueError):verified_collection([self.a],['wrong'])
        with self.assertRaises(ValueError):verified_collection([self.a,self.a],[self.a.digest,self.b.digest])
    def test_no_causal_upgrade(self):
        a,_=verified_collection([self.a,self.b],[self.a.digest,self.b.digest])
        with self.assertRaises(ValueError):a.window.decision_count(self.start)
        self.assertEqual(self.a.bins(900,'North1South0')[0]['status'],'schema_absent')

if __name__=='__main__':unittest.main()
