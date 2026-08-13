#!/usr/bin/env python3
"""Aggregate crashout logs from ~/.hermes/crashout/.

Usage:
    python3 analyze.py            # all months
    python3 analyze.py 2026-08    # one month

Stdlib only. Prints summary tables: entries per month/model/profile,
trigger histogram, average heat, high-heat entries, and fix ideas.
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

LOG_DIR = Path.home() / ".hermes" / "crashout"

ENTRY_RE = re.compile(r"^## (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) — (.+)$")
FIELD_RE = re.compile(r"^- (profile|model|trigger|heat|task): (.*)$")


def parse_file(path: Path):
    entries = []
    current = None
    section = None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = ENTRY_RE.match(line)
        if m:
            if current:
                entries.append(current)
            current = {
                "when": m.group(1), "summary": m.group(2),
                "profile": "?", "model": "?", "trigger": "?", "heat": None,
                "task": "", "fix": "", "month": path.stem.replace("crashout-", ""),
            }
            section = None
            continue
        if current is None:
            continue
        f = FIELD_RE.match(line)
        if f:
            key, val = f.group(1), f.group(2).strip()
            if key == "heat":
                try:
                    current["heat"] = int(val.split()[0])
                except (ValueError, IndexError):
                    current["heat"] = None
            else:
                current[key] = val
            section = None
            continue
        if line.startswith("**Fix idea:**"):
            section = "fix"
            continue
        if line.startswith("**") and line.endswith(":**"):
            section = None
            continue
        if section == "fix" and line.strip():
            current["fix"] += line.strip() + " "
    if current:
        entries.append(current)
    return entries


def bar(count: int, total: int, width: int = 30) -> str:
    n = round(width * count / total) if total else 0
    return "█" * n


def main():
    month_filter = sys.argv[1] if len(sys.argv) > 1 else None
    files = sorted(LOG_DIR.glob("crashout-*.md"))
    if month_filter:
        files = [f for f in files if month_filter in f.name]
    if not files:
        print(f"No crashout logs found in {LOG_DIR}"
              + (f" for {month_filter}" if month_filter else ""))
        return 0

    entries = []
    for f in files:
        entries.extend(parse_file(f))
    if not entries:
        print("Log files exist but no parseable entries found.")
        return 1

    total = len(entries)
    print(f"Crashout analysis — {total} entr{'y' if total == 1 else 'ies'}"
          f" across {len(files)} file(s)\n")

    def table(title, counter):
        print(title)
        for key, count in counter.most_common():
            print(f"  {key:<22} {count:>3}  {bar(count, total)}")
        print()

    table("By month:", Counter(e["month"] for e in entries))
    table("By trigger:", Counter(e["trigger"] for e in entries))
    table("By model:", Counter(e["model"] for e in entries))
    table("By profile:", Counter(e["profile"] for e in entries))

    heats = [e["heat"] for e in entries if e["heat"] is not None]
    if heats:
        print(f"Heat: avg {sum(heats)/len(heats):.1f}  "
              f"max {max(heats)}  n={len(heats)}\n")

    hot = [e for e in entries if (e["heat"] or 0) >= 4]
    if hot:
        print(f"High-heat entries (4-5): {len(hot)}")
        for e in hot:
            print(f"  [{e['heat']}] {e['when']} ({e['profile']}/{e['model']}) {e['summary']}")
        print()

    fixes = [e for e in entries if e["fix"] and not e["fix"].lower().startswith("none")]
    if fixes:
        print(f"Fix ideas ({len(fixes)} of {total} entries):")
        for e in fixes:
            print(f"  {e['when']} [{e['trigger']}] {e['fix'].strip()}")
        print()

    print("Raw logs: " + str(LOG_DIR))
    return 0


if __name__ == "__main__":
    sys.exit(main())
