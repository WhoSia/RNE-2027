# T2 v6.3-P0: Stop/go viability envelope (20261103)

Status: **theoretical diagnostic only**, not a real-world signal controller or field safety guarantee. Base: v6.2-P2 independent single-junction simulation.

State: speed v [m/s], stop-line distance d [m], lower-bound braking b_min [m/s²], reaction delay tau [s], clearance buffer d0 [m], green remaining g [s], constant-speed pass allowance c [s].

Under reaction-then-constant-braking assumptions, stop feasibility requires d >= d_stop = v*tau + v²/(2*b_min) + d0. Under an intentionally idealized constant-speed green passage, pass feasibility requires d <= d_pass = v*max(g-c,0). When d_pass < d < d_stop, neither action is feasible within both idealized restrictions. For v>0, a nonempty dilemma interval exists when g < c + tau + v/(2*b_min) + d0/v (assuming g>=c).

Numerical negative control: v=11, b_min=3, tau=0.5, d0=4, g=2, c=0.5 -> pass threshold=16.5m, stop threshold=29.667m. Vehicle at d=20m lies in the model dilemma interval.

Critical limitations: the pass threshold does not include acceleration, pedestrian/intersection clearance, other cars, swept-body geometry, or physically measured yellow/all-red timing. The stop model assumes one bounded reaction delay and constant braking after it. A state at which neither action is feasible is a counterexample to the **simplified decision specification**, not proof of road danger. Fixed 1s guard cannot by itself certify viability over the whole state space.

Follow-up gate: design a viable-set controller with state-continuous upstream IDM prediction, remaining signal phase, downstream storage, and explicit infeasible-state handling; test it against v6.2 using matched OD lists and independent scenario blocks.
