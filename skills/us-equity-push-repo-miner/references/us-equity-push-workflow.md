# US Equity Push Repo Workflow

## Local Assets To Check First

Always inspect these before recommending external code:

- `/Users/araki/Documents/Codex/2026-07-03/zhe/agent_tools_integrated`
  - Current branch observed: `codex/integrated-daily-market-desk`.
  - Primary US equity push and Daily Market Desk repo.
  - Key files: `00_System/DAILY_MARKET_DESK.md`, `00_System/FULL_MARKET_RESEARCH_PROTOCOL.md`, `00_System/PUBLIC_PRIVATE_BOUNDARY.md`, `AGENTS.md`, `scripts/run_premarket_daily.py`, `scripts/run_intraday_daily.py`, `scripts/run_postclose_daily.py`, `scripts/run_position_health_push.py`, `scripts/mobile_push_card.py`, `scripts/position_health_push_card.py`, `12_Notifications/pushplus.py`.
  - Tests to look for: `tests/test_mobile_push_card.py`, `tests/test_pushplus_safety_gate.py`, `tests/test_position_health_push_card.py`, `tests/test_portfolio_health.py`, `tests/test_public_private_boundary.py`, `tests/test_full_market_protocol.py`, `tests/test_premarket_generation.py`, `tests/test_postclose_generation.py`.
- `/Users/araki/Documents/Codex/2026-07-03/codex-task-investment-os-trading-system`
  - Current branch observed: `feature/execution-feedback-kernel-v1`.
  - Durable rules, execution-feedback kernel, and broker guard material.
  - Key files: `14_Broker/pretrade_gate.py`, `14_Broker/tests/test_pretrade_gate.py`, `10_Review/feedback_metrics.py`, `ibkr-trading/SKILL.md`.
- `/Users/araki/ibkr-grid`
  - Backend-only portfolio scan path and IBKR execution tooling.
  - For push discovery, prefer read-only scan/report pieces: `portfolio_scan_push.py`, `run_portfolio_scan.sh`, `scan_positions.py`, `data_freshness.py`, `positions/scan_report_*.yaml`.
  - Treat order scripts as off-limits unless the user explicitly asks for execution tooling and the execution gate permits it.
- `/Users/araki/Developer/report-system`
  - Legacy report and PushPlus path.
  - Key files: `wx_push_us.py`, `us_stock_brief.py`, `us_stock_final.py`, `持仓扫描.py`, `data_health_check.py`, `scan_result_validator.py`.

## Required Local Search

Use `rg` before external discovery:

```bash
rg -n "PushPlus|pushplus|wx_push|IBKR|Interactive Brokers|Futu|OpenD|Daily Market Desk|premarket|postclose|position_health|portfolio_health|mobile_push_card|watchlist|market traffic|Execution Gate" /Users/araki/Documents/Codex /Users/araki/ibkr-grid /Users/araki/Developer/report-system
```

Also list repo state:

```bash
git -C /path/to/repo status --short --branch
git -C /path/to/repo remote -v
```

## External Repo Search Queries

Use GitHub search or the GitHub connector. Mix narrow Chinese and English terms:

- `PushPlus 美股`
- `PushPlus stock alert`
- `IBKR PushPlus portfolio`
- `Interactive Brokers WeChat stock alert`
- `Interactive Brokers portfolio scanner Python`
- `Futu OpenD PushPlus`
- `Futu OpenD US stock alert`
- `US stock premarket postclose report Python`
- `US stock watchlist WeChat alert`
- `portfolio health stock alert Python`
- `market breadth dashboard Python GitHub`
- `StockTwits portfolio alert GitHub`
- `Polygon FRED VIX market dashboard Python`
- `IBKR portfolio Telegram alert`
- `WeChat market report GitHub`

When using the adjacent last30days engine for social/web recency, run it from the new skill directory with the existing engine path:

```bash
python3 ../last30days/scripts/last30days.py "IBKR PushPlus US stock alert GitHub" --search=github,hackernews,reddit,web,stocktwits --days=90 --emit=compact
```

If the topic is a named product, repo, author, or company, generate a query plan first and pass it via `--plan`, following the original last30days contract.

## Candidate Data To Capture

For each candidate repo, capture:

- `repo`: owner/name and URL.
- `purpose`: what it does in one sentence.
- `activity`: last commit/release date, issue velocity, stars/forks only as secondary signal.
- `license`: usable, unclear, or blocked.
- `language/runtime`: Python, JS, Go, etc.
- `data sources`: IBKR, Futu, Polygon, yfinance, FRED, CBOE, RSS, StockTwits, news, manual CSV.
- `push channels`: PushPlus, WeChat, Telegram, email, Slack, webhook.
- `schedule`: cron, GitHub Actions, launchd, APScheduler, none.
- `safety`: account freshness, stale-data handling, secret handling, no-order boundary.
- `tests`: unit tests, smoke tests, CI, none.
- `integration surface`: exact files or functions likely to reuse.

## Scoring Rubric

Score 0-100:

- 20 data-source fit: IBKR account truth, Futu read-only quote check, official macro/filings, exchange/broker quotes.
- 15 mobile push fit: PushPlus/WeChat support, compact Chinese card shape, no wide tables.
- 15 repo health: recent activity, tests, license, docs, low setup friction.
- 15 integration fit: small patch surface and clear landing in existing local repos.
- 15 safety: no automatic orders, private-data boundary, freshness gates, no token leakage.
- 10 signal quality: full-market-to-position reasoning, multi-source verification, stale/missing data handling.
- 10 maintainability: simple config, deterministic scripts, observable failure path.

Decision bands:

- `80-100`: strong reuse candidate. Adapt with tests.
- `60-79`: useful reference, integrate only selected pieces.
- `40-59`: watch or borrow ideas, do not import code.
- `<40`: reject.

Hard rejects:

- Places trades, cancels orders, or unlocks a trading context without an explicit execution gate.
- Treats sample positions, local markdown positions, or stale broker export as live account truth.
- Stores NAV, cash, position size, cost, PnL, account IDs, tokens, or raw broker responses in public GitHub.
- Uses only yfinance/RSS/social posts for executable position actions.
- Pushes full dashboards, debug logs, raw CI output, or wide tables to PushPlus.
- Has no compatible license when code reuse is being considered.

## Araki Data Discipline

- IBKR is account truth.
- Futu OpenD is read-only market cross-check, never account truth.
- Public GitHub may store methodology, sanitized reports, data-source status, and generic risk levels only.
- PushPlus may carry private summaries only from a private runner or local path.
- Fresh IBKR private snapshot allows normal position-health output.
- Recent stale IBKR can support manual-review candidates only.
- Missing/corrupted/too-stale IBKR blocks ticker-level actions and requires `UPDATE_POSITIONS`.
- No discovered public repo can override the Execution Gate.

## Output Template

```text
结论:
- 首选: owner/repo, score X/100. Why it helps Araki now.
- 不接: owner/repo, blocker.

落点:
- 本地仓库: /absolute/path
- 文件: exact file(s)
- 推送链路: data -> report -> mobile card -> PushPlus -> full report path

候选:
- owner/repo | X/100 | 可复用: module/function | 风险: blocker | 动作: adapt/reference/reject

安全门禁:
- IBKR freshness:
- private-data boundary:
- no-order boundary:
- tests:

下一步:
- 已改:
- 已验证:
- 未完成/阻塞:
```

Keep PushPlus-facing language short and action-first. Reserve broad radar, PMCL, anomaly, divergence, and self-check detail for the full report on disk.
