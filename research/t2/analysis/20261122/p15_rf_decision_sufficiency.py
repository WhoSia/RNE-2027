"""P15 exact artificial label-to-decision audit, NOT a PHYS or radio experiment.

Each artificial world supplies *stipulated* costs for an identical named action
contract. This module cannot infer costs from a CSI label or control traffic.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
import json

LABELS = frozenset({'no_demand', 'free', 'pocket', 'downstream', 'both'})


def _fraction(value: object) -> Fraction:
    if type(value) is int or type(value) is Fraction:
        return Fraction(value)
    raise ValueError('costs must be exact integers or Fractions; bool/float prohibited')


@dataclass(frozen=True)
class World:
    world_id: str
    cohort: str
    arrival_group: str
    rf_label: str
    pocket_vehicles: int
    downstream_free_cells: int
    contract: str
    costs: tuple[tuple[str, Fraction], ...]
    provenance: str = 'ARTIFICIAL_FIXTURE'

    def __post_init__(self) -> None:
        for k in ('world_id', 'cohort', 'arrival_group', 'contract', 'provenance'):
            v = getattr(self, k)
            if not isinstance(v, str) or not v.strip():
                raise ValueError(f'{k} must be a nonempty string')
        if self.rf_label not in LABELS:
            raise ValueError('unrecognized staged RF class')
        for k in ('pocket_vehicles', 'downstream_free_cells'):
            v = getattr(self, k)
            if type(v) is not int or v < 0:
                raise ValueError(f'{k} must be a nonnegative integer')
        if type(self.costs) is not tuple or len(self.costs) < 2:
            raise ValueError('two or more named feasible actions required')
        names = []
        canonical = []
        for entry in self.costs:
            if type(entry) is not tuple or len(entry) != 2:
                raise ValueError('action entries must be pairs')
            name, cost = entry
            if not isinstance(name, str) or not name.strip():
                raise ValueError('invalid action name')
            names.append(name)
            canonical.append((name, _fraction(cost)))
        if len(set(names)) != len(names):
            raise ValueError('duplicate action names')
        if names != sorted(names):
            raise ValueError('actions must be sorted for immutable canonical input')
        object.__setattr__(self, 'costs', tuple(canonical))


def audit(worlds: tuple[World, ...], *, epsilon: Fraction = Fraction(5)) -> tuple[dict, ...]:
    """Audit a finite set; no probability distribution or physical validity implied.

    Separate cohorts are distinct thought experiments. Never pool action sets
    or action contracts into a false observational alias.
    """
    if type(worlds) is not tuple or any(not isinstance(w, World) for w in worlds):
        raise TypeError('worlds must be a tuple of World objects')
    eps = _fraction(epsilon)
    if eps < 0:
        raise ValueError('epsilon must be nonnegative')
    ids = [w.world_id for w in worlds]
    if len(ids) != len(set(ids)):
        raise ValueError('reused world ID')
    groups: dict[tuple, list[World]] = {}
    for w in worlds:
        actions = tuple(name for name, _ in w.costs)
        key = (w.cohort, w.rf_label, w.contract, actions)
        groups.setdefault(key, []).append(w)
    result = []
    for (cohort, label, contract, actions), rows in sorted(groups.items()):
        optima = []
        by_world = []
        for w in rows:
            costs = dict(w.costs)
            minimum = min(costs.values())
            opt = frozenset(a for a in actions if costs[a] == minimum)
            optima.append(opt)
            by_world.append((w, costs, minimum))
        common = set(actions).intersection(*optima)
        regrets = {a: max((costs[a] - best for _, costs, best in by_world)) for a in actions}
        minimax = min(regrets.values())
        robust = tuple(a for a in actions if regrets[a] == minimax)
        # Witnesses are all exact two-action sign oppositions beyond epsilon.
        witness = []
        cross_group_witness = []
        within_group_witness = []
        if 'baseline' in actions and 'treatment' in actions:
            delta = [(w.world_id, w.arrival_group,
                      costs['treatment'] - costs['baseline'])
                     for w, costs, _ in by_world]
            for (id_a, group_a, da), (id_b, group_b, db) in combinations(delta, 2):
                if (da < -eps and db > eps) or (db < -eps and da > eps):
                    pair = (id_a, id_b)
                    witness.append(pair)
                    if group_a != group_b:
                        cross_group_witness.append(pair)
                    else:
                        within_group_witness.append(pair)
        state_signatures = {(w.pocket_vehicles, w.downstream_free_cells) for w in rows}
        result.append({
            'cohort': cohort, 'rf_label': label, 'contract': contract,
            'feasible_actions': actions, 'world_count': len(rows),
            'independent_arrival_groups': len({w.arrival_group for w in rows}),
            'state_alias': len(state_signatures) > 1,
            'common_optimal_actions': tuple(sorted(common)),
            'decision_sufficient_in_enumerated_worlds': bool(common),
            'minimax_regret': str(minimax), 'minimax_actions': robust,
            'strict_opposition_pairs': tuple(witness),
            'cross_arrival_group_pairs': tuple(cross_group_witness),
            'same_arrival_group_pairs': tuple(within_group_witness),
            'epsilon': str(eps),
            'scope': 'EXACT_ARTIFICIAL_COST_FIXTURE_NOT_PHYS_NOT_CSI',
        })
    return tuple(result)


def fixed_fixtures() -> tuple[World, ...]:
    """Arbitrary costs chosen to exhibit BOTH failure and non-failure cases."""
    return (
        World('o1', 'OPPOSITION', 'clock1', 'pocket', 1, 3, 'virtual_same',
              (('baseline', 0), ('treatment', -8))),
        World('o2', 'OPPOSITION', 'clock2', 'pocket', 4, 0, 'virtual_same',
              (('baseline', 0), ('treatment', 9))),
        World('c1', 'COMMON', 'clock3', 'pocket', 1, 3, 'virtual_same',
              (('baseline', 0), ('treatment', -3))),
        World('c2', 'COMMON', 'clock4', 'pocket', 4, 0, 'virtual_same',
              (('baseline', 0), ('treatment', -1))),
        World('t1', 'TIE', 'clock5', 'both', 1, 0, 'virtual_same',
              (('baseline', 0), ('treatment', 0))),
        World('t2', 'TIE', 'clock6', 'both', 4, 0, 'virtual_same',
              (('baseline', 0), ('treatment', 2))),
    )


def report_json() -> str:
    return json.dumps(audit(fixed_fixtures()), ensure_ascii=False, indent=2) + '\n'


if __name__ == '__main__':
    print(report_json(), end='')
