import unittest
from dataclasses import replace
from p18_clock_position_action import (
    build_config,arrival_clock_pair,evaluate_world,alias_screen,screen_cross_clock,
    signature,OVERRIDES,EPSILON)

class P18Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg=build_config(104,1650,.5,14.,2,0.)
        cls.original,cls.changed=arrival_clock_pair(cls.cfg.base)
        cls.a=evaluate_world(cls.cfg,cls.original,'legacy',check_direct=True)
        cls.b=evaluate_world(cls.cfg,cls.changed,'reshuffled_time')
    def test_route_count_and_order_frozen(self):
        self.assertEqual(len(self.original),len(self.changed))
        self.assertEqual([r for _,r in self.original],[r for _,r in self.changed])
    def test_temporal_tapes_differ(self):
        self.assertNotEqual(self.original,self.changed)
    def test_distinct_hashes(self):
        self.assertNotEqual(self.a['tape_hash'],self.b['tape_hash'])
        self.assertEqual(self.a['route_hash'],self.b['route_hash'])
    def test_exact_world_regression(self):
        self.assertEqual(self.a,evaluate_world(self.cfg,self.original,'legacy',check_direct=True))
    def test_both_actions_scored(self):
        self.assertEqual(set(self.a['delta']),set(OVERRIDES))
    def test_min_green_gate(self):
        self.assertFalse(self.a['illustrative_green_min6_eligible']['left_4s'])
        self.assertTrue(self.a['illustrative_green_min6_eligible']['left_8s'])
        self.assertFalse(self.a['actual_yellow_red_pedestrian_modeled'])
    def test_matching_geometry_signature(self):
        self.assertEqual(signature(self.a)[:5],signature(self.b)[:5])
    def test_mismatch_geometry_is_distinct_group(self):
        other=dict(self.a,b_share=.5,seed=105)
        out=alias_screen([self.a,other],'left_8s')
        self.assertEqual(out['groups'],2)
    def test_corrupt_route_hash_rejected(self):
        b=dict(self.b,route_hash='corrupt')
        with self.assertRaises(AssertionError):screen_cross_clock([self.a,b],'left_8s')
    def test_incomplete_clock_pair_rejected(self):
        with self.assertRaises(ValueError):screen_cross_clock([self.a],'left_8s')
    def test_alias_no_false_claim_on_empty(self):
        self.assertEqual(alias_screen([],'left_8s')['opposite_sign_groups'],0)
    def test_same_counts_opposite_sign_requires_margin(self):
        a=dict(self.a,delta={'left_4s':-5,'left_8s':-6})
        b=dict(self.a,clock='reshuffled_time',seed=105,tape_hash='different',delta={'left_4s':6,'left_8s':7})
        self.assertEqual(alias_screen([a,b],'left_4s')['opposite_sign_groups'],0)
        self.assertEqual(alias_screen([a,b],'left_8s')['opposite_sign_groups'],1)
    def test_extra_position_separates_coarse_alias(self):
        a=dict(self.a,delta={'left_4s':-8,'left_8s':-8})
        b=dict(self.a,clock='reshuffled_time',seed=105,tape_hash='different',delta={'left_4s':9,'left_8s':9},positions=[[-4],[],[],[]])
        self.assertEqual(alias_screen([a,b],'left_8s')['opposite_sign_groups'],1)
        self.assertEqual(alias_screen([a,b],'left_8s',positions=True)['opposite_sign_groups'],0)
    def test_direct_checkpoint_does_not_mutate(self):
        self.assertEqual(self.a['generated'],len(self.original))
    def test_label_not_measured(self):
        self.assertTrue(self.a['model_clearance_validated'])
        self.assertIn('left_8s',self.a['delta'])

if __name__=='__main__':unittest.main()
