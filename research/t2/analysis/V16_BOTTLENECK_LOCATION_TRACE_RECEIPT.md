# T2 v1.6 — Bottleneck location trace and conservative causal boundary
Date: 2026-10-31. Branch: `research/t2-spatial-fig2-v02`.

## Why this research unit exists
v1.5 shows pocket-length and downstream-signal interaction through aggregate
network exits. A new engineering question is *where congestion signatures
appear* as a physical pocket is extended: in front of the left-turn fork,
at the first cell of the receiving link, or both?

## Executed local investigation
- Base: extracted v1.5 local bundle; inherited 76 tests passed.
- Added post-step frame diagnostic and 5 local tests: **81/81 PASS**.
- 384 paired runs: pocket lengths 14/28/42/70m; receiving link 2/4/8
  cells; downstream offset 0/15/30/45s; 8 seeded arrival streams.
- 720-second horizon, demand 1500 vehicles/hour, left share 30%,
  B-lane through assignment 50%, downstream signal green 30s/60s.
- Each seed reuses the same vehicle arrival timestamps and turn types.

At 4 downstream cells, downstream offset 0, 8-seed means:
| Pocket | Network completed | Fork joint-occupancy frames | Receiver entry-cell occupied frames |
|---|---:|---:|---:|
| 14m | 123.750 | 382.125 | 321.750 |
| 28m | 142.875 | 346.625 | 344.750 |
| 42m | 152.250 | 283.250 | 365.250 |
| 70m | 156.500 | 210.000 | 373.500 |

**Conditional interpretation:** longer pocket alleviates joint occupancy
at its fork while more traffic reaches the downstream receiving link,
which is occupied more frequently. In this model these mechanisms can
coexist. Do not infer that the coincident frame conditions prove an
individual vehicle's cause of denied movement.

## What remains unresolved
The diagnostic uses *end-of-step frames*.
The actual attempted stopline denial events occur earlier in the
simulation update. Joint occupancy can be present even when no service
attempt is made, and a denied attempt can be followed by a changed frame.
Therefore the frame signature must be labelled **not causal attribution**.
Next: add exact service-attempt event logging with vehicle ID, movement,
blocking link cell/vehicle ID, and phase, then reconcile event totals
with the original stopline-denied counters. Also test whether the model
results persist with a more physically grounded downstream lane inventory.

## Reproducibility
Local archive `T2_v16_trace_bundle.zip`, eight members including SHA256
manifest; archive SHA256:
`ed85befcdbd643475e782b2374c816b909129b0b4f0be4ff6c545c5dcb24e395`.
GitHub connector-created files and local extracted source are **not
proven byte-identical** and GitHub-HEAD testing is still outstanding.
This archive reports local source execution only.
No GitHub Actions, no workflow changes, no main merge.
