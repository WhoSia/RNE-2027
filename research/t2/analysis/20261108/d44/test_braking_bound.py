"""D44 reproduces braking-bound issue in unmodified D27 micro reference.

The expected-failure test documents a known physical inconsistency.
When it unexpectedly succeeds, remove decorator and replace with an enforced regression.
No real-world traffic control use.
"""
import sys
import unittest
from pathlib import Path

MICRO_SRC=Path(__file__).resolve().parents[2]/"20261106"/"p11ab_d26_d30"/"d27"/"src"
sys.path.insert(0,str(MICRO_SRC))
from micro_world import Road, Vehicle, FixedSignal, run

class D44BrakingAudit(unittest.TestCase):
    def scenario(self):
        r={"R": Road("R", length_m=12.0, lanes=1, speed_limit_mps=12)}
        v=[Vehicle("car1", route=("R",), depart_s=0,
                   length_m=4.5, desired_mps=12, accel_mps2=1.5,
                   decel_mps2=0.25)]
        result=run(r,v,horizon_s=5,signals={"R":FixedSignal(cycle_s=10,green_s=1)})
        return result,v[0]

    def test_input_and_conservation(self):
        result,_=self.scenario()
        self.assertEqual(result.collision_violations,0)
        self.assertEqual(list(result.admissions),["car1"])
        self.assertEqual(len(result.finishes),0)

    @unittest.expectedFailure
    def test_physical_deceleration_bound_unmet(self):
        """Existing engine abruptly brakes from 3m/s to 0; should be <= 0.25m/s^2."""
        result,vehicle=self.scenario()
        speeds=[result.states[t]["car1"][3] for t in sorted(result.states)]
        decels=[(v0-v1) for v0,v1 in zip(speeds,speeds[1:])]
        self.assertLessEqual(max(decels), vehicle.decel_mps2*1+1e-9)

if __name__=="__main__":
    unittest.main()
