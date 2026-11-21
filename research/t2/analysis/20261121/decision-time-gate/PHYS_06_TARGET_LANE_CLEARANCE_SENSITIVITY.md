# PHYS-06 — target-lane clearance sensitivity after observation analysis

**2026-11-21 · SYNTHETIC_UNCALIBRATED · source-derived local simulation**

## Decision and physical modification

After the PHYS-04 parity study and PHYS-05 decision-observation ablation,
the first physics extension was chosen from a real model limitation:
`dual_lane_v11.py` originally permits a straight vehicle to change A→B
when the target cell and the immediate front/rear B cells are empty.
This is a fixed, non-empirical safety proxy, not a Hidas-style full
free/forced/cooperative gap-acceptance model.

The backward-compatible parameter
`lane_change_target_gap_cells: int = 1` extends the B-lane clearance to
`[x-g, ..., x, ..., x+g]`, with strict integer range checks.
It counts **motivated candidate-tick gap denials**, not distinct drivers
or observed human rejected maneuvers. For g=1 it preserves the legacy
crossing behavior; only the new denial counter and metadata are added.
Changing this physical parameter within a resumed same-state branch is
rejected.

## Design

Use downstream receiver capacity **4 cells** with all 8 original seeds,
pocket lengths 14/28/70m, B preassignment shares 0/0.5, and g=1/2/3.
Within each (gap,seed,pocket,share), branch at t=84 into the original
phase and a future left-turn reallocation; the before/after trajectories
have the same exact checkpoint.

**Across g, traffic has evolved differently before t=84.** Thus these
are three alternative physical model worlds, NOT direct same-state
causal treatments of the target gap.

## Local numeric results (48 paired policies per gap)

| Gap cells | Intervention favored | Baseline favored | Ties | Mean delta | Baseline lane changes | Motivated target-gap candidate-tick denials |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 17 | 3 | 28 | -49.958 | 721 | 12415 |
| 2 | 19 | 5 | 24 | -47.417 | 650 | 14112 |
| 3 | 21 | 8 | 19 | -19.250 | 579 | 15280 |

Negative delta denotes lower cost under the intervention.

Two strict preference reversals when changing gap policy across g=1,2,3:

- seed 0, pocket 14m, B share 0: delta [-152, +1458, +248].
- seed 4, pocket 14m, B share 0.5: delta [0, -330, +973].

The total recorded lane changes decrease from 721→650→579 across
g=1→2→3 on these fixtures, but **individual outcomes or policy effects
need not vary monotonically** due to interaction with queues and
receiver supply. The overall mean delta is still slightly negative for
all three settings, but that hides the opposite-signed witnesses.

## Verification and receipts

- All 144 gap-specific baseline vs checkpoint-resume controls passed
  in the local source-derived execution.
- The g=1 pre-existing PHYS-04 configuration preserved all 13
  independently checked outcome fields across all 144 capacity cases.
- The targeted local regression suite passed 8/8 executed test methods
  after fixing a false equality oracle involving copied Random objects.
- Gap-sensitivity JSON was generated twice locally with equal bytes;
  SHA-256: `6ca2b75720fae789c752718cae2b8cf01f35a30fe8cb84a229337057dc8aac39`.

**Execution scope**: local copies of source-derived transition logic with
imported helper APIs; exact GitHub blob hashes NOT independently matched
inside the Python runtime. Committed repository tests must still run in
a clean exact checkout. No GitHub Actions were invoked.

## Research decision and falsifiers

The model now exposes the current physics assumption instead of
implicitly hard-coding it. The observed sign reversals mean that
policy studies should report target-gap sensitivity alongside signal
timing and receiver storage assumptions. Do not call g=2 or g=3
an empirically safe human maneuver; no relative-speed, acceleration,
acceptance probability, cooperative response or driver heterogeneity
has been measured.

Next controlled capability: a separately switchable relative-speed
acceptance test **only after** detector/noise study and exact-code
reproducibility, using bounded parameter ranges and falsification.
Stop if the extended model breaks default g=1 historic outputs,
vehicle conservation, identical checkpoint replay or phase clearance.
