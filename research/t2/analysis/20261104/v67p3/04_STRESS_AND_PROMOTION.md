# P3 stress and special reviewer gates

Additional 24 P3 runs: 12 seeds960..971 x walk0/8s. Exactly one run has two braking warning ticks, pedestrian interval overlap zero in all 24. No run fully drains at horizon360s. There is no real-world validation, independent SUMO or physical pedestrian agent.

Verdict: software contract and cross-lineage source audit accepted; signal-safety promotion HELD. P4 must use joint stop/go viability; guard against unreachable stoplines, sub-step swept polygon conflicts, real pedestrian movement and actual receiving-link spatial occupancy, plus field calibrated headways and independent SUMO/held-out field testing. The one-connector exclusion is conservative and cannot prove simultaneous vehicle flow capacity.

Keep the 20261104 shared-drive original sources and tests unmodified. GitHub Actions bot cannot be contributor.