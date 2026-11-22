"""Independent confirmation of dropping the arrival-family sensor."""
import json
from p59_policy_breadth import experiment

data = experiment(range(401, 425))
rows = data['rows']
stats = {}
for name in ('fixed', 'always', 'calendar_capacity', 'with_family'):
    selected = [r for r in rows if name == 'always' or
                (name in ('calendar_capacity', 'with_family') and r['capacity'] == 4
                 and r['offset'] == 15 and (name == 'calendar_capacity' or r['family'] == 'platoon4'))]
    stats[name] = dict(n=len(selected), total=sum(r['delta60'] for r in selected),
                       better=sum(r['delta60'] < 0 for r in selected),
                       worse=sum(r['delta60'] > 0 for r in selected))
print(json.dumps(dict(stats=stats, tapes=data['tapes'], rows=rows), indent=2))
