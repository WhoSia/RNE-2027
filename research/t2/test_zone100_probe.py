import json
from pathlib import Path
from unittest import TestCase
from zone100_probe import experiment

class Zone100ExplorationTests(TestCase):
 @classmethod
 def setUpClass(cls):
  cls.source=json.loads(Path('window_384_runs.json').read_text())
  cls.results=experiment(cls.source)
 def test_full_exploratory_grid(self):
  self.assertEqual(self.results['summary']['n_runs'],128)
  self.assertEqual(self.results['summary']['n_timing_pairs'],16)
 def test_no_change_control_unchanged(self):
  self.assertEqual(self.results['summary']['original_never_identical'],32)
 def test_actual_moves_in_enlarged_zone(self):
  self.assertGreater(self.results['summary']['early_changes'],0)
  self.assertGreater(self.results['summary']['late_changes'],0)
 def test_reversal_count_and_no_ties(self):
  self.assertEqual(self.results['summary']['reversal_by_penalty'],{'0':4,'60':3,'120':3})
  self.assertEqual(self.results['summary']['ties_p60'],0)
