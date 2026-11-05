"""COT Data API example (Python).

Step 1 calls the free demo endpoint. It needs no key and returns a fixed
synthetic sample (not real market data), so you can check your parser.

Step 2 runs only when the COT_API_KEY environment variable is set. It reads
the latest Legacy report for Gold (CFTC code 088691) and its COT Index.
Get a key at https://cot-reports.com/api/

Docs: https://cot-reports.com/api-docs/
"""

import os
import sys

import requests

BASE_URL = "https://cot-reports.com/api/v1"
GOLD_CFTC_CODE = "088691"
TIMEOUT_SECONDS = 20

# Legacy report trader groups: (label, column prefix)
GROUPS = [
    ("Non-commercial", "noncomm"),
    ("Commercial", "comm"),
    ("Non-reportable", "nonrept"),
]


class ApiError(Exception):
    pass


def get_json(path, api_key=None, params=None):
    """GET a path under /api/v1/ (every path ends with a slash)."""
    headers = {"Accept": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    resp = requests.get(f"{BASE_URL}{path}", headers=headers, params=params, timeout=TIMEOUT_SECONDS)

    if resp.status_code == 200:
        return resp.json()

    # Errors come back as {"error": "<machine_code>", "message": "<human text>"}
    try:
        body = resp.json()
    except ValueError:
        body = {}
    code = body.get("error", "unknown_error")
    message = body.get("message", resp.text[:200])

    if resp.status_code == 401:
        raise ApiError(
            f"401 Unauthorized ({code}): the key is missing or not recognized. "
            "Check COT_API_KEY, or create a key at https://cot-reports.com/api/"
        )
    if resp.status_code == 403:
        raise ApiError(f"403 Forbidden ({code}): {message}")
    if resp.status_code == 429:
        retry = resp.headers.get("Retry-After", "a while")
        raise ApiError(
            f"429 Too Many Requests ({code}): rate limit reached. Retry after {retry} seconds. "
            "The demo allows a few calls a day per network address; a key has its own published limits."
        )
    raise ApiError(f"HTTP {resp.status_code} ({code}): {message}")


def fmt(n):
    return f"{n:,}" if isinstance(n, (int, float)) else str(n)


def print_positions(row):
    """Print long, short, net and weekly change for each Legacy trader group."""
    print(f"  Market:        {row.get('market_name')}")
    print(f"  Report date:   {row.get('report_date')}")
    print(f"  Open interest: {fmt(row.get('open_interest'))}")
    print()
    print(f"  {'Group':<16}{'Long':>12}{'Short':>12}{'Net':>12}{'Chg long':>11}{'Chg short':>11}")
    for label, prefix in GROUPS:
        long_ = row.get(f"{prefix}_long") or 0
        short = row.get(f"{prefix}_short") or 0
        print(
            f"  {label:<16}{fmt(long_):>12}{fmt(short):>12}{fmt(long_ - short):>12}"
            f"{fmt(row.get(f'change_{prefix}_long')):>11}{fmt(row.get(f'change_{prefix}_short')):>11}"
        )


def step1_demo():
    print("Step 1: free demo endpoint (no key, synthetic sample)")
    print("-" * 74)
    data = get_json("/demo/")
    print_positions(data["row"])
    print()
    print(f"  Note from the API: {data.get('message')}")
    print()


def step2_live(api_key):
    print(f"Step 2: live data for Gold (CFTC {GOLD_CFTC_CODE})")
    print("-" * 74)
    latest = get_json(f"/cot/{GOLD_CFTC_CODE}/latest/", api_key)
    print_positions(latest["row"])

    index = get_json(f"/cot/{GOLD_CFTC_CODE}/index/", api_key, params={"lookback": 52})
    print()
    print(
        f"  COT Index ({index['lookback_weeks']} weeks, non-commercial net): {index['cot_index']} "
        f"(net {fmt(index['latest_net_position'])}, window {fmt(index['window_min_net'])} "
        f"to {fmt(index['window_max_net'])})"
    )
    print()
    print("  More markets, report families and full history: https://cot-reports.com/api-docs/")


def main():
    try:
        step1_demo()
        api_key = os.environ.get("COT_API_KEY", "").strip()
        if not api_key:
            print("Step 2 skipped: set COT_API_KEY to read live data. Get a key at https://cot-reports.com/api/")
            return 0
        step2_live(api_key)
        return 0
    except ApiError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1
    except requests.RequestException as err:
        print(f"Network error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
