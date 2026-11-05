import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from spat_observations import validate
class SpatTests(unittest.TestCase):
    def test_real_public_record_schema(self):
        v=validate([{'intersection_id':'5502','tmstp_utc':'2025-03-10T13:50:52.896','signalgroup2':'R','signalgroup4':'G','failure_flash':'0'}],True)
        self.assertEqual(v['groups_seen'],['signalgroup2','signalgroup4'])
    def test_actual_timestamp_ordered_sample(self):
        a=[{'intersection_id':'5502','tmstp_utc':'2025-03-01T00:00:00.052','signalgroup2':'G','signalgroup4':'R'},
           {'intersection_id':'5502','tmstp_utc':'2025-03-01T00:00:00.451','signalgroup2':'G','signalgroup4':'R'}]
        self.assertEqual(validate(a,True)['observed_transition_count'],0)
    def test_missing_group_not_converted_to_red(self):
        r=validate([{'intersection_id':'1','tmstp_utc':'2025-03-01T00:00:00','signalgroup2':'G'}],True)
        self.assertEqual(r['groups_seen'],['signalgroup2'])
    def test_mixed_intersections_blocked(self):
        a=[{'intersection_id':str(i),'tmstp_utc':'2025-03-01','signalgroup2':'G'} for i in (1,2)]
        with self.assertRaises(ValueError):validate(a,True)
    def test_time_order_assertion(self):
        a=[{'intersection_id':'1','tmstp_utc':f'2025-03-01T00:00:0{i}','signalgroup2':'G'} for i in (1,0)]
        with self.assertRaises(ValueError):validate(a,True)
    def test_missing_timestamp_or_groups(self):
        with self.assertRaises(ValueError):validate([{'intersection_id':'1','signalgroup2':'G'}])
        with self.assertRaises(ValueError):validate([{'intersection_id':'1','tmstp_utc':'2025-03-01'}])
    def test_unsupported_state_rejected(self):
        with self.assertRaises(ValueError):validate([{'intersection_id':'1','tmstp_utc':'2025-03-01','signalgroup2':'UNKNOWN!'}])
if __name__=='__main__':unittest.main()
