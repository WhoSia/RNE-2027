# PHYS-10 / PHYS-11 — Evidence handoff, exact-blob core and unresolved gates

2026-11-21 · R&E 2027 / T2 · canonical working branch `main`

## Research-unit scope

1. **PHYS-10**, pre-registered before running novel seeds72–79:
   576 same-state policy pairs across four moderate one-variable
   traffic demand shifts; clean, 12-second stale and correlated
   contiguous A-lane detector-occlusion readings. Result: numerous
   harmful signal actions passed a training-support OOD gate; full
   detector blackout led to unconditional abstention and loss of
   many beneficial synthetic interventions. The zero-distance
   feature alias with +306 actual cost was preserved.
2. **PHYS-11**, pre-registered before novel seeds80–87:
   backward-compatible per-vehicle consecutive eligible-gap
   confirmation feature with settings 1/2/3. 144 policy pairs
   on new simulated seeds. Default1 matches all older PHYS-04
   numeric fields; no strict policy preference reversals were
   observed across the three modified physics worlds. This is
   a legitimate **null strict-reversal finding**, not omitted data.

## Shared Drive evidence

The full ZIP was uploaded to the confirmed R&E shared Drive and its
filename, size, drive ID and parent were read back:

- [PHYS-10 / PHYS-11 exact-core evidence archive](https://drive.google.com/file/d/1mcnPyQRoSSji5bulvK0E4tXUFOXcgTTh/view?usp=drivesdk)
- Drive file ID: `1mcnPyQRoSSji5bulvK0E4tXUFOXcgTTh`.
- Parent folder: `20261121 김우준의 사유` ID
  `198h73YvJlPeBC0l3U-rar1q9zLPmsI9j`.
- Uploaded Drive size: **100,947 bytes**;
  `application/zip`; ZIP had 25 entries and passed
  the local ZIP CRC/integrity check.
- Local ZIP SHA-256:
  `60fd63225382b0294c5a34788e3ad4fdf19941311444f02e392e0e689ffcded1`.
- The upload was confirmed by metadata readback; remote bytes
  were **not** downloaded again and hashed, so do not claim a
  remote cryptographic equality seal.

Archive includes the exact five-module core, new experiment
runners and regression tests, the original PHYS-04 training
dataset, prior PHYS-07/08/09 outputs, new PHYS-10/11 full JSON
outputs and an individual-file SHA-256/Git-blob manifest.
Source filenames may be reconstructed from the ZIP's README;
no external Python package is needed for the core execution.

## Verified code identities

The canonical traffic engine with PHYS-11 is GitHub exact blob
`6c18490c42f63e65dc830ad60839c19008b8d647`.
Four imported modules also have exact GitHub-local byte identity:
`spatial_v10.py` `ffbf3fc3f8b9a64a819d4f73ce70b264b877e84e`,
`receiving_cells_v15.py` `b078cf215c74b76ace6dffcbcbacab6ae22c3673`,
`physical_transfer_screen.py` `8d75745053ff720db6c8af0001aaaf13ba1f295e`,
`physical_checkpoint_observation_ablation.py`
`db9ceb2774ee1b7e70728a340b50d41f4c884c18`.

New GitHub-versus-execution blob identities:
- PHYS-10 runner: `459e11987b0fc423f26f96e1aff0adf42c0f7cd6`.
- PHYS-10 tests: `1d06d7e2fd6aaabc35818ec7df8b76e619f86a15`.
- PHYS-11 runner: `2ef0bd3996e06c47152ee410b086bb67b3de2659`.
- PHYS-11 engine tests: `b0facd25654a5396500ad32dd4db29e64cc15f91`.
- PHYS-11 prospective-result tests:
  `e9df217a0e0ac2fa7fff59a29dc3ccc33e87c486`.

## Actual Python checks

Python **3.13.5** in a local isolated container, PYTHONPATH set
to the SHA-verified core and exact experiment scripts.

- **PHYS-04**: 144 direct-vs-restarted baselines and 1,872/1,872
  independent-reference fields agree with original results after
  adding PHYS-11's default=1 field. Old 144-case JSON SHA-256
  `0d91beab746b8e67bf1fa5ea327e3c982d10e39b57cd5cf2fef020ad328e1001`.
- **PHYS-07/08/09**: rerun using the five-module exact core,
  prior saved full JSON byte equality. PHYS-10's full output
  also rerun using both the pre- and post-PHYS-11 engine
  (default=1), with identical bytes.
- **PHYS-10**: 576 paired cases; full JSON twice byte-identical:
  SHA-256 `ebd182b7c18d684cde6072557298943dc1480cdc15d6e8508ce032411f22cb8b`.
- **PHYS-11**: 144 paired cases; full JSON twice byte-identical:
  SHA-256 `d27a58af091952458032ddcd4f25cc36e3ab4cb1d0dbcf4c159f0d0ee958c84c`.
- **34/34** committed PHYS-07/08/09/10/11 local test methods
  passed; eight additional local core contract checks passed.
  This statement is **not** an assertion about every historical
  repository test.

## Running the archive

After extracting the ZIP in a clean Python 3.13 environment:

```sh
PYTHONPATH=core:scripts python scripts/physical_checkpoint_near_support.py input/PHYS04_training_144.json /tmp/phys10.json
PYTHONPATH=core:scripts python scripts/physical_checkpoint_gap_confirmation_screen.py /tmp/phys11.json
PYTHONPATH=core:scripts python -m unittest discover -s scripts -p 'test_physical_checkpoint_*.py' -v
```

**Outstanding reproducibility gate:** obtain an authenticated full
GitHub clone and record its tree/head SHA; execute the entire historical
704-case and integration regression suite. Our verification closure is
the named exact-blob files, not the entire repository. GitHub Actions
and `github-actions[bot]` were not used. K047 remains sealed.

**Scientific limitation:** all numeric effects are consequences of an
uncalibrated synthetic cell traffic simulator with privileged
model-internal observations and incomplete physics. They do
not establish observed human gap acceptance, legally compliant
signal control, field travel time improvement or road safety.
