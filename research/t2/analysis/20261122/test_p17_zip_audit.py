import unittest
from p17_zip_audit import audit_zip,screen,key_for


def observation(b_positions=(-2,),p_positions=(-1,),receiver=(0,)):
    return {'outside_A':0,'outside_B':0,'approach_A':1,'approach_B':len(b_positions),
            'pocket_vehicles':len(p_positions),'receiver_vehicles':len(receiver),
            'approach_A_positions':[-2],'approach_B_positions':list(b_positions),
            'pocket_positions':list(p_positions),'receiver_occupied_cells':list(receiver)}


def record(seed,delta,share=0,positions=(-2,)):
    x={'checkpoint_identity':True,'capacity':2,'pocket_m':14.,'b_share':share,
       'seed':seed,'decision_observation':observation(positions)}
    for p in (0,60,120):
        x[f'cost_baseline_p{p}']=100
        x[f'cost_treatment_p{p}']=100+delta
        x[f'delta_p{p}']=delta
    return x


class TestP17(unittest.TestCase):
    def test_fixture_weak_vs_strong(self):
        rows=[record(0,-305),record(3,1,positions=(-3,))]
        self.assertEqual(screen(rows,0)['opposition_groups'],1)
        self.assertEqual(screen(rows,5)['opposition_groups'],0)
    def test_disallow_cross_geometry_label(self):
        rows=[record(0,-305,0),record(0,1477,.5)]
        self.assertEqual(screen(rows,5)['opposition_groups'],0)
        self.assertEqual(screen(rows,5,mode='drop_b_share')['opposition_groups'],1)
        self.assertFalse(screen(rows,5,mode='drop_b_share')['witnesses'][0]['independent_arrival_tapes_verified'])
    def test_same_count_different_position(self):
        a,b=record(0,-305),record(3,1,positions=(-3,))
        self.assertEqual(key_for(a),key_for(b))
        self.assertNotEqual(a['decision_observation']['approach_B_positions'],b['decision_observation']['approach_B_positions'])
    def test_position_resolved_removes_count_alias(self):
        rows=[record(0,-305),record(3,1,positions=(-3,))]
        self.assertEqual(screen(rows,0,mode='strict')['opposition_groups'],1)
        self.assertEqual(screen(rows,0,mode='strict_positions')['opposition_groups'],0)
    def test_wrong_cost_rejected(self):
        a=record(0,2);a['delta_p60']=3
        with self.assertRaises(ValueError):screen([a])
    def test_full_link_must_include_cell_zero(self):
        a=record(0,2);a['decision_observation']['receiver_vehicles']=2
        a['decision_observation']['receiver_occupied_cells']=[1,1]
        with self.assertRaises(ValueError):screen([a])
    def test_epsilon_boundary(self):
        rows=[record(0,-5),record(1,6)]
        self.assertEqual(screen(rows,5)['opposition_groups'],0)
        self.assertEqual(screen(rows,4)['opposition_groups'],1)
    def test_invalid_epsilon(self):
        for x in (-1,True):
            with self.assertRaises(ValueError):screen([],epsilon=x)
    def test_historical_exact_zip_optional(self):
        import os
        path=os.environ.get('P17_HISTORICAL_ZIP', 'T2_PHYS04_05_05b_06_20261121_Research_Bundle.zip')
        if not os.path.exists(path):self.skipTest('historical evidence ZIP not mounted')
        data=audit_zip(path)
        strict={(x['epsilon'],x['penalty']):x for x in data['comparisons'] if x['mode']=='strict'}
        self.assertEqual(strict[(0,60)]['opposition_groups'],1)
        self.assertEqual(strict[(5,60)]['opposition_groups'],0)
        self.assertEqual(strict[(0,60)]['collision_groups'],11)
        self.assertEqual(strict[(0,60)]['observation_groups'],133)
        self.assertEqual(strict[(0,60)]['witnesses'][0]['negative'][0]['delta'],-305)
        self.assertEqual(strict[(0,60)]['witnesses'][0]['positive'][0]['delta'],1)
        positioned={(x['epsilon'],x['penalty']):x for x in data['comparisons'] if x['mode']=='strict_positions'}
        self.assertEqual(positioned[(0,60)]['observation_groups'],141)
        self.assertEqual(positioned[(0,60)]['collision_groups'],3)
        self.assertEqual(positioned[(0,60)]['opposition_groups'],0)

if __name__=='__main__':unittest.main()
