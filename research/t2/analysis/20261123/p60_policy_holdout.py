"""Evaluate the P59 rule on fresh tapes without retuning."""
import json
from p59_policy_breadth import experiment


def evaluate():
    rows = experiment(range(301, 325))['rows']
    for row in rows:
        row['extend'] = (row['family'] == 'platoon4' and
                         row['capacity'] == 4 and row['offset'] == 15)
    stats = {}
    for name, chosen in [('fixed', []), ('always', rows),
                         ('conditional', [r for r in rows if r['extend']])]:
        stats[name] = dict(extensions=len(chosen), wins=sum(r['delta60'] < 0 for r in chosen),
                           losses=sum(r['delta60'] > 0 for r in chosen),
                           cost_delta=sum(r['delta60'] for r in chosen))
    return dict(rows=rows, stats=stats, tapes=len({r['tape'] for r in rows}))


if __name__ == '__main__':
    print(json.dumps(evaluate(), indent=2))
