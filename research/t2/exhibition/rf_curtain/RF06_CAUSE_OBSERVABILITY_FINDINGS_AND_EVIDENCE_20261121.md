# RF06-B — Exact finite-state observation and task-specific sensor value: finding and reproducibility receipt

**Date:** 2026-11-21. **Scientific status:** MATHEMATICAL_TOY_CONFIRMED / PHYSICAL_SENSING_NOT_TESTED / T2_POLICY_NOT_TESTED.

## Provenance and frozen hypotheses

[Pre-registration before result inspection](RF06_CAUSE_OBSERVABILITY_PREREG_20261121.md), commit `b92a041b807d944cc8537d799800a073f98e2693`, specified four uniformly probable abstract microscopic states `(P,D) ∈ {00,01,10,11}`, ideal channels and exact Bayes 0/1 loss criteria. The exercise was inspired by two ORIGINAL documents now held in Research OS 10_PAPERS:
- Hu & Fan (2024), *Sensor placement considering the observability of traffic dynamics: On the algebraic and graphical perspectives*, DOI 10.1016/j.trb.2024.103057, [original PDF](https://drive.google.com/file/d/18GmpK9i-5yfnXNZzL9MImxDjLOl8PYem/view). The authors analyze traffic link-density observability using eigenstructure and graph methods; we have NOT implemented their piecewise-linear road dynamics or sensor optimizer.
- Zhang, Fakhrmoosavi & Zaghi (2026), *Information-Theoretic Traffic Sensor Placement with Graph-Based Macroscopic Traffic-State Reconstruction*, arXiv 2609.13212v2, [original PDF](https://drive.google.com/file/d/1OCDtJcGTh8Red2IlpwYFtTMnl8Bd1pBB/view). The authors investigate information/redundancy and graph-based reconstruction on a simulated Chicago network; we have NOT replayed their dataset or IGNNK implementation.

This is original *project-specific toy analysis* of an established theorem, NOT a claim to have invented observability, information theory, or first sensor-position research.

## Exact results

Define idealized observation channels: aggregate `Y=P+D`; global RF-like OR `R=P∨D` (strictly a manufactured logical bit, NOT a simulated radio channel); local ideal `S_P=P`; local ideal `S_D=D`; static motion-only `M=0`.

For the uniform four-state prior and ideal sensors, deterministic I(State;Output)=H(Output) bits. Bayes errors below assume one-shot zero-one classification of the specified target:

| Channel(s) | Mutual information about FULL state (bits) | 4-state class Bayes error | Target “is P blocked?” Bayes error |
|---|---:|---:|---:|
| aggregate Y | 1.5 | 1/4 | 1/4 |
| global OR R | 0.8112781244591328 | 1/2 | 1/4 |
| local pocket S_P | 1.0 | 1/2 | **0** |
| static motion M | 0 | 3/4 | 1/2 |
| aggregate Y + S_P | 2.0 | 0 | 0 |
| local S_P + local S_D | 2.0 | 0 | 0 |
| global OR R + local S_P | 1.5 | 1/4 | 0 |

The key exact *decision-specific* counterexample is Y vs S_P: **more bits of total state information (1.5 > 1) can yield worse prediction of the particular target P (1/4 > 0)**. In this toy there is no actual signal policy or cost model; *target prediction risk* is NOT a causal traffic-control improvement estimate. Some near-random continuous-channel RF might be much less informative than these ideal channels.

**Spatial alias:** Y=1 corresponds to both `(0,1)` and `(1,0)`; a generic queue sum loses the bottleneck source. A hypothetical perfect local sensor P combined with sum Y breaks the alias. OR+P still confuses `(1,0)` and `(1,1)`. Minimum number of listed ideal channels separating all four states is exactly **two** (three minimal pairs, in machine-readable JSON). No claim that two *real wireless links* suffice.

**Temporal observability:** for `x(t+1)=diag(a,b)x(t)` and `y(t)=[1,1]x(t)`, the 2-observation matrix `O=[[1,1],[a,b]]` has exact determinant `b-a`. With a=b=1 it is rank-deficient even with exact noiseless repeated measurements. With `a=4/5,b=81/100`, det=1/100, formally rank2 but one-step outputs for `(1,0)` vs `(0,1)` differ by only 0.01. If each measured next-step value may have unknown bounded error `epsilon>=0.005`, observation intervals overlap, so **guaranteed discrimination fails** absent more assumptions/data. For immediate two different ideal measurements Y,P the determinant is -1. These results are not a calibrated road traffic dynamic, and external inflows, realistic phase changes and measurement error require a different model.

## Execution and integrity

- [Exact source](rf_cause_observability.py), local executed Git blob `230f7aeb47a42a2b1f186ec759ff51b70f33eb0a` **matched remote main fetched SHA**.
- [Unit tests](test_rf_cause_observability.py), local executed Git blob `bad14cf674e305ce720244d22e60f5faae3724f4` **matched remote main fetched SHA**.
- Exact Python 3.13.5, `python -m unittest -v test_rf_cause_observability.py`, **11/11 tests PASS**, including uniform and asymmetric priors, sensor aliases, entropy, target-specific Bayes errors, rank/determinant, malformed inputs and deterministic JSON.
- [Machine-readable exact result](rf06_exact_observability_results.json), local SHA-256 `7653307032fc32886cd51e1947290c876305305d55a0303d6744486a4b559f35`; local Git blob `772b4f12159283600a7de5d9ba2609328daed7a4` **matched GitHub main fetched blob**.
- **Scope**: only 11 NEW RF06-B unit tests were run in this unit. Prior RF05 local 40/40 pass was from the PREVIOUS unit; do not claim 51/51 in the present checkout. The full T2 integration suite, OpenCSI hardware, and real source datasets were not exercised.

## Source-to-model boundary

The 23 newly admitted PDFs (20 sensing/traffic, 3 methodological) were read at abstract and **selected** method level and the canonical Drive parents verified; see [20-source receipt](RF06_20_PNK_INTAKE_HARVEST_RECEIPT_20261121.md) and [three-source receipt](RF06_META_METHOD_THREE_PAPERS_RECEIPT_20261121.md). Their original figures, tables, appendices and code are NOT all independently replicated. Article PDF != dataset downloaded.

Kane (2013) cautions that the use/interpretation of a score requires its own validity chain; Barr et al. (2015) explain that executing a test does not itself establish a correct answer oracle; Zave & Jackson (1997) distinguish environment/domain assumptions and software requirements. For our project the inference gates are: **raw authorized CSI → reproducible channel response → genuine physical blockage source → causally valid traffic mechanism → operationally feasible abstract action → independently justified real-world use**. Each step needs distinct evidence.

## Decision for T2 and exhibition

**ACCEPT** mathematical equivalence classes, target-specific information-vs-risk distinction, linear rank and ill-conditioning under declared inputs. **REJECT** extrapolating these numbers to RF detection F1, magnetic sensing, real intersection bottleneck causality, reduced travel time, or safe traffic signal schedules.

**NEXT GATE:** sensor design should optimize the conditional uncertainty or worst-case regret of the *specified cause/decision*, not generic CSI feature count or unconditional entropy alone. But physical sensitivity, independent lab truth labels and session×placement shifted reliability must be MEASURED first; no invented CSI distributions. Parallel T2 physical simulator remains a separate evidence stream: earlier 480 synthetic arrival-time worlds include no same-six-count policy-sign reversal proof and no operationally certified phase. `CIM dataset.zip` remains entirely **UNTOUCHED / HOLD**; no K047 unsealing and no GitHub Actions or bot commit.
