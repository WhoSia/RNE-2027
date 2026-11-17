from unittest import TestCase
from collections import Counter

from daypart_decision import experiment
from daypart_scenarios import BASELINE, COUNTS, plans, worlds
from receiving_diagnostics import assess
from signal_model import run


class DaypartDecisionTest(TestCase):
    def test_paired_worlds_keep_counts_comparable(self):
        cases = tuple(worlds(17))
        assert len(cases) == 12
        assert len(plans()) == len(set(plans())) == 18
        assert {p.cycle for p in plans()} == {84}
        for open_case, tight_case in zip(cases[::2], cases[1::2]):
            arrivals = open_case.scenario.arrivals
            assert arrivals == tight_case.scenario.arrivals
            assert tuple(Counter(m for _, m in arrivals)[m] for m in range(7)) == COUNTS[open_case.band]

    def test_observed_components_reconcile_with_engine_score(self):
        for w in worlds(23):
            s = w.scenario
            row = assess(BASELINE, s)
            outcome = run(BASELINE, s, fast=True)
            assert row["vehicle_time_area"] + row["pedestrian_wait_area"] == outcome.area
            assert row["cost"] == outcome.cost == outcome.area + s.terminal * sum(outcome.remaining)

    def test_saved_formulation_distinguishes_cost_and_regret(self):
        result = experiment()
        assert result["train_seed"] != result["evaluation_seed"]
        assert all(p["regret"] >= 0 for w in result["worlds"].values() for p in w["policies"].values())
        summary = result["summary"]
        assert summary["band_minimax_regret"]["worst_regret"] < summary["pooled_minimax_regret"]["worst_regret"]
        assert summary["band_minimax_regret"]["worst_cost"] > summary["pooled_minimax_cost"]["worst_cost"]
        assert any(w["policies"]["fixed_baseline"]["downstream_blocked_opportunities"] > 0
                   for w in result["worlds"].values())
