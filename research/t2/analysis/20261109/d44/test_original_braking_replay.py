"""D44: directly exercise the sealed D26-D30 src/micro_world.py without edits.

Run from the extracted D26-D30 ZIP root:
 PYTHONPATH=src python -m unittest -v test_d44_original_replay
Requires this file placed at the extracted ZIP root or a matching source path.
"""
import unittest
from micro_world import Road, Vehicle, FixedSignal, run

def witness(decel=0.25):
    roads={"R":Road("R",length_m=12.0,lanes=1,speed_limit_mps=12)}
    cars=[Vehicle("car1",("R",),depart_s=0,length_m=4.5,desired_mps=12,
                  accel_mps2=1.5,decel_mps2=decel)]
    return run(roads,cars,horizon_s=5,signals={"R":FixedSignal(cycle_s=10,green_s=1)})

class ReplayObserved(unittest.TestCase):
    def test_speed_trace(self):
        r=witness()
        self.assertEqual([r.states[t]["car1"][3] for t in range(1,6)],[1.5,3,3,0,0])
    def test_position_trace(self):
        r=witness()
        self.assertEqual([r.states[t]["car1"][2] for t in range(1,6)],[1.5,4.5,7.5,7.5,7.5])
    def test_parameter_insensitivity(self):
        self.assertEqual(witness(.25).states,witness(3).states)
    def test_no_collision_indicator(self):
        self.assertEqual(witness().collision_violations,0)
    def test_twelvefold_deceleration(self):
        s=[0]+[witness().states[t]["car1"][3] for t in range(1,6)]
        self.assertAlmostEqual(max(a-b for a,b in zip(s,s[1:])),3.0)
    def test_nonunit_dt_still_rejected(self):
        with self.assertRaises(ValueError):
            run({"R":Road("R",12,1,12)},[Vehicle("v",("R",),0)],dt_s=.5)

class KnownPhysicalFailures(unittest.TestCase):
    @unittest.expectedFailure
    def test_configured_decel_limit(self):
        r=witness(.25)
        s=[0]+[r.states[t]["car1"][3] for t in range(1,6)]
        self.assertLessEqual(max(a-b for a,b in zip(s,s[1:])),.25+1e-9)
    @unittest.expectedFailure
    def test_decel_parameter_should_affect_physics(self):
        self.assertNotEqual(witness(.25).states,witness(3).states)

if __name__=="__main__": unittest.main()
