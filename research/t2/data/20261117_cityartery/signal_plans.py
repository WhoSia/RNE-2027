"""Read the source workbook as nominal plans, retaining each source row."""
import argparse
from collections import Counter
from io import BytesIO
import json
from pathlib import Path
import re
from zipfile import ZipFile


def phase(cell):
    match = re.fullmatch(r"(.+):\s*(.+)\s+(\d+)s", cell.strip())
    if not match or int(match[3]) <= 0:
        raise ValueError(f"Bad nominal phase: {cell}")
    directions = sorted(match[1].split("-"))
    movements = sorted(s.strip() for s in match[2].split("+"))
    if set(directions) - {"North", "South", "East", "West"} or set(movements) - {"Straight", "Left Turn"}:
        raise ValueError(f"Unexpected movement: {cell}")
    return {"directions": directions, "movements": movements, "seconds": int(match[3])}


def audit(path):
    import openpyxl

    with ZipFile(path) as source:
        names = [n for n in source.namelist() if n.endswith("/Signal Timing Records.xlsx")]
        if len(names) != 1:
            raise ValueError("Expected one nominal plan workbook")
        book = openpyxl.load_workbook(BytesIO(source.read(names[0])), read_only=True, data_only=True)
    try:
        plans = []
        for sheet in book:
            site = None
            for number, (label, period, *slots) in enumerate(sheet.values, 1):
                if number == 1 or not period:
                    continue
                site = label or site
                phases = [phase(cell) for cell in slots if cell and cell != "/"]
                plans.append({"sheet": sheet.title, "excel_row": number, "site": site, "period": period,
                              "site_label_inherited": not bool(label), "phases": phases,
                              "sum_listed_phase_s": sum(p["seconds"] for p in phases)})
    finally:
        book.close()
    counts = Counter((p["sheet"],p["site"],p["period"]) for p in plans)
    for plan in plans:
        plan["ambiguous_site_period"] = counts[plan["sheet"],plan["site"],plan["period"]] != 1
    return {"time_semantics": "nominal durations, without demonstrated phase epoch, offsets or event log",
            "plans": plans}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(audit(args.archive), indent=2) + "\n")
