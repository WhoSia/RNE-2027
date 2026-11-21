# PHYS-04 / 05 / 05b / 06 — Evidence handoff and verification ledger

Date: 2026-11-21 · Branch: `main` · Project: R&E 2027 / T2

## Shared Drive raw archive

Uploaded into the verified R&E shared Drive, inside
`20261121 김우준의 사유`:

[T2_PHYS04_05_05b_06_20261121_Research_Bundle.zip](https://drive.google.com/file/d/1nIHmzoz0Yk3YUqaaxvbBWH7ztgR2ddo-/view?usp=drivesdk)

- Drive file ID: `1nIHmzoz0Yk3YUqaaxvbBWH7ztgR2ddo-`
- Parent folder ID: `198h73YvJlPeBC0l3U-rar1q9zLPmsI9j`
- Drive metadata readback: `application/zip`, 52,090 bytes
- Local ZIP SHA-256: `7f7eff90b83cfe5e1f071bb02d5880face9c0e047abcd17349cd3fb06392758e`
- Includes 20 members (source-derived Python files, independent
  reference, all numeric JSON results, SHA manifest, README).
- ZIP integrity check returned no invalid members.
- **Drive metadata was verified, but the uploaded bytes were not
  re-downloaded and cryptographically compared.** Do not conflate the
  local ZIP digest with an authenticated remote-byte digest.

## Local execution outputs

| Experiment | Unit | Local result SHA-256 | Local executed status |
|---|---|---|---|
| PHYS-04 | 144 policy pairs, 1,872 reference field matches | `0d91beab746b8e67bf1fa5ea327e3c982d10e39b57cd5cf2fef020ad328e1001` | PASS in source-derived local runtime |
| PHYS-05 | 144 leave-one-seed-out policy decisions | `a381cdbbb4a136e36b5d59f148dbf54c37e88ba69b50a1e12871ae2233ca11fe` | RUN |
| PHYS-05 holdout | 432 unseen-seed policy pairs | `843bda4a78980dcae0dda168e67cf1bd318dd5c3dc2c856e676a55a52c921572` | RUN; byte-identical double replay |
| PHYS-05b | frozen-policy observation corruption (8 replicates per noisy scenario) | `309ad56f67946519127bdeb7cdca6b3b4883a6179058e4119ec40f4f2cf42a98` | RUN; byte-identical double replay |
| PHYS-06 | 144 gap sensitivity policy pairs | `6ca2b75720fae789c752718cae2b8cf01f35a30fe8cb84a229337057dc8aac39` | RUN; byte-identical double replay |

The Python code underlying the local outputs is **manually
source-derived from the connector-readable GitHub files**, with
reconstructed imports. No exact-blob GitHub checkout could be
established in the container, so results are *not* a final clean
canonical engine certification. No GitHub Actions, scheduled
background execution or private holdout K047 release occurred.

## Required final verification gate

1. Make a clean exact Git checkout of `main` and record HEAD and Python version.
2. Run committed unit tests, including pickle-based checkpoint stability
   tests, target-gap parameter tests and observation/noise contracts.
3. Generate `physical_checkpoint_capacity_screen.py` output and check
   144/144 keys with `compare_physical_checkpoint_reference.py`,
   using the ZIP's three independent reference JSONs.
4. Generate PHYS-05 exploratory, PHYS-05 holdout, PHYS-05b corruption
   and PHYS-06 gap outputs in that checkout; compare all result fields
   and byte-identical reruns; investigate any deviations.
5. Independently verify the Drive ZIP SHA-256 after a fresh download
   if labeling it a remote cryptographic seal.
6. Advance to K047 only after separately approved holdout release
   procedures, never via informal exploratory reuse.

## Canonical research notes

- [PHYS-04 checkpoint parity](PHYS_04_LOCAL_PARITY_AND_CHECKPOINT_TESTS.md)
- [PHYS-05 observation and unseen seeds](PHYS_05_OBSERVATION_ABLATION_AND_NEW_SEED_HOLDOUT.md)
- [PHYS-05b synthetic detector corruption](PHYS_05B_DETECTOR_ERROR_FALSIFICATION.md)
- [PHYS-06 lane clearance sensitivity](PHYS_06_TARGET_LANE_CLEARANCE_SENSITIVITY.md)
