# P12 — Implementation receipt with open exact-execution gate

Date 2026-11-21. This receipt is **not** an executed policy-simulation result.

## Canonical GitHub main artifacts
- Pre-implementation design: `T2_P12_ACTION_FEASIBILITY_PREREG_20261121.md`, blob `f253a1b5bdb2a32d1ea6d86fd7bf19ba93ddf8a5`
- Harvest transfer: `T2_P12_HARVEST_DECISION_BRIDGE_20261121.md`, blob `cb4ee3018c10719b00b25ed2353ed3df36023dd7`
- Implementation: `t2_p12_phase_contract.py`, blob `f5a0e37c27fb041d80cffee6de16dea9235d748d`
- 15 independently named unittest methods: `test_t2_p12_phase_contract.py`, blob `52e8aeda41e3075ba9e02420d8335d14bc91eb42`

The four files were re-fetched using the GitHub connector with explicit ref `main`. This establishes the uploaded file versions; it does **not** establish that tests were run.

## Expected contract distinctions
- An invented minimum green of 6 ticks rejects a 4-tick left service.
- An invented minimum of 4 ticks does not reject the service **on minimum green alone**.
- A movement change demands explicit invented yellow/red clearance fields; an abstract label '-' cannot stand for yellow.
- Pedestrian clearance is checked under the stipulated toy inequality. No pedestrian conflicts or controller ring-barrier logic are modeled.

## Verification
`python -m unittest -v test_t2_p12_phase_contract.py` in the named directory is **NOT RUN on the fetched canonical sources**. An attempt to retrieve raw public GitHub bytes in the local execution environment failed with DNS resolution error, so test execution was not silently inferred.

Next: obtain an authenticated exact-byte checkout, run 15 test methods, add a real run log and SHA. Any later failure must be fixed and the receipt revised. No GH Actions/bot, no road controller, no assertion of Korean legal compliance.

## Correction within this research unit
The first source iteration did not reject consecutive duplicate movement stages despite the design contract. An explicit guard was added and two regression cases cover adjacent duplicates and a single-stage cyclic non-duplicate. This restriction is a model simplification, not a general statement that real signal controllers cannot reuse phases. Source commit `7e13b3e3986e01b586d5cda23a81cde53e4e2579`; test commit `7d57a473e8e94418c5f7a1fdc2b3d4e2686d9354`. Both revised files were fetched from `main`. The 15 tests remain **NOT EXECUTED** in the authenticated exact-source runtime.
