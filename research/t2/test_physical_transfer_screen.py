import unittest
from physical_transfer_screen import cases,paired,summarize,score,experiment

class TransferScreenDesignTests(unittest.TestCase):
 def test_preregistered_192_unique_cases(self):
  all_cases=cases()
  self.assertEqual(len(all_cases),192)
  self.assertEqual(len(set(all_cases)),192)
 def test_loss_counts_queued_vehicles_and_terminal(self):
  y={'generated':4,'network_out_S':2,'network_out_L':1,'remaining':1,
     'outside_vehicle_seconds':20,'upstream_vehicle_seconds':30,
     'receiver_vehicle_seconds':7}
  self.assertEqual(score(y),117)
  with self.assertRaises(AssertionError):score(dict(y,generated=5))
 def test_pairing_reversals_without_hidden_ties(self):
  rows=[]
  for c in cases():
   outcome={'seed':c.seed,'pocket_m':c.pocket_m,'b_share':c.b_share,
            'change':c.change,'order':c.order,'objective':
           (10 if c.order=='leading' and not c.change else
            7 if c.order=='lagging' and not c.change else
            4 if c.order=='leading' and c.change else 6),
            'generated':3,'network_out_S':2,'network_out_L':1}
   rows.append(outcome)
  pairs=paired(rows)
  s=summarize(pairs)
  self.assertEqual(s['scenario_count'],192)
  self.assertEqual(s['paired_phase_comparisons'],96)
  self.assertEqual(s['paired_lane_change_comparisons'],48)
  self.assertEqual(s['strict_sign_reversals_on_lane_change_permission'],48)
 def test_injected_engine_runs_all_cases_without_canonical_engine(self):
  def fake_run(cfg,stream):
   r={'generated':12,'network_out_S':8,'network_out_L':4,'remaining':0,
      'outside_vehicle_seconds':3,'upstream_vehicle_seconds':2,
      'receiver_vehicle_seconds':1,'pocket_block_seconds':0,
      'changes_A_to_B':int(cfg.allow_lane_changes),
      'receiver_denied_attempts':0,'receiver_denied_seconds':0}
   return r
  out=experiment(fake_run)
  self.assertEqual(out['summary']['paired_phase_comparisons'],96)
  self.assertEqual(len(out['runs']),192)
  self.assertEqual(out['summary']['strict_sign_reversals_on_lane_change_permission'],0)
