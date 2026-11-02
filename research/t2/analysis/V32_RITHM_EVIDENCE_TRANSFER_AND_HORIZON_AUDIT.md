# T2 v3.1 — RITHM evidence transfer and finite-horizon audit (2026-11-02)

Re-ran archived v3.0 engine from ZIP SHA256 5202c0d346e7f464ca3b7b7e06a9ec02726cd1cf8ca92efb4a2d8e2d729376b8. All five original unit tests PASS. Added independent, non-mutating Python sweep with 288 simulations: seeds 0–3 × capacity 4/12 × main .35/.7 × side .15/.4 × horizons 450/900/1800 × fixed/coordinated/pressure. Original v3.0 engine bytes unchanged. Each run asserts vehicle conservation and link storage; fixed and coordinated identical when offset=0, identity failures=0.

Mean completed OD trips (fixed vs pressure heuristic): 450s 185.1875 vs 188.875; 900s 384.0625 vs 381.40625; 1800s 776.8125 vs 768.9375. Thus finite-horizon average rank flips in this synthetic subset, but the arrival-generation horizon changes as well; NOT a fixed-demand-cohort clearance experiment. Does NOT disprove formal max-pressure theorem.

RITHM transfer: preserved byte-exact evidence root; distinguish event time, result publication and archival receipt; type generation/crossing/OD completion/denial separately; negative evidence has scope; compare model claims to counterexamples; never infer human adaptation from aggregate traffic count. Protocol and executable CSV archive locally SHA256 d471a7f56a6e548c014e228cfd7697cc01222ba7ba6287e57ce4e348d96371aa.

Code limitations: origin0 has no side demand yet fixed-time phase wastes green; j0 boundary admits outside independently of green; current 'pressure' subtracts downstream occupancy and is not mathematically formal MP; only a single destination, no route choice or multi-destination OD matrix. Full repo parity and physical validation remain unresolved.

Next: freeze incoming cohort at 450s, run 1800s clearance, instrument every movement offer/denial and preserve ID-level immutable event log. Build independent event replayer and fix impossible first-junction phase before comparing policy superiority. GitHub Actions/bot forbidden.
