#!/usr/bin/env python3
"""
Unit tests for Pre-Flight Architecture Gate & Gap Analysis Engine.
"""

import unittest

from architecture_gate import (
    ArchitectureBlueprint,
    GapSeverity,
    PreFlightGate,
    build_internship_preflight_gate,
    validate_ssot_baseline,
)


class TestPreFlightGate(unittest.TestCase):
    def setUp(self):
        self.blueprint = ArchitectureBlueprint(
            core_objective="Automate Scale AI internship application to Review stage",
            definition_of_done="All fields match SSOT with Strict Diff = 0 and visible browser halts at Review screen",
            hard_constraints=["Zero Auto-Submit", "Visible Whale Browser", "SSOT Immutability"],
            data_flow=["Raw SSOT", "Text Normalizer", "Browser Fill", "Reconciliation Engine"],
            state_and_error_management=["Failure Cache", "Retry up to 3 times", "DOM reset on mismatch"],
            tool_mapping=["CDP 9222", "reconciliation_engine.py", "text_normalizer.py"],
        )
        self.gate = PreFlightGate(self.blueprint)

    def test_blueprint_completeness(self):
        self.assertTrue(self.blueprint.is_complete())

        incomplete = ArchitectureBlueprint(core_objective="Some task", definition_of_done="")
        self.assertFalse(incomplete.is_complete())
        gate_incomplete = PreFlightGate(incomplete)
        status = gate_incomplete.can_execute()
        self.assertFalse(status.can_proceed)
        self.assertEqual(status.status, "Awaiting Clarification")

    def test_ready_when_gap_score_zero(self):
        self.assertEqual(self.gate.calculate_gap_score(), 0)
        status = self.gate.can_execute()
        self.assertTrue(status.can_proceed)
        self.assertEqual(status.status, "Ready")

    def test_critical_gap_blocks_execution(self):
        self.gate.register_gap(
            dimension="Dependencies & Prerequisites",
            description="Whale browser CDP port 9222 not running",
            remedy="Launch whale.exe with --remote-debugging-port=9222",
            severity=GapSeverity.CRITICAL,
        )
        self.assertEqual(self.gate.calculate_gap_score(), 1)
        status = self.gate.can_execute()
        self.assertFalse(status.can_proceed)
        self.assertEqual(status.status, "Awaiting Clarification")

    def test_resolve_gap_enables_execution(self):
        self.gate.register_gap(
            dimension="Input Completeness",
            description="Resume PDF path needs validation",
            remedy="Check file existence on disk",
            severity=GapSeverity.CRITICAL,
        )
        self.assertFalse(self.gate.can_execute().can_proceed)

        resolved = self.gate.resolve_gap("Input Completeness", "PDF verified at 01_Resumes/Kyubin_Yun_Resume_2027.pdf")
        self.assertTrue(resolved)
        self.assertEqual(self.gate.calculate_gap_score(), 0)
        self.assertTrue(self.gate.can_execute().can_proceed)

    def test_minor_gap_with_assumption_allows_execution(self):
        self.gate.register_gap(
            dimension="Edge Cases & Failure Modes",
            description="Unknown dropdown delay behavior",
            remedy="Use fallback explicit wait of 3000ms",
            severity=GapSeverity.MINOR,
            applied_assumption="Defaulting to 3000ms explicit wait",
        )
        self.assertEqual(self.gate.calculate_gap_score(), 0)
        status = self.gate.can_execute()
        self.assertTrue(status.can_proceed)
        self.assertEqual(status.status, "Ready with Assumptions")

    def test_unknown_dimension_raises_error(self):
        with self.assertRaises(ValueError):
            self.gate.register_gap(dimension="NonExistentDimension", description="Invalid", remedy="None")

    def test_generate_review_report(self):
        self.gate.register_gap(
            dimension="Verification Loop",
            description="Missing post-write inspection",
            remedy="Hook into reconciliation_engine.py",
            severity=GapSeverity.CRITICAL,
        )
        report = self.gate.generate_review_report()
        self.assertIn("[Architecture & Pre-Flight Review]", report)
        self.assertIn("작업 목적 및 DoD:", report)
        self.assertIn("제안 시스템 구조:", report)
        self.assertIn("식별된 잠재 누락/위험 요소:", report)
        self.assertIn("[Verification Loop]", report)
        self.assertIn("실행 여부: [Awaiting Clarification]", report)

    def test_build_internship_preflight_gate_default_ready(self):
        gate = build_internship_preflight_gate()
        self.assertEqual(gate.calculate_gap_score(), 0)
        status = gate.can_execute()
        self.assertTrue(status.can_proceed)
        self.assertEqual(status.status, "Ready")
        report = gate.generate_review_report()
        self.assertIn("[Architecture & Pre-Flight Review]", report)
        self.assertIn("실행 여부: [Ready]", report)

    def test_build_internship_preflight_gate_with_company(self):
        gate = build_internship_preflight_gate(company="scale_ai")
        self.assertEqual(gate.calculate_gap_score(), 0)
        status = gate.can_execute()
        self.assertTrue(status.can_proceed)
        self.assertIn("SCALE_AI", gate.blueprint.core_objective)

    def test_build_internship_preflight_gate_missing_browser_blocks(self):
        gate = build_internship_preflight_gate(override_checks={"browser_installed": False})
        self.assertGreater(gate.calculate_gap_score(), 0)
        status = gate.can_execute()
        self.assertFalse(status.can_proceed)
        self.assertEqual(status.status, "Awaiting Clarification")
        self.assertIn("critical gap(s) unresolved", status.reason)

    def test_build_internship_preflight_gate_missing_resume_blocks(self):
        gate = build_internship_preflight_gate(override_checks={"resume_exists": False})
        self.assertGreater(gate.calculate_gap_score(), 0)
        status = gate.can_execute()
        self.assertFalse(status.can_proceed)
        self.assertEqual(status.status, "Awaiting Clarification")

    def test_build_internship_preflight_gate_invalid_ssot_blocks(self):
        gate = build_internship_preflight_gate(override_checks={"ssot_valid": False})
        self.assertGreater(gate.calculate_gap_score(), 0)
        status = gate.can_execute()
        self.assertFalse(status.can_proceed)
        self.assertEqual(status.status, "Awaiting Clarification")

    def test_both_browser_and_resume_missing_registers_two_gaps(self):
        gate = build_internship_preflight_gate(override_checks={"browser_installed": False, "resume_exists": False})
        self.assertEqual(gate.calculate_gap_score(), 2)
        status = gate.can_execute()
        self.assertFalse(status.can_proceed)
        self.assertEqual(status.status, "Awaiting Clarification")
        report = gate.generate_review_report()
        self.assertIn("Visible browser", report)
        self.assertIn("Resume PDF not found", report)

    def test_unknown_company_without_url_blocks_execution(self):
        gate = build_internship_preflight_gate(company="unregistered_xyz_corp")
        self.assertGreater(gate.calculate_gap_score(), 0)
        status = gate.can_execute()
        self.assertFalse(status.can_proceed)
        self.assertEqual(status.status, "Awaiting Clarification")
        report = gate.generate_review_report()
        self.assertIn("Unknown target company 'unregistered_xyz_corp'", report)

    def test_unknown_company_with_url_passes(self):
        gate = build_internship_preflight_gate(company="unregistered_xyz_corp", target_url="https://xyzcorp.com/apply")
        self.assertEqual(gate.calculate_gap_score(), 0)
        status = gate.can_execute()
        self.assertTrue(status.can_proceed)
        self.assertEqual(status.status, "Ready")

    def test_validate_ssot_baseline_catches_errors(self):
        from reconciliation_engine import SSOT_CANDIDATE_BASELINE

        valid, errors = validate_ssot_baseline(SSOT_CANDIDATE_BASELINE)
        self.assertTrue(valid, f"Expected baseline to be valid, got errors: {errors}")
        self.assertEqual(len(errors), 0)

        # Test corrupted copy
        corrupted = dict(SSOT_CANDIDATE_BASELINE)
        corrupted["degree"] = "BA"
        corrupted["preferred_name"] = "Jeff"
        corrupted["workday_password"] = "short"
        corrupted["work_authorization"] = "No"
        valid_bad, errors_bad = validate_ssot_baseline(corrupted)
        self.assertFalse(valid_bad)
        self.assertGreaterEqual(len(errors_bad), 4)


if __name__ == "__main__":
    unittest.main()
