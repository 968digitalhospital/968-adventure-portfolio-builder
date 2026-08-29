#!/usr/bin/env python3
"""Convert an ADIF logbook export into a compact Recent QSOs JSON file."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

TOKEN_RE = re.compile(r"<([A-Z0-9_]+)(?::([0-9]+)(?::[^>]+)?)?>", re.IGNORECASE)


def parse_adif(text: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    current: dict[str, str] = {}
    pos = 0
    while True:
        match = TOKEN_RE.search(text, pos)
        if not match:
            break
        name = match.group(1).upper()
        pos = match.end()
        if name == "EOR":
            if current.get("CALL"):
                records.append(current)
            current = {}
            continue
        length_text = match.group(2)
        if length_text is None:
            continue
        length = int(length_text)
        value = text[pos : pos + length].strip()
        pos += length
        current[name] = value
    if current.get("CALL"):
        records.append(current)
    return records


def normalize(record: dict[str, str]) -> dict[str, str]:
    qso_date = record.get("QSO_DATE", "")
    time_on = record.get("TIME_ON", "")
    date = f"{qso_date[:4]}-{qso_date[4:6]}-{qso_date[6:]}" if len(qso_date) == 8 and qso_date.isdigit() else ""
    return {
        "date": date,
        "utc": time_on[:4] if len(time_on) >= 4 else time_on,
        "call": record.get("CALL", ""),
        "band": record.get("BAND", ""),
        "mode": record.get("MODE", ""),
        "rst": record.get("RST_SENT", "") or record.get("RST_RCVD", ""),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="ADIF input file")
    parser.add_argument("output", type=Path, help="JSON output file")
    parser.add_argument("--limit", type=int, default=25, help="Maximum QSOs to publish (default: 25)")
    args = parser.parse_args()

    records = [normalize(record) for record in parse_adif(args.input.read_text(encoding="utf-8", errors="replace"))]
    records.sort(key=lambda item: f"{item.get('date', '')}T{item.get('utc', '')}", reverse=True)
    output = records[: max(args.limit, 0)]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(output)} QSOs to {args.output}")


if __name__ == "__main__":
    main()
