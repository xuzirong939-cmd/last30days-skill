import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "us-equity-push-repo-miner"


class TestUsEquityPushRepoMinerSkill(unittest.TestCase):
    def test_skill_files_exist(self) -> None:
        self.assertTrue((SKILL_ROOT / "SKILL.md").is_file())
        self.assertTrue((SKILL_ROOT / "references" / "us-equity-push-workflow.md").is_file())
        self.assertTrue((SKILL_ROOT / "agents" / "openai.yaml").is_file())

    def test_skill_frontmatter_and_core_triggers(self) -> None:
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("name: us-equity-push-repo-miner", text)
        self.assertIn("美股推送", text)
        self.assertIn("IBKR", text)
        self.assertIn("PushPlus", text)
        self.assertIn("Daily Market Desk", text)

    def test_workflow_references_existing_araki_paths(self) -> None:
        text = (SKILL_ROOT / "references" / "us-equity-push-workflow.md").read_text(encoding="utf-8")

        self.assertIn("/Users/araki/Documents/Codex/2026-07-03/zhe/agent_tools_integrated", text)
        self.assertIn("/Users/araki/ibkr-grid", text)
        self.assertIn("/Users/araki/Developer/report-system", text)
        self.assertIn("Hard rejects", text)


if __name__ == "__main__":
    unittest.main()
