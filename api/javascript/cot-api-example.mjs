// COT Data API example (Node.js 18+, built-in fetch, no dependencies).
//
// Step 1 calls the free demo endpoint. It needs no key and returns a fixed
// synthetic sample (not real market data), so you can check your parser.
//
// Step 2 runs only when the COT_API_KEY environment variable is set. It reads
// the latest Legacy report for Gold (CFTC code 088691) and its COT Index.
// Get a key at https://cot-reports.com/api/
//
// Docs: https://cot-reports.com/api-docs/

const BASE_URL = 'https://cot-reports.com/api/v1'
const GOLD_CFTC_CODE = '088691'
const TIMEOUT_MS = 20_000

// Legacy report trader groups: [label, column prefix]
const GROUPS = [
  ['Non-commercial', 'noncomm'],
  ['Commercial', 'comm'],
  ['Non-reportable', 'nonrept'],
]

class ApiError extends Error {}

/** GET a path under /api/v1/ (every path ends with a slash). */
async function getJson(path, apiKey, params) {
  const url = new URL(BASE_URL + path)
  for (const [k, v] of Object.entries(params ?? {})) url.searchParams.set(k, String(v))
  const headers = { Accept: 'application/json' }
  if (apiKey) headers.Authorization = `Bearer ${apiKey}`

  const res = await fetch(url, { headers, signal: AbortSignal.timeout(TIMEOUT_MS) })
  if (res.ok) return res.json()

  // Errors come back as {"error": "<machine_code>", "message": "<human text>"}
  let body = {}
  try {
    body = await res.json()
  } catch {
    // not JSON, keep the defaults below
  }
  const code = body.error ?? 'unknown_error'
  const message = body.message ?? res.statusText

  if (res.status === 401) {
    throw new ApiError(
      `401 Unauthorized (${code}): the key is missing or not recognized. ` +
        'Check COT_API_KEY, or create a key at https://cot-reports.com/api/',
    )
  }
  if (res.status === 403) throw new ApiError(`403 Forbidden (${code}): ${message}`)
  if (res.status === 429) {
    const retry = res.headers.get('Retry-After') ?? 'a while'
    throw new ApiError(
      `429 Too Many Requests (${code}): rate limit reached. Retry after ${retry} seconds. ` +
        'The demo allows a few calls a day per network address; a key has its own published limits.',
    )
  }
  throw new ApiError(`HTTP ${res.status} (${code}): ${message}`)
}

const fmt = (n) => (typeof n === 'number' ? n.toLocaleString('en-US') : String(n))

/** Print long, short, net and weekly change for each Legacy trader group. */
function printPositions(row) {
  console.log(`  Market:        ${row.market_name}`)
  console.log(`  Report date:   ${row.report_date}`)
  console.log(`  Open interest: ${fmt(row.open_interest)}`)
  console.log()
  console.log(
    '  ' + 'Group'.padEnd(16) + 'Long'.padStart(12) + 'Short'.padStart(12) + 'Net'.padStart(12) +
      'Chg long'.padStart(11) + 'Chg short'.padStart(11),
  )
  for (const [label, prefix] of GROUPS) {
    const long = row[`${prefix}_long`] ?? 0
    const short = row[`${prefix}_short`] ?? 0
    console.log(
      '  ' + label.padEnd(16) + fmt(long).padStart(12) + fmt(short).padStart(12) + fmt(long - short).padStart(12) +
        fmt(row[`change_${prefix}_long`]).padStart(11) + fmt(row[`change_${prefix}_short`]).padStart(11),
    )
  }
}

async function step1Demo() {
  console.log('Step 1: free demo endpoint (no key, synthetic sample)')
  console.log('-'.repeat(74))
  const data = await getJson('/demo/')
  printPositions(data.row)
  console.log()
  console.log(`  Note from the API: ${data.message}`)
  console.log()
}

async function step2Live(apiKey) {
  console.log(`Step 2: live data for Gold (CFTC ${GOLD_CFTC_CODE})`)
  console.log('-'.repeat(74))
  const latest = await getJson(`/cot/${GOLD_CFTC_CODE}/latest/`, apiKey)
  printPositions(latest.row)

  const index = await getJson(`/cot/${GOLD_CFTC_CODE}/index/`, apiKey, { lookback: 52 })
  console.log()
  console.log(
    `  COT Index (${index.lookback_weeks} weeks, non-commercial net): ${index.cot_index} ` +
      `(net ${fmt(index.latest_net_position)}, window ${fmt(index.window_min_net)} to ${fmt(index.window_max_net)})`,
  )
  console.log()
  console.log('  More markets, report families and full history: https://cot-reports.com/api-docs/')
}

async function main() {
  try {
    await step1Demo()
    const apiKey = (process.env.COT_API_KEY ?? '').trim()
    if (!apiKey) {
      console.log('Step 2 skipped: set COT_API_KEY to read live data. Get a key at https://cot-reports.com/api/')
      return 0
    }
    await step2Live(apiKey)
    return 0
  } catch (err) {
    if (err instanceof ApiError) console.error(`Error: ${err.message}`)
    else console.error(`Network error: ${err instanceof Error ? err.message : err}`)
    return 1
  }
}

process.exitCode = await main()
