"""Exact-source synthetic physical followup verification. No real signal operations."""
import copy
import json
import os
import unittest
from pathlib import Path
from dataclasses import replace

from p25_p26_physical_followups import (
 SEED_REGIMES,HEADWAYS,DURATIONS,worlds,action,key,frozen_p19,replay_pair,
 p25,p26)
from p27_stage_opportunity_extension import longer_action,run_full,crossings
from dual_lane_v11 import run
from physical_transfer_screen import score

REFERENCE=Path(os.getenv('P25_P19_REFERENCE',
 '/mnt/data/t2_p18_canonical/p19_receiver_service_opportunity_results.json'))

class FollowupTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.reference=json.loads(REFERENCE.read_text(encoding='utf8'))
 def test_factorial_64_unique_world_keys(self):
  cases=list(worlds())
  self.assertEqual(len(cases),64)
  self.assertEqual(len({k for k,_,_ in cases}),64)
  self.assertEqual(len({tuple(tape) for _,_,tape in cases}),4)
 def test_p19_reference_256_unique(self):
  self.assertEqual(len(frozen_p19(self.reference)),256)
 def test_reject_forged_p19_reference(self):
  bad=copy.deepcopy(self.reference);bad['records'].append(bad['records'][0])
  with self.assertRaises(ValueError):frozen_p19(bad)
 def test_reject_unknown_dose(self):
  for n in (0,4,12,100):
   with self.assertRaises(ValueError):action(n)
   with self.assertRaises(ValueError):longer_action(n)
 def test_model_interventions_have_no_overlap(self):
  for n in (6,8,10,16,24):
   a=action(n) if n in DURATIONS else longer_action(n)
   self.assertEqual(a[0],(84,87,'-'))
   self.assertEqual(a[1],(87,87+n,'L'))
   self.assertEqual(a[2],(87+n,120,'-'))
 def test_checkpoint_replay_immutable_and_same_future(self):
  _,cfg,tape=next(worlds())
  base,treated,sha=replay_pair(cfg,tape,8,direct_gate=True)
  self.assertEqual(len(sha),64)
  self.assertEqual(base['generated'],len(tape))
  self.assertEqual(treated['generated'],len(tape))
 def test_model_conservation_failure_detected(self):
  _,cfg,tape=next(worlds());base,treated,_=replay_pair(cfg,tape,8)
  corrupt=copy.deepcopy(base);corrupt['generated']+=1
  with self.assertRaises(AssertionError):score(corrupt,60)
 def test_p25_full_frozen_regression(self):
  x=p25(self.reference)
  self.assertEqual(x['worlds'],192)
  self.assertEqual(x['unique_full_arrival_tapes'],4)
  self.assertEqual([r['worlds'] for r in x['strata']],[64]*3)
  self.assertEqual(sum(x['strata'][1][k] for k in ('beneficial','harmful','ties')),64)
 def test_p26_same_checkpoint_dose(self):
  x=p26(self.reference)
  self.assertEqual(x['worlds'],64)
  self.assertEqual(x['unique_full_arrival_tapes'],4)
  self.assertEqual(sum(x['candidate_best_tie_sets'].values()),64)
  self.assertTrue(all(len({r['checkpoint_sha256']})==1 for r in x['records']))
 def test_p27_full_exploratory_disclosure_and_crossings(self):
  x=run_full(self.reference)
  self.assertTrue(x['pilot_informed'])
  self.assertEqual(x['worlds'],128)
  self.assertEqual(x['unique_tapes'],4)
  self.assertEqual(sum(x['rank_24_vs6'].values()),128)
  self.assertEqual(sum(x['first_tested_duration_differing_from6'].values()),128)
  self.assertEqual(len(x['strata']),8)
 def test_p27_trace_event_counts_are_nonnegative(self):
  _,cfg,tape=next(worlds())
  cp=run(replace(cfg,receiver_headway_s=1),tape,trace=True,checkpoint_at=84)
  out=run(replace(cfg,receiver_headway_s=1),tape,trace=True,
     resume_from=cp,phase_overrides=longer_action(24))
  c=crossings(out)
  self.assertEqual(set(c),{'L','S'})
  self.assertTrue(all(v>=0 for v in c.values()))

if __name__=='__main__':unittest.main()
