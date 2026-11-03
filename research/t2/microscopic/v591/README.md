# T2 v5.9.1 — 20261103 trajectory entry-state audit

The v5.9 synthetic Bezier speed profile can silently decrease the requested
entry speed to satisfy a speed ceiling or downstream braking constraints.
This breaks state continuity with the upstream IDM network.

An optional strict_entry=True mode now raises ValueError instead of silently
substituting a lower speed. A fully coupled model must predict permissible
entry speeds and initiate deceleration on upstream links. The default mode
remains backward-compatible with v5.9; strict mode must be explicitly selected.

36-case historical audit: 6/36 clipped the 11 m/s requested entry to 9 m/s
because the specified maximum speed was 9 m/s. This is a boundary-setting
problem, not proof of curvature-based failure. In an additional sharp-turn
stress case (lateral acceleration 1 m/s^2, braking .5 m/s^2, requested
13 m/s) the feasible speed at entry falls to around 5.52 m/s.

14 tests passed, 10 historical + 4 new. Synthetic only; no field or SUMO
validation and no complete upstream IDM-to-intersection coupling.
