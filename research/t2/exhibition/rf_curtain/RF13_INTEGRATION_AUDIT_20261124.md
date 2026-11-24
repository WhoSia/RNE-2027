# RF13 integration audit (2026-11-24)
Source: RF10 blob 4d5bf2e6b99e9ee0e5d128df2ea120a0678a590c; RF05 crossed evaluator 961ef22561eb72dbb381d1d0dea3019827efa292; pilot evaluator 3ed96b70c8b8569424480c0ba12940d07ee8266f.
All scores are editorial, P144 weights I/V/F/R/C, each 0..5.
- Separate analyst features and private truth until prediction lock: 5/5/4/5/4 = 94. Implement independent synthetic-only join contract first.
- Preserve entire planned denominator, including both-link missing trials: 5/5/4.5/5/4 = 96. Reject missing IDs rather than silently dropping.
- Report common-support vs sensor-specific availability separately: 5/5/4/4.5/4 = 92.5. Preserve RF05 original metric as legacy; do not retroactively change its gate.
- Keep reserve out of training, prediction and quality gating: 5/5/4/5/4 = 94. Current RF05 session_quality reads reserve quality, so reserve can influence eligibility even without fitting. New protocol must separate reserve before analysis.
- Actual RF measurement 0; hardware authorization and source profile still required. SUMO parity remains unresolved.
RF10 exports labels along with features; RF05 accepts labelled holdouts. No claim of operational blind isolation. Future pipeline requires independent operator custody and prediction freeze, not simply a checksum generated after viewing labels.
