#!/usr/bin/env python3
"""Lightweight CLI for B2B SEO workflow operations."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List


def to_int(value: str) -> int:
    try:
        return int(float(value.strip()))
    except (ValueError, AttributeError):
        return 0


def compute_priority(row: Dict[str, str]) -> int:
    business = to_int(row.get("business_value(0-5)", "0"))
    difficulty = to_int(row.get("ranking_difficulty(0-5)", "0"))
    fit = to_int(row.get("content_fit(0-5)", "0"))
    lead = to_int(row.get("lead_potential(0-5)", "0"))
    return business + (5 - difficulty) + fit + lead


def read_keywords(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["computed_priority"] = str(compute_priority(row))
    return rows


def pick_weekly(rows: List[Dict[str, str]], limit: int) -> List[Dict[str, str]]:
    candidates = [
        r
        for r in rows
        if r.get("status", "").strip().lower() in {"backlog", "planned", ""}
    ]
    candidates.sort(key=lambda r: int(r["computed_priority"]), reverse=True)
    return candidates[:limit]


def write_plan(rows: List[Dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "keyword",
        "cluster_topic",
        "funnel_stage",
        "computed_priority",
        "owner",
        "status",
        "next_status",
    ]
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "keyword": row.get("keyword", ""),
                    "cluster_topic": row.get("cluster_topic", ""),
                    "funnel_stage": row.get("funnel_stage", ""),
                    "computed_priority": row.get("computed_priority", "0"),
                    "owner": row.get("owner", ""),
                    "status": row.get("status", ""),
                    "next_status": "brief_ready",
                }
            )


def cmd_weekly_plan(args: argparse.Namespace) -> int:
    rows = read_keywords(Path(args.keywords))
    weekly = pick_weekly(rows, args.limit)
    write_plan(weekly, Path(args.out))
    print(f"Generated weekly plan: {args.out} ({len(weekly)} items)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="B2B SEO workflow helper")
    sub = parser.add_subparsers(dest="command", required=True)

    weekly = sub.add_parser("weekly-plan", help="Generate weekly SEO task plan")
    weekly.add_argument("--keywords", required=True, help="Keyword CSV path")
    weekly.add_argument("--limit", type=int, default=5, help="Number of items")
    weekly.add_argument("--out", default="ops/weekly-plan.csv", help="Output CSV path")
    weekly.set_defaults(func=cmd_weekly_plan)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
