import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "skills" / "imo-tutor" / "references"


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


if __name__ == "__main__":
    unittest.main()
