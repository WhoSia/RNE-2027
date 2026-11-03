# T2 v6.4-P0 — 20261103 custody/repro receipt

Shared Research OS Drive folder: 02_RESEARCH_LOG/20261103 김우준의 사유.
Folder: https://drive.google.com/drive/folders/1ju66sCxLLSo2Q_V3CuMg9hW1k_PCSgVd
Artifact: https://drive.google.com/file/d/1ctxqjwnmmO2mETfkz9Votize5K2Dx81f/view
Package: T2_v64_P0_field_readiness_policy_value_20261103.zip
SHA256: 4cf647fd211e1a80bf12aef5d906ddf337451d9ffa559068addad308fb6773d3
15 files: 4 Python scripts (including tests), 3 original v6.3 synthetic CSV snapshots, 2 newly generated summary CSVs, 2 methods JSONs, field protocol documentation, peer review, README, SHA manifest.
Reproduce: Python standard library: python -m unittest -q test_v64.py (8/8 passed); python observation_value.py; python policy_holdout.py.
Important denominator: 150,000 synthetic **sensor draws**, ZERO new vehicle simulation runs. Do not inflate vehicle run count.
Provenance: source CSV and transformation scripts retained. Do not create GitHub Actions[bot] commits/contributions. Full executable byte archive is Drive canonical artifact; GitHub research notes are a navigable interpretation layer until complete code sync.
