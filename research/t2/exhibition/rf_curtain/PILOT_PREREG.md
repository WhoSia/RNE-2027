# RF-CURTAIN — Pre-registered staged exhibit feasibility study
2026-11-21 · **frozen before any project-specific CSI measurement**

## H0 / H1 / H2

H0: Under an unseen sensing layout/session, RF measurement cannot
reliably tell whether an induced lab model is empty/free, blocked
at the turn-bay entry, occupied at the downstream boundary, or both.

H1: Multiple fixed observation links retain class-specific
information across unseen sessions/placements, exceeding a
single-link RSSI-only comparison in a camera-free **toy apparatus**.

H2: Additional RF class information actually resolves at least
one ambiguity relevant to which explanation should appear on the
demo display; no automatic real-signal actuation or real-world delay
reduction is implied.

## Stage A — feasibility with NO new purchases

Before construction, inventory **available school-owned/approved
Wi-Fi devices** and determine whether they export real CSI. If only
RSSI is available, mark CSI stage **BLOCKED** rather than calling
RSSI 'CSI'. Inspect the exact chip, hardware revision, firmware and
documentation. Do not connect to unrelated Wi-Fi networks or capture
third-party MACs/frames.

Create a paper/tabletop geometry with two **longitudinal** links at
(1) the short left-turn-pocket entrance, and (2) the downstream
receiving-link boundary. The simulated 2.4GHz first-Fresnel
midpoint-disc audit is an early exclusion test, not proof of sensor
selectivity. If two links are physically indistinguishable from one
another for stationary model vehicles, report failure and stop
multi-cause classification.

No installation on public roads, no traffic-controller wiring,
no RF capture of bystanders, no students entering live roadways.

## Stage B — five physical labeled classes

Five mutually exclusive lab model truth labels, independently
assigned by an operator *before reading RF features*:

- `no_demand`: no model vehicle approaching
- `free`: model vehicle traverses unobstructed
- `pocket`: model vehicle obstructs short-pocket entrance
- `downstream`: downstream receiving section blocked
- `both`: pocket entrance AND downstream section blocked

Include **stationary** objects, moving objects, background furniture,
vehicle material variation and resets. These are controlled labels,
not verified real-world causes of queue or legal signal phases.

Stage B pilot: ≥5 repetitions × 5 labels × 2 independent setup
sessions × 2 antenna placements = ≥100 independently reset
trials if hardware available. The purpose is to check sensor
recordability, class balance and failure modes, not to publish a
cross-condition accuracy claim.

## Stage C — blinded generalization evaluation

After a successful pilot, independently collect at least
3 separately initialized sessions × 2 placements × 5 classes ×
10 resets = **300 physical trials**. Order conditions within each
session by preassigned randomization independent of RF output.

Primary holdout is placement `P2` in the most recent
session `S3`, which is not touched for feature design or
model tuning. All learned feature scaling/centroids use only
the designated training sessions under `P1`.
If too few training examples remain, report **INCONCLUSIVE**.

Compare:
1. constant majority-class baseline,
2. first-link RSSI only,
3. both-link RSSI,
4. both-link CSI summary features (only if actual CSI supported),
5. optional combined RSSI+CSI (exploratory, never primary).

**Locked metrics:** full five-class confusion matrix,
balanced accuracy, macro-F1, every class recall, class-wise
false pocket/downstream attribution, missing/abstention rate,
synchronization loss and per-event inference latency.
Never evaluate only correctly captured or visually easy samples.
Do not split frames from the same trial between train/test.
Do not reselect holdout after inspecting outcomes.

**Provisional go criterion (not statistical guarantee):**
valid frames on ≥80% of intended trials in each physical session;
CSI both-link macro-F1 ≥0.70, smallest per-class recall ≥0.50,
and improvement ≥0.10 macro-F1 over the best RSSI baseline,
all on the frozen held-out placement/session. Otherwise classify
the specific generalization claim as NOT SUPPORTED; the study can
still be a valid negative-result exhibition.

Report a cluster bootstrap over independent trial resets within
sessions if enough sessions exist, and separately disclose the
3-session limit. Do not treat packets as independent traffic scenes.

## Stage D — only after real measurements

Estimate detector errors and time lags from the laboratory data,
then input those **empirically observed estimates** into a *separate*
T2 diagnostic simulation. Observe whether cause attribution improves
the number of identifiable model states or changes regret in a
feasible abstract decision set. Do not substitute synthetic CSI for
actual radio recordings or combine field claims with toy measurements.

## Hold / stop / protection

If no CSI interface is available, remain Stage A. No purchase
authorization, no public-road installation, no modification of
traffic signals. Consent/teacher supervision required for any
experiments in school shared spaces. No bystander imaging, person
pose estimation, MAC tracking, or raw packet payload retention.

A negative result (no static-object signal, low cross-placement
accuracy, or confusion between pocket and downstream) is an
expected scientifically valuable result, not grounds to tune on
the test set.
