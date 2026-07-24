---
name: us-equity-market-push-miner
description: Mine full-market US equity signals with the original last30days multi-source research flow, then shape them into Araki's Daily Market Desk and PushPlus workflow. Use when the request mentions 美股推送, 全市场扫描, 市场水温, 盘前/盘中/盘后, US stocks, market breadth, Reddit/X/YouTube/HN/Polymarket/web signals, watchlists, position health, IBKR, Futu OpenD, PushPlus, or market-desk alert automation.
---

# US Equity Market Push Miner

Use this skill to run full-market US equity signal discovery through the existing `last30days` research engine and convert the result into Araki-style market-desk push decisions.

## Operating Rule

Start from broad market context before any ticker or position. This skill is for market-signal mining, not GitHub repo discovery. Treat GitHub as one public signal source only when repo/developer activity is market-relevant.

Read [references/us-equity-market-scan-workflow.md](references/us-equity-market-scan-workflow.md) for query packs, source roles, scoring, output shape, and safety gates.

## Workflow

1. Inspect local market-desk context first.
   - Check the existing Daily Market Desk, PushPlus card, data-source router, and safety-gate files listed in the reference.
   - Record branch state and relevant push/report scripts before proposing changes.
2. Run full-market discovery.
   - Use the original last30days engine for public signal mining across Reddit, X, YouTube, Hacker News, Polymarket, GitHub, and grounded web when available.
   - Use multiple query packs: macro/liquidity, rates/FX/credit, indexes/breadth, sectors/factors, AI/semis, major single-stock narratives, options/volatility, retail/social heat, and policy/geopolitics.
   - Unless the user explicitly asks only to edit, explain, or avoid running tools, execute the complete scan; do not stop at a proposed plan.
3. Separate signal from action.
   - Public/social sources can change attention, narrative, or watchlist priority.
   - Ticker-level action requires fresh IBKR account truth plus the existing Execution Gate.
   - Futu OpenD is read-only quote cross-check, never account truth.
4. Render for PushPlus.
   - PushPlus gets a compact Chinese action card: conclusion, traffic light, top drivers, allowed/blocked actions, data confidence, and next trigger.
   - Keep PMCL, radar, anomaly, divergence, raw sources, and self-check detail in the full report on disk.
5. Deliver or edit directly.
   - If asked to change the skill/plugin, patch this skill and tests.
   - If asked to run a scan, return the scan result in the output shape below and cite live public sources when used.
   - If the local Daily Market Desk repo is available, prefer its `scripts/run_last30days_market_push.py` runner for scheduled PushPlus scans because it saves the full report and only sends a safe mobile card.

## Output Shape

Write in compact Chinese by default:

1. `结论`: market light, strongest driver, what to do / not do now.
2. `全市场水温`: macro, rates, breadth, sector/factor, volatility, social/retail, policy/geopolitics.
3. `信号挖掘`: top 5-8 public signals with source, freshness, confidence, and impact.
4. `推送卡`: PushPlus-ready mobile action card.
5. `账户门禁`: IBKR freshness, private-data boundary, blocked ticker actions.
6. `下一步`: exact file/workflow changes, validation result, and next scan trigger.

Never expose real IBKR holdings, NAV, costs, orders, account IDs, tokens, or raw broker responses in public reports, GitHub commits, or shared memory.