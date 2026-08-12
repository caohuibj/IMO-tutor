import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "skills" / "imo-tutor" / "references"
WORKFLOWS = ROOT / "skills" / "imo-tutor" / "workflows"


class ContractTests(unittest.TestCase):
    def load_json(self, name):
        with (REF / name).open(encoding="utf-8") as f:
            return json.load(f)

    def test_reference_json_parses(self):
        for path in REF.glob("*.json"):
            with path.open(encoding="utf-8") as f:
                json.load(f)

    def test_difficulty_scale(self):
        cfg = self.load_json("difficulty.json")
        self.assertEqual(cfg["increment"], 0.5)
        for value in [5.5, 6.5, 7.5, 8.0, 9.5, 10.0]:
            self.assertEqual((value * 2) % 1, 0)
            self.assertGreaterEqual(value, cfg["scale_min"])
            self.assertLessEqual(value, cfg["scale_max"])

    def test_domains_are_canonical(self):
        domains = self.load_json("domains.json")["domains"]
        self.assertEqual(set(domains), {"ALG", "CMB", "GEO", "NT"})

    def test_concept_and_method_tags_are_unique(self):
        for name in ["concepts.json", "methods.json"]:
            data = self.load_json(name)
            tags = [tag for group in data.values() for tag in group]
            self.assertEqual(len(tags), len(set(tags)), name)

    def test_error_tags_are_unique(self):
        errors = self.load_json("errors.json")
        full = [f"{category}.{item}" for category, items in errors.items() for item in items]
        self.assertEqual(len(full), len(set(full)))

    def test_sheet_headers_contain_retrieval_fields(self):
        with (REF / "Problem_Index.csv").open(encoding="utf-8", newline="") as f:
            problem_headers = next(csv.reader(f))
        self.assertIn("problem_id", problem_headers)

        with (REF / "Attempts.csv").open(encoding="utf-8", newline="") as f:
            attempt_headers = next(csv.reader(f))
        for field in ["attempt_id", "problem_id", "primary_domain", "difficulty_rating", "result_bucket", "submitted_at", "search_text"]:
            self.assertIn(field, attempt_headers)

    def test_retrieval_goldens_parse(self):
        path = ROOT / "evals" / "retrieval.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(data["cases"]), 3)
        first = data["cases"][0]["expected"]
        self.assertEqual(first["domains"], ["GEO"])
        self.assertEqual(first["result_buckets"], ["INCORRECT"])
        self.assertEqual(first["limit"], 2)

    def test_retrieval_sort_keys_match_schema(self):
        allowed = set(self.load_json("search-query.schema.json")["properties"]["sort_by"]["enum"])
        retrieval = json.loads((ROOT / "evals" / "retrieval.json").read_text(encoding="utf-8"))
        for case in retrieval["cases"]:
            sort_by = case["expected"].get("sort_by")
            if sort_by:
                self.assertIn(sort_by, allowed)

        lifecycle = json.loads((ROOT / "evals" / "lifecycle.json").read_text(encoding="utf-8"))
        for case in lifecycle["cases"]:
            for query in case.get("queries", []):
                sort_by = query["structured"].get("sort_by")
                if sort_by:
                    self.assertIn(sort_by, allowed)

    def test_retrieval_workflow_matches_contract(self):
        workflow = (WORKFLOWS / "problem-retrieval.md").read_text(encoding="utf-8")
        self.assertIn("`最近` -> sort by `attempt_at` descending.", workflow)
        self.assertNotIn("sort by `submitted_at` descending", workflow)
        self.assertIn("only the first (latest) Attempt encountered for each `problem_id`", workflow)
        self.assertIn("`historical_result_match=true`", workflow)

    def test_attempt_lifecycle_is_transient_until_finalized(self):
        intake = (WORKFLOWS / "problem-intake.md").read_text(encoding="utf-8")
        hints = (WORKFLOWS / "hint-manager.md").read_text(encoding="utf-8")
        archive = (WORKFLOWS / "drive-archive.md").read_text(encoding="utf-8")
        retrieval = (WORKFLOWS / "problem-retrieval.md").read_text(encoding="utf-8")

        self.assertIn("transient active attempt", intake)
        self.assertIn("transient active attempt", retrieval)
        self.assertIn("Do not write an incomplete `Attempts` row", archive)
        self.assertIn("verdict=UNSOLVED", hints)
        self.assertIn("result_bucket=UNSOLVED", hints)
        self.assertIn("If H6 caused the attempt to end, record `hint_max=H6`", archive)

    def test_lifecycle_goldens(self):
        data = json.loads((ROOT / "evals" / "lifecycle.json").read_text(encoding="utf-8"))
        cases = {case["id"]: case for case in data["cases"]}

        retrieval = cases["latest_vs_historical_results"]
        attempts = retrieval["attempts"]

        def matches(attempt, query):
            domains = set(query.get("domains", []))
            buckets = set(query.get("result_buckets", []))
            return (not domains or attempt["primary_domain"] in domains) and (not buckets or attempt["result_bucket"] in buckets)

        def select_problem_ids(query):
            ordered = sorted(attempts, key=lambda row: row["submitted_at"], reverse=True)
            selected = []
            seen = set()
            if query.get("historical_result_match", False):
                for attempt in ordered:
                    if attempt["problem_id"] in seen or not matches(attempt, query):
                        continue
                    seen.add(attempt["problem_id"])
                    selected.append(attempt)
            else:
                latest = {}
                for attempt in ordered:
                    latest.setdefault(attempt["problem_id"], attempt)
                selected = [attempt for attempt in latest.values() if matches(attempt, query)]
                selected.sort(key=lambda row: row["submitted_at"], reverse=True)
            return [row["problem_id"] for row in selected[: query.get("limit", 100)]]

        for query_case in retrieval["queries"]:
            self.assertEqual(select_problem_ids(query_case["structured"]), query_case["expected_problem_ids"])

        give_up = cases["transient_attempt_hints_then_give_up"]
        self.assertEqual(give_up["expect_before_end"]["durable_attempt_rows"], 0)
        self.assertEqual(give_up["expect_after_end"]["verdict"], "UNSOLVED")
        self.assertEqual(give_up["expect_after_end"]["result_bucket"], "UNSOLVED")

        h6 = cases["h6_before_submission"]["expected"]
        self.assertEqual(h6["verdict"], "UNSOLVED")
        self.assertEqual(h6["result_bucket"], "UNSOLVED")
        self.assertEqual(h6["hint_max"], "H6")


if __name__ == "__main__":
    unittest.main()
