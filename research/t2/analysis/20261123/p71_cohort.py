"""Complete the archived P70 cohort without selecting on the T2 outcome."""
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory
from p70_offset_transfer import compare


def replay(reference):
    with TemporaryDirectory() as root:
        row = compare(reference["seed"], Path(root), include_sumo=True)
    if any(row[key] != reference[key] for key in ("tape", "t2")):
        raise ValueError("Archived P70 pair did not replay")
    return row


if __name__ == "__main__":
    cohort = json.loads(Path(__file__).with_name("P70_RESULT.json").read_text())[1:]
    assert [r["seed"] for r in cohort] == list(range(701,765))
    with ProcessPoolExecutor(max_workers=4) as pool:
        print(json.dumps(list(pool.map(replay, cohort)), indent=2))
