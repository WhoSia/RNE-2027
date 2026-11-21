# RF06-B — Preregistered exact two-blockage observability and decision-value theorem checks

Date 2026-11-21. **Commit this spec before writing/inspecting exact enumeration code.**

## Motivation and original sources
Hu & Fan (2024), *Sensor placement considering the observability of traffic dynamics*, DOI 10.1016/j.trb.2024.103057, Drive original 18GmpK9i-5yfnXNZzL9MImxDjLOl8PYem, develops eigenstructure/graph observability of road-link density models. Zhang, Fakhrmoosavi & Zaghi (2026), arXiv 2609.13212v2, Drive original 1OCDtJcGTh8Red2IlpwYFtTMnl8Bd1pBB, tests normalized mutual information-based sensor placement to reconstruct a simulated Chicago traffic network. We transfer **only basic exact finite-state and two-state linear algebra**, not original road models, dataset or experiments.

## Frozen toy design
There are two bits of true staged blockage at a classroom intersection: P=pocket entrance blocked and D=downstream receiving section blocked. The four equally probable microscopic states are (P,D)=(0,0),(0,1),(1,0),(1,1), prior 1/4 each, no temporal variation, no real RF characteristics.

Idealized deterministic observation functions:
- `aggregate_count` reports P+D (ternary 0,1,2). This is a theoretical perfect aggregate counting instrument, NOT something known to emerge from RF or one camera.
- `any_rf_change` reports 1 if P or D, otherwise 0. This is a **manufactured logical OR proxy** for an all-area binary detector, not a measured Wi-Fi CSI mechanism.
- `pocket_probe` reports P (perfect conceptual local sensor, not a measured magnetometer).
- `downstream_probe` reports D (same restriction).
- `motion_event` always 0 in static-state snapshots, intentionally models a hypothetical movement-only detector in a perfectly static interval; actual event cameras may produce noise and motion artifacts.
One observation is one frozen state, not packet frames.

## Exact predeclared claims
**C1** Four-state Shannon H=2 bits under uniform prior. The observations `aggregate_count`, `any_rf_change`, `pocket_probe`, `motion_event` have entropies **1.5 bits**, **H_b(1/4)=0.8112781244591328 bits**, **1 bit**, **0 bits** respectively. Because observation maps are deterministic, these are mutual informations I(State;Obs).

**C2** Uniform-prior Bayes optimal four-class 0/1 loss errors are:
- Aggregate count = 1/4 (pocket-only vs downstream-only alias)
- Binary OR RF = 1/2 (three positive states alias)
- Pocket probe = 1/2
- Motion event = 3/4
- Aggregate count plus pocket probe = 0
- Pocket probe plus downstream probe = 0.
A sensor combination `any_rf_change+pocket_probe` STILL aliases P=1,D=0 vs P=1,D=1 and has four-class error 1/4.

**C3** Decision-specific query `is P blocked?` with 0/1 loss:
- Aggregate count error 1/4, despite delivering 1.5 total state bits.
- Pocket probe error ZERO, despite delivering just 1 total state bit.
This is a counterexample to choosing a detector solely by maximizing state mutual information when the task is pocket occupancy. It makes no real traffic signal action optimal.

**C4** Linear dynamics contrast: x_{t+1}=A x_t, A=diag(a,b), y_t=[1,1]x_t. The two-row observability matrix O=([1,1],[a,b]) has determinant b-a. If a=b (including stationary A=I), infinitely many pairs of pocket/downstream hidden states with the same sum yield identical temporal outputs; zero rank contrast. If a=0.80 and b=0.81, exact determinant 0.01, and two distinct state vectors (1,0) vs (0,1) have first readings 1 and second readings 0.80 and 0.81. A 0.01-sized observation difference is sensitive to signal noise and unknown inflow. Adding an independent immediate pocket channel row [1,0] makes two-channel measurement matrix ([1,1],[1,0]) determinant -1 regardless of a,b.

**C5** Uniform minimum number of ideal sensors to fully separate all four states is exactly 2, e.g. `pocket_probe+downstream_probe`, or `aggregate_count+pocket_probe`. No single listed channel distinguishes four states. This is not evidence two real RF links always suffice.

## Fail and abuse controls
- All probabilities must be nonnegative exact fractions and sum1; any malformed prior, unknown sensor or empty-state collection rejected.
- For nonuniform prior, report exact Bayes risk and correct mutual information; never silently retain uniform probabilities.
- No action optimization or road signal timing; labels are mock blockages only, not validated roadway physics.
- No downloads/access to `CIM dataset.zip`. No field sensing or hardware; K047 sealed.

## Gate
Full code and unit tests can establish **toy mathematical equivalence classes and decision-specific Bayes risk only**. This research remains ANALYTICAL_CLAIM, not experimental T2 traffic efficacy or real Wi-Fi sensor accuracy. Code and tests must be executed, source fingerprint and GitHub main commit recorded before upgrading test status.
