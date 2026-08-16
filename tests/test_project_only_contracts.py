import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "imo-tutor"
PROJECT_ONLY = ROOT / "project-only"

RUNTIME_FILES = [
    "workflows/first-round-routing.md",
    "workflows/problem-intake.md",
    "workflows/no-spoiler-analysis.md",
    "workflows/hint-manager.md",
    "workflows/solution-review.md",
    "workflows/solution-compare.md",
    "workflows/note-compiler.md",
    "workflows/drive-archive.md",
    "workflows/problem-retrieval.md",
    "references/difficulty.json",
    "references/domains.json",
    "references/errors.json",
    "references/concepts.json",
    "references/methods.json",
    "references/problem.schema.json",
    "references/attempt.schema.json",
    "references/search-query.schema.json",
    "references/math-note-template.md",
]


class ProjectOnlyContractTests(unittest.TestCase):
    def test_runtime_upload_manifest_has_exactly_18_existing_files(self):
        self.assertEqual(len(RUNTIME_FILES), 18)
        self.assertEqual(len(RUNTIME_FILES), len(set(RUNTIME_FILES)))
        for relative in RUNTIME_FILES:
            self.assertTrue((SKILL / relative).is_file(), relative)

    def test_csv_templates_are_setup_only(self):
        setup = (PROJECT_ONLY / "SETUP_CHECK.md").read_text(encoding="utf-8")
        archive = (SKILL / "workflows" / "drive-archive.md").read_text(encoding="utf-8")
        for name in ["Problem_Index.csv", "Attempts.csv"]:
            self.assertIn(name, setup)
        self.assertIn("not required as Project runtime sources", setup)
        self.assertIn("CSV templates are setup assets and are not required as Project runtime sources", archive)

    def test_project_instructions_lock_core_behavior(self):
        instructions = (PROJECT_ONLY / "PROJECT_INSTRUCTIONS.md").read_text(encoding="utf-8")
        for required in [
            "PROJECT-ONLY mode",
            "Do not depend on an installed imo-tutor Skill",
            "first-round-routing.md",
            "Notion",
            "Google Drive + Google Sheets",
            "Never use one durable storage domain as a fallback for the other",
            "SOLUTION_LOCKED",
            "Redo isolation",
            "forbidden input",
            "00｜使用说明",
            "01｜题库检索",
            "IMO Tutor Data",
            "IMO Learning DB",
            "one student's private learning database",
        ]:
            self.assertIn(required, instructions)

    def test_setup_check_covers_all_runtime_files_and_hard_contracts(self):
        setup = (PROJECT_ONLY / "SETUP_CHECK.md").read_text(encoding="utf-8")
        for relative in RUNTIME_FILES:
            self.assertIn(Path(relative).name, setup)
        for required in [
            "exactly 18 Project files",
            "FILES FOUND: n/18",
            "1.0-10.0",
            "IMO/Shortlist baseline 只是校准锚点，不是下界",
            "SOLUTION_LOCKED",
            "Redo finalize 前禁止读取旧 Attempt solution information",
            "compact JSON array",
            "Problem_Index header parity",
            "Attempts header parity",
            "Project-only memory",
            "Installed imo-tutor Skill absent",
            "FIRST-ROUND CONTRACTS",
            "Notion persistence schema: DEFERRED TO PR2",
        ]:
            self.assertIn(required, setup)

    def test_first_round_routing_contract_is_project_based_and_isolated(self):
        routing = (SKILL / "workflows" / "first-round-routing.md").read_text(encoding="utf-8")
        for required in [
            "Do not depend on an installed `imo-tutor` Skill",
            "Durable source of truth: **Notion**",
            "FILL_SET",
            "CALC_SET",
            "PRACTICE",
            "FULL_EXAM",
            "Explicit stored Problem identity wins",
            "Explicit first-round intent wins over implicit chat state",
            "Implicit proof follow-ups stay with the active proof Attempt",
            "never allocate a `Pxxxxxx` Problem ID",
            "never read or write `Problem_Index` for first-round persistence",
            "never read or write `Attempts` for first-round persistence",
            "do not fall back to Google Drive or Google Sheets",
            "Do not apply H0-H6 or `SOLUTION_LOCKED`",
        ]:
            self.assertIn(required, routing)

    def test_first_round_acceptance_examples_cover_explicit_system_switch(self):
        routing = (SKILL / "workflows" / "first-round-routing.md").read_text(encoding="utf-8")
        for example in [
            "新的一题 IMO 2024 P2",
            "重做 P000237",
            "高联一试填空复盘",
            "再给一点提示",
            "高联一试计算题复盘",
            "解析几何一试专项 6 题",
            "complete first-round 8+3 upload",
        ]:
            self.assertIn(example, routing)

    def test_proof_system_contracts_remain_explicitly_scoped(self):
        instructions = (PROJECT_ONLY / "PROJECT_INSTRUCTIONS.md").read_text(encoding="utf-8")
        self.assertIn("No-spoiler rule — proof / second-round only", instructions)
        self.assertIn("Redo isolation — critical, proof / second-round only", instructions)
        self.assertIn("Do not apply H0-H6 or `SOLUTION_LOCKED` to first-round work", instructions)
        self.assertIn("keep Google Drive / Google Sheets as the durable source of truth", (SKILL / "workflows" / "first-round-routing.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
