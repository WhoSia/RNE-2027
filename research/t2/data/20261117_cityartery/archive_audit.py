"""Fingerprint the CityArtery distribution without extracting or rewriting it."""
import argparse
from collections import defaultdict
from hashlib import file_digest
import json
from pathlib import Path
from zipfile import ZipFile


def inventory(path):
    with open(path, "rb") as source:
        sha = file_digest(source, "sha256").hexdigest()
    with ZipFile(path) as archive:
        members = sorted((info for info in archive.infolist() if not info.is_dir()), key=lambda info: info.filename)
        names = [info.filename for info in members]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate member paths")
        by_hash = defaultdict(list)
        rows = []
        for info in members:
            with archive.open(info) as stream:
                digest = file_digest(stream, "sha256").hexdigest()
            by_hash[digest].append(info.filename)
            rows.append({"name": info.filename, "bytes": info.file_size, "sha256": digest})
    return {"source": "10.17632/ftzzmh2cmt.1", "archive_bytes": Path(path).stat().st_size,
            "archive_sha256": sha, "file_members": len(rows), "unique_contents": len(by_hash),
            "duplicate_groups": [group for group in by_hash.values() if len(group) > 1],
            "members": rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(inventory(args.archive), indent=2) + "\n", encoding="utf-8")
