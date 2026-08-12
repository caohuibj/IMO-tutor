import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "skills" / "imo-tutor" / "references"
WORKFLOWS = ROOT / "skills" / "imo-tutor" / "workflows"
EVALS = ROOT / "evals"


def normalize_problem_id(raw):
    match = re.fullmatch(r"P([0-9]{1,6})", raw)
    if not match:
        raise ValueError(raw)
    return f"P{int(match.group(1)):06d}"


def error_matches(actual_tags, requested):
    for requested_tag in requested:
        if requested_tag.endswith(".*"):
            prefix = requested_tag[:-1]
            if not any(tag.startswith(prefix) for tag in actual_tags):
                return False
        elif requested_tag not in actual_tags:
            return False
    return True


def execute_attempt_query(attempts, query):
    hint_rank = {f"H{i}": i for i in range(7)}

    rows = sorted(attempts, key=lambda row: row["submitted_at"], reverse=True)
    if query.get("result_buckets") and not query.get("historical_result_match", False):
        latest = {}
        for row in rows:
            latest.setdefault(row["problem_id"], row)
        rows = list(latest.values())

    def matches(row):
        if query.get("domains") and row["primary_domain"] not in query["domains"]:
            return False
        if query.get("difficulty_gte") is not None and row["difficulty_rating"] < query["difficulty_gte"]:
            return False
        if query.get("difficulty_lte") is not None and row["difficulty_rating"] > query["difficulty_lte"]:
            return False
        if query.get("result_buckets") and row["result_bucket"] not in query["result_buckets"]:
            return False
        if query.get("hint_min") and hint_rank[row["hint_max"]] < hint_rank[query["hint_min"]]:
            return False
        if query.get("method_tags") and not all(tag in row.get("method_tags", []) for tag in query["method_tags"]):
            return False
        if query.get("error_tags") and not error_matches(row.get("error_tags", []), query["error_tags"]):
            return False
        if query.get("keywords"):
            search_text = row.get("search_text", "").lower()
            if not all(keyword.lower() in search_text for keyword in query["keywords"]):
                return False
        return True

    matched = [row for row in rows if matches(row)]
    matched.sort(key=lambda row: row["submitted_at"], reverse=query.get("sort_order", "desc") == "desc")

    result = []
    seen = set()
    for row in matched:
        if row["problem_id"] in seen:
            continue
        seen.add(row["problem_id"])
        result.append(row["problem_id"])
        if len(result) >= query.get("limit", 100):
            break
    return result


class RetrievalV04Tests(unittest.TestCase):
    def load_json(self, path):
        return json.loads(path.read_text(encoding="utf-8"))

    def test_exact_id_normalization_and_schema(self):
        self.assertEqual(normalize_problem_id("P00237"), "P000237")
        self.assertEqual(normalize_problem_id("P237"), "P000237")
        self.assertEqual(normalize_problem_id("P000237"), "P000237")
        with self.assertRaises(ValueError):
            normalize_problem_id("P1234567")

        schema = self.load_json(REF / "search-query.schema.json")
        pattern = re.compile(schema["properties"]["problem_id"]["pattern"])
        self.assertRegex("P000237", pattern)
        self.assertNotRegex("P00237", pattern)

    def test_retrieval_examples_parse_to_structured_fields(self):
        data = self.load_json(EVALS / "retrieval.json")
        self.assertEqual(data["exact_cases"][0]["expected_problem_id"], "P000237")

        cases = {case["input"]: case["expected"] for case in data["cases"]}
        self.assertEqual(cases["最近做错的2道几何题"]["result_buckets"], ["INCORRECT"])
        self.assertEqual(cases["难度8以上用过H3提示的数论题"]["hint_min"], "H3")
        self.assertEqual(cases["那道我用了反演但最后逻辑有问题的几何题"]["method_tags"], ["M.GEO.Inversion"])
        self.assertEqual(cases["那道我用了反演但最后逻辑有问题的几何题"]["error_tags"], ["LOGIC.*"])

    def test_retrieval_execution_goldens(self):
        data = self.load_json(EVALS / "retrieval.json")
        attempts = data["execution_fixture"]
        for case in data["execution_cases"]:
            self.assertEqual(execute_attempt_query(attempts, case["query"]), case["expected_problem_ids"], case["id"])

    def test_retrieval_workflow_prefers_structure_and_has_no_vector_dependency(self):
        workflow = (WORKFLOWS / "problem-retrieval.md").read_text(encoding="utf-8")
        self.assertIn("Apply domain, difficulty, date, result, hint, concept, method, and error filters before `search_text`", workflow)
        self.assertIn("Use `search_text` only for unresolved `keywords`", workflow)
        self.assertIn("do not introduce vector search", workflow)
        self.assertIn("follow its `note_url` and return the durable problem note", workflow)

    def test_attempt_fields_capture_student_method_for_fuzzy_retrieval(self):
        workflow = (WORKFLOWS / "solution-review.md").read_text(encoding="utf-8")
        self.assertIn("methods actually used by the student", workflow)
        self.assertIn("`M.GEO.Inversion`", workflow)
        self.assertIn("`Attempts.method_tags` records the student's actual approach", workflow)

    def test_redo_isolates_history_until_finalization(self):
        workflow = (WORKFLOWS / "problem-retrieval.md").read_text(encoding="utf-8")
        redo = self.load_json(EVALS / "redo.json")["cases"][0]

        self.assertIn("do **not** load the durable note or old `Attempts` rows before the new attempt is finalized", workflow)
        self.assertTrue(redo["expected"]["solution_locked"])
        self.assertEqual(redo["expected"]["new_problem_index_rows"], 0)
        self.assertIn("solution_transcription", redo["must_not_load_before_submission"])
        self.assertIn("reference solution", redo["must_not_load_before_submission"])

    def test_redo_progress_comparison_uses_attempts_only(self):
        case = self.load_json(EVALS / "redo.json")["cases"][1]
        previous = case["previous"]
        current = case["current"]
        expected = case["expected"]

        self.assertEqual(current["duration_minutes"] - previous["duration_minutes"], expected["duration_delta"])
        self.assertEqual(f'{previous["hint_max"]}->{current["hint_max"]}', expected["hint_change"])
        self.assertEqual(current["estimated_score"] - previous["estimated_score"], expected["score_delta"])
        self.assertEqual(f'{previous["result_bucket"]}->{current["result_bucket"]}', expected["result_change"])
        self.assertEqual(expected["comparison_source"], "Attempts")

        workflow = (WORKFLOWS / "problem-retrieval.md").read_text(encoding="utf-8")
        self.assertIn("Only after the new Attempt is finalized", workflow)
        self.assertIn("no additional persistence layer is needed", workflow)


if __name__ == "__main__":
    unittest.main()
