import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "us-equity-market-push-miner"


class TestUsEquityMarketPushMinerSkill(unittest.TestCase):
    def test_skill_files_exist(self) -> None:
        self.assertTrue((SKILL_ROOT / "SKILL.md").is_file())
        self.assertTrue((SKILL_ROOT / "references" / "us-equity-market-scan-workflow.md").is_file())
        self.assertTrue((SKILL_ROOT / "agents" / "openai.yaml").is_file())

    def test_skill_frontmatter_and_core_triggers(self) -> None:
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("name: us-equity-market-push-miner", text)
        self.assertIn("全市场扫描", text)
        self.assertIn("Reddit/X/YouTube/HN/Polymarket/web signals", text)
        self.assertIn("IBKR", text)
        self.assertIn("PushPlus", text)
        self.assertIn("Daily Market Desk", text)
        self.assertNotIn("GitHub or local repositories", text)

    def test_workflow_uses_original_last30days_market_scan(self) -> None:
        text = (SKILL_ROOT / "references" / "us-equity-market-scan-workflow.md").read_text(encoding="utf-8")

        self.assertIn("python3 ../last30days/scripts/last30days.py", text)
        self.assertIn('--plan "$QUERY_PLAN_FILE"', text)
        self.assertIn("reddit,x,youtube,tiktok,instagram,hackernews,polymarket,github,web", text)
        self.assertIn("Query Packs", text)
        self.assertIn("Macro/liquidity", text)
        self.assertIn("breadth-rotation", text)
        self.assertIn("ai-semiconductors", text)
        self.assertIn("SPY", text)
        self.assertIn("QQQ", text)
        self.assertIn("VIX", text)
        self.assertIn("Use `--quick` only for smoke tests", text)
        self.assertIn("Avoid broad `US equities`-only search strings", text)
        self.assertIn("Retail/social", text)
        self.assertIn("PushPlus-facing language", text)
        self.assertIn("run_last30days_market_push.py", text)

    def test_workflow_preserves_local_market_desk_gates(self) -> None:
        text = (SKILL_ROOT / "references" / "us-equity-market-scan-workflow.md").read_text(encoding="utf-8")

        self.assertIn("/Users/araki/Documents/Codex/2026-07-03/zhe/agent_tools_integrated", text)
        self.assertIn("/Users/araki/ibkr-grid", text)
        self.assertIn("/Users/araki/Developer/report-system", text)
        self.assertIn("IBKR: private account truth", text)
        self.assertIn("Futu OpenD: read-only", text)
        self.assertIn("Hard rejects", text)
        self.assertIn("scheduled PushPlus workflow", text)

    def test_required_search_excludes_noisy_or_sensitive_paths(self) -> None:
        text = (SKILL_ROOT / "references" / "us-equity-market-scan-workflow.md").read_text(encoding="utf-8")

        for pattern in [
            "--glob '!**/.git/**'",
            "--glob '!**/.venv/**'",
            "--glob '!**/venv/**'",
            "--glob '!**/private/**'",
            "--glob '!**/logs/**'",
            "--glob '!**/reports_archive/**'",
            "--glob '!**/memory*/**'",
            "--glob '!**/*.bak*'",
        ]:
            self.assertIn(pattern, text)


if __name__ == "__main__":
    unittest.main()