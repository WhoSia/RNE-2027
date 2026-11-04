# P3 reproducibility and custody

Shared Research OS: 02_RESEARCH_LOG / 20261104 김우준의 사유. ZIP filename T2_v67_P3_signal_vehicle_integration_20261104.zip. The ZIP holds original P1a and P1b Python sources, new timeline contract, P3 engine and deterministic generator, baseline runner, unit tests, 36 matched replays, 24 stress runs, raw CSV, reviewer notes, and SHA-256 manifest.

Run after extraction: python build_p3.py; python -m unittest -q test_signal_contract test_replay_regression; python replay_three.py; python stress_signal_p3.py. Run historical tests separately within legacy/A and legacy/B. The GitHub research notes are NOT complete executable-source synchronization; complete bytes are in dated Drive ZIP.

Status P3-HOLD, not safe real-road controller, no calibrated physical parameters, no 3-junction production corridor integration.