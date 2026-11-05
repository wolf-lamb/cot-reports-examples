# COT CSV: net positions per report

`net_positions.py` reads a COT-Reports.com Legacy CSV with Python's standard `csv` module and prints, for each report, the non-commercial long and short positions, the net position (long minus short) and its change from the previous report.

```bash
python net_positions.py cot-legacy-australian-dollar-sample.csv
```

```text
Report date      NC long    NC short      NC net      Change
2026-10-06        38,000      95,000     -57,000
2026-10-13        39,500      91,000     -51,500      +5,500
...
```

(The numbers above are illustrative, not real data.)

## Get the free sample CSV

1. Create a [free account](https://cot-reports.com/signup/) (or sign in).
2. Open the [COT Data Dump](https://cot-reports.com/data-dump/#free-sample) page and use the free sample button.
3. You get `cot-legacy-australian-dollar-sample.csv`: the Australian Dollar (CME, 6A), the newest 52 reports of the Legacy report, Futures Only.

The script reads columns by name (`report_date`, `noncomm_long`, `noncomm_short`, and `market_name` when present), so it does not depend on the column order.

## The full history, same format

The sample is one slice of the [COT Data Dump](https://cot-reports.com/data-dump/): every CFTC market, every report family and the full history, written in the same CSV format (plus NDJSON). Its Legacy files have exactly the sample's columns, so code you write against the sample runs on them unchanged. For weekly updates from code, see the [COT Data API](https://cot-reports.com/api/).

No dataset is included in this repository.
