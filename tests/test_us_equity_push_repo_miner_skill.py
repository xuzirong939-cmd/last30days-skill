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

    def test_required_search_excludes_noisy_or_sensitive_paths(self) -> None:
        text = (SKILL_ROOT / "references" / "us-equity-push-workflow.md").read_text(encoding="utf-8")

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

    def test_last30days_engine_path_has_skill_dir_and_repo_root_forms(self) -> None:
        text = (SKILL_ROOT / "references" / "us-equity-push-workflow.md").read_text(encoding="utf-8")

        self.assertIn("python3 ../last30days/scripts/last30days.py", text)
        self.assertIn("python3 skills/last30days/scripts/last30days.py", text)


if __name__ == "__main__":
    unittest.main()
