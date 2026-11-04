# v6.7-P3 SignalTimeline

Study date 20261104. Canonical 60s cycle: main green [0,30), lost [30,33), side vehicle green [33,49), pedestrian-only phase [49,57), lost [57,60). Without WALK side vehicle green runs until57. Intervals half-open.

New SignalTimeline class enforces phase sum and pedestrian duration; computes current M/R/S/P, remaining green, WALK windows and permitted side-vehicle admission with rear-clearance requirement. P3 integrates it with the actual P1b vehicle model; this is a phase-contract integration, not full P1a-P1b physical reconciliation.

IMPORTANT: the P3 side clearance entry guard can still leave an approaching car unable to stop before the line. No continuous-time safety proof or physical pedestrian-agent simulation. P3 is HOLD pending viable-set handling.