import unittest
from dataclasses import replace
from p19_receiver_service_opportunity import evaluate,_events
from p18_clock_position_action import build_config,arrival_clock_pair

class P19Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg=replace(build_config(112,1650,.50,14.,2,.5),downstream_offset_s=0)
        cls.tape=arrival_clock_pair(cls.cfg.base)[1]
        cls.row=evaluate(cls.cfg,cls.tape)
    def test_true_single_tape_id(self):
        self.assertEqual(len(self.row['tape_hash']),64)
    def test_same_checkpoint_immutability(self):
        self.assertEqual(self.row,evaluate(self.cfg,self.tape))
    def test_valid_action_cost(self):
        self.assertIsInstance(self.row['model_delta'],int)
    def test_distinct_baseline_and_treatment_paths(self):
        self.assertEqual(set(self.row['baseline']),set(self.row['treatment']))
    def test_both_paths_conserve(self):
        self.assertGreaterEqual(self.row['baseline']['remaining'],0)
        self.assertGreaterEqual(self.row['treatment']['remaining'],0)
    def test_capacity_change_is_different_world(self):
        cfg=replace(self.cfg,receiver_slots=4)
        other=evaluate(cfg,self.tape)
        self.assertNotEqual(other['receiver_capacity'],self.row['receiver_capacity'])
        self.assertEqual(other['tape_hash'],self.row['tape_hash'])
    def test_offset_change_is_different_world(self):
        cfg=replace(self.cfg,downstream_offset_s=15)
        other=evaluate(cfg,self.tape)
        self.assertNotEqual(other['downstream_offset_s'],self.row['downstream_offset_s'])
        self.assertEqual(other['tape_hash'],self.row['tape_hash'])
    def test_event_window_nonnegative(self):
        for x in ('baseline','treatment'):
            self.assertGreaterEqual(self.row[x]['receiver_denials_84_129'],0)
    def test_excludes_real_signal_claim(self):
        self.assertIn('NOT_LEGAL',self.row['scope'])

if __name__=='__main__':unittest.main()
