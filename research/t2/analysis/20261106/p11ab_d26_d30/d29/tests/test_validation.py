import tempfile,unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from validation import *
from od_and_policy import *
class ValidationTests(unittest.TestCase):
    def test_sumo_no_fake_reference(self):
        with self.assertRaises(FileNotFoundError):sumo_tripinfo('/not/an/existing/sumo.xml')
    def test_sumo_synthetic_xml_parser_and_metrics(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'tripinfo.xml'
            p.write_text('<tripinfos><tripinfo id="1" depart="1" arrival="5" departDelay="0" duration="4" /></tripinfos>')
            a=sumo_tripinfo(p)
            self.assertEqual(compare_trips({'1':1},{'1':5},a)['mae_duration_s'],0)
    def test_sumo_invalid_duration_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'tripinfo.xml';p.write_text('<tripinfos><tripinfo id="v" depart="0" arrival="5" departDelay="0" duration="2" /></tripinfos>')
            with self.assertRaises(ValueError):sumo_tripinfo(p)
    def test_sumo_mismatched_cohorts_error(self):
        with self.assertRaises(ValueError):compare_trips({'a':0},{'a':1},{'b':Trip('b',0,1,0,1)})
    def test_field_counts_not_queue(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'count.csv';p.write_text('time_s,vehicle_count\n1,3\n2,4\n')
            with self.assertRaises(ValueError):field_queue_csv(p)
    def test_field_queue_monotone(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'queue.csv';p.write_text('time_s,queue_vehicles\n1,3\n2,4\n')
            self.assertEqual(field_queue_csv(p),[(1,3),(2,4)])
    def test_od_reproducible(self):
        a=make_od_demand({'a':('A','B'),'b':('A','C')},6,71,bus_every=2)
        b=make_od_demand({'b':('A','C'),'a':('A','B')},6,71,bus_every=2)
        self.assertEqual(a,b)
    def test_policy_result_separated_by_holdout(self):
        x=court()
        self.assertEqual(len(x['train']),3)
        self.assertEqual(len(x['holdout']),3)
        self.assertEqual(x['policy_status'],'SYNTHETIC_OFFLINE_ONLY')
        self.assertTrue(all(r['collision_violations']==0 for rec in x['raw'].values() for r in rec))
if __name__=='__main__':unittest.main()
