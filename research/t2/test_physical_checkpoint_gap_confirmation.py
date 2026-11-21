"""PHYS-11: target-lane gap persistence is checkpoint-safe and default-preserving."""
import pickle
import unittest
from dataclasses import replace
from dual_lane_v11 import DualConfig, run
from spatial_v10 import Config, arrivals
from physical_transfer_screen import score


def case(confirm=1, seed=0, pocket=14.):
    base=Config(seed=seed,pocket_length_m=pocket,duration_s=240,
                demand_vph=1800,left_fraction=.5,phase_order='leading')
    return DualConfig(base=base,through_B_share=0.,allow_lane_changes=True,
                      change_zone_m=100.,receiver_slots=4,receiver_mode='cells',
                      lane_change_gap_confirmation_s=confirm)


class GapConfirmationTests(unittest.TestCase):
    def test_default_one_is_original_fixture(self):
        c=case()
        self.assertEqual(c.lane_change_gap_confirmation_s,1)
        r=run(c,arrivals(c.base))
        self.assertEqual(score(r),14011)
        self.assertEqual(r['changes_A_to_B'],34)
        self.assertEqual(r['network_out_S'],30)
        self.assertEqual(r['network_out_L'],15)
        self.assertEqual(r['lane_change_gap_confirmation_wait_s'],0)

    def test_confirmation_two_three_wait_and_change_counts(self):
        for confirm,expected_changes,expected_waits in ((2,33,65),(3,33,137)):
            with self.subTest(confirm=confirm):
                c=case(confirm)
                r=run(c,arrivals(c.base))
                self.assertEqual(r['changes_A_to_B'],expected_changes)
                self.assertEqual(r['lane_change_gap_confirmation_wait_s'],expected_waits)
                self.assertEqual(r['generated'],r['remaining']+r['network_out_S']+r['network_out_L'])

    def test_full_checkpoint_history_replay_and_snapshot_immutability(self):
        for confirm in (1,2,3):
            for trace in (False,True):
                with self.subTest(confirm=confirm,trace=trace):
                    c=case(confirm,seed=80)
                    tape=arrivals(c.base)
                    cp=run(c,tape,checkpoint_at=84,trace=trace)
                    frozen=pickle.dumps(cp,protocol=4)
                    direct=run(c,tape,trace=trace)
                    restarted=run(c,tape,trace=trace,resume_from=cp)
                    self.assertEqual(direct,restarted)
                    self.assertEqual(pickle.dumps(cp,protocol=4),frozen)
                    if trace:
                        alternative=run(c,tape,trace=True,resume_from=cp,
                           phase_overrides=((84,87,'-'),(87,91,'L'),(91,120,'-')))
                        self.assertEqual(alternative['frames'][:84],direct['frames'][:84])

    def test_gap_physics_cannot_be_switched_mid_checkpoint(self):
        c=case(2)
        tape=arrivals(c.base)
        cp=run(c,tape,checkpoint_at=84)
        with self.assertRaisesRegex(ValueError,'incompatible physical parameters'):
            run(replace(c,lane_change_gap_confirmation_s=3),tape,resume_from=cp)

    def test_invalid_confirmation_values_rejected(self):
        for bad in (0,-1,11,True,False,1.5,'2',None):
            with self.subTest(bad=bad):
                c=case(bad)
                with self.assertRaisesRegex(ValueError,'gap confirmation'):
                    run(c,arrivals(c.base))


if __name__=='__main__':
    unittest.main()
