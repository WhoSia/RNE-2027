"""Compare a fixed downstream closure with its open-gate counterfactual.

This audit attributes *excess* unadmitted source demand to the closure under
identical model parameters. It does not infer a real-world causal effect.
"""
from dataclasses import dataclass, replace
from math import isfinite

from .cell_link_model import Config, simulate


@dataclass(frozen=True)
class PairedSummary:
    first_any_source_queue_s: float | None
    first_excess_source_queue_s: float | None
    max_excess_source_queue_veh: float
    final_excess_source_queue_veh: float
    final_departure_deficit_veh: float
    max_flow_conservation_residual: float


def compare(config: Config, tolerance: float = 1e-9) -> tuple[PairedSummary, list[dict]]:
    if not isfinite(tolerance) or tolerance < 0:
        raise ValueError('tolerance must be finite and nonnegative')
    treatment = simulate(config)
    reference = simulate(replace(config, downstream_closed_until_s=0.))
    pairs = []
    for closed, open_gate in zip(treatment['rows'], reference['rows'], strict=True):
        excess = closed['source_queue_veh'] - open_gate['source_queue_veh']
        depart_deficit = open_gate['cumulative_departed_veh'] - closed['cumulative_departed_veh']
        internal_difference = open_gate['in_network_veh'] - closed['in_network_veh']
        # Conservation in both worlds implies this signed balance exactly.
        residual = excess - (depart_deficit + internal_difference)
        pairs.append({
            't_end_s': closed['t_end_s'],
            'source_queue_closed_veh': closed['source_queue_veh'],
            'source_queue_open_veh': open_gate['source_queue_veh'],
            'excess_source_queue_veh': excess,
            'departure_deficit_veh': depart_deficit,
            'mass_balance_residual': residual,
        })
    first_queue = next((p['t_end_s'] for p in pairs if p['source_queue_closed_veh'] > tolerance), None)
    first_excess = next((p['t_end_s'] for p in pairs if p['excess_source_queue_veh'] > tolerance), None)
    return PairedSummary(
        first_any_source_queue_s=first_queue,
        first_excess_source_queue_s=first_excess,
        max_excess_source_queue_veh=max(p['excess_source_queue_veh'] for p in pairs),
        final_excess_source_queue_veh=pairs[-1]['excess_source_queue_veh'],
        final_departure_deficit_veh=pairs[-1]['departure_deficit_veh'],
        max_flow_conservation_residual=max(abs(p['mass_balance_residual']) for p in pairs),
    ), pairs
