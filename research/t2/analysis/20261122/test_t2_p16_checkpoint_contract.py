import unittest
from t2_p16_checkpoint_contract import summarize_checkpoint, audit_phys04_pairs


def obs(p=1,r=(0,),a=(-1,),b=()):
    return dict(outside_A=2,outside_B=0,approach_A=len(a),approach_B=len(b),
                pocket_vehicles=p,receiver_vehicles=len(r),pocket_positions=tuple(-i-1 for i in range(p)),
                approach_A_positions=a,approach_B_positions=b,receiver_occupied_cells=r)


def row(seed,delta,ob=None,pocket=14.,capacity=2,share=.5):
    return dict(seed=seed,delta_p60=delta,capacity=capacity,pocket_m=pocket,b_share=share,
                checkpoint_identity=True,decision_observation=obs() if ob is None else ob)


class P16Tests(unittest.TestCase):
    def test_proxy_detects_occupancy_without_claiming_cause(self):
        r=summarize_checkpoint(obs(),receiver_capacity=2)
        self.assertTrue(r['pocket_present'])
        self.assertFalse(r['receiver_full'])
        self.assertIsNone(r['rf_five_class_label'])
    def test_full_is_not_same_as_entry_cell(self):
        r=summarize_checkpoint(obs(p=0,r=(1,)),receiver_capacity=2)
        self.assertFalse(r['receiver_full'])
        self.assertFalse(r['receiver_entry_cell_occupied'])
        self.assertEqual(r['receiver_free_cells'],1)
    def test_entry_occupied_without_full(self):
        r=summarize_checkpoint(obs(p=0,r=(0,)),receiver_capacity=2)
        self.assertTrue(r['receiver_entry_cell_occupied'])
        self.assertFalse(r['receiver_full'])
    def test_full_link(self):
        r=summarize_checkpoint(obs(r=(0,1)),receiver_capacity=2)
        self.assertTrue(r['receiver_full'])
        self.assertEqual(r['receiver_free_cells'],0)
    def test_full_implies_entry_cell_occupied(self):
        for capacity in (1,2,3,4):
            o=obs(p=0,r=tuple(range(capacity)))
            summary=summarize_checkpoint(o,receiver_capacity=capacity)
            self.assertTrue(summary['receiver_full'])
            self.assertTrue(summary['receiver_entry_cell_occupied'])
    def test_invalid_capacity(self):
        for v in (0,True,-1):
            with self.assertRaises(ValueError): summarize_checkpoint(obs(),receiver_capacity=v)
    def test_invalid_count(self):
        x=obs();x['pocket_vehicles']=True
        with self.assertRaises(ValueError):summarize_checkpoint(x,receiver_capacity=2)
    def test_mismatched_positions(self):
        x=obs();x['pocket_positions']=()
        with self.assertRaises(ValueError):summarize_checkpoint(x,receiver_capacity=2)
    def test_duplicate_receiver_cells(self):
        x=obs(r=(0,0))
        with self.assertRaises(ValueError):summarize_checkpoint(x,receiver_capacity=3)
    def test_receiver_out_of_bounds(self):
        with self.assertRaises(ValueError):summarize_checkpoint(obs(r=(2,)),receiver_capacity=2)
    def test_invalid_observation_type(self):
        with self.assertRaises(TypeError):summarize_checkpoint(None,receiver_capacity=2)
    def test_no_data_means_no_alias(self):
        self.assertEqual(audit_phys04_pairs([]),())
    def test_opposite_artificial_fixture(self):
        result=audit_phys04_pairs([row(0,-8),row(1,9)])
        self.assertEqual(result[0]['seed_groups'],2)
        self.assertIsNone(result[0]['rf_label'])
    def test_same_seed_does_not_mean_two_groups(self):
        result=audit_phys04_pairs([row(0,-8),row(0,9)])
        self.assertEqual(result[0]['seed_groups'],1)
    def test_different_counts_no_alias(self):
        self.assertEqual(audit_phys04_pairs([row(0,-8),row(1,9,obs(p=2))]),())
    def test_different_geometry_no_alias(self):
        self.assertEqual(audit_phys04_pairs([row(0,-8),row(1,9,pocket=28.)]),())
    def test_border_not_strict(self):
        self.assertEqual(audit_phys04_pairs([row(0,-5),row(1,9)]),())
    def test_bad_checkpoint_rejected(self):
        x=row(0,-8);x['checkpoint_identity']=False
        with self.assertRaises(ValueError):audit_phys04_pairs([x])
    def test_bad_delta_rejected(self):
        x=row(0,float('nan'))
        with self.assertRaises(ValueError):audit_phys04_pairs([x])
    def test_invalid_epsilon(self):
        for x in (-1,True,float('nan')):
            with self.assertRaises(ValueError):audit_phys04_pairs([],epsilon=x)


if __name__=='__main__':unittest.main()
