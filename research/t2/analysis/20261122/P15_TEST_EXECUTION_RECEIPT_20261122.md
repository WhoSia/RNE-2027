# P15 execution receipt — 2026-11-22 KST

Execution environment: Python 3.13.5, local isolated project workdir (not GitHub Actions and not an RF device).

Exact command:
```sh
cd research/t2/analysis/20261122
python -m unittest discover -v -p 'test_p15_rf_decision_sufficiency.py'
python p15_rf_decision_sufficiency.py > p15_rf_decision_sufficiency_results.json
```

**Final run:** 19 tests, 19 passed, 0 errors, 0 failures, in approximately 0.002 seconds.

Executed test methods:
```
test_action_order_and_duplicate_rejected
test_alias_alone_not_decision_failure
test_bool_cost_rejected
test_contracts_never_cross
test_distinct_group_count
test_duplicate_id_rejected
test_empty_and_determinism
test_epsilon_strict_border
test_feasible_action_sets_never_cross
test_float_cost_rejected
test_fraction_costs_exact
test_invalid_epsilon_and_input
test_invalid_label_rejected
test_negative_state_and_bool_rejected
test_strict_opposition_not_claimed_from_same_group_as_independent
test_three_actions_common_optimum
test_three_fixture_groups
test_ties_give_common_optimum
test_true_opposition_in_invented_costs
```

SHA-256 of the local full verbose stdout/stderr log: `1c8b434d3881b098455a216a49d4862611b3da16dd37a91bb2275bba650e6063`.

Canonical `main` blob comparisons (the exact locally executed source pair and generated JSON):
- implementation: `71ecea34e2014325ba88b8e81cae2cdf44fca92d`
- test suite: `45323d98156fefa7f5a5b41432b1c495435806c4`
- deterministic results JSON: `de1c8a3b926e70126840a286c51870eabac64b68`

Each blob was re-fetched at ref `main` and compared to `git hash-object` of the locally executed file. A standalone local ZIP preserving code, test, generated JSON, verbose run log and SHA256SUMS was created for the user's manual sharing; **that ZIP is a chat artifact, not a GitHub repo file and is not claimed to be uploaded to shared Drive**.

Scope: artificial cost-selection fixtures only; no PHYS engine execution, no RF measurement, no real signal intervention, no field calibration. `arrival_group` strings are not verified independent arrival tapes. Reviewer must still test whether the protocol is physically meaningful.
