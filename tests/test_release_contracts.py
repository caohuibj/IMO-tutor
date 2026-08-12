import json
import re
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "imo-tutor"
PROJECT = ROOT / "project"


class ReleaseContractTests(unittest.TestCase):
    def test_version_and_manifest_are_release_candidate_synced(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))

        self.assertEqual(manifest["version"], version)
        self.assertRegex(version, re.compile(r"^1\.0\.0(?:-rc\.[0-9]+)?$"))
        self.assertEqual(manifest["data_contract_version"], 1)
        self.assertEqual(manifest["taxonomy_version"], 1)

    def test_student_docs_are_present_and_linked(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for name in ["SETUP.md", "PROJECT_GUIDE.md", "USER_GUIDE.md", "PROJECT_INSTRUCTIONS.md"]:
            self.assertTrue((PROJECT / name).exists(), name)
            self.assertIn(f"project/{name}", readme)

    def test_v1_scope_is_single_student_and_excludes_classroom_features(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("single-user learning tool", readme)
        self.assertIn("v1.x 明确不做", readme)
        for excluded in [
            "teacher profile",
            "班级管理",
            "共享学生数据库",
            "教师 dashboard",
            "学生权限系统",
            "多人协作 Project",
            "教师统计后台",
        ]:
            self.assertIn(excluded, readme)

    def test_supported_environment_is_capability_gated(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        setup = (PROJECT / "SETUP.md").read_text(encoding="utf-8")

        self.assertIn("capability-gated", readme)
        self.assertIn("Plugins → Skills → Create → Upload from your computer", readme)
        self.assertIn("Google Drive / Docs / Sheets", readme)
        self.assertIn("## 0. Preflight", setup)
        self.assertIn("Upload from your computer", setup)
        self.assertIn("Google Drive / Docs / Sheets 的写操作可用", setup)
        self.assertIn("只读连接不足", setup)

    def test_workspace_sidebar_and_chat_lifecycle_are_documented(self):
        guide = (PROJECT / "PROJECT_GUIDE.md").read_text(encoding="utf-8")
        user = (PROJECT / "USER_GUIDE.md").read_text(encoding="utf-8")
        setup = (PROJECT / "SETUP.md").read_text(encoding="utf-8")

        for text in [guide, user]:
            self.assertIn("00｜使用说明", text)
            self.assertIn("01｜题库检索", text)

        self.assertIn("一道题一个工作 Chat", guide)
        self.assertIn("完成即归档", guide)
        self.assertIn("P000237-A02｜Redo", guide)
        self.assertIn("Pin chat", guide)
        self.assertIn("Pin 到 sidebar", setup)
        self.assertIn("一题一 Chat", user)
        self.assertIn("重做 P000237", user)

    def test_setup_covers_fresh_student_acceptance_path(self):
        setup = (PROJECT / "SETUP.md").read_text(encoding="utf-8")
        for required in [
            "GitHub Release",
            "imo-tutor-v<version>.zip",
            "Problem_Index.csv",
            "Attempts.csv",
            "PROJECT_INSTRUCTIONS.md",
            "IMO Tutor Data",
            "IMO Learning DB",
            "Problem_Index",
            "Attempts",
            "00｜使用说明",
            "01｜题库检索",
            "SOLUTION_LOCKED",
            "ARCHIVED",
            "P000001-A01",
            "P000001-A02",
            "新 Chat 检索测试",
            "重做测试",
            "迁移到新的 ChatGPT Project",
        ]:
            self.assertIn(required, setup)

        self.assertIn("目标 ChatGPT account/workspace/surface", setup)
        self.assertNotIn("在新的 ChatGPT Project 安装", setup)

    def test_installable_skill_bundle_has_one_root_and_no_private_files(self):
        self.assertTrue((SKILL / "SKILL.md").exists())
        self.assertTrue((SKILL / "workflows").is_dir())
        self.assertTrue((SKILL / "references").is_dir())

        forbidden_names = {
            ".env",
            "credentials.json",
            "service-account.json",
            "client_secret.json",
            "token.json",
        }
        files = [path for path in SKILL.rglob("*") if path.is_file()]
        self.assertGreater(len(files), 3)
        for path in files:
            self.assertNotIn(path.name.lower(), forbidden_names)

        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp) / "imo-tutor-test.zip"
            with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                for path in files:
                    zf.write(path, Path("imo-tutor") / path.relative_to(SKILL))

            with zipfile.ZipFile(archive) as zf:
                names = zf.namelist()

        self.assertIn("imo-tutor/SKILL.md", names)
        self.assertTrue(all(name.startswith("imo-tutor/") for name in names))
        self.assertFalse(any(name.startswith("project/") for name in names))

    def test_release_workflow_validates_packages_and_attaches_onboarding_assets(self):
        workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
        self.assertIn("tags:", workflow)
        self.assertIn("'v*'", workflow)
        self.assertIn("python -m unittest discover -s tests", workflow)
        self.assertIn('test "${GITHUB_REF_NAME}" = "v${VERSION}"', workflow)
        self.assertIn("cp -R skills/imo-tutor/. dist/imo-tutor/", workflow)
        self.assertIn('zip -qr "imo-tutor-v${VERSION}.zip" imo-tutor', workflow)
        self.assertIn('"dist/imo-tutor-v${VERSION}.zip"', workflow)
        for asset in [
            "skills/imo-tutor/references/Problem_Index.csv",
            "skills/imo-tutor/references/Attempts.csv",
            "project/SETUP.md",
            "project/PROJECT_INSTRUCTIONS.md",
            "project/PROJECT_GUIDE.md",
            "project/USER_GUIDE.md",
        ]:
            self.assertIn(asset, workflow)
        self.assertIn("gh \"${args[@]}\"", workflow)
        self.assertIn("--prerelease", workflow)


if __name__ == "__main__":
    unittest.main()
