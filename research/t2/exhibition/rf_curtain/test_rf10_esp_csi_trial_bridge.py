"""Synthetic parser and missing-data tests; NO measured CSI or real traffic."""
import csv
import tempfile
import unittest
from pathlib import Path
from rf10_esp_csi_trial_bridge import (parse_iq,load_owned_csv,
     aggregate_trials,export_trials)


class RF10Tests(unittest.TestCase):
    def test_signed_interleaved_iq(self):
        a=parse_iq('[3,4,0,5,-3,-4,0,0]', '8', '0')
        self.assertEqual(a,(5.0,5.0,5.0,0.0))
        for bad in ('[3,4]','[3,4,5,6,0,0,0,200]', '__import__("os").system("x")'):
            with self.assertRaises(ValueError):parse_iq(bad,'8','0')
        with self.assertRaises(ValueError):parse_iq('[3,4,0,5,-3,-4,0,0]','8','1')
        with self.assertRaises(ValueError):parse_iq('[3,4,0,5,-3,-4,0,0]','7','0')
        repaired=parse_iq('[12,99,11,98,3,4,0,5,-3,-4,0,0]','12','1',
                          invalid_policy='esp32_drop_first_four')
        self.assertEqual(repaired,(5.0,5.0,5.0,0.0))
        with self.assertRaises(ValueError):
            parse_iq('[3,4,0,5,-3,-4,0,0]','8','1',
                     invalid_policy='esp32_drop_first_four')

    def test_auth_and_timestamp_order(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'raw.csv'
            def write(ts):
                with path.open('w',newline='') as f:
                    w=csv.DictWriter(f,fieldnames=['type','mac','rssi','local_timestamp','len','first_word','data'])
                    w.writeheader()
                    for t in ts:w.writerow(dict(type='CSI_DATA',mac='not-persisted',rssi='-45',local_timestamp=t,
                                                len=8,first_word=0,data='[3,4,0,5,-3,-4,0,0]'))
            write([100,200])
            with self.assertRaises(PermissionError):load_owned_csv(path,lab_authorized=False)
            packets=load_owned_csv(path,lab_authorized=True)
            self.assertEqual(len(packets),2)
            self.assertTrue(all('mac' not in r for r in packets))
            write([100,100])
            with self.assertRaisesRegex(ValueError,'nonmonotone'):load_owned_csv(path,lab_authorized=True)

    def test_two_link_trial_whitelist_and_missing_abstain(self):
        def pk(t,signal):return dict(timestamp_us=t,rssi=-45,mean_amplitude=signal,subcarrier_dispersion=0.0)
        links={'1':[pk(100,1),pk(200,3),pk(300,4)],'2':[pk(100,2),pk(200,2)]}
        def entry(tid,link,start,stop,label='pocket'):
            return dict(trial_id=tid,session_id='S1',placement_id='P1',label=label,
                 ground_truth_source='manual_model_state',trial_origin='synthetic_test_fixture',
                 link_id=link,start_us=str(start),stop_us=str(stop))
        rows=aggregate_trials([entry('A','1',0,260),entry('A','2',0,260),
                 entry('B','1',260,450),entry('B','2',260,450)],links)
        self.assertEqual(rows[0]['quality'],'ok')
        self.assertEqual(rows[1]['quality'],'missing')
        self.assertEqual(rows[1]['rssi_2_dbm'],'')
        self.assertGreater(rows[0]['csi_1_amp_dispersion'],0)
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'out.csv'
            export_trials(rows,path)
            text=path.read_text()
            self.assertNotIn('mac',text)
            self.assertNotIn('timestamp_us',text)
        with self.assertRaisesRegex(ValueError,'inconsistent trial truth'):
            aggregate_trials([entry('A','1',0,260),entry('A','2',0,260,'both')],links)
        with self.assertRaisesRegex(ValueError,'duplicate trial'):
            aggregate_trials([entry('A','1',0,260)]*2,links)
        with self.assertRaisesRegex(ValueError,'overlapping reset trials'):
            aggregate_trials([entry('A','1',0,260),entry('B','1',100,300)],links)

if __name__=='__main__':unittest.main()
