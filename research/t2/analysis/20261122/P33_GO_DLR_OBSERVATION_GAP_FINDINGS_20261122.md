# T2-P33 — Independent Go DLR signal/trajectory time fidelity: a common-mode observation gap

**2026-11-22 (KST). REAL external DLR-UT v1.3.1 CSV observation-quality audit, not a model intervention, lane alignment, or intersection diagnosis.**

## Origin question and Polyglot selection

The previous P24 Python analysis verified the *official* signal state labels and observed 26,970 signal rows across 30 signal-head IDs but could not resolve which lane/stopline each signal controls. P33 asks whether two exact observed raw streams are timestamp-consistent enough to justify *future* movement-specific synchronization. [Frozen P33 protocol](P33_GO_DLR_TEMPORAL_FIDELITY_PREREG_20261122.md) was committed **before** the full P33 run.

Per the [Research OS Polyglot Computation Atlas](https://app.notion.com/p/3e9ef561cf9281008219e330bcce1b55), language follows actual boundary: **Go 1.23 stdlib** independently streams raw CSV through typed time/ID checks and SHA locks; **Python stdlib** independently recomputes key raw measurements to test the Go↔JSON boundary. Neither replaces the canonical Python cellular simulator; language count is not a goal. Source, tests and result on GitHub `main`:

- [Go module](dlr_temporal_gate_go/go.mod); [Go parser/temporal auditor](dlr_temporal_gate_go/main.go), source Git blob `9267f71ceff95d2204418b2060413f3a996e040b`.
- [13 Go tests](dlr_temporal_gate_go/main_test.go), exact Git blob `00faf2972a9a628ff7210b9ede73b893bca6f00c`; **13/13 PASS**, `go vet` PASS, race-instrumented tests PASS.
- [Independent Python parity oracle](p33_python_csv_parity.py), blob `f7b54d7ccccb312e450aba1639696e4c03e29a97`: **18 measurement checks PASS**.
- [Full JSON observation ledger](P33_GO_DLR_FIELD_FIDELITY_FULL_20261122.json), blob `cdabdf11abc2cfa5cf56f5b4331e2b522775fda0`; SHA-256 `fc70c9cd0859a73a2d113ecbeea8a531b23151901391959d18ffabf1c1dc7687`.

## Raw immutable observations

- Traffic-signal CSV 1,015,948 bytes, SHA256 `95802b0c00f1232572279fed62668dfb484d8ea2303c4d3eb4a88339d41a8f0c`.
- Trajectory CSV 1,478,064 bytes, SHA256 `6ba8920caa839dc20e2fd7f2fe2dedd553aeb4c27e4be3ea453054de0b09af50`.
- Originating documents remain in the R&E 2027 shared-drive 02_DATASETS observed folder; no new field observation was acquired or data modified.

| Direct CSV diagnostic | Measured result |
|---|---:|
| Signal state rows / distinct signal-head IDs | 26,970 / 30 |
| Distinct global signal timestamps | 899 |
| Signal-head records **at every** global timestamp | 30 / 30 |
| Per-head observed state changes between consecutive samples | 869 total |
| Rows with official state code 3 (red) / 5 (green) | 20,924 / 4,680 |
| Distinct sampled green runs (all heads) | 306 |
| Sampled green run length median / maximum | 13 / 36 *samples*, NOT verified phase seconds |
| Tracked-object trajectory rows / tracked IDs | 8,624 / 37 |
| Median inter-sample interval per tracked object | 50ms |
| Intervals exceeding 100ms per tracked object | 0 |
| Rows marked interpolated | 116 |
| Speed-magnitude inconsistency >0.1 m/s | 0 |
| Maximum discrepancy: reported speed vs hypot components | 0.0011023 m/s |
| Top-class label change within object-ID time series | 0 |
| Object observations outside global signal time coverage | 0 |
| Global **range** intersection length | 892.150s; not lane-specific match |

P24's raw-record count, distinct signals and state-change number reproduce exactly. The 1Hz signal samples and ~20Hz object trajectories are *different measurement systems*. Do not treat their time resolutions as interchangeable or as full traffic participation.

### New shared observation gap (P33 result)

Every one of the **30** signal-head series has the *same* consecutive observed-sample gap:

`2023-09-24T23:31:44.010Z → 2023-09-24T23:31:46.014Z`, duration **2.004s**.

There are **899** common observed timestamps, each with all 30 IDs. Thus the data show a *synchronized missing nominal 1Hz observation*, not 30 independent outages. **The raw bytes do not identify whether the cause was sensor logging, data processing, packet loss, or actual control failure**. In particular, never claim a traffic light was turned off.

Among the 30 signal heads, **three** show a different code on the two sides of that gap:
- Head **12**: code **5 (green)** → **7 (yellow)**.
- Head **20** and **21**: code **5 (green)** → **3 (red)**.

The 2.004s is the span between *sample instants*. It is **not** the duration of an unseen signal phase, nor does observing equal endpoints on the other 27 heads prove no intermediate transitions. Exact transition instants within the open/closed window cannot be inferred from these 1Hz samples. A 50ms trajectory sample in the middle does **not** restore the missing phase measurement.

The independent trajectory reader finds **40 tracked-object rows from one object ID** whose timestamps fall strictly inside this common signal-observation gap (t23:31:44.016482–23:31:45.966482 UTC). These are 40 *observed track samples*, **not** 40 distinct vehicles and **not** evidence that any particular signal head controls this object's movement. No lane/head join has been established.

### Signal classification and relation to road scene

Official P24 codebook verified codes 0–9 from the DLR documentation, but P24 also found **four live IDs (10–13) without official pole coordinates** and that static OpenDRIVE signal IDs cannot simply be equated with live IDs. The 30 ID time series therefore cannot yet be joined to specific vehicle lane/turn movements; the Go tool deliberately keeps separate signal-head and object-ID namespaces.

## Adversarial check and decision

**Data quality skeptic:** Correct total record count alone is insufficient; group gaps across sensor IDs. New synchronized gap is found and explicitly emitted.

**Causal skeptic:** A 2.004s shared sample gap does not imply a 2.004s physical red/green outage, and a sampled change does not locate the change instant. New gap output carries **head IDs** and interval bounds rather than a fabricated onset.

**Independent implementation skeptic:** Go and Python parse the original CSV separately and agree on 18 measures, including exact group gap and three changed heads. SHA locks fail closed on tampered raw bytes. Go unit tests include timestamp offset, duplicate ID time, schema tamper, invalid signal code/class, 50ms object sample validation and real-data integration.

**Action-shaping result:** Do **not** use this first 15-minute DLR window as a high-resolution lane-specific green/no-discharge causation example yet. First match official head positions and controlled movement groups, and propagate the common gap as interval uncertainty. For frame-level pairing at 50ms, require a decision-time signal observation within an explicitly justified freshness tolerance and mark samples inside the gap `UNOBSERVABLE_SIGNAL_PHASE` rather than nearest-fill without qualification.

## Return-to-origin receipt

EXPLANANDUM: Can observed signal timestamps support traffic-event evidence?
METHODS SELECTED: Observer-First Drift Audit; Exact-Runtime Certification; Bridge Intent ≠ Bridge Closure.
RAVEL-CHANGING ATTACK: Common-mode one-sample disappearance invalidates independent-head continuity assumption; 3 heads change code across gap, so time of transition remains interval-unidentified.
AUTHORITY CEILING: Raw real CSV temporal quality only, **not** causal spillback, green starvation, field signal tuning, or physical model calibration.
CORE/ENABLING/FORK: ENABLING with concrete road-world contact.
RETURN EDGE: Promote exact map-controlled movement correspondence or explicit observation-gap-censored crossing study; if no such match, demote this branch and prioritize independently calibrated SUMO/field validation.
DEBT: 1; do not stack another metadata-only enabling stage without returning to physical question.
