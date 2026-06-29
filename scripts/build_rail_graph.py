#!/usr/bin/env python3
"""Pre-build rail station graph for commute-area (isochrone) feature.

Reads rail_stations.json and emits rail_graph.json containing the adjacency list
used by the client-side Dijkstra. Same algorithm as the JS buildRailGraph(),
just executed offline so the client doesn't pay the CPU cost.

Output format: a 2D array indexed by station id (= position in rail_stations.json).
Each entry is a flat array [id1, w1, id2, w2, ...] of neighbor (id, weight) pairs.
Weights are travel minutes (float, 2 decimal places).

Run: python3 scripts/build_rail_graph.py
"""

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATIONS_JSON = ROOT / "rail_stations.json"
GRAPH_JSON = ROOT / "rail_graph.json"

# Average operating speed (km/h) — same logic as JS railSpeedKmh
def rail_speed(op: str, line: str) -> float:
    if op == "西日本旅客鉄道":
        if "東海道" in line or "山陽" in line:
            return 55
        return 45
    if op == "東海旅客鉄道":
        return 55
    if op == "近畿日本鉄道" and "特急" not in line:
        return 45
    if op == "南海電気鉄道":
        return 45
    if op == "京阪電気鉄道":
        return 42
    if op == "阪急電鉄":
        return 42
    if op == "阪神電気鉄道":
        return 38
    if op == "山陽電気鉄道":
        return 42
    if op == "神戸電鉄":
        return 38
    if "市" in op or op == "大阪市高速電気軌道" or op == "神戸新交通":
        return 32
    if op == "京福電気鉄道" or op == "阪堺電気軌道":
        return 22
    return 35


def dist_m(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    dy = (lat2 - lat1) * 111000
    dx = (lng2 - lng1) * 111000 * math.cos((lat1 + lat2) / 2 * math.pi / 180)
    return math.sqrt(dx * dx + dy * dy)


def main() -> None:
    stations = json.loads(STATIONS_JSON.read_text())
    n = len(stations)
    print(f"Loaded {n} stations")

    # Apply 西日本 line splits (same as runtime JS)
    LNG_KYOTO = 135.7615
    LNG_OSAKA = 135.5023
    LNG_HIMEJI = 134.6904
    for s in stations:
        if s.get("o") != "西日本旅客鉄道":
            continue
        if s["l"] == "東海道線":
            if s["lng"] >= LNG_KYOTO:
                s["l"] = "東海道線(米原〜京都)"
            elif s["lng"] >= LNG_OSAKA:
                s["l"] = "東海道線(京都〜大阪)"
            else:
                s["l"] = "東海道線(大阪〜姫路)"
        elif s["l"] == "山陽線":
            if LNG_HIMEJI < s["lng"] < LNG_OSAKA:
                s["l"] = "東海道線(大阪〜姫路)"

    # Group by (operator, line)
    by_line: dict[tuple[str, str], list[tuple[int, dict]]] = {}
    for i, s in enumerate(stations):
        key = (s["o"], s["l"])
        by_line.setdefault(key, []).append((i, s))

    # Adjacency: id -> list of (neighbor_id, weight_min)
    adj: list[list[tuple[int, float]]] = [[] for _ in range(n)]

    # In-line edges: connect each station to its 2 nearest neighbors on the same line
    for (op, line), group in by_line.items():
        speed = rail_speed(op, line)
        for idx, st in group:
            others = [
                (j, dist_m(st["lat"], st["lng"], o["lat"], o["lng"]))
                for j, o in group
                if j != idx
            ]
            others.sort(key=lambda x: x[1])
            for nb_id, d in others[:2]:
                t = (d / 1000) / speed * 60 + 0.5  # 駅停車 30 秒
                adj[idx].append((nb_id, t))

    # Transfer edges: any 2 stations within 400m on different lines = walking transfer + 2min
    GRID = 0.005
    grid: dict[tuple[int, int], list[int]] = {}
    for i, s in enumerate(stations):
        key = (int(s["lat"] / GRID), int(s["lng"] / GRID))
        grid.setdefault(key, []).append(i)

    transfer_count = 0
    seen = set()
    for i, s in enumerate(stations):
        gy = int(s["lat"] / GRID)
        gx = int(s["lng"] / GRID)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                for j in grid.get((gy + dy, gx + dx), []):
                    if j <= i:
                        continue
                    sj = stations[j]
                    if s["o"] == sj["o"] and s["l"] == sj["l"]:
                        continue
                    d = dist_m(s["lat"], s["lng"], sj["lat"], sj["lng"])
                    if d > 400:
                        continue
                    t = d / 80 + 2
                    key = (i, j)
                    if key in seen:
                        continue
                    seen.add(key)
                    adj[i].append((j, t))
                    adj[j].append((i, t))
                    transfer_count += 1

    edge_count = sum(len(a) for a in adj)
    print(f"Edges built: {edge_count} (transfer pairs: {transfer_count})")

    # Compact output: list[list[int|float]] where each entry is [id1, w1, id2, w2, ...]
    out: list[list] = []
    for nbrs in adj:
        flat: list = []
        for nb_id, w in nbrs:
            flat.append(nb_id)
            flat.append(round(w, 2))
        out.append(flat)

    GRAPH_JSON.write_text(json.dumps(out, separators=(",", ":"), ensure_ascii=False))
    size_kb = GRAPH_JSON.stat().st_size / 1024
    print(f"Wrote {GRAPH_JSON} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
