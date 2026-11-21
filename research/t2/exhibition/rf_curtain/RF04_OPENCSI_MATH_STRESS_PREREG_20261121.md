# RF04-B — Prior-registered math stress tests of OpenCSI-style calibration

Dated 2026-11-21, BEFORE writing executable stress runner. **Analytic synthetic input ONLY; no captured CSI / measured driver or passenger data.**

## Literature basis and deliberate simplification
Khamaisi, Sigg & Rodrigues (2026) OpenCSI arXiv 2607.26665v2, [original PDF](https://drive.google.com/file/d/1rqlZxB_wmDxYrpF6o28KeLJwE17qcSyw/view), uses quiet-period Welford mean and standard deviation of per-link CSI amplitude and z=|mean_amplitude-mu|/sigma, maturity and reliability tags. Real paper includes packet parsing, AGC / phase sanitization, outlier rejection, automatic quiet detection, bootstrap (120s), reanchoring (~30s), chip/room evaluations. **NONE of those full features are implemented in this mathematics pilot.**

This unit models one scalar mean amplitude per time step, known-empty calibration explicitly labeled by an external operator, a sample-standard-deviation Welford accumulator and a conservative abstention for insufficient calibration or near-zero variance. No learned training labels or real radio recordings.

## Locked tests before implementation
- **H1 exact affine gain invariance**: transform both quiet calibration inputs and later reading by y=a*x+b, with a>0, and check mathematically identical z (floating tolerance 1e-12). This is a property of scalar normalization, NOT measured hardware robustness.
- **H2 additive noise/variance change breaks transfer**: baseline x=(9,10,11,10,10), event=13, threshold=3; increase baseline variance by changing quiet values while keeping its mean 10 and event 13, and demonstrate lower z / potential class flip. Numerical illustration only.
- **H3 occupied-bootstrap contamination**: baseline trained on values near 13 instead of known-empty values near 10, later event13 returns z approximately 0 and is classified negative or unresolved even if the true state is occupied. Not a field false-negative rate.
- **H4 stale quiet baseline**: quiet drift without changed true occupancy can make z exceed the fixed threshold, a possible false alert.
- **H5 invalid and missing signal**: fewer than 3 known-empty samples, no quiet bootstrap, zero variance, NaN/Inf readings must fail with explicit abstention or input rejection, never an invented confident class.
- **H6 two-zone information**: identical one-link scalar z for different physical causes cannot justify choosing 'pocket' versus 'downstream'; separately test missing-link abstention and carry two link scores with source IDs.

## Exact artificial fixtures
- Original quiet stream [9,10,11,10,10], occupied reading 13, threshold 3, sample std ddof=1.
- Affine gain (a=2,b=7) applied to all 5 empty readings and occupied event.
- Variance-amplified quiet stream [8,10,12,10,10] against same event13.
- Occupied baseline [12,13,14,13,13] and later occupied13.
- Drifted empty measurement 14 against original quiet stream.
- Zero-variance stream [10,10,10,10,10], missing/NaN tests.

No parameter search, feature selection or architecture tuning will be performed after viewing these fixture outcomes; even a complete pass demonstrates only expected algebra and robustness coding.

## Decision boundary
If any test fails: fix implementation or downgrade. If all pass: **ACCEPT MATH CONTRACT ONLY**. Measured CSI collection, independent mounting positions, physical truth and full OpenCSI implementation remain **OPEN**. Never transform this into an actual Wi-Fi detector success or road signal action recommendation.

Follow-up: independent, consented school-lab measurements and two-region spatial attribution, frozen cross-day and cross-placement test. K047 sealed; no GitHub Actions.
