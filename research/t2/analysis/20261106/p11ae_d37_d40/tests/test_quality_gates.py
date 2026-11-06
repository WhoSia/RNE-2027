from pathlib import Path
import sys,tempfile,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from trajectory_gate import parse_csv,summarize,verify_observed_file
from empirical_summary import load_manifest, describe
from parity_contract import Evidence,evaluate_pair,audited_trip_rows,source_receipt
from queue_observation import Track,LaneMeasurement,count_stopped_approach

ROOT=Path(__file__).resolve().parents[1]
H='AV_speed,AV_x,AV_y,AV_acc,AV_distance_to_light,nearest_light_x,nearest_light_y,nearest_light_state,AV_speed_enhanced,AV_acc_enhanced\n'
RAW=(H+'0.0,0,0,0,8,0,8,4,0,0\n1.5,1,0,0,7,0,8,6,1.5,0\n').encode()

class GateTests(unittest.TestCase):
 def test_raw_snippet(self):
  r=summarize(RAW);self.assertEqual(r['frames'],2);self.assertEqual(r['frames_below_0p5_mps'],1);self.assertEqual(r['red_or_red_arrow_frames'],1)
 def test_accept_unknown_minus_one_but_not_green(self):
  x=RAW.replace(b',4,0,0',b',-1,0,0');r=summarize(x);self.assertEqual(r['red_or_red_arrow_frames'],0);self.assertEqual(r['unknown_state_frames'],1)
 def test_reject_unsupported_code(self):
  with self.assertRaises(ValueError):parse_csv(RAW.replace(b',4,0,0',b',99,0,0'))
 def test_reject_duplicate_header(self):
  with self.assertRaises(ValueError):parse_csv(RAW.replace(b'AV_acc,',b'AV_speed,'))
 def test_reject_bad_frame(self):
  with self.assertRaises(ValueError):parse_csv(RAW.replace(b'1.5,1,0,0',b'NaN,1,0,0'))
 def test_reject_missing_source(self):
  with self.assertRaises(ValueError):parse_csv(b'')
 def test_verify_derived_values(self):
  s=summarize(RAW);entry={k:s[k] for k in ['frames','frames_below_0p5_mps','red_or_red_arrow_frames','green_or_green_arrow_frames','mean_speed_mps']};verify_observed_file(RAW,entry)
 def test_forged_metadata_rejected(self):
  s=summarize(RAW);s['frames']=99
  with self.assertRaises(ValueError):verify_observed_file(RAW,s)
 def test_real_derived_manifest(self):
  x=load_manifest(ROOT/'data/cats_16_derived.json');summary=describe(x);self.assertEqual(sum(z['frames'] for z in summary),1456);self.assertEqual([z['stopped_frames'] for z in summary],[328,87])
 def test_not_independent_sumo_without_raw(self):
  a=Evidence('a','T2 ref','G','D','S','s','m','trip','stationary in lane',2,False)
  b=Evidence('','', 'G','D','S','s','m','trip','stationary in lane',2,False)
  o=evaluate_pair(a,b);self.assertFalse(o['ready_for_metric_comparison']);self.assertGreaterEqual(len(o['blocked_reasons']),2)
 def test_sumo_geometry_mismatch(self):
  a=Evidence('a','T2','G1','D','S','s','m','trip','stationary',1,False)
  b=Evidence('b','SUMO 1.28','G2','D','S','s','m','trip','stationary',1,True)
  self.assertIn('missing or conflicting network_geometry_fingerprint',evaluate_pair(a,b)['blocked_reasons'])
 def test_valid_parity_allows_comparison_not_certification(self):
  a=Evidence('a','T2','G','D','S','s','m','trip','stationary',1,False)
  b=Evidence('b','SUMO 1.28','G','D','S','s','m','trip','stationary',1,True)
  o=evaluate_pair(a,b);self.assertTrue(o['ready_for_metric_comparison']);self.assertIn('not validated',o['claim_if_ready'])
 def test_bad_sumo_tripinfo_refused(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'tripinfo.xml';p.write_text('<tripinfos><tripinfo id="v1" depart="8" arrival="4" /></tripinfos>')
   with self.assertRaises(ValueError):audited_trip_rows(p)
 def test_valid_sumo_tripinfo(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'tripinfo.xml';p.write_text('<tripinfos><tripinfo id="v1" depart="2" arrival="4" /></tripinfos>')
   self.assertEqual(len(audited_trip_rows(p)),1);self.assertEqual(len(source_receipt(p)['sha256']),64)
 def test_lane_calibration_required(self):
  with self.assertRaises(ValueError):LaneMeasurement('A',10,0)
 def test_observed_stopped_window_not_spillback(self):
  m=LaneMeasurement('A',100,30);s=[Track('a',10,'A',90,0.1),Track('b',10,'A',86,3),Track('c',10,'B',92,0)]
  r=count_stopped_approach(s,m,10);self.assertEqual(r['stationary_count'],1);self.assertEqual(r['observed_vehicles_in_window'],2)
 def test_duplicate_obs_refused(self):
  m=LaneMeasurement('A',100,30);x=Track('a',10,'A',90,0.1)
  with self.assertRaises(ValueError):count_stopped_approach([x,x],m,10)

if __name__=='__main__':unittest.main()
