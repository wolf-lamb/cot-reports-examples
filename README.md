# COT-Reports.com examples

Small, runnable examples for working with Commitments of Traders (COT) data from [COT-Reports.com](https://cot-reports.com/): the COT Data API in Python and JavaScript, the CSV format, and the MCP server for AI assistants.

## What the COT report is

The Commitments of Traders (COT) report is published by the U.S. Commodity Futures Trading Commission (CFTC). For each U.S. futures market above the reporting threshold, it shows the open interest and how it splits between trader groups, such as non-commercial traders (large speculators), commercial traders (hedgers) and non-reportable positions (small traders), with the long and short positions of each group and the change since the previous report. The CFTC publishes it on a fixed schedule, listed on the [CFTC release schedule](https://cot-reports.com/cftc-release-schedule/) page.

## Quick start

The API example runs out of the box: step 1 calls the free demo endpoint, which needs no key and returns a fixed synthetic sample.

```bash
git clone <this repository>
cd cot-reports-examples

# Python
pip install -r api/python/requirements.txt
python api/python/cot_api_example.py

# Node.js 18 or newer (no dependencies)
node api/javascript/cot-api-example.mjs
```

With a COT Data API key, step 2 reads live data for Gold:

```bash
export COT_API_KEY=cot_live_...   # Windows PowerShell: $env:COT_API_KEY = "cot_live_..."
python api/python/cot_api_example.py
```

## Folder map

| Folder | What it shows |
|---|---|
| [`api/python/`](api/python/) | COT Data API with `requests`: the free demo, then the latest positions and COT Index for one market |
| [`api/javascript/`](api/javascript/) | The same in Node.js with the built-in `fetch`, no dependencies |
| [`csv/`](csv/) | A standard-library parser for the free sample CSV: net non-commercial position per report and its change |
| [`ai-assistants/`](ai-assistants/) | Connect Claude, ChatGPT, Cursor, VS Code or Gemini CLI to the COT-Reports MCP server |

## Free on cot-reports.com

No code needed for any of these:

- [COT report, simplified](https://cot-reports.com/cot-report-simplified/): non-commercial net positions and weekly change for every CFTC market
- [COT charts](https://cot-reports.com/cot-report-charts/): net positions against price and open interest, every market
- [COT Index](https://cot-reports.com/cot-index/): the formula and a chart of the 0 to 100 index for every market
- [COT extremes](https://cot-reports.com/cot-extremes/): markets where speculators hold a 3-year extreme in the latest report
- [COT weekly summary](https://cot-reports.com/cot-report-weekly-summary/): net positions and weekly change for the key markets in one table
- [CFTC release schedule](https://cot-reports.com/cftc-release-schedule/): every release date, with holiday delays

A [free account](https://cot-reports.com/signup/) adds longer history on the report pages and the free sample CSV used in [`csv/`](csv/).

## Need more?

These examples are a starting point. For real work, the products below do the heavy lifting. Prices are on each page.

| Product | What it gives you |
|---|---|
| [COT Premium](https://cot-reports.com/pricing/) | The full site: Disaggregated, TFF and Supplemental reports, long history, CSV export and the advanced analytics |
| [COT Data API](https://cot-reports.com/api/) | Every CFTC market and all four report families over REST: bearer key, JSON, weekly history and a built-in COT Index ([docs](https://cot-reports.com/api-docs/)) |
| [COT Data Dump](https://cot-reports.com/data-dump/) | The full history of every market and every report family in one download, CSV and NDJSON |
| [COT Report Spreadsheet](https://cot-reports.com/spreadsheets/) | A Microsoft Excel workbook that refreshes the COT data when you open it |
| [MCP server](https://cot-reports.com/mcp/) | COT data inside your AI assistant: free to start, more with a free account or COT Premium |

## Data source

CFTC public data, normalized by COT-Reports.com. More on the [data sources](https://cot-reports.com/data-sources/) page.

## Disclaimer

The data and the examples are for information only. They are not financial advice and not a recommendation to buy or sell anything. Trading futures involves risk.

## License

The code in this repository is released under the [MIT License](LICENSE). The COT data itself comes from the CFTC; use of COT-Reports.com services is subject to its [terms](https://cot-reports.com/terms/).
