#!/usr/bin/env python3
"""
Comprehensive integrity test for workspace directives, rule indexing, and link validation.
Ensures zero broken links, exact AGENTS.md synchronization, and full protocol coverage.
"""

import re
import unittest
import urllib.parse
from pathlib import Path

WORKSPACE_ROOT = Path(r"G:\My Drive\Kyubin_Yun_Workspace\04_Internship")


class TestWorkspaceIntegrity(unittest.TestCase):
    def test_agents_md_byte_identity(self):
        root_agents = WORKSPACE_ROOT / "AGENTS.md"
        dot_agents = WORKSPACE_ROOT / ".agents" / "AGENTS.md"

        self.assertTrue(root_agents.exists(), "Root AGENTS.md must exist")
        self.assertTrue(dot_agents.exists(), ".agents/AGENTS.md must exist")

        root_bytes = root_agents.read_bytes()
        dot_bytes = dot_agents.read_bytes()
        self.assertEqual(root_bytes, dot_bytes, "AGENTS.md and .agents/AGENTS.md must be 100% identical")

    def test_all_file_uri_links_valid(self):
        broken_links = []
        total_checked = 0

        for md_file in WORKSPACE_ROOT.rglob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            links = re.findall(r"file:///([^\s\)\"\'>]+)", content)
            for link in links:
                total_checked += 1
                local_path = Path(urllib.parse.unquote(link))
                if not local_path.exists():
                    broken_links.append((str(md_file), link, str(local_path)))

        self.assertGreater(total_checked, 50, "Should check at least 50 links")
        self.assertEqual(len(broken_links), 0, f"Broken links found: {broken_links}")

    def test_all_rules_indexed_in_agents_md(self):
        agents_content = (WORKSPACE_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        rules_dir = WORKSPACE_ROOT / ".agents" / "rules"

        for rule_file in rules_dir.glob("*.md"):
            self.assertIn(rule_file.name, agents_content, f"Rule {rule_file.name} must be indexed in AGENTS.md")

    def test_all_skills_indexed_in_agents_md(self):
        agents_content = (WORKSPACE_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        skills_dir = WORKSPACE_ROOT / ".agents" / "skills"

        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                self.assertIn(
                    f".agents/skills/{skill_dir.name}/SKILL.md",
                    agents_content,
                    f"Skill {skill_dir.name} must be indexed in AGENTS.md",
                )

    def test_architecture_gap_analysis_section_coverage(self):
        agents_content = (WORKSPACE_ROOT / "AGENTS.md").read_text(encoding="utf-8")

        # Must have Section 6 with full 5-dimension table
        self.assertIn("## 6. 컨텍스트 기반 아키텍처 설계 및 갭 분석 프로토콜", agents_content)
        self.assertIn("Dependencies & Prerequisites", agents_content)
        self.assertIn("Input Completeness", agents_content)
        self.assertIn("Edge Cases & Failure Modes", agents_content)
        self.assertIn("Verification Loop", agents_content)
        self.assertIn("Side Effects & Reversibility", agents_content)
        self.assertIn("[Architecture & Pre-Flight Review]", agents_content)
        self.assertIn("Gap Score = 0", agents_content)
        self.assertIn("/boost", agents_content)

    def test_subproject_agents_md_coverage(self):
        sub_agents = (WORKSPACE_ROOT / "2027_Summer2_Internship" / ".agents" / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("## 7. 컨텍스트 기반 아키텍처 설계 및 갭 분석 프로토콜", sub_agents)
        self.assertIn("Dependencies & Prerequisites", sub_agents)
        self.assertIn("[Architecture & Pre-Flight Review]", sub_agents)
        self.assertIn("context-driven-architecture-gap-analysis.md", sub_agents)
        self.assertIn("meta-prompt-architecture-gap-analysis.md", sub_agents)

    def test_index_md_coverage(self):
        index_content = (WORKSPACE_ROOT / "INDEX.md").read_text(encoding="utf-8")
        self.assertIn("context-driven-architecture-gap-analysis.md", index_content)
        self.assertIn("meta-prompt-architecture-gap-analysis.md", index_content)
        self.assertIn("excel-tracker-architecture.md", index_content)
        self.assertIn("workspace-linting.md", index_content)

    def test_ground_truth_consistency_across_rules_and_code(self):
        from reconciliation_engine import SSOT_CANDIDATE_BASELINE

        self.assertEqual(SSOT_CANDIDATE_BASELINE["legal_name"], "Kyubin Yun")
        self.assertEqual(SSOT_CANDIDATE_BASELINE["preferred_name"], "")
        self.assertEqual(SSOT_CANDIDATE_BASELINE["email"], "zcjtyun@ucl.ac.uk")
        self.assertEqual(SSOT_CANDIDATE_BASELINE["workday_password"], "Jeff0825!!!!")
        self.assertEqual(SSOT_CANDIDATE_BASELINE["standard_password"], "Jeff0825!!")
        self.assertEqual(SSOT_CANDIDATE_BASELINE["phone_prefix"], "+44")
        self.assertEqual(SSOT_CANDIDATE_BASELINE["degree"], "BSc")
        self.assertEqual(SSOT_CANDIDATE_BASELINE["korean_name"], "윤규빈")

        # Verify candidate-ground-truth.md has exact matches
        gt_rule = (WORKSPACE_ROOT / ".agents" / "rules" / "candidate-ground-truth.md").read_text(encoding="utf-8")
        self.assertIn("Kyubin Yun", gt_rule)
        self.assertIn("zcjtyun@ucl.ac.uk", gt_rule)
        self.assertIn("Jeff0825!!!!", gt_rule)
        self.assertIn("Jeff0825!!", gt_rule)
        self.assertIn("+44 7787 442404", gt_rule)
        self.assertIn("*(None / Blank)*", gt_rule)

    def test_no_obsolete_ucl_summer2intern_paths(self):
        violations = []
        this_file = Path(__file__).resolve()
        for ext in ("*.py", "*.md"):
            for path in WORKSPACE_ROOT.rglob(ext):
                # Skip pytest cache, pycache, or this test file itself
                if path.resolve() == this_file or ".pytest_cache" in path.parts or "__pycache__" in path.parts:
                    continue
                try:
                    text = path.read_text(encoding="utf-8")
                    if "UCL/Summer2intern" in text or "UCL\\Summer2intern" in text:
                        violations.append(str(path))
                except Exception:
                    pass
        self.assertEqual(len(violations), 0, f"Found obsolete UCL/Summer2intern paths in: {violations}")

    def test_cookiecutter_data_science_structure(self):
        sub_root = WORKSPACE_ROOT / "2027_Summer2_Internship"
        required_dirs = [
            sub_root / "data" / "raw",
            sub_root / "data" / "interim",
            sub_root / "data" / "processed",
            sub_root / "notebooks",
            sub_root / "src" / "data",
            sub_root / "src" / "features",
            sub_root / "src" / "models",
            sub_root / "src" / "visualization",
            sub_root / "reports",
            sub_root / "Templates",
        ]
        for d in required_dirs:
            self.assertTrue(d.is_dir(), f"Required CCDS directory missing: {d}")

    def test_markdown_table_integrity(self):
        """Ensures markdown tables have no accidental blank lines splitting rows."""
        corrupted_tables = []
        for md_file in WORKSPACE_ROOT.rglob("*.md"):
            if ".pytest_cache" in md_file.parts or ".ruff_cache" in md_file.parts:
                continue
            lines = md_file.read_text(encoding="utf-8").splitlines()
            for i in range(len(lines) - 2):
                if lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                    if lines[i + 1].strip() == "":
                        next_line = lines[i + 2].strip()
                        if next_line.startswith("|") and next_line.endswith("|"):
                            if i + 3 < len(lines) and re.match(r"\|[\s\-:]+\|", lines[i + 3].strip()):
                                continue
                            corrupted_tables.append((str(md_file), i + 2, lines[i].strip(), next_line))

        self.assertEqual(
            len(corrupted_tables), 0, f"Found corrupted markdown tables with blank line breaks: {corrupted_tables}"
        )

    def test_all_rules_frontmatter_presence(self):
        """Ensures all rule files across root and subproject have valid YAML frontmatter."""
        rule_dirs = [
            WORKSPACE_ROOT / ".agents" / "rules",
            WORKSPACE_ROOT / "2027_Summer2_Internship" / ".agents" / "rules",
        ]
        for r_dir in rule_dirs:
            for rule_file in r_dir.glob("*.md"):
                content = rule_file.read_text(encoding="utf-8")
                self.assertTrue(
                    content.startswith("---\n"),
                    f"Rule file {rule_file} must start with YAML frontmatter delimiter '---'",
                )
                self.assertIn(
                    "description:",
                    content,
                    f"Rule file {rule_file} must contain a description field in frontmatter",
                )

    def test_interlinked_bidirectional_tree(self):
        """Ensures all rules and subproject directives link back to main AGENTS.md."""
        for rule_file in (WORKSPACE_ROOT / ".agents" / "rules").glob("*.md"):
            content = rule_file.read_text(encoding="utf-8")
            self.assertIn(
                "AGENTS.md",
                content,
                f"Rule {rule_file.name} must contain a backlink to AGENTS.md",
            )

        sub_agents = (WORKSPACE_ROOT / "2027_Summer2_Internship" / ".agents" / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("04_Internship AGENTS.md", sub_agents, "Subproject AGENTS.md must link to parent AGENTS.md")

    def test_telemetry_columns_hidden_in_tracker(self):
        """Ensures telemetry columns G to K are hidden in 2.Research_Database sheet."""
        import openpyxl

        tracker_path = WORKSPACE_ROOT / "2027_Summer2_Internship" / "2027_BCI_Internship_Tracker.xlsx"
        wb = openpyxl.load_workbook(tracker_path)
        ws = wb["2.Research_Database"]
        for col_letter in ["G", "H", "I", "J", "K"]:
            self.assertTrue(
                ws.column_dimensions[col_letter].hidden,
                f"Telemetry column {col_letter} in 2.Research_Database must be hidden",
            )

    def test_subproject_standard_files(self):
        """Ensures 2027_Summer2_Internship contains standard README.md and .gitignore."""
        sub_root = WORKSPACE_ROOT / "2027_Summer2_Internship"
        self.assertTrue((sub_root / "README.md").is_file(), "Subproject README.md must exist")
        self.assertTrue((sub_root / ".gitignore").is_file(), "Subproject .gitignore must exist")


if __name__ == "__main__":
    unittest.main()
