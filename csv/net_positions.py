"""Print the net non-commercial position per report from a COT-Reports CSV.

Works with the free sample CSV (Australian Dollar, Legacy Futures Only) and
with the Legacy files of the COT Data Dump, which use the same columns.

Usage:
    python net_positions.py path/to/cot-legacy-australian-dollar-sample.csv

Only the Python standard library is used. Columns are read by name, so the
column order does not matter.
"""

import csv
import sys

REQUIRED = ("report_date", "noncomm_long", "noncomm_short")


def to_int(value):
    value = (value or "").strip()
    if not value:
        return None
    return int(float(value))


def read_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(
                f"{path} is missing column(s): {', '.join(missing)}. "
                "Expected a Legacy report CSV from COT-Reports.com."
            )
        rows = []
        for r in reader:
            long_ = to_int(r["noncomm_long"])
            short = to_int(r["noncomm_short"])
            if long_ is None or short is None:
                continue
            rows.append(
                {
                    "date": r["report_date"],
                    "market": r.get("market_name", ""),
                    "long": long_,
                    "short": short,
                    "net": long_ - short,
                }
            )
    # Oldest first, whatever order the file uses
    rows.sort(key=lambda x: x["date"])
    return rows


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    path = argv[1]
    try:
        rows = read_rows(path)
    except (OSError, ValueError) as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1
    if not rows:
        print("No data rows found.", file=sys.stderr)
        return 1

    markets = sorted({r["market"] for r in rows if r["market"]})
    if markets:
        print(f"Market: {', '.join(markets)}")
    print(f"Reports: {len(rows)} ({rows[0]['date']} to {rows[-1]['date']})")
    print()
    print(f"{'Report date':<12}{'NC long':>12}{'NC short':>12}{'NC net':>12}{'Change':>12}")
    previous = None
    for r in rows:
        change = "" if previous is None else f"{r['net'] - previous:+,}"
        print(f"{r['date']:<12}{r['long']:>12,}{r['short']:>12,}{r['net']:>12,}{change:>12}")
        previous = r["net"]
    print()
    print("NC = non-commercial. Change = net position minus the previous report's net position.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
