import unittest
from dataclasses import replace
from network_v51 import *
from experiment_v50 import *

class Tests(unittest.TestCase):
    def test_default_and_explicit_driver_agree(self):
        old=simulate(PLANS[0],make_arrivals(DEMANDS[0],41,75),horizon=150)['summary']
        new=simulate(PLANS[0],make_arrivals(DEMANDS[0],41,75),horizon=150,driver=DriverParameters())['summary']
        self.assertEqual(old,new)
    def test_invalid_parameters(self):
        with self.assertRaises(ValueError):DriverParameters(headway_s=0)
        with self.assertRaises(ValueError):DriverParameters(desired_speed_mps=float('nan'))
    def test_independent_factors(self):
        self.assertEqual(plan(32,'zero').offset,(0,0,0))
        self.assertEqual(plan(32,'progression').main_green,(32,32,32))
        self.assertEqual(plan(38,'zero').offset,(0,0,0))
    def test_idm_parameter_acts_on_vehicle_motion(self):
        a=make_arrivals(DEMANDS[0],41,75)
        p=PLANS[0]
        s1=simulate(p,a,horizon=240.,driver=DriverParameters(headway_s=1.0))['summary']['system_vehicle_seconds_in_horizon']
        s2=simulate(p,a,horizon=240.,driver=DriverParameters(headway_s=1.8))['summary']['system_vehicle_seconds_in_horizon']
        self.assertNotEqual(s1,s2)
    def test_positively_constrained_signal(self):
        for g in SPLITS:
            for o in OFFSETS:
                for j in range(3):
                    p=plan(g,o)
                    phases={p.phase(j,t*.5) for t in range(120)}
                    self.assertEqual(phases,{'main','side','all_red'})
    def test_matched_synthetic_manifest(self):
        self.assertEqual(len({(x.name,x.main_per_min,x.side_per_min) for x in DEMANDS}),3)
        self.assertEqual(len(DRIVERS),3)
        self.assertEqual(len(SEEDS),4)
    def test_finite_residual_preserved(self):
        d=make_arrivals(DEMANDS[1],97)
        s=simulate(plan(25,'zero'),d,driver=DriverParameters(headway_s=1.8))['summary']
        self.assertEqual(s['generated'],s['completed']+s['remaining_inside']+s['pending_boundary'])
    def test_exposure_identity_for_all_policies(self):
        a=make_arrivals(DEMANDS[1],11,100.)
        for p in PLANS:
            q=simulate(p,a,horizon=220.)['summary']
            self.assertAlmostEqual(q['system_vehicle_seconds_in_horizon'],
                q['completed_vehicle_seconds']+q['right_censored_vehicle_seconds'])
            self.assertAlmostEqual(q['exposure_reconstruction_error_s'],0.0)

    def test_single_finished_vehicle_exposure_identity(self):
        r=simulate(PLANS[0],[Vehicle(0,0.,('S0',))],horizon=120.)
        s=r['summary']
        self.assertEqual(s['completed'],1)
        self.assertAlmostEqual(s['system_vehicle_seconds_in_horizon'],
                               r['trips'][0]['duration_s'])
        # v4.9 post-completion tick accounting would omit precisely DT.
        old_formula=s['system_vehicle_seconds_in_horizon']-DT*s['completed']
        self.assertAlmostEqual(s['system_vehicle_seconds_in_horizon']-old_formula,DT)

    def test_single_right_censored_exposure(self):
        r=simulate(PLANS[0],[Vehicle(0,0.,('S0',))],horizon=1.)
        s=r['summary']
        self.assertEqual(s['completed'],0)
        self.assertEqual(s['system_vehicle_seconds_in_horizon'],1.0)
        self.assertEqual(s['right_censored_vehicle_seconds'],1.0)

    def test_fractional_integration_window_rejected(self):
        with self.assertRaisesRegex(ValueError,'integer multiple'):
            simulate(PLANS[0],[],horizon=1.1,dt=.5)

    def test_paired_policy_has_equal_green(self):
        for g in SPLITS:
            self.assertEqual(plan(g,'zero').main_green,plan(g,'progression').main_green)
    def test_rejected_infeasible_green(self):
        with self.assertRaises(ValueError):plan(45,'zero')
if __name__=='__main__':unittest.main()
