"""Check an eight-cycle observation pilot and compare independent coding."""
import argparse
import csv
import json
from pathlib import Path

CYCLE_COUNT = 8
CYCLE_FIELDS = ("cycle", "start_ms", "end_ms", "signal", "queue", "gaps", "receiving", "notes")
# Each gap refers to a pre-marked lane-change zone and the candidate vehicle in view.
GAP_FIELDS = ("cycle", "open_ms", "close_ms", "move", "cross_ms", "notes")
VISIBILITY = {"visible", "unknown"}


def read_rows(path, fields):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != fields:
            raise ValueError(f"{path.name}: expected columns {', '.join(fields)}")
        for row in reader:
            if None in row or None in row.values():
                raise ValueError(f"{path.name}, row {reader.line_num}: wrong number of columns")
            yield {key: value.strip() for key, value in row.items()}


def millis(value, label):
    if not value.isascii() or not value.isdecimal():
        raise ValueError(f"{label}: enter a nonnegative integer in milliseconds")
    return int(value)


def audit(folder):
    cycles = []
    rows = list(read_rows(folder / "cycles.csv", CYCLE_FIELDS))
    if len(rows) != CYCLE_COUNT:
        raise ValueError(f"Expected {CYCLE_COUNT} consecutive cycles, found {len(rows)}")
    for index, row in enumerate(rows, 1):
        if row["cycle"] != str(index):
            raise ValueError(f"Expected cycle {index}")
        start, end = (millis(row[key], f"cycle {index} {key}") for key in ("start_ms", "end_ms"))
        if start >= end or (cycles and start != cycles[-1]["end_ms"]):
            raise ValueError(f"Cycle {index}: boundaries must be positive-length and consecutive")
        visibility = {key: row[key] for key in ("signal", "queue", "gaps", "receiving")}
        if set(visibility.values()) - VISIBILITY:
            raise ValueError(f"Cycle {index}: each visibility entry must be visible or unknown")
        if "unknown" in visibility.values() and not row["notes"]:
            raise ValueError(f"Cycle {index}: explain missing visibility")
        cycles.append({"cycle": index, "start_ms": start, "end_ms": end,
                       "visibility": visibility, "notes": row["notes"], "windows": []})

    for row in read_rows(folder / "gaps.csv", GAP_FIELDS):
        index = millis(row["cycle"], "gap cycle")
        if not 1 <= index <= CYCLE_COUNT:
            raise ValueError(f"Gap refers to unknown cycle {index}")
        cycle = cycles[index - 1]
        start = cycle["start_ms"]
        end = cycle["end_ms"]
        opens, closes = (millis(row[key], f"cycle {index} {key}") for key in ("open_ms", "close_ms"))
        if not start <= opens < closes <= end:
            raise ValueError(f"Cycle {index}: gap interval falls outside its cycle")
        move = row["move"]
        at = millis(move, f"cycle {index} move") if move not in {"no", "unknown"} else None
        if at is not None and not opens <= at < closes:
            raise ValueError(f"Cycle {index}: observed move must begin inside its gap interval")
        crossing = row["cross_ms"]
        # A move in this cycle can cross the stop line during a later cycle.
        if crossing and (at is None or millis(crossing, f"cycle {index} cross_ms") < at):
            raise ValueError(f"Cycle {index}: a crossing requires a preceding observed move")
        if not row["notes"]:
            raise ValueError(f"Cycle {index}: record a frame, vehicle marker or evidence note for the gap")
        cycle["windows"].append({"start_offset_ms": opens - start, "end_offset_ms": closes - start,
                                 "move": at if at is not None else move,
                                 "cross_ms": int(crossing) if crossing else None, "notes": row["notes"]})

    for cycle in cycles:
        windows = cycle["windows"]
        windows.sort(key=lambda row: row["start_offset_ms"])
        if any(a["end_offset_ms"] > b["start_offset_ms"] for a, b in zip(windows, windows[1:])):
            raise ValueError(f"Cycle {cycle['cycle']}: gap intervals overlap")
        partial = cycle["visibility"]["gaps"] == "unknown"
        cycle["gap_status"] = "unknown" if partial else ("observed" if windows else "none_observed")
        cycle["gap_total_ms"] = None if partial else sum(
            row["end_offset_ms"] - row["start_offset_ms"] for row in windows)
    return {"cycles": cycles}


def compare(a, b):
    """Match identical preselected windows without pooling reviewer observations."""
    report = []
    for left, right in zip(a["cycles"], b["cycles"], strict=True):
        if any(left[key] != right[key] for key in ("cycle", "start_ms", "end_ms")):
            raise ValueError(f"Reviewer cycle boundaries differ at cycle {left['cycle']}")
        paired = {key: [left["visibility"][key], right["visibility"][key]] for key in left["visibility"]}
        report.append({"cycle": left["cycle"], "visibility": paired,
                       "joint_full_visibility": all(pair == ["visible", "visible"] for pair in paired.values()),
                       "gap_status": [left["gap_status"], right["gap_status"]],
                       "gap_total_ms": [left["gap_total_ms"], right["gap_total_ms"]]})
    return {"joint_full_visibility_cycles": [row["cycle"] for row in report if row["joint_full_visibility"]],
            "cycles": report}


def template(folder):
    folder.mkdir(parents=True)
    with (folder / "cycles.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(CYCLE_FIELDS)
        writer.writerows([index, *([""] * (len(CYCLE_FIELDS) - 1))] for index in range(1, CYCLE_COUNT + 1))
    with (folder / "gaps.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        csv.writer(stream).writerow(GAP_FIELDS)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("template").add_argument("folder", type=Path)
    check = commands.add_parser("audit")
    check.add_argument("review_a", type=Path)
    check.add_argument("review_b", type=Path, nargs="?")
    args = parser.parse_args()
    try:
        if args.command == "template":
            template(args.folder)
            return
        a = audit(args.review_a)
        if args.review_b is None:
            result = a
        else:
            if args.review_a.resolve() == args.review_b.resolve():
                raise ValueError("Use two separate reviewer folders")
            b = audit(args.review_b)
            result = {"comparison": compare(a, b), "review_a": a, "review_b": b}
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
