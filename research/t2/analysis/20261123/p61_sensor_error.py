"""Expected cost when a binary arrival-family label has symmetric error."""
import json
from pathlib import Path

rows = json.loads(Path(__file__).with_name('P60_RESULT.json').read_text())['rows']
eligible = [r for r in rows if r['capacity'] == 4 and r['offset'] == 15]
correct = sum(r['delta60'] for r in eligible if r['family'] == 'platoon4')
flipped = sum(r['delta60'] for r in eligible if r['family'] == 'uniform')
print(json.dumps([dict(error=e, expected_delta=(1-e)*correct + e*flipped)
                  for e in (0, .1, .25, .5, 1)], indent=2))
