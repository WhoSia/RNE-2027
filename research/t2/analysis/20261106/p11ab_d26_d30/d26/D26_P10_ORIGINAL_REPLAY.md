# D26 — Original P10 causal event replay: PASS, bounded scope

Date: 2026-11-06. Original files obtained from the R&E 2027 shared Drive, **not recreated from memory**.

- Original P10 ZIP `sources/P10_20261104_original.zip` SHA256 `9fa06146b781bcbbd1f5e19dc25b277e1e98c695b13e61fc0b291b58cd53b59c` (verified against sealed receipt).
- Original linked P9 ZIP `sources/P9_20261104_original.zip` SHA256 `3f5dbf4d81756208e1a5c46e4906a32b95fe50ac0a61e4f142ba39097c2139bd`.
- P2 `reference/T2_v69_P2/corridor.py` SHA256 `12987786fb36409a272a50233c12c006d0a23d5f75a5487be68d51392c4614cc` (matches P10 receipt).
- Exact archival `p10_boundary_trace.py` and `p10_capacity_ablation.py` were executed with the unchanged P2 source. Original `test_p10_mechanism.py`: **8/8 pass**.
- Byte-for-byte equality with original P10 ZIP output: `boundary_trace.csv`, `boundary_mechanism.json`, `capacity_gate_ablation.csv` **3/3**.

Mechanism: `upstream_peak`, storage 18m, seed223, `(24,24,24)`, vehicle8 last-side-entry 47.1625s. Original dt0.5: vehicle1 receive at47.50s, vehicle8 connector at47.00s (retroactive). Original dt0.25: 87.25s vehicle8 connector. Patched capacity-time-gate dt0.5: 88.0s. This **fixes the specific source backdating witness only**; at other dt values, the side-phase boundary remains sensitive. No complete causal time semantics proof, convergence certification, SUMO reproduction, or field validation.

Reproduce from extracted project root:
`PYTHONPATH="$PWD/d26_p9/code:$PWD/d26_p9/reference/T2_v69_P2:$PWD/d26_p10" python -m unittest discover -s d26_p10 -p test_p10_mechanism.py -v`

**Important:** The archived, original source has been copied intact. We did not modify the original P2 or P10 ZIP. Changes for new micro reference are isolated under `src/`.
