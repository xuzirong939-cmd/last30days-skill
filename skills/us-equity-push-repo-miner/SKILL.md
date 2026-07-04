---
name: us-equity-push-repo-miner
description: Mine and evaluate GitHub or local repositories for Araki's US equity research and mobile push workflows. Use when the request mentions 美股推送, US stock alerts, stock/portfolio scanners, Daily Market Desk, premarket/postclose reports, position health, watchlists, IBKR, Futu OpenD, PushPlus, WeChat alerts, or finding/adapting repos for market-desk automation.
---

# US Equity Push Repo Miner

Use this skill to find, score, and adapt repositories that can improve Araki's US equity market-desk and PushPlus workflow.

## Operating Rule

Start from Araki's existing local assets before recommending or changing any external repo. Do not rebuild functionality that already exists in `agent_tools_integrated`, `ibkr-grid`, `report-system`, or `trading-system-shared`.

Read [references/us-equity-push-workflow.md](references/us-equity-push-workflow.md) for the path map, search queries, scoring rubric, output shape, and safety gates.

## Workflow

1. Inspect local context first.
   - Search `/Users/araki/Documents/Codex`, `/Users/araki/ibkr-grid`, and `/Users/araki/Developer/report-system` with `rg --files` and `rg`.
   - Record current branches, dirty files, existing push scripts, workflow files, schedule assumptions, and test coverage.
   - Identify the current best landing repo before looking outward.
2. Mine candidates.
   - Use the GitHub connector or GitHub search first for repo discovery.
   - Use the adjacent last30days engine only when social/web recency matters: `../last30days/scripts/last30days.py`.
   - Search for both English and Chinese terms around IBKR, Futu OpenD, PushPlus, WeChat, US stock alerts, portfolio health, premarket, postclose, watchlists, and market dashboards.
3. Gate every candidate.
   - Reject repos that auto-trade without an execution gate, leak account facts, require stale local Gateway-only account data, lack a usable license for code reuse, fabricate prices, or turn full reports into mobile pushes.
   - Downgrade repos with no tests, no recent commits, unclear data freshness, or single-source market data.
4. Score for Araki fit.
   - Prioritize deterministic pipelines, mobile-first Chinese action cards, explicit data freshness, IBKR-as-account-truth discipline, PushPlus/WeChat delivery, self-hosted/private-runner compatibility, and small integration surface.
   - Treat public GitHub code as method input, not account truth.
5. Deliver or edit directly.
   - If the user asks to change a repo, implement the patch in the most relevant local checkout.
   - If the user asks for discovery, lead with the top 1-3 candidates and the no-go list.
   - Always state what lands where: file path, branch, push route, schedule, secret/runner dependency, and test command.

## Output Shape

Write in compact Chinese by default:

1. `结论`: best repo(s) to reuse or whether to reject all.
2. `落点`: exact local repo and files to modify.
3. `候选`: compact bullets with score, reason, and blocker.
4. `推送链路`: data source -> report generator -> PushPlus/mobile card -> full report path.
5. `安全门禁`: account freshness, private-data boundary, no-order boundary, tests.
6. `下一步`: implemented changes, validation result, and remaining blocked items.

Never expose real IBKR holdings, NAV, costs, orders, account IDs, tokens, or raw broker responses in public reports, GitHub commits, or shared memory.
