import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "imo-tutor"
PROJECT_ONLY = ROOT / "project-only"

RUNTIME_FILES = [
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
    "references/Problem_Index.csv",
    "references/Attempts.csv",
]


class ProjectOnlyContractTests(unittest.TestCase):
    def test_runtime_upload_manifest_has_exactly_19_existing_files(self):
        self.assertEqual(len(RUNTIME_FILES), 19)
        self.assertEqual(len(RUNTIME_FILES), len(set(RUNTIME_FILES)))
        for relative in RUNTIME_FILES:
            self.assertTrue((SKILL / relative).is_file(), relative)

    def test_project_instructions_lock_core_behavior(self):
        instructions = (PROJECT_ONLY / "PROJECT_INSTRUCTIONS.md").read_text(encoding="utf-8")
        for required in [
            "PROJECT-ONLY mode",
            "Do not depend on an installed imo-tutor Skill",
            "SOLUTION_LOCKED",
            "Redo isolation",
            "forbidden input",
            "00｜使用说明",
            "01｜题库检索",
            "IMO Tutor Data",
            "IMO Learning DB",
            "Problem_Index.csv",
            "Attempts.csv",
            "one student's private learning database",
        ]:
            self.assertIn(required, instructions)

    def test_setup_check_covers_all_runtime_files_and_existing_contracts(self):
        setup = (PROJECT_ONLY / "SETUP_CHECK.md").read_text(encoding="utf-8")
        for relative in RUNTIME_FILES:
            self.assertIn(Path(relative).name, setup)
        for required in [
            "exactly 19 Project files",
            "FILES FOUND: n/19",
            "1.0-10.0",
            "SOLUTION_LOCKED",
            "Redo finalize 前禁止读取旧 Attempt solution information",
            "CSV runtime contract",
            "Problem_Index header parity",
            "Attempts header parity",
            "Project-only memory",
            "Installed imo-tutor Skill absent",
        ]:
            self.assertIn(required, setup)

    def test_csv_templates_remain_runtime_sources_in_this_baseline(self):
        setup = (PROJECT_ONLY / "SETUP_CHECK.md").read_text(encoding="utf-8")
        archive = (SKILL / "workflows" / "drive-archive.md").read_text(encoding="utf-8")
        self.assertIn("Use the exact columns in the bundled CSV templates", archive)
        self.assertIn("Problem_Index.csv", setup)
        self.assertIn("Attempts.csv", setup)
        self.assertIn("remain Project runtime sources in this baseline", setup)


if __name__ == "__main__":
    unittest.main()
