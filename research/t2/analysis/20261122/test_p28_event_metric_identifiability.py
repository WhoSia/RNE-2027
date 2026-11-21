"""P28 frozen paired-event audit tests: score collisions must not be over-interpreted."""
import copy
import json
import os
import unittest
from pathlib import Path
from p28_event_metric_identifiability import source,inspect,SHA_P25P26,SHA_P27

BASE=Path(os.environ.get('T2_FOLLOWUPS_DIR','/mnt/data/t2_p18_canonical'))
class EventMetricTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.a=source(BASE/'p25_p26_results.json',SHA_P25P26)
  cls.b=source(BASE/'p27_results.json',SHA_P27)
 def test_exact_sha_locked_inputs(self):
  self.assertEqual(len(self.a['P26']['records']),64)
  self.assertEqual(len(self.b['records']),128)
 def test_all_score_collisions_still_have_event_differences(self):
  o=inspect(self.a,self.b)
  self.assertEqual(o['P26_equal_cost_but_changed_denial_attempts'],64)
  self.assertEqual(o['P26_6_vs10_denial_attempt_delta_hist'],{4:64})
  self.assertEqual(o['P26_6_vs10_terminal_remaining_different'],0)
 def test_cross_trial_64_worlds_agree(self):
  self.assertEqual(inspect(self.a,self.b)['cross_reproduced_P26_P27_h2_worlds'],64)
 def test_denial_count_not_unique_vehicles(self):
  o=inspect(self.a,self.b)
  self.assertEqual(o['P27_6_vs10_denial_attempt_delta_hist'],{4:128})
  self.assertEqual(o['P27_10_vs16_denial_attempt_delta_hist'],{6:128})
 def test_equal_score_can_change_true_crossings(self):
  o=inspect(self.a,self.b)
  self.assertEqual(o['P27_6_vs10_left_crossing_delta_hist'],{0:96,1:32})
  self.assertEqual(o['P27_same_cost_different_left_crossings_by_headway'],{1:16,2:16})
 def test_duplicate_key_detected(self):
  b=copy.deepcopy(self.b)
  b['records'][1]['key']=b['records'][0]['key']
  b['records'][1]['headway_s']=b['records'][0]['headway_s']
  with self.assertRaises(ValueError):inspect(self.a,b)
 def test_wrong_file_hash_rejected(self):
  with self.assertRaises(ValueError):source(BASE/'p27_results.json','0'*64)
 def test_tampered_independent_frozen_replay_rejected(self):
  b=copy.deepcopy(self.b)
  for r in b['records']:
   if r['headway_s']==2:
    r['effects']['10']['delta_cost']+=1
    break
  with self.assertRaises(AssertionError):inspect(self.a,b)

if __name__=='__main__':unittest.main()
