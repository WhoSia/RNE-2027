# T2 P33 — Independent Go DLR time-series fidelity gate (prospective protocol)

Date: 2026-11-22, KST. CORE / world-contact enabling step. Executable plan frozen **before** P33 full field-data computation. No live road signal control.

## Origin and measurements
Question: Is a 15-minute real DLR-UT v1.3.1 signal/vehicle window internally reliable enough to support later downstream-head/lane temporal matching? We already have P24 official signal-code verification (PDF table4, codes 0–9). This probe independently analyzes raw CSV streams, **not** reconstructed Python P24 result JSON.

Input sha256, exact files:
- `traffic-lights_230924-233000_230924-234500.csv`: `95802b0c00f1232572279fed62668dfb484d8ea2303c4d3eb4a88339d41a8f0c`
- `trajectories_230924-233000_230924-234500.csv`: `6ba8920caa839dc20e2fd7f2fe2dedd553aeb4c27e4be3ea453054de0b09af50`

## Language rationale (Research OS Polyglot)
PROBLEM: two CSV measurement streams and a prior Python-only analytic lineage. REQUIRED PROPERTY: independent parse-and-aggregate implementation with bounded per-ID memory, typed timestamp validation, no dependency install. ECOSYSTEM FIT: Go stdlib `encoding/csv`, `time`, `crypto/sha256`, `encoding/json`; bridge raw CSV -> typed Go maps -> JSON result -> Python parity audit. No new simulator, no rewrite, no external dependencies, no GitHub Actions. Language count is not a metric.

## Measurements to freeze
- strict schema (signal columns exactly timestamp,id,state; trajectory 21 exact documented fields), UTF-8 CSV, timestamp timezone, numeric parsing, ID positivity; complete raw SHA check.
- Signal per ID: count, state labels, transitions **between consecutive observed samples** (no inferred transition time), nonpositive or duplicate sample tick rejection, intervals >1.5s (measurement gaps), maximum consecutive green-observation runs (codes5,6), distribution of sampled green streak lengths, per-ID coverage.
- Trajectory per ID: count, sample median interval, gaps >100ms, distinct object count, class top-label drift (descriptive, no ground truth), interpolated true rows, |reported speed − hypot(vx,vy)| disagreement thresholds >0.1 and >0.5 m/s (do not assume perfect agreement), global time bounds.
- Global overlap between signal and trajectory time coverage, percentage of trajectory observation timestamps inside global signal interval (NOT same signal-to-lane match). Distinct source ID columns intentionally treated in distinct namespaces.
- Require Go result numeric raw counts **exactly equal** earlier P24 signals 26,970 observations, 30 IDs, 869 consecutive state changes; and initial P20 trajectories 8,624 observations, 37 IDs, otherwise FAIL and investigate instead of suppressing.
- Count samples separately from actual duration. Do not infer zero throughput or legal signal phase transitions without map and movement coupling.

## Falsification and hold
Failures: raw digest differs; duplicate same-ID timestamp; reversed time; invalid code; invalid route/timestamp; count mismatch; signal/vehicle no time overlap. Preserve error report rather than silently drop rows. A large number of >1.5s signal gaps or interpolation/class drift can demote exact time-alignment plans (decision depends on measured distributions). No p-values treating repeated samples as independent traffic events.

## RAVEL compressed
Explanandum: field observation fidelity. Selected: Observer-First Drift Audit, Exact-Runtime Certification, Bridge Intent ≠ Bridge Closure. Attacks: timestamp parser must accept UTC offset with microseconds; state transition is sample-to-sample not verified actual green onset; per-vehicle ID namespace must never join signal ID. Return edge: use result to admit/hold external DLR microphysics. Authority ceiling: field CSV observation QC only; not traffic mechanism/counterfactual, not signal control. Debt=1 if no external physical comparison follows.
