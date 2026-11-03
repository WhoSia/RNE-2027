# T2 v6.2-P2 — controlled 2×2 mechanism audit (20261103)

36 paired blocks = 3 synthetic demand cohorts × 12 holdout seeds. Each block was run with all 4 combinations of terminal-green admission guard (0/1 s) and connector-to-downstream overshoot retention (off/on); 144 additional synthetic runs.

| Guard | Overshoot retained | Mean exposure (veh·s) | Completed across blocks | Stopline/braking warning ticks | Geometric reset jumps |
| --- | --- | ---: | ---: | ---: | ---: |
| 0s | no | 6043.32 | 649 | 288 | 684 |
| 0s | yes | 6031.96 | 651 | 288 | 0 |
| 1s | no | 6092.73 | 639 | 0 | 674 |
| 1s | yes | 6078.65 | 642 | 0 | 0 |

Factorial paired main effect of green margin: +48.0486 vehicle-seconds. Main effect of overshoot retention: −12.7222 vehicle-seconds. Interaction −2.7222 vehicle-seconds. **The interventions have opposite exposure effects**, meaning it is incorrect to attribute all v6.1→v6.2 changes to geometry alone.

Two new tests make the two interventions independently observable; total suite **40/40 pass**. All synthetic executions across today's v6.2 work: **792**. This is not proof of stopline safety in arbitrary states. The 1-second margin remains an empirically *unvalidated heuristic*. Single-occupant connector and 0.25s snapshots do not certify real collision-free movements or swept-volume conflicts. SUMO and actual traffic data absent.

Current immutable reproducibility ZIP (20 items, code, tests, CSV, per-file SHA): [Drive v6.2-P2 factorial package](https://drive.google.com/file/d/1plXvKhewDnckTLFGR-iTX3XBMCwsPYHI/view). SHA256: `d73340af1685e3ed2b08638b3f03ef27bd23f816c067a94156d050eff2f1b1a0`.

### Gate
Next implement a geometrical swept-footprint oracle, derive rather than heuristically choose braking viability bounds, reintegrate the full corridor, and test against SUMO and observed vehicle trajectories. Model now admits position/projection inspection but is *not yet* a verified 2D interacting-dynamics model.

See [20261103 research log](https://docs.google.com/document/d/1oxsUpQ6W_A71FqC_9D7_YKQCj7XHQejbLI6mfcMW-9U/edit).
