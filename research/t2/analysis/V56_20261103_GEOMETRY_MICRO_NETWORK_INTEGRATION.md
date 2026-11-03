# T2 v5.6 — 20261103 geometric concurrent dispatch integration

## Chronology
This is November 3 (`20261103`), not a continuation recorded under `20261102`. Today’s standalone Google Docs ledger is https://docs.google.com/document/d/1oxsUpQ6W_A71FqC_9D7_YKQCj7XHQejbLI6mfcMW-9U/edit . Today’s Drive reproducibility ZIP is https://drive.google.com/file/d/1wnECQaMxEDI2jwo7pcbVp2PUQga8H7c8/view .

## Implemented
Original 12-movement synthetic geometric centerline and clearance conflict graph embedded in a 3-junction per-vehicle IDM simulation with actual two-vehicle same-timestep crossing for geometric-compatible main-through + side-exit movements. Conflicting side merges and main-through do not cross together. Crossing audits, vehicle conservation and spacing assertions retained. The model maps generic 4-way W>E/W>S/N>E/N>W connections to a simplified three-signal corridor and has not been surveyed in Changwon. Added parallel stage window for 12 s of main green; do not confuse with a capacity-neutral phase reallocation.

## Validation and experiments
Seven new tests pass. Baseline exact numeric check against unchanged historical v5.3 engine passes 48 combinations (3 demand groups, 4 seeds, 2 policies and 2 pocket lengths), including completed counts, exposure, blocked transfers, releases and pocket diversions. New experiment has 3 demand groups ×24 seeds ×2 policies =144 synthetic runs, followed by 3×12 new seeds ×2 policies =72 independent holdout runs. Paired means of concurrent minus sequential exposure (vehicle-seconds) in exploratory runs: balanced −357.08 (22/24 negative), main-peak −231.23 (24/24), side-peak −1307.40 (24/24). Holdout means: −354.42, −227.75, −1178.17 respectively; 12/12 negative in every demand group. No measured traffic outcomes are inferred.

## Research limits
Signal green resources are unequal in the comparison: parallel dispatch adds a side-exit opportunity during main green. Neither real road safety nor physical conflict occupancy intervals, realistic vehicle swept body, horizontal lane changes, verified signal plans or external SUMO validation are established. The findings support a constructed software mechanism and its synthetic effect, NOT an operational traffic optimization recommendation.

## Split outputs
Exhibition: validated refinement and integration of physically motivated multi-lane, finite-storage signalized IDM microsimulation. Paper: future hypothesis regarding information sufficiency and policy stability under uncertain movement conflicts. Paths: research/t2/microscopic/v56/EXHIBITION_20261103.md and PAPER_20261103.md.

## Evidence
ZIP SHA256: 2675ece0879e47b007073f70c3852652e06efecbb6d4d0127d1a35fa6235e7fa.
