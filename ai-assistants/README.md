# COT data in your AI assistant (MCP)

The COT-Reports MCP server lets an AI assistant answer questions about the Commitments of Traders report from the CFTC data on COT-Reports.com. Every answer with data names the report date and links to the matching page, so you can check it.

- Server address (streamable HTTP): `https://mcp.cot-reports.com`
- Official MCP Registry name: `com.cot-reports/cot`
- Setup guide with every app: [cot-reports.com/mcp](https://cot-reports.com/mcp/)

You can start without an account. When you want more history, the app asks you to sign in to COT-Reports. Signing in works from Claude, ChatGPT, Claude Code, Cursor, VS Code and Gemini CLI.

## Claude (web, desktop, mobile)

Customize, then Connectors, then **+ Add**, then **Add custom connector**. Name it `COT-Reports` and paste:

```text
https://mcp.cot-reports.com
```

Available on every Claude plan (the Free plan allows one custom connector).

## ChatGPT

Plugins, then **+**, then **Add custom MCP server**, with the address `https://mcp.cot-reports.com` (older accounts: Settings, then Apps, then Developer mode). Needs a paid ChatGPT plan.

## Claude Code

```bash
claude mcp add --transport http --scope user cot-reports https://mcp.cot-reports.com
```

`--scope user` makes the server available in every project; leave it out to add it to the current project only. For more history, type `/mcp` in Claude Code and sign in.

## Cursor

Add this to `~/.cursor/mcp.json` (or to your project's `.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "cot-reports": {
      "url": "https://mcp.cot-reports.com"
    }
  }
}
```

## VS Code (GitHub Copilot)

Add this to `.mcp.json` at your project's root, or run "MCP: Add Server" from the command palette:

```json
{
  "mcpServers": {
    "cot-reports": {
      "type": "http",
      "url": "https://mcp.cot-reports.com"
    }
  }
}
```

## Gemini CLI

Add this to `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "cot-reports": {
      "httpUrl": "https://mcp.cot-reports.com"
    }
  }
}
```

## Other MCP apps

Any app that supports remote MCP servers over HTTP can connect. Most read this shape:

```json
{
  "mcpServers": {
    "cot-reports": {
      "type": "http",
      "url": "https://mcp.cot-reports.com"
    }
  }
}
```

## Already have a COT Data API key?

Apps that accept a header can send your [COT Data API](https://cot-reports.com/api/) key instead of signing in. It counts together with your REST API calls (one key, one plan):

```bash
claude mcp add --transport http cot-reports https://mcp.cot-reports.com \
  --header "Authorization: Bearer cot_live_..."
```

## Example prompts

- "What is the net position of large speculators in crude oil, and how did it change this week?"
- "Give me this week's COT overview of the currency futures."
- "Show me the COT Index of the euro over three years." (free account)
- "Which markets have speculators most crowded long?" (COT Premium)
- "When is the next COT report released?"

## What each level includes

| | Without an account | Free account | COT Premium |
|---|---|---|---|
| Markets | Every market | Every market | Every market |
| History | The last 26 weekly reports | 10 years | Full history |
| Report families | Legacy | Legacy | Legacy, Disaggregated, TFF, Supplemental |
| CFTC variants | Each report's default | Each report's default | Futures Only and Futures & Options Combined |
| COT Index | 26 or 52 weeks | Every lookback | Every lookback |
| Positioning extremes scan | Not included | Not included | Included |
| Close prices | Not included | Not included | Included |

A COT Data API key gives every market and report family with full history, without the extremes scan and close prices. Fair-use limits apply; the [setup guide](https://cot-reports.com/mcp/) lists them. To unlock everything, see [COT Premium](https://cot-reports.com/pricing/).

## The tools

Nine read-only tools: `list_markets`, `get_latest_positions`, `get_latest_snapshot`, `get_history`, `get_cot_index`, `get_weekly_summary`, `get_release_schedule`, `explain_cot` and, with COT Premium, `scan_extremes`.

COT-Reports.com is not affiliated with Anthropic, OpenAI, Anysphere, Microsoft or Google; their product names are used only to say which apps can connect. The answers are information about positioning, not trading advice.
