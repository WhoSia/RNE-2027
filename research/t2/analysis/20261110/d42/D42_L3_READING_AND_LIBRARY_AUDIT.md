# D42-L3 | 2026-11-10 — New paper intake, direct reading and novelty gate

## Corrected inventory (actual Drive files)
Eight user-uploaded T2 originals were detected in Research OS `00_INTAKE`. Each paper's body and bibliography were checked before **rename+move with the original Drive file ID preserved** into canonical `10_PAPERS`:

|Paper|Original ID|Reading/metadata status|
|---|---|---|
|Lighthill & Whitham 1955, *On Kinematic Waves II*|1ojhVinBiW4UBUa-S-KGHK7CkNnzAxw0e|Body, controlled-junction limitation checked|
|Richards 1956, *Shock Waves on the Highway*|1edTpArBeQCm3FMnlrjOx4r8U04EpzDPs|12-page scanned PDF; page 3 and 7 rendered visually; text extraction inadequate; remaining full-page transcription not claimed|
|Newell 1993, *A Simplified Theory of Kinematic Waves I*|1tCZ4fja6JGYVKdXYCj0PQMZuv7h22Dhu|Body, lower-envelope cumulative count formulation checked|
|Tampère et al. 2011, first-order node models|1yEbxz7-us7MkMYmxULtItrwCgUy6Ojo_|Abstract+conclusions, supply/demand/conservation/SCIR checked|
|Grégoire et al. 2015, capacity-aware backpressure|1zBez5spAY8un4rHlPIxfgED2jOnq8Ycy|Body+conclusion, finite-storage non-work-conservation checked|
|Wang, Huang & Lo 2020, shockwave+recursive BN|1dYxUA2LCWhrsFV6WmlhvlmvTqGXQaZnc|Abstract+conclusion, EM/PF and residual queues checked|
|Yang, Yang & Du 2024, trajectory shockwave speed|1bLRPdsG7BPJEmoxU0VW9F8I-aT1dnXEW|Body+conclusion, FFT/turning-point/DBSCAN/L1 regression checked|
|Wang et al. 2024, low-penetration signal optimization|1-B2MU1y-7eJtXe-lxf42NNFdAqCxsf4D|Body, Newellian probabilistic time-space diagram and real-world limits checked|

Each file now has its first-author (year) — exact title — journal/bibliography — DOI standardized filename. No file content was changed. Source folder `1MLtYh0pv8QUZDReYzRqjDrOjRkSJAD16` and destination `1D2M4LHcejREhlyp6vTd71xxLLx-6ldUP`.

**Remaining six title-search-missing candidates, NOT independently proven absent:** Han et al. 2024 field-tested spillover, You et al. 2026 LPR spillover, Xiang/Xu/Yan 2022 queue estimation, Wang et al. 2025 shockwave conflicts, Krauß 1998 dissertation, Luo 2023 probe-based queue estimates.

## Actual implications for T2

- **Traffic-wave baseline:** LWR conservation law `∂t k + ∂x Q(k) = 0`; Richards' particular linear speed-density model `V = c(1-d)` leads to `F = c Dmax d(1-d)`. This is a *model assumption*, not universally calibrated field physics. Newell's cumulative `A(x,t)` has a lower-envelope selection rule for shocks. Build interval-censored in/out count envelopes from *verified* stopline events before interpreting queue-tail speed.
- **Node-model contract:** Tampère et al. require flow maximization, nonnegative flows, conservation, demand/supply limits, turn fractions and invariance; they leave complex node supply constraints as work for later. Do not code a toy junction with unrealistic movement priorities and claim independent ground truth.
- **Known capacity failure:** Grégoire et al. already showed that infinite-buffer backpressure can be non-work-conserving with bounded queues and proposed normalized pressure, so neither phenomenon is novel to our R&E.
- **Strong empirical alternatives:** Wang et al. (2020) do shockwave+three-layer recursive Bayesian network with EM and particle filtering to infer residual queues and volume; Yang et al. (2024) do FFT+DBSCAN+robust-regression shockwaves on NGSIM highway data; Wang et al. (2024) do Newellian stochastic point-queue and city-scale signal retiming on sparse trajectories. Do not claim 'first trajectory reconstruction' or 'first shockwave uncertainty analysis'.
- **More defensible research direction:** quantify how *publisher traffic count bin origin, finite lane-specific stopline geometry, censored 20Hz trajectories, physical braking and numerical event timing* affect the **credibility of traffic-signal policy ranking**. Current D42 45-min ±1-s matches are same-sensor-lineage internal checks, not a validated policy experiment.

Full direct-reading notes and corrected six-item missing-candidate register:
https://docs.google.com/document/d/1hACtEeWhYBIpqTFCAZQmXmd2JkkJTDgktNjXnrI0-TA/edit
Daily T2 research ledger:
https://docs.google.com/document/d/1fkzetvDIyGTho0wyccceYvFhUvB5ZPtPAMhjmJK9DH8/edit

**Next experiment acceptance:** compute frozen DLR lane geometry/track→turn labels without fitting counts, preserve UNKNOWN, derive Newell cumulative curves only from admissible gate events; validate D44 stopping constraints against a separate microscopic reference and pinned SUMO.
