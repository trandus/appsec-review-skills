#!/usr/bin/env python3
"""Offline ASVS lookup for the sec-* skill set."""

import argparse
import json
from pathlib import Path


def load_data() -> dict:
    path = Path(__file__).resolve().parents[1] / "references" / "asvs-5.0.0-local.json"
    return json.loads(path.read_text(encoding="utf-8"))


def matches(item: dict, query: str, level: str | None, chapter: str | None) -> bool:
    if level and level not in item["levels"]:
        return False
    if chapter and not item["id"].startswith(f"{chapter}."):
        return False
    if not query:
        return True
    haystack = " ".join(
        [
            item["id"],
            item["chapter"],
            item["area"],
            item["summary"],
            " ".join(item["keywords"]),
        ]
    ).lower()
    return all(part in haystack for part in query.lower().split())


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline lookup for the local OWASP ASVS 5.0.0 reference set.")
    parser.add_argument("--query", nargs="*", default=[], help="Keywords, for example authorization or csrf.")
    parser.add_argument("--level", choices=["L1", "L2", "L3"], help="ASVS level.")
    parser.add_argument("--chapter", help="ASVS chapter number, for example 8.")
    args = parser.parse_args()

    data = load_data()
    query = " ".join(args.query)
    results = [item for item in data["requirements"] if matches(item, query, args.level, args.chapter)]

    for item in results:
        levels = ",".join(item["levels"])
        print(f"v{data['version']}-{item['id']} [{levels}] {item['chapter']} / {item['area']}")
        print(f"  {item['summary']}")
    if not results:
        print("No match in the local offline dataset. Record a Follow-up or write a short mapping rationale.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
