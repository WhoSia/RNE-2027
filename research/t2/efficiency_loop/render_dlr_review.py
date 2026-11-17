"""Combine the offline review template and blinded replay payload."""
import argparse
import json
from pathlib import Path

MARKER = "__K047_REPLAY_DATA__"
TEMPLATE = Path(__file__).parent / "review" / "k047-review.html"


def render(template, payload):
    if template.count(MARKER) != 1:
        raise ValueError("Expected one replay data marker")
    return template.replace(MARKER, json.dumps(payload, separators=(",", ":")).replace("<","\\u003c"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("payload", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(render(TEMPLATE.read_text(),json.loads(args.payload.read_text())),encoding="utf-8")
