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

## Direct service-event extension (2026-10-31, latest)

The simulator now optionally emits `service_events` directly from the
stopline service branch. Each logged refusal contains the precise
simulation time, movement, lane, vehicle ID, and reason
(`receiver_entry_cell_busy` or `receiver_capacity_full`).
Each accepted service logs `stopline_cross`. Logging is trace-only,
not enabled for standard factorial execution. A separate test validates
the refusal event count against the old aggregate counter, checks that
crossed vehicle IDs remain unique, and rejects same-second denial and
successful crossing of the same vehicle. These tests passed locally.

Local unit tests **85/85 PASS** (76 inherited + 5 snapshot diagnostic +
4 exact service event). The 384-run snapshot factorial remains unchanged.
An additional **32 exact-event simulations** (four pockets × eight
paired seeds) compared distinct outcome types.

4-cell receiver, downstream offset 0, 8-seed mean in 720s:
| Pocket length | Network completed | Exact refusal attempts | Distinct refused vehicles | Entry occupied frames | Fork joint occupancy frames |
|---|---:|---:|---:|---:|---:|
| 14m | 123.750 | 276.250 | 22.625 | 321.750 | 382.125 |
| 28m | 142.875 | 334.125 | 21.875 | 344.750 | 346.625 |
| 42m | 152.250 | 384.750 | 19.875 | 365.250 | 283.250 |
| 70m | 156.500 | 400.125 | 19.500 | 373.500 | 210.000 |

Repeated refusal attempts can rise even as the number of different
vehicles refused falls. Attempts, vehicles and frame counts are
fundamentally different observables. Still not an empirical claim that
a specific real-world vehicle was delayed by a specific road geometry.

Updated reproducibility archive:
`T2_v16_spillback_research_bundle.zip`, 14 members, ZIP CRC check PASS,
SHA256 `ce449136ea1ad6969661ea6e4c6ce1f23b90efe49413790efdb516b9c2a49c64`.
The earlier v1.6 81-test/384-run archive is now historical.
All tests executed on a locally extracted source tree; remote GitHub
source bytes remain unverified. No GitHub Actions or workflow edits.
