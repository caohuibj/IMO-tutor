import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "imo-tutor"
WORKFLOWS = SKILL / "workflows"
REF = SKILL / "references"


class FeedbackV052ContractTests(unittest.TestCase):
    def read_workflow(self, name):
        return (WORKFLOWS / name).read_text(encoding="utf-8")

    def test_checkpoint_does_not_finalize_or_run_transfer(self):
        review = self.read_workflow("solution-review.md")
        self.assertIn("checkpoint submission", review)
        self.assertIn("Do not infer completion", review)
        self.assertIn("Before `此题完成`, stop here.", review)
        self.assertIn("Do not create a second durable Attempt row", review)

    def test_explicit_completion_is_six_module_gate(self):
        review = self.read_workflow("solution-review.md")
        transfer = self.read_workflow("post-review-transfer.md")
        self.assertIn("explicit `此题完成` trigger", review)
        self.assertIn("Require the explicit completion trigger `此题完成`", transfer)
        for name in [
            "Historical Transfer",
            "Mathematical Extraction",
            "Higher Mathematics Bridge",
            "Reinforcement Problems",
            "Visual Model",
        ]:
            self.assertIn(name, transfer)

    def test_h6_and_give_up_preserve_substantive_work(self):
        hints = self.read_workflow("hint-manager.md")
        review = self.read_workflow("solution-review.md")
        self.assertIn("substantive checkpoint submissions", hints)
        self.assertIn("do not force `UNSOLVED`", hints)
        self.assertIn("Finalize the current student work **before** revealing the H6 solution", hints)
        self.assertIn("Neither give-up nor H6 activates Historical Transfer", review)

    def test_historical_transfer_is_attempt_grain_and_excludes_current(self):
        retrieval = self.read_workflow("problem-retrieval.md")
        self.assertIn("Attempt grain", retrieval)
        self.assertIn("exclude the current `attempt_id`", retrieval)
        self.assertIn("do not deduplicate by `problem_id`", retrieval)
        self.assertIn("thinking-patterns.json", retrieval)

    def test_thinking_pattern_vocabulary_is_note_level(self):
        patterns = json.loads((REF / "thinking-patterns.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(patterns), 10)
        self.assertTrue(all(key.startswith("TP.") for key in patterns))
        compiler = self.read_workflow("note-compiler.md")
        self.assertIn("They are not Sheet columns", compiler)

    def test_note_is_attempt_bounded(self):
        compiler = self.read_workflow("note-compiler.md")
        template = (REF / "math-note-template.md").read_text(encoding="utf-8")
        self.assertIn("attempt-bounded block per finalized Attempt", compiler)
        self.assertIn("{{attempt_blocks}}", template)
        self.assertIn("## Problem-level Synthesis", template)

    def test_reinforcement_links_do_not_spoil(self):
        transfer = self.read_workflow("post-review-transfer.md")
        self.assertIn("problem-only / official statement link", transfer)
        self.assertIn("do **not** give that direct student-facing link", transfer)

    def test_visual_model_has_math_qa_gate(self):
        transfer = self.read_workflow("post-review-transfer.md")
        archive = self.read_workflow("drive-archive.md")
        self.assertIn("### Mathematical QA gate", transfer)
        self.assertIn("reject and regenerate", transfer)
        self.assertIn("SCHEMATIC — not metrically faithful", transfer)
        self.assertIn("`<attempt_id>-visual-<NN>.<ext>`", archive)

    def test_schemas_are_not_extended_for_transfer_modules(self):
        attempt = json.loads((REF / "attempt.schema.json").read_text(encoding="utf-8"))
        problem = json.loads((REF / "problem.schema.json").read_text(encoding="utf-8"))
        forbidden = {
            "historical_transfer",
            "thinking_patterns",
            "higher_math_bridge",
            "reinforcement_problems",
            "visual_model",
        }
        self.assertTrue(forbidden.isdisjoint(attempt["properties"]))
        self.assertTrue(forbidden.isdisjoint(problem["properties"]))


if __name__ == "__main__":
    unittest.main()
