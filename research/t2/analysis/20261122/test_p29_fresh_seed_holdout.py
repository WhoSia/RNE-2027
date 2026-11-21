import unittest
from collections import Counter
from dataclasses import replace
from p29_fresh_seed_holdout import holdout,FRESH_SEEDS,RECEIVERS,OFFSETS,HEADWAYS
from p27_stage_opportunity_extension import longer_action
from p19_receiver_service_opportunity import build_config,arrival_clock_pair
from dual_lane_v11 import run
from physical_transfer_screen import score

class FreshSeedTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=holdout()
 def test_four_fresh_untouched_seed_labels(self):
  self.assertEqual(tuple(x[0] for x in FRESH_SEEDS),(120,121,122,123))
  self.assertTrue(all(s not in range(104,120) for s,_,_ in FRESH_SEEDS))
 def test_factorial_completeness(self):
  r=self.data
  self.assertEqual(r['worlds'],128)
  self.assertEqual(r['unique_tapes'],4)
  keys={(x['seed'],x['receiver_slots'],x['downstream_offset_s'],
      x['pocket_m'],x['b_share'],x['receiver_headway_s']) for x in r['records']}
  self.assertEqual(len(keys),128)
 def test_32_worlds_per_headway_offset(self):
  self.assertEqual([r['worlds'] for r in self.data['strata']],[32]*4)
  self.assertEqual({(r['headway_s'],r['offset_s']) for r in self.data['strata']},
     {(1,0),(1,15),(2,0),(2,15)})
 def test_policy_ranking_has_explicit_ties(self):
  for r in self.data['strata']:
   self.assertEqual(sum(r[k] for k in ('24_better','24_equal','24_worse')),r['worlds'])
 def test_rank_is_paired_not_cross_offset_causal(self):
  for r in self.data['records']:
   self.assertEqual(len(r['checkpoint_sha256']),64)
   self.assertEqual(set(r['effects']),{'6','24'})
   self.assertIn(r['receiver_headway_s'],HEADWAYS)
 def test_model_validator_still_enforced(self):
  _,d,l=FRESH_SEEDS[0]
  cfg=build_config(120,d,l,14.,2,0.)
  tape=arrival_clock_pair(cfg.base)[1]
  cp=run(cfg,tape,checkpoint_at=84)
  with self.assertRaises(ValueError):
   run(cfg,tape,resume_from=cp,phase_overrides=((84,85,'L'),(85,120,'S')))
 def test_deterministic_full_128_world_repetition(self):
  self.assertEqual(self.data,holdout())

if __name__=='__main__':unittest.main()
