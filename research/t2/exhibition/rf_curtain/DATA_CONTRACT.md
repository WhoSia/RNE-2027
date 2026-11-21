# RF-CURTAIN — Measurement row, privacy and split contract

Status: **schema only; NO CSI observations acquired**.
One CSV record = one **independently reset trial**, not a single
CSI packet. Five classes (see PILOT_PREREG.md), and all measurements
must be aggregates of **our own** authorized Wi-Fi link packets.

Required columns:

| Field | Meaning |
|---|---|
| trial_id | Unique trial identifier; do not put participant names |
| session_id | Whole independently reset collection session/date |
| placement_id | Antenna geometry revision `P1`, `P2` |
| label | One of no_demand/free/pocket/downstream/both, assigned from ground truth |
| quality | `ok` or `missing`; missing trials retained as abstention, not dropped |
| ground_truth_source | `manual_model_state` or other documented safe external label |
| rssi_1_dbm, rssi_2_dbm | Mean RSSI of authorized links in dBm (trial summary) |
| csi_1_amp_dispersion, csi_2_amp_dispersion | Nonnegative dispersion of CSI amplitude across a locked subcarrier/time window, only when actual CSI exposed |

To measure CSI amplitude dispersion consistently, calibration and
sample-rate windows must be defined **before** collecting holdout
records. Do not calculate variance on a different number of packets
for different classes without documenting sample count and quality.

A `missing` record must still exist, with missing numeric values,
and must count as an abstention in test metrics. `ok` requires
all fields used by a selected model to be nonmissing and finite.
For RSSI-only baselines, missing CSI is allowed; for CSI models,
CSI absence is an abstention and cannot silently become RSSI.

No raw Wi-Fi device addresses, packet payloads, location identifiers
of bystanders, raw human pose, or unconsented recorded images.
Any ground-truth clip, if explicitly authorized, must be kept
separate and minimized. Do not upload identifiable media to GitHub.

Split in evaluation code by independent session and placement:
train on preselected `P1` sessions; test exclusively on
`P2` and `S3`; neither thresholds, centroids nor scaling
can be fit on the test set. Training coverage must contain all 5
classes; if not, the experiment is inconclusive rather than
silently dropping a class. Trial IDs may never overlap between
train and test.

The exploratory code contains a clearly marked **synthetic fixture**
for testing score calculations. It is not laboratory evidence,
does not estimate any CSI detector accuracy, and cannot be used
to populate experimental results.
