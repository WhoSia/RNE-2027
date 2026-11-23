"""Quantify interval widths against a four-second intervention."""
import json
from pathlib import Path

audit = json.loads((Path(__file__).resolve().parents[2] /
                    'data/20261117_jinju/audit.json').read_text())
widths = {int(k): v for k, v in audit['recorded_elapsed_seconds'].items()}
assert sum(widths.values()) == audit['rows']
print(json.dumps(dict(source_sha256=audit['sha256'], rows=audit['rows'],
                      zero=widths.get(0, 0),
                      positive_at_most_four=sum(v for k,v in widths.items() if 0 < k <= 4),
                      over_four=sum(v for k,v in widths.items() if k > 4),
                      site_labels=audit['site_labels']), indent=2))
