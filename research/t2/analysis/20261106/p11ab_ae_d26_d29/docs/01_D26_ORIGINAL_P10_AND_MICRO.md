# D26 — historical P10 integrity replay and micro event reference

## Source provenance
- Original P10 Drive ZIP retrieved intact (17,909 bytes), SHA256 `9fa06146b781bcbbd1f5e19dc25b277e1e98c695b13e61fc0b291b58cd53b59c`.
- Original P9 Drive ZIP retrieved intact (64,453 bytes). The included `reference/T2_v69_P2/corridor.py` SHA256 `12987786fb36409a272a50233c12c006d0a23d5f75a5487be68d51392c4614cc`, matches the 2026-11-04 original source receipt.
- Unmodified P2 28 regression tests PASS; P10 8 mechanism tests PASS; original 8-grid `p10_boundary_trace.py` output matches archived `boundary_mechanism.json` exactly for `runs` and `mechanism`.

## Direct replay results
| dt(s) | vehicle 1 link receipt(s) | vehicle 8 connector admission(s) | early capacity reuse(s) |
|---:|---:|---:|---:|
| .5 | 47.5 | 47.0 | .5 |
| .4 | 48.0 | 87.6 | 0 |
| .25 | 47.5 | 87.25 | 0 |
| .2 | 47.4 | 87.4 | 0 |
| .125 | 47.25 | 47.125 | .125 |
| .1 | 47.1 | 47.0 | .1 |
| .0625 | 47.125 | 47.0625 | .0625 |
| .05 | 47.05 | 47.0 | .05 |

Selected original event-time gate at `.5s` changes vehicle 8's old 47.0s admission to a next-cycle admission. This is a *historical model experiment*, not a traffic signal recommendation. We reproduced the original code and its tests; we have **not** proved a universal temporal consistency theorem.

## New micro reference
- State: vehicle length, link, longitudinal front position, speed, acceleration cap, route, bus stop phase.
- Synchronous fixed-step movement; incoming demand admitted only when start-of-tick receiving space exists.
- Held-out evidence requirement: measure absolute trajectory errors at identical timestamps. No observed calibration has been done.
