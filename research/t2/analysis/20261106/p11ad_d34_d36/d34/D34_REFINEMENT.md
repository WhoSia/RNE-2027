# D34 — independent time step sensitivity reference

An independently coded **single-vehicle** semi-implicit Euler kinematics reference varies time step 1, 0.5, 0.25, 0.125, 0.0625, 0.03125 seconds, with 40m road, 4.5m car, 1.5m/s² acceleration and 8m/s speed cap. It records the analytically interpolated exit time within the final integration step.

**This is NOT convergence of the D27/D33 `micro_world.py` engine**, which explicitly accepts only `dt_s=1`, and is NOT the P10 timestamp regression. The purpose is to generate a numerical error measurement harness and define the missing integration contract. Do not claim a numerical convergence theorem from six points. No signal optimization was performed in D34.

Next: implement a shared state integrator and change the original engine's longitudinal update to use dt_s while retaining lane and boundary invariants, then compare earliest differing physical events, not just final trip time.
