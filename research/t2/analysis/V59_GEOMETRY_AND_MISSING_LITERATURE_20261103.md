# T2 v5.9 — 20261103 physical-path kernel and provisional missing-literature audit

## Scope and completed experiment
Built standalone 2D cubic Bezier centreline, curvature from first/second derivatives, lateral-acceleration speed cap v <= sqrt(a_lat/|kappa|), forward/backward longitudinal acceleration/braking envelope, sample-wise travel time, square-zone intersection occupancy plus vehicle-length rear clearance. **This is NOT coupled with the v5.8 three-signal IDM network** and is NOT a true continuous swept-vehicle collision model or a calibrated road geometry.

Local Python: 10 tests passed; 36 parameter combinations = 2 synthetic movement shapes × 3 lateral-acceleration limits × 3 entry speeds × 2 speed limits. The chosen turn movement gave occupancy 3.5–5.0 seconds; chosen through 2.0–2.5 seconds (rounded to 0.5-s bins). At entry 7 m/s, lateral max 1.8 m/s², speed cap 13 m/s, turn occupancy 4.5 seconds and through occupancy 2.0 seconds. These are synthetic kinematic sensitivity outputs. The full 14-file ZIP includes raw CSV paths, 241-point traces, exact local test runner, SHA256 manifest, and two distinct research positions.

## Bibliography and provenance
Ten candidates were crosschecked by exact-title Google Drive metadata filters. No exact-title file match was returned; **this is a provisional missing-inventory result, not hash-level proof of absence**, because PDFs can be stored under numeric/scanned/renamed filenames. Metadata sheet with title, authors, DOI, priority, reference links and status is available at https://drive.google.com/file/d/17934WrC_iUFaoArv8hCpKjKrFLvjw4nT/view .

Top three relevant originals: Zhao, Knoop & Wang (2023), Microscopic Traffic Modeling Inside Intersections: Interactions Between Drivers, DOI 10.1287/trsc.2022.1163; Lu et al. (2023), Modeling Vehicle Paths at Intersections: A Unified Approach Based on Entrance and Exit Lanes, DOI 10.1109/TITS.2023.3298344; Lin et al. (2024), Modeling of Vehicle Left-Turn Trajectories and Exit Lane Selection at Signalized Intersections, DOI 10.1061/JTEPBS.TEENG-8054. Read publisher summaries and selectively examined accessible source detail; full original texts are not all acquired/read. Wang et al. (2024) macro-micro consistency, DOI 10.1016/j.trc.2023.104439, and Vasconcelos & Bandeira (2025) IDM calibration, DOI 10.3390/futuretransp5020057, are also high priority.

Important retained Drive titles (not missing): Yin et al. 2011, Yang et al. 2022, Hidas 2005, Kesting et al. 2007, Treiber & Kesting 2013, and Shahdah et al. 2026.

## Engineering and scientific gates
1. Georeference or survey actual approaches, exits, turn trajectories and occupancy envelopes; fit path control points using holdout trajectory data. Avoid artificial endpoint-tangent path loops.
2. Couple physical traversal-time estimates into actual v5.8 junction scheduler with collision-point-specific reservations, preserve FIFO conservation and signal transition invariants.
3. Compare independent SUMO and field observations for trajectory RMSE, conflict-point clearance and queue spillback before claiming real prediction.
4. Exhibition: prioritize realism of reconstructed physical traffic, demonstrated by external validation. Paper: explicitly investigate whether geometry/observability assumptions can reverse optimal signal advice, but no such result was established here.
5. Preserve no GitHub Actions bot contributor rule.

20261103 research ledger: https://docs.google.com/document/d/1oxsUpQ6W_A71FqC_9D7_YKQCj7XHQejbLI6mfcMW-9U/edit
