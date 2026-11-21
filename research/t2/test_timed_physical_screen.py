import json
import unittest
from pathlib import Path
from timed_physical_screen import experiment,assert_baseline_equal,WINDOWS

class PhysicalTimingScreenTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=experiment()
 def test_case_and_pair_counts(self):
  self.assertEqual(len(self.r['runs']),384)
  self.assertEqual(len(self.r['phase_pairs']),192)
  self.assertEqual(len(self.r['early_late_contrasts']),48)
 def test_equal_legal_window_durations(self):
  self.assertEqual(sum(b-a for a,b in WINDOWS['early']),90)
  self.assertEqual(sum(b-a for a,b in WINDOWS['late']),90)
  self.assertEqual(len(WINDOWS['early']),len(WINDOWS['late']))
 def test_original_192_controls_reproduce_exactly(self):
  baseline=json.loads(Path('physical_192_runs.json').read_text())
  self.assertEqual(assert_baseline_equal(self.r,baseline),192)
 def test_reversal_grid_and_penalty_robustness(self):
  self.assertEqual(self.r['summary']['reversals_by_penalty'],{'0':25,'60':25,'120':24})
  self.assertEqual(self.r['summary']['ties_p60'],0)
 def test_equal_actual_change_count_is_not_sufficient(self):
  witnesses=[x for x in self.r['early_late_contrasts']
             if x['early_delta_p60']*x['late_delta_p60']<0 and x['early_changes']==x['late_changes']]
  self.assertEqual(len(witnesses),3)
  self.assertTrue(all(x['early_changes']>0 for x in witnesses))
 def test_zero_bypass_in_degenerate_geometry(self):
  self.assertTrue(all(x['early_changes']==x['late_changes']==0
    for x in self.r['early_late_contrasts'] if x['pocket_m']==70.))
