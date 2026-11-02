# T2 v4.9 — Exhibition artifacts and microscopic network integration (2026-11-02)

## Verified implementations
- Individual vehicle IDM dynamics and finite gaps; 3 active main-side signals with individual phase offsets; real route-indexed intermediate OD exits and side-incoming vehicles; finite receiving links and pending origin demand. **A numerical non-overlap cap does not prove safety of general microscopic dynamics.**
- 13 unit tests passed locally, including deterministic OD manifests, legal paths, phase feasibility, conservation per time step, speed/position limits and stress load.
- 60 experimental runs = 3 synthetic demand regimes × 4 policies × 5 shared seeds; dt 0.5 s, generation 320s, horizon 580s. Policies on equal OD demand, not optimized policies.

## Raw outcomes (average total system vehicle-seconds)
| Demand | fixed_32 | coordinated_32 | main_priority_38 | side_priority_25 |
|---|---:|---:|---:|---:|
| balanced | 11035.4 | 10692.3 | 8951.0 | 14896.0 |
| main_peak | 28251.6 | 27862.3 | 23968.1 | 33174.2 |
| side_peak | 25017.3 | 25364.0 | 26071.2 | 27318.9 |

Main-priority reduces synthetic time exposure by 18.9%/15.2% for balanced/main peak, and raises it 4.2% for side peak. Both offsets and green duration change versus fixed; no isolated causal attribution. Because each 580-second horizon censors some trips, also show completed/residual vehicles and avoid naive completed-only mean comparisons.

## Artifacts
Poster PDF (A3, 2 pages, PDF rendered+inspected): https://drive.google.com/file/d/13YG5cnta0S99T32I1isD-QyGnY9Xacij/view
Offline interactive microscopic signal/vehicle demo: https://drive.google.com/file/d/19sKz0SQKZ7G6-8oXCFUFqEvEx0eAQbD0/view
Reproducible ZIP containing full code, 5 figures, raw CSV, experiment manifest, poster and HTML: https://drive.google.com/file/d/1M80THBvfxpUovwGA_o7V6ZYPsdGFiFsT/view
SHA256 ZIP 30246a78eeff28e273d1254fbbfdf26b2900f02db05354d16a55ded111ecc96f; 19 members, integrity passed.

## Limits and follow-up
All link lengths, origin volumes and stage timings are hypothetical. No actual Changwon or Gyeongnam road calibration; no SUMO side-by-side run; no bus or pedestrian movements; no heterogeneous drivers, lane change, turn-lane conflict matrix or terrain. The combined simulator has NOT yet linked back to the identifiability noise/observation experiments. Research next: SUMO identical-network comparison, held-out real counts/phase observations, separate offset-vs-split ablation, observational-policy ambiguity in this micro-network. Keep both precise micro modeling AND trustworthy control recommendations as coequal pillars.