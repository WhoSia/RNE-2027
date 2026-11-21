# T2-PHYS-01 — actual execution receipt (2026-11-21)

**Status: RUN / verified original source, not an empirical road study.**

The registered 192-case physical-transfer screen was actually executed with the existing Python `dual_lane_v11.py` engine: 8 demand seeds × three pocket lengths (14,28,70 m) × two preassignment shares for B (0,.5) × lane-change permission on/off × two phase orders (leading/lagging). Horizon 720 s, demand 1800 veh/h, left fraction .5, downstream 4 cellular slots, permitted lateral movement zone 70 m, terminal remaining penalty 60 vehicle-ticks. Primary grid and evaluation were preregistered in `PHYSICAL_TRANSFER_PROTOCOL.md`; no samples were removed.

## Exact code byte identities
The original Git blob SHA-1 values were matched against the independently reconstructed Python execution files:
- `research/t2/spatial_v10.py`: `ffbf3fc3f8b9a64a819d4f73ce70b264b877e84e` (8085 bytes)
- `research/t2/dual_lane_v11.py`: `9dc08764a1a118d389dd476366a58a19836421f2` (11760 bytes)
- `research/t2/receiving_cells_v15.py`: `b078cf215c74b76ace6dffcbcbacab6ae22c3673` (3574 bytes)
- `research/t2/physical_transfer_screen.py`: `8d75745053ff720db6c8af0001aaaf13ba1f295e` (5590 bytes)
- `research/t2/test_physical_invariants_v22.py`: `c337a38e7d9024c3e7caddec36082872fb45ab1c` (1897 bytes)

The experiment was independently run twice; its complete 192-case JSON was **byte-identical**, SHA-256 `415a006e9f5cc508ad837fc63841f5707fa2b24b5ae0f6883170fa0d5308763b`. Both runs completed, 192 rows plus 96 phase-order pairs and 48 permission pairs. The raw full 122 kB JSON was retained as a local conversation artifact, not represented as a GitHub file; the complete 48-pair exact delta table is committed separately as `physical_192_paired_costs.csv`.

The **five original** v2.2 trace-backed tests passed: actual changes A→B occurred, one position/lane dimension at most per second, pocket refusal events equal counters, downstream denial attempt/events vs distinct seconds match, and duplicate seeded runs agree.

## Primary results
- **16/48** geometry × preassignment × seed strata strictly reverse the preferred phase order when lane-change permission changes (penalty 60).
- 96 phase-order pairs have 62 through-first and 34 left-first winners; no ties.
- 70-m pocket has zero successful lateral changes: with 70-m change zone, the geometric condition x<-k leaves no upstream cells eligible. It is **not** evidence that longer pockets generally eliminate need for bypass.
- This screen compares **different lane-change-permission rules from the beginning of each run**, not two futures sharing a proved identical decision-time microscopic state.
- Summary sign reversals when changing terminal remaining penalty to 0/30/60/120: **15/15/16/15** out of 48; no zero-delta ties at those levels. Mechanistic signs are not determined solely by the default terminal penalty.

## What is not established
This is a synthetic deterministic cellular approximation; it omits speed/acceleration-dependent gap acceptance, real driver choices and field observation. No claim of field throughput gain or safe real-world phase timing. K047's holdout remains sealed, and no HTML playback or mock field data was used.

The next preregistered step is to keep a **single physical lane-change rule** but alter only equal-duration time-local opportunity windows, to ask whether **when** an actually spatially admissible move can occur is sufficient to flip the phase preference. Design is saved before results in `PHYS_WINDOW_PROTOCOL.md`.
