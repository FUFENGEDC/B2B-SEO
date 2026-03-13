#!/usr/bin/env python3
"""Build cluster-level writing priorities from a keyword table."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Tuple

COMMERCIAL_HINTS = {"pricing", "vendor", "software", "solution", "demo", "服务", "报价", "对比", "平台"}
LONGTAIL_SUFFIXES = ["指南", "模板", "清单", "最佳实践", "案例", "vs", "怎么做", "是什么"]


def parse_int(value: str, default: int = 0) -> int:
    try:
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return default


def pick(row: Dict[str, str], keys: List[str], default: str = "") -> str:
    for k in keys:
        if k in row and str(row[k]).strip() != "":
            return str(row[k]).strip()
    return default


def intent_score(intent: str, keyword: str) -> int:
    low = f"{intent} {keyword}".lower()
    score = 2
    if "commercial" in low or "transactional" in low:
        score = 5
    elif "informational" in low:
        score = 3
    if any(h in low for h in COMMERCIAL_HINTS):
        score = min(5, score + 1)
    return score


def normalize_volume(v: int) -> int:
    if v >= 5000:
        return 5
    if v >= 2000:
        return 4
    if v >= 800:
        return 3
    if v >= 200:
        return 2
    return 1


def reverse_difficulty(d: int) -> int:
    # higher score means easier to rank
    if d <= 20:
        return 5
    if d <= 35:
        return 4
    if d <= 50:
        return 3
    if d <= 70:
        return 2
    return 1


def wave(score: int) -> str:
    if score >= 19:
        return "Now"
    if score >= 15:
        return "Next"
    return "Later"


def expand_longtails(keyword: str) -> str:
    return "|".join(f"{keyword} {s}" for s in LONGTAIL_SUFFIXES)


def row_to_plan(row: Dict[str, str]) -> Dict[str, str]:
    keyword = pick(row, ["keyword", "关键词"])
    intent = pick(row, ["intent", "search_intent", "意图"], "informational")
    volume = parse_int(pick(row, ["search_volume", "volume", "搜索量"], "0"))
    diff = parse_int(pick(row, ["difficulty", "kd", "难度"], "50"))

    i_score = intent_score(intent, keyword)
    v_score = normalize_volume(volume)
    d_score = reverse_difficulty(diff)
    conversion = min(5, max(1, i_score))
    synergy = 4 if len(keyword.split()) >= 2 else 3
    priority = i_score + v_score + d_score + conversion + synergy

    return {
        "keyword": keyword,
        "intent": intent,
        "search_volume": str(volume),
        "difficulty": str(diff),
        "business_intent_score": str(i_score),
        "conversion_potential": str(conversion),
        "cluster_synergy": str(synergy),
        "priority_score": str(priority),
        "write_wave": wave(priority),
        "expanded_longtails": expand_longtails(keyword),
    }


def build_plan(rows: List[Dict[str, str]], limit: int) -> List[Dict[str, str]]:
    plans = [row_to_plan(r) for r in rows if pick(r, ["keyword", "关键词"])]
    plans.sort(key=lambda r: parse_int(r["priority_score"]), reverse=True)
    return plans[:limit] if limit > 0 else plans


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "keyword",
        "intent",
        "search_volume",
        "difficulty",
        "business_intent_score",
        "conversion_potential",
        "cluster_synergy",
        "priority_score",
        "write_wave",
        "expanded_longtails",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build B2B SEO cluster priority plan")
    parser.add_argument("--input", required=True, help="Keyword research CSV")
    parser.add_argument("--output", default="ops/cluster-priority-plan.csv", help="Output CSV")
    parser.add_argument("--limit", type=int, default=50, help="Top N rows, <=0 for all")
    args = parser.parse_args()

    rows = read_csv(Path(args.input))
    plan = build_plan(rows, args.limit)
    write_csv(Path(args.output), plan)
    print(f"Generated {len(plan)} rows -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
