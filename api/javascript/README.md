# COT Data API: JavaScript (Node.js) example

One ES module, no dependencies. Needs Node.js 18 or newer (built-in `fetch`).

```bash
node cot-api-example.mjs
```

## What it does

1. **Free demo, no key.** Calls `GET https://cot-reports.com/api/v1/demo/` and prints a small table: long, short, net and weekly change for each Legacy trader group. The demo returns a fixed synthetic sample (not a real market) and allows a few calls a day per network address. Use it to check your parsing.
2. **Live data, with a key.** If `COT_API_KEY` is set, it reads the latest Legacy report for Gold (CFTC code `088691`) from `GET /api/v1/cot/088691/latest/` and its COT Index from `GET /api/v1/cot/088691/index/?lookback=52`. Without a key it prints where to get one.

```bash
export COT_API_KEY=cot_live_...          # macOS / Linux
$env:COT_API_KEY = "cot_live_..."        # Windows PowerShell
node cot-api-example.mjs
```

Errors are reported in plain words: `401` (missing or unknown key), `403` (revoked key), `429` (rate limit, with the `Retry-After` value).

## Going further

- Get a key: [COT Data API](https://cot-reports.com/api/)
- Every endpoint, parameter and field: [API documentation](https://cot-reports.com/api-docs/), or the [OpenAPI 3.0 spec](https://cot-reports.com/api/v1/openapi.json/) to generate a client
- Other report families (`family=disagg|tff|supp`), the Futures & Options Combined variant (`variant=combined`) and the weekly history (`/api/v1/cot/{cftc_code}/`) use the same key

Keep your key out of the browser and out of source control: call the API from a server or a script, and read the key from the environment.
