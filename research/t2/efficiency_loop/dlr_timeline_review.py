"""Align observed leader tracks and context for independent DLR case review."""
import argparse
import csv
from html import escape
import json
from math import ceil
from pathlib import Path

import pandas as pd

from dlr_green_audit import audit
from dlr_green_service import CONFIG, digest, outlet
from dlr_queue_identity import STOP_M, THROUGH_LANES, queue_ids

# Mask interval numbers and the exploratory case/control labels in the review sheet.
CASES = dict(zip("ABCDE", (8, 3, 9, 7, 5), strict=True))


def build(root, comparison):
    block = "1230"
    offset = 1800
    base = root / "week1" / "wide" / block
    cache = base / "east_tracks_working.pkl"
    crossings = base / "daylight_crossings.csv"
    raw = root / "day" / f"day{block}_tracks.csv"
    map_path = root / "map.xodr"
    cfg = json.loads(CONFIG.read_text())
    if digest(map_path) != cfg["map_sha256"]:
        raise ValueError("OpenDRIVE map differs from the pinned geometry")
    west = outlet(raw, cfg)
    frame = pd.read_pickle(cache)  # Existing project-generated cache.
    frame = frame.loc[~frame.interpolated].copy()
    frame["tick"] = (2 * frame.time).round().astype(int)
    frame["error"] = (frame.time - frame.tick / 2).abs()
    sampled = frame[frame.error <= .026]
    sampled = sampled.loc[sampled.groupby(["id", "tick"]).error.idxmin()]
    queues = queue_ids(sampled[sampled.lane.isin(THROUGH_LANES)], 1, 8)
    with crossings.open(newline="") as stream:
        stops = {int(r["id"]): r for r in csv.DictReader(stream)}
    green = audit(root, block)
    context_report = json.loads(comparison.read_text())
    for path, sha in context_report["input_sha256"].items():
        if green["hashes"].get(path) != sha:
            raise ValueError(f"Context was generated from different inputs: {path}")
    context = {r["interval"]: r for r in context_report["cases"]}
    cases = {}
    for label, interval in CASES.items():
        cycle = next(c for c in green["cycles"] if c["interval"] == interval)
        a0, a1 = (t + offset for t in cycle["on_bracket_s"])
        tick = ceil(2 * a1)
        row = context[interval]
        rel = lambda t: round(t - a1, 3)
        leaders = {}
        for lane in THROUGH_LANES:
            ident = queues[tick, lane][0]
            if stops[ident]["movement"] != "through":
                raise ValueError(f"Leader in {label}/{lane} was not classified through")
            samples = frame[(frame.id == ident) & frame.time.between(a1-2, a1+6)]
            leaders[str(lane)] = {
                "crossing_s": rel(float(stops[ident]["stop"])),
                "samples": [[rel(v.time), round(v.velocity_magnitude, 3),
                             round(STOP_M - v.s - v.dimension_length / 2, 3), int(v.lane)]
                            for v in samples.sort_values("time").itertuples()],
            }
        gap = leaders["-3"]["crossing_s"] - leaders["-4"]["crossing_s"]
        if abs(gap - row["lane_minus3_minus_minus4_s"]) > .0011:
            raise ValueError(f"Crossing gap disagrees with paired-leader audit in {label}")
        outlet_ticks = []
        for i in range(ceil(2*(a1-2)), int(2*(a1+6))+1):
            v = west[west.tick == i]
            windows = [v[v.distance.between(low, high, inclusive="left")]
                       for low, high in cfg["windows_m"]]
            outlet_ticks.append([rel(i/2), [[len(w), int((w.velocity_magnitude <= 2).sum())]
                                           for w in windows]])
        cases[label] = {
            "green_bracket_s": [rel(a0), 0],
            "leaders": leaders,
            "heads": row["candidate_head_states"],
            "queues": row["detected_queues"],
            "outlet_ticks": outlet_ticks,
        }
    inputs = {str(p.relative_to(root)): digest(p) for p in (cache, crossings, raw, map_path)}
    inputs.update(green["hashes"])
    return {"inputs_sha256": inputs, "head_comparison_sha256": digest(comparison),
            "outlet_config_sha256": digest(CONFIG), "cases": cases}


def review_html(report):
    sections = []
    for label, case in report["cases"].items():
        bracket = case["green_bracket_s"][0]
        tracks = case["leaders"]
        rows = []
        for lane, track in tracks.items():
            rows.extend((t, f"직진 {lane}", f"{v:.3f} m/s · 정지선까지 {d:.3f} m · 관측 차로 {l}")
                        for t, v, d, l in track["samples"])
            rows.append((track["crossing_s"], f"직진 {lane}", "차량 중심의 정지선 검지선 통과"))
        for head, observations in case["heads"].items():
            rows.extend((t, f"헤드 {head}", f"상태 {state}") for t, state in observations)
        rows.extend((t, "정지 대기열", f"차로 {lane}에서 {count}대 검출")
                    for t, lane, count in case["queues"])
        rows.extend((t, "서쪽 출구", " · ".join(f"{all_}대 중 ≤2 m/s {slow}대"
                    for all_, slow in counts)) for t, counts in case["outlet_ticks"])
        rows.sort()
        table = "".join(f"<tr><td>{t:+.3f}</td><td>{escape(kind)}</td><td>{escape(value)}</td></tr>"
                        for t, kind, value in rows)
        sections.append(f'<section id="{label}"><h2>사례 {label}</h2>'
                        f"<p>녹색 시작 범위 {bracket:.3f}~0.000초</p>"
                        '<table><thead><tr><th>시각 (초)</th><th>관측 대상</th><th>기록</th>'
                        f"</tr></thead><tbody>{table}</tbody></table></section>")
    links = " · ".join(f'<a href="#{label}">사례 {label}</a>' for label in report["cases"])
    return """<!doctype html><html lang="ko"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>DLR 직진 출발 검토표</title>
<style>
body {font: 1rem/1.6 system-ui,sans-serif; max-width: 56rem; margin: auto; padding: 1.5rem; color:#172738}
section {margin: 3rem 0} table {border-collapse: collapse; width: 100%; font-variant-numeric: tabular-nums}
th,td {text-align:left;padding:.25rem .6rem;border-bottom:1px solid #dae1e9}
thead {position: sticky; top:0; background:#eaf0f7} td:first-child {white-space: nowrap}
a {color:#155a87} tr:nth-child(even) {background:#f5f7fa}
</style>
<h1>DLR 직진 출발 검토표</h1>
<p>0초는 기준 헤드에서 녹색이 처음 관측된 시각이다. 모든 사례에 같은 시간 범위 −2~+6초를 적용했다.
거리 표본은 접근로 투영 앞범퍼 기준이고, 통과 시각은 기존 차량 중심 검지선을 따른다. 헤드 상태 3은 적색, 4는 적황색, 5는 녹색이다.
서쪽 출구 두 열은 검지선 기준 [0, 8) m와 [−6, 2) m에 관측된 표본 수다. 0대는 검출 0회를 뜻한다.</p>
<p>두 검토자는 사례별 근거 시각과 불명 구간을 각각 기록한다. 대기열 행은 정지 검출이며 교차 경로 점유를 직접 측정하지 않는다.</p>
""" + f"<nav>{links}</nav>" + "".join(sections) + "</html>\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("comparison", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("html", type=Path)
    args = parser.parse_args()
    report = build(args.root, args.comparison)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    args.html.write_text(review_html(report))
