# US Equity Market Scan Workflow

## Local Assets To Check First

Always inspect these before changing market-desk behavior:

- `/Users/araki/Documents/Codex/2026-07-03/zhe/agent_tools_integrated`
  - Current branch observed: `codex/integrated-daily-market-desk`.
  - Primary Daily Market Desk and PushPlus repo.
  - Key files: `00_System/DAILY_MARKET_DESK.md`, `00_System/FULL_MARKET_RESEARCH_PROTOCOL.md`, `00_System/PUBLIC_PRIVATE_BOUNDARY.md`, `00_System/EXECUTION_GATE.md`, `AGENTS.md`, `scripts/run_premarket_daily.py`, `scripts/run_intraday_daily.py`, `scripts/run_postclose_daily.py`, `scripts/run_position_health_push.py`, `scripts/mobile_push_card.py`, `scripts/position_health_push_card.py`, `scripts/daily_push_report.py`, `12_Notifications/pushplus.py`, `14_Broker/futu_readonly/README.md`, `14_Broker/ibkr_readonly/ibkr_snapshot.py`.
  - Tests to look for: `tests/test_mobile_push_card.py`, `tests/test_pushplus_safety_gate.py`, `tests/test_position_health_push_card.py`, `tests/test_portfolio_health.py`, `tests/test_public_private_boundary.py`, `tests/test_full_market_protocol.py`, `tests/test_premarket_generation.py`, `tests/test_postclose_generation.py`, `tests/test_ibkr_snapshot.py`.
- `/Users/araki/Documents/Codex/2026-07-03/codex-task-investment-os-trading-system`
  - Current branch observed: `feature/execution-feedback-kernel-v1`.
  - Durable execution-feedback and broker guard material.
- `/Users/araki/ibkr-grid`
  - Backend-only private portfolio scan path.
  - For this skill, prefer read-only scan/report pieces: `portfolio_scan_push.py`, `run_portfolio_scan.sh`, `scan_positions.py`, `data_freshness.py`.
  - Order scripts are off-limits unless the user explicitly asks for execution tooling and the execution gate permits it.
- `/Users/araki/Developer/report-system`
  - Legacy report and PushPlus path.
  - Key files: `wx_push_us.py`, `us_stock_brief.py`, `us_stock_final.py`, `data_health_check.py`, `scan_result_validator.py`.

## Required Local Search

Use `rg` before external discovery:

```bash
rg -n "Daily Market Desk|full-market|FULL_MARKET|market traffic|Traffic Light|PushPlus|pushplus|mobile_push_card|position_health|portfolio_health|IBKR|Futu|OpenD|Execution Gate|Polymarket|Reddit|YouTube|Hacker News|breadth|VIX|DIX|GEX|MOVE|FRED|Cboe|rates|FX|sector|semis|AI" \
  /Users/araki/Documents/Codex /Users/araki/ibkr-grid /Users/araki/Developer/report-system \
  --glob '!**/.git/**' \
  --glob '!**/.venv/**' \
  --glob '!**/venv/**' \
  --glob '!**/__pycache__/**' \
  --glob '!**/private/**' \
  --glob '!**/logs/**' \
  --glob '!**/reports/**' \
  --glob '!**/reports_archive/**' \
  --glob '!**/docs/observation_log/**' \
  --glob '!**/memory*/**' \
  --glob '!**/skills/**/analysis/**' \
  --glob '!**/skills/**/references/articles.md' \
  --glob '!**/*.bak*'
```

Also list repo state:

```bash
git -C /path/to/repo status --short --branch
git -C /path/to/repo remote -v
```

## last30days Engine

Generate and pass a query plan. Do not run the engine with only one broad topic string; that falls back to weak deterministic planning.

From this skill directory:

```bash
QUERY_PLAN_FILE="$(mktemp -t us-equity-market-plan.XXXXXX.json)"
cat > "$QUERY_PLAN_FILE" <<'JSON'
{
  "intent": "breaking_news",
  "freshness_mode": "strict_recent",
  "cluster_mode": "story",
  "subqueries": [
    {
      "label": "macro-risk",
      "search_query": "SPY QQQ IWM FOMC Treasury yields DXY risk appetite",
      "ranking_query": "What macro, rate, dollar, and liquidity signals are driving SPY, QQQ, and IWM now?",
      "sources": ["reddit", "x", "youtube", "tiktok", "instagram", "hackernews", "polymarket", "grounding"],
      "weight": 1.0
    },
    {
      "label": "breadth-rotation",
      "search_query": "SPY QQQ IWM market breadth equal weight RSP sector rotation",
      "ranking_query": "Is the US equity tape broadening, narrowing, rotating, or breaking down?",
      "sources": ["reddit", "x", "youtube", "grounding"],
      "weight": 0.9
    },
    {
      "label": "ai-semiconductors",
      "search_query": "NVDA AVGO AMD semiconductors AI data center capex software multiples",
      "ranking_query": "How are AI, semiconductor, data-center, and software narratives affecting US equity leadership?",
      "sources": ["reddit", "x", "youtube", "hackernews", "github", "grounding"],
      "weight": 0.9
    },
    {
      "label": "vol-retail-policy",
      "search_query": "VIX options gamma put call dealer positioning tariffs recession market odds",
      "ranking_query": "What volatility, retail-positioning, options, policy, and geopolitical risks are surfacing for US equities?",
      "sources": ["reddit", "x", "youtube", "polymarket", "grounding"],
      "weight": 0.8
    }
  ]
}
JSON
python3 ../last30days/scripts/last30days.py "SPY QQQ IWM full market signal scan" --plan "$QUERY_PLAN_FILE" --search=reddit,x,youtube,tiktok,instagram,hackernews,polymarket,github,web --days=14 --emit=compact
```

From the repository root:

```bash
python3 skills/last30days/scripts/last30days.py "SPY QQQ IWM full market signal scan" --plan "$QUERY_PLAN_FILE" --search=reddit,x,youtube,tiktok,instagram,hackernews,polymarket,github,web --days=14 --emit=compact
```

Run `--preflight` first when validating a new environment. If a source is unavailable, mark it gray and continue with the remaining sources; do not fabricate missing data.
Use `--quick` only for smoke tests; do not use it for production full-market scans because it can collapse coverage.
Avoid broad `US equities`-only search strings; anchor public-source queries with market symbols and indicators such as `SPY`, `QQQ`, `IWM`, `RSP`, `DXY`, `VIX`, `NVDA`, `AVGO`, and `AMD` to reduce generic US-news noise.

## Query Packs

Use several narrow runs instead of one vague run when time permits:

- Macro/liquidity: `Fed cuts inflation jobs Treasury yields dollar liquidity risk appetite US equities`.
- Rates/FX/credit: `2Y 10Y yields dollar DXY credit spreads MOVE market stress stocks`.
- Index/breadth: `S&P 500 Nasdaq Russell 2000 market breadth advance decline 52 week highs lows`.
- Sector/factor: `AI semiconductors software defensives financials small caps momentum value market rotation`.
- Vol/options: `VIX options gamma dealer positioning put call skew hedging flows`.
- Retail/social: `retail traders Reddit X WallStreetBets most discussed US stocks today`.
- Polymarket/policy: `Fed decision recession election tariffs geopolitics market odds`.
- Watchlist narrative: `NVDA AVGO AMD MSFT AAPL META TSLA PLTR CRWD IWM QQQ SPY market narrative`.

## Source Roles

- Reddit / X-like public chatter: sentiment, crowding, panic/euphoria, ticker narrative heat.
- YouTube / podcasts: popular narrative propagation; use as attention signal, not fact anchor.
- Hacker News / GitHub: AI/dev tool demand, open-source momentum, developer adoption, infra narratives.
- Polymarket: event probability and market-implied narrative risk; verify with primary sources.
- Grounded web/news: fact check, official links, earnings, macro data, and current catalysts.
- IBKR: private account truth only; never inferred from public sources.
- Futu OpenD: read-only market quote cross-check only; default `count_in_signal=false` unless explicitly upgraded by rules.

## Scoring Rubric

Score each signal 0-100:

- 20 source reliability: primary/official > licensed API > mainstream news > social.
- 20 freshness: current session/24h > this week > stale.
- 15 breadth: appears across independent source types, not one echo chamber.
- 15 market impact: likely to move index, factor, sector, or owned exposure.
- 10 direction clarity: risk-on/risk-off/rotation/volatility is explicit.
- 10 contradiction handling: conflicting evidence captured and downgraded.
- 10 actionability: maps to allowed action, blocked action, watch trigger, or no-op.

Decision bands:

- `80-100`: primary driver candidate.
- `60-79`: supporting driver or watchlist trigger.
- `40-59`: narrative color only.
- `<40`: reject or ignore.

Hard rejects:

- Uses social/news/yfinance-only data to produce ticker-level account actions.
- Treats stale or missing IBKR data as live position truth.
- Pushes full dashboards, raw source dumps, debug logs, or wide tables to PushPlus.
- Leaks private holdings, NAV, costs, PnL, orders, account IDs, tokens, or raw broker responses.
- Recommends orders, cancellations, or position changes without the Execution Gate.

## Output Template

```text
结论:
- 市场灯号:
- 主驱动:
- 现在能做:
- 现在不能做:

全市场水温:
- 宏观/利率:
- 指数/广度:
- 行业/因子:
- 波动/期权:
- 社媒/散户:
- 政策/地缘:

信号挖掘:
- signal | score | source/freshness | impact | action

推送卡:
- 标题:
- 一句话:
- 三条信号:
- 允许动作:
- 禁止动作:
- 下次触发:

账户门禁:
- IBKR:
- Futu:
- public/private:

下一步:
- 已改:
- 已验证:
- 阻塞:
```

PushPlus-facing language must be short, mobile-first, Chinese, and action-led. Keep detailed PMCL/radar/anomaly/divergence/source audit in the full report on disk.
