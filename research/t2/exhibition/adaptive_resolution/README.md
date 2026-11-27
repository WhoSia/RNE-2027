# Adaptive Resolution Lab — R&D software prototype

**Status: laboratory-model demonstration only. No actual road-signal control, RF measurements, field efficacy, or student-independent acceptance.**

This vertical slice connects the H08H/T180/T181 mathematical results to an executable, replaceable set of components. A shared FIFO queue with two finite pockets has a known probabilistic model, an initial observation class of four possible arrangements of three S and one L vehicle, and four abstract stages. Service may be fixed or fluctuate between 1 and 2 slots. Free queue counts may be erased, while pocket occupancy remains exactly known. Paid head/full observations are idealized, exact, and optional in a known schedule. Every path is constrained to the same maximum acquisition-credit budget; head costs 1 credit, full 4; 1 credit costs 1/64 in the abstract objective. Equal maximum budget does not imply equal realized expenditure.

## Run

Python 3.11+ standard library suffices for the solver. From this directory:

```sh
python -m unittest -v test_lab test_session test_certify test_lazy
python run.py > results.json
python benchmark.py > benchmark_results.json
python audit_mismatch.py > mismatch_results.json
python run_auto.py > auto_results.json
python run_lazy.py > lazy_results.json
python build_demo.py
```

Open `adaptive_resolution_demo.html` locally in a browser. It is a standalone viewer/replay over the 32 computed contexts and seven policy choices, not a live optimizer. The source template and generator are provided. Optional `python test_browser.py` needs Python Playwright and Chromium; adapt the executable path if required. In the test environment file-URL navigation was blocked, so the test loaded the exact HTML text into Chromium; desktop/mobile DOM interactions and screenshots were inspected. The first responsive layout overflowed the mobile viewport and was repaired. The final generated HTML is a Drive/ZIP artifact, not a large Git blob. 

## Module contract

- `model.py`: exact transition, observation and posterior mass, conservation; observation erasure is not a misclassification model. Service realization is hidden from policy but actual stock cost is evaluated. Model geometry is fixed within a trial.
- `planner.py`: exact rational finite-horizon belief DP, rolling depth, fixed ambiguity baselines, hard path budget, fully observed relaxation, actual policy evaluation.
- `trace.py`: evaluator-only physical state and event streams; exhaustive event-tree expectation independent of policy-value recursion but sharing policy and transition functions, not a separate optimizer.
- `session.py`: observation-only interface. Sequential stage request → measurement if needed → decision → next observation. Credits reserved when requested; unsupported observations and out-of-order calls abstain without emitting a subsequent action. Does not authenticate sensors, establish wall-clock freshness, or recover from model mismatch. No actuators.
- `certify.py`, `lazy_certificate.py`: anytime lower/upper bound selection; latter checks incumbent before evaluating a newly planned policy. It retains only evaluated feasible policies as upper bounds; depth cap is not a certificate.
- `run.py`, `benchmark.py`, `audit_mismatch.py`, `run_auto.py`, `run_lazy.py`: experiments and cold timing. JSONs are model outputs, not measured traffic. Timing is local Python wall-clock, 7 randomized repeats, includes tail and policy evaluation, excludes startup/UI, not a deployment benchmark.

## Student/teacher acceptance (not yet performed)

Two students independently derive the H08H four-state class, compute cost on fixed arrival cards, record answers before revealing the automatic key, and explain why missing observation is not zero traffic. A teacher-approved tabletop exercise can compare identical arrangements and arrival cards under two observation schedules and hard credit budgets. Record observed counts, actual array and decision separately; if disagreement occurs, preserve both labels and abstain. No public-road changes or unauthorized sensing. AI-produced code and student contributions must be described separately. Existing T2 field analysis and RF-CURTAIN remain distinct; ingest sensor errors only after valid independent measurement. The demonstration is useful even if the optional hardware track fails.

## Next R&D gates

1. Extend from one witness to preregistered diverse initial distributions and independent physical model, then quantify average and tail gains against strong equal-capacity / equal-budget baselines. Do not optimize only a rare witness.
2. Add alternative traffic objectives (movement equity, terminal queue, deadline, demand service) and transparent weights/constraints; no live signal plan claims. Evaluate tradeoffs, not a single flattering metric.
3. Add estimated observation likelihood, timestamps/age, and support/uncertainty diagnostics; use separately labeled observations, not assumed real error rates. Reject unsupported inputs; a broad model's zero observed abort does not establish safety or correctness under arbitrary mismatch.
4. Measure full computational overhead, cache/memory cost and Pareto curves. Lazy certification improves two measured contexts but not all; preserve slower cases. Stop feature additions until student reproduction and independently measured input are available.
