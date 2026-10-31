# T2 v0.9 — World-contact modeling and local execution receipt
Date: 2026-10-31. Branch: `research/t2-spatial-fig2-v02`.
STATUS: LOCAL PROTOTYPE EXECUTED; REMOTE GITHUB SOURCE NOT BYTE-PARITY CERTIFIED;
FIELD VALIDITY NOT ESTABLISHED.

## Core modules
- `world_contact_v09.py`: finite bay, finite straight storage,
  finite upstream, arrivals waiting outside the link, demand/admission/
  discharge conservation, independent protected signals, cycle history.
  Arrival pattern: uniform or platooned; feeder policy: FIFO, bounded
  lookahead, or unlimited lookahead.
- `test_world_contact_v09.py`: conservation, geometry, phase,
  negative controls, deterministic generation, bounded lookahead,
  signal-service upper bound, event signatures.
- `stress_world_contact_v09.py`: 384 synthetic comparisons.
- `window_sensitivity_v09.py`: 160 additional synthetic comparisons.
- `field_compare_v09.py`: aggregate cycle-count comparison, time alignment
  and independent errors by L/S movement. Does not calibrate on its own.
- `analyze_paired_v08.py`: 18 descriptive paired marginal-gain contrasts
  from the original 192-row run, with all eight seed-level contrasts.
- `plot_window_v09.py`: labeled synthetic sensitivity plot.

## Source-grounded world-contact risks
- Osei-Asamoah et al. (2010), DOI 10.3141/2173-10: their probabilistic
  approach assumes undersaturation and no previous-cycle residual queues;
  authors explicitly flag high-demand intercycle dependence.
- Liu et al. (2019), DOI 10.1061/JTEPBS.0000210: assumes lane changing
  finished before short-lane entrance, omits lane-change dynamics.
- Emtenan & Day (2021), DOI 10.1177/03611981211017139: late lane changes
  and field data calibration can affect discharge and fitted results.
These limitations motivate tests; they are not evidence our toy model
already reproduces real vehicle trajectory dynamics.

## Executed local results
The v0.8 recovered model's 7 tests PASS. Local field comparison tests:
4 PASS. The locally reconstructed v0.9 model: 15 tests PASS, together
26 tests. A total of 384 cross-factor simulations and 160 bounded-lookahead
comparisons ran locally, including per-step mass conservation checks.

At left_share=.3, arrival_rate=1500 veh/h, horizon=1800s, straight
storage=56m, leading left, n=8 deterministic seeds, through exits:
| Feeder assumption | 14m bay | 70m bay | Delta |
|---|---:|---:|---:|
| FIFO | 241.000 | 363.875 | +122.875 |
| lookahead 2 | 283.875 | 369.375 | +85.500 |
| lookahead 4 | 346.000 | 372.125 | +26.125 |
| lookahead 8 | 371.875 | 373.000 | +1.125 |
| unrestricted lookahead | 373.000 | 373.000 | 0 |

**Interpretation is conditional on the model.** The feeder policy
is a queue-selection abstraction, NOT actual multi-lane geometry.
The unrestricted policy represents an intentionally unrealistic
comparator. Differences cannot be presented as predicted roadworks
benefits or statistical confidence intervals for real drivers.

## Important validation separation
The GitHub source was manually composed through the authenticated
connector. A separately reconstructed local implementation was used
for the full 384+160 computations. The two implementations share
documented transition mechanics but are not byte-identical. The
branch's source tests and full stress run must be repeated from the
checked-out exact GitHub HEAD before treating this as a sealed
GitHub-release execution. Do not equate Git blob SHA with a local
SHA256, and do not present the locally generated JSON as remote execution.

Local result SHA256:
- recovered `paired_grid_v08.csv`: `bd102a1f0b739a52917b2b980c9976c5b02a49bfc022e9cf9819a0bd97aca9e5`
- `world_contact_v09.json`: `d7a7b5c8348132dc2dd43c17e53396e6e738502ee2d88e0b64dbdbe290582879`
- `window_sensitivity_v09.json`: `fd349d0d3863edf14cd0bf0efeed4abe84b6b23713881f1d95549d377e7f2739`
- `v09_policy_sensitivity.png`: `e0b3211479cb081db72a154bec075a49287e5516d3fce02997db32962875d0a7`

## Next development gate, exhibition-first
1. Execute exact checked-out GitHub source, rerun 26 tests and 544
   simulations, and compare summary JSON against local execution.
2. Implement physical dual-lane spatial movement and merge reachability,
   rather than tuning queue lookahead to match an attractive result.
3. Freeze a realistic interchange geometry; collect safe anonymous
   movement counts, protected signal timing, and lane dimensions.
4. Compare no-passing, bounded merging, and explicit lane-changing
   mechanisms under identical time-stamped demand.
5. Demonstrate interaction and recommendations only for calibrated
   geometries, alongside sensitivity and errors.
