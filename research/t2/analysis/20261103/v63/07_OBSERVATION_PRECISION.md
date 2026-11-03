# T2 v6.3-P0 — Observation channels and quantization

Within the **15 new seeds** where both physically different v6.2 models matched on three baseline aggregate indicators, replay each baseline model with 0s guard to read the precise simulator event log. This is 30 additional synthetic simulations.

Discrimination by additional observation:
- Connector-entry vehicle count: **0/15**; side entry count 0/15.
- Exact connector entry time series: **7/15**.
- Mean connector-entry speed (rounding to 0.0001 m/s): **15/15**.
- Quantizing that mean to 0.1 m/s: **14/15**.
- Quantizing it to 0.5 m/s: **5/15**.
- Exact exit timestamps: **6/15**.
The underlying model separation in average entry speeds is only 0.0809..0.2150 m/s.

These exact numerical comparisons use synthetic event logs and fixed rounding; they do NOT include sensor sampling errors, localization bias, occlusions, or noise. Quantization outcomes depend on boundaries and true speed values; do not assume all low-precision sensors fail at the same rate. Do not claim that a single mean-speed sensor is minimally sufficient outside this selected two-model test. Next pre-specified test: noisy observations with measurement error variance, explicit cost of sensor channels, and policies judged on proper out-of-sample decision regret.
