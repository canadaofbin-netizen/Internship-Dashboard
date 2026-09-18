#!/usr/bin/env python3
"""
Unit tests for Ground-Truth Integrity & Reconciliation Engine.
"""

import unittest

from reconciliation_engine import (
    SSOT_CANDIDATE_BASELINE,
    AuditRecord,
    FailureCache,
    ReconciliationEngine,
)


class TestFailureCache(unittest.TestCase):
    def setUp(self):
        self.cache = FailureCache()

    def test_record_and_get_remedy(self):
        self.cache.record_failure(
            field_type="text_input",
            failure_mode="TEXT_APPENDED_OVERWRITE_FAILED",
            remedy="FORCE_SELECT_ALL_BACKSPACE_CLEAR",
        )
        self.assertTrue(self.cache.has_remedy("text_input"))
        self.assertEqual(self.cache.get_remedy("text_input"), "FORCE_SELECT_ALL_BACKSPACE_CLEAR")
        self.assertIsNone(self.cache.get_remedy("unknown_type"))

    def test_field_specific_remedy_precedence(self):
        self.cache.record_failure("combobox", "DROPDOWN_MISMATCH", "GENERIC_COMBO_REMEDY")
        self.cache.record_failure(
            "combobox", "STALE_CONTAINER", "SPECIFIC_SPONSORSHIP_REMEDY", field_name="sponsorship"
        )

        # Generic combobox gets generic remedy
        self.assertEqual(self.cache.get_remedy("combobox", field_name="gender"), "GENERIC_COMBO_REMEDY")
        # Specific field gets specific remedy
        self.assertEqual(self.cache.get_remedy("combobox", field_name="sponsorship"), "SPECIFIC_SPONSORSHIP_REMEDY")

    def test_clear_cache(self):
        self.cache.record_failure("select", "MISMATCH", "RESELECT")
        self.cache.clear()
        self.assertFalse(self.cache.has_remedy("select"))
        self.assertEqual(len(self.cache.history), 0)


class TestReconciliationEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ReconciliationEngine(max_retries=3)

    def test_payload_parsing(self):
        raw = {"name": "  Kyubin Yun  \r\n", "count": 42, "address": "40 Merchant St\r\nLondon"}
        parsed = self.engine.parse_payload(raw)
        self.assertEqual(parsed["name"], "Kyubin Yun")
        self.assertEqual(parsed["count"], 42)
        self.assertEqual(parsed["address"], "40 Merchant St\nLondon")

    def test_calculate_diff_exact_match(self):
        self.assertEqual(self.engine.calculate_diff("London", "London"), 0)
        self.assertEqual(self.engine.calculate_diff(123, 123), 0)
        self.assertEqual(self.engine.calculate_diff(True, True), 0)

    def test_calculate_diff_whitespace_normalization(self):
        # Trims trailing spaces and normalizes \r\n to \n
        expected = "• First bullet   \n• Second bullet"
        actual = "• First bullet\r\n• Second bullet   "
        self.assertEqual(self.engine.calculate_diff(expected, actual), 0)

    def test_calculate_diff_numeric_coercion(self):
        # Numeric vs string equality
        self.assertEqual(self.engine.calculate_diff(2028, "2028"), 0)
        self.assertEqual(self.engine.calculate_diff("2028", 2028), 0)
        self.assertEqual(self.engine.calculate_diff(2028, 2029), 1)

    def test_calculate_diff_boolean_coercion(self):
        # Boolean vs string representations
        self.assertEqual(self.engine.calculate_diff(True, "Checked (True)"), 0)
        self.assertEqual(self.engine.calculate_diff(True, "true"), 0)
        self.assertEqual(self.engine.calculate_diff(True, "Checked"), 0)
        self.assertEqual(self.engine.calculate_diff(False, "Unchecked (False)"), 0)
        self.assertEqual(self.engine.calculate_diff(False, "false"), 0)
        self.assertEqual(self.engine.calculate_diff(True, "Unchecked (False)"), 1)

    def test_calculate_diff_phone_normalization(self):
        # Phone spacing and formatting variations
        self.assertEqual(self.engine.calculate_diff("+44 7787 442404", "+447787442404"), 0)
        self.assertEqual(self.engine.calculate_diff("+44 7787 442404", "+44 7787-442404"), 0)
        self.assertEqual(self.engine.calculate_diff("+44 7787 442404", "+1 7787 442404"), 1)

    def test_calculate_diff_empty_and_none(self):
        # None vs empty string
        self.assertEqual(self.engine.calculate_diff("", None), 0)
        self.assertEqual(self.engine.calculate_diff(None, ""), 0)
        self.assertEqual(self.engine.calculate_diff(None, None), 0)
        self.assertEqual(self.engine.calculate_diff("value", None), 1)

    def test_calculate_diff_mismatch(self):
        self.assertEqual(self.engine.calculate_diff("London", "Little London"), 1)
        self.assertEqual(self.engine.calculate_diff("Male", "Female"), 1)
        self.assertEqual(self.engine.calculate_diff(True, False), 1)

    def test_execute_and_reconcile_happy_path(self):
        mock_ui_state = {}

        def mock_writer(field, val, remedy):
            mock_ui_state[field] = val
            return True

        def mock_reader(field):
            return mock_ui_state.get(field)

        ok, record = self.engine.execute_and_reconcile(
            field_name="email",
            expected_value="zcjtyun@ucl.ac.uk",
            field_type="text_input",
            writer_fn=mock_writer,
            reader_fn=mock_reader,
        )
        self.assertTrue(ok)
        self.assertEqual(record.status, "MATCH")
        self.assertEqual(record.attempts, 1)

    def test_execute_and_reconcile_self_healing_retry(self):
        """
        Simulates defect on attempt 1 (e.g. text appended),
        then FailureCache remedy applied on attempt 2 successfully.
        """
        self.engine.failure_cache.clear()
        mock_ui_state = {"location": "Little London"}
        attempts_seen = []

        def mock_writer(field, val, remedy):
            attempts_seen.append(remedy)
            if remedy == "FILTER_ACTIVE_NON_LEAVING_CONTAINER_AND_EXACT_MATCH":
                mock_ui_state[field] = val
            else:
                mock_ui_state[field] = "Little London"
            return True

        def mock_reader(field):
            return mock_ui_state.get(field)

        ok, record = self.engine.execute_and_reconcile(
            field_name="location",
            expected_value="London, England, United Kingdom",
            field_type="combobox",
            writer_fn=mock_writer,
            reader_fn=mock_reader,
        )
        self.assertTrue(ok)
        self.assertEqual(record.status, "MATCH")
        self.assertEqual(record.attempts, 2)
        self.assertIn("FILTER_ACTIVE_NON_LEAVING_CONTAINER_AND_EXACT_MATCH", attempts_seen)

    def test_execute_and_reconcile_exhausted_retries_with_writer_failure(self):
        # Stubborn mismatch where writer also returns False
        def mock_writer(field, val, remedy):
            return False

        def mock_reader(field):
            return "Persistent Error"

        ok, record = self.engine.execute_and_reconcile(
            field_name="gender",
            expected_value="Male",
            field_type="select",
            writer_fn=mock_writer,
            reader_fn=mock_reader,
        )
        self.assertFalse(ok)
        self.assertEqual(record.status, "MISMATCH")
        self.assertEqual(record.attempts, 3)
        self.assertIn("Writer function returned failure", record.diagnostics)

    def test_submission_gate_pass_and_block(self):
        engine = ReconciliationEngine()
        # Case 1: Empty audit
        passed, text = engine.verify_submission_gate()
        self.assertFalse(passed)
        self.assertIn("BLOCK", text)

        # Case 2: One match, one mismatch
        engine.audit_log.append(AuditRecord("name", "Kyubin", "Kyubin", "MATCH"))
        engine.audit_log.append(AuditRecord("gender", "Male", "Female", "MISMATCH"))
        passed, text = engine.verify_submission_gate()
        self.assertFalse(passed)
        self.assertIn("MISMATCH", text)
        self.assertIn("BLOCKED", text)

        # Case 3: 100% Match
        engine.audit_log.clear()
        engine.audit_log.append(AuditRecord("name", "Kyubin", "Kyubin", "MATCH"))
        engine.audit_log.append(AuditRecord("gender", "Male", "Male", "MATCH"))
        passed, text = engine.verify_submission_gate()
        self.assertTrue(passed)
        self.assertIn("PASSED", text)
        self.assertIn("Field: name | Expected: Kyubin | Actual: Kyubin | Status: MATCH", text)

    def test_ssot_baseline_integrity(self):
        self.assertEqual(SSOT_CANDIDATE_BASELINE["email"], "zcjtyun@ucl.ac.uk")
        self.assertEqual(SSOT_CANDIDATE_BASELINE["phone_prefix"], "+44")
        self.assertEqual(SSOT_CANDIDATE_BASELINE["graduation_year"], "2028")
        self.assertEqual(SSOT_CANDIDATE_BASELINE["workday_password"], "Jeff0825!!!!")
        self.assertEqual(SSOT_CANDIDATE_BASELINE["gender_tiktok"], "Man")
        self.assertEqual(SSOT_CANDIDATE_BASELINE["race_tiktok"], "East Asian / East Asian British")
        self.assertEqual(SSOT_CANDIDATE_BASELINE["preferred_name"], "")
        self.assertEqual(SSOT_CANDIDATE_BASELINE["degree"], "BSc")
        self.assertEqual(SSOT_CANDIDATE_BASELINE["korean_name"], "윤규빈")
        self.assertIn("UK Student Route", SSOT_CANDIDATE_BASELINE["sponsorship_explanation"])
        self.assertIn("Graduate Route", SSOT_CANDIDATE_BASELINE["sponsorship_explanation"])
        self.assertTrue(SSOT_CANDIDATE_BASELINE["language_english_native"])
        self.assertTrue(SSOT_CANDIDATE_BASELINE["language_korean_native"])

    def test_calculate_diff_nbsp_normalization(self):
        self.assertEqual(self.engine.calculate_diff("Kyubin Yun", "Kyubin\u00a0Yun"), 0)
        self.assertEqual(self.engine.calculate_diff("40 Merchant St,\u00a0London", "40 Merchant St, London"), 0)

    def test_calculate_diff_multi_space_collapsing(self):
        self.assertEqual(self.engine.calculate_diff("Kyubin   Yun", "Kyubin Yun"), 0)

    def test_failure_cache_defaults_active(self):
        fc = FailureCache()
        self.assertTrue(fc.has_remedy("text_input"))
        self.assertTrue(fc.has_remedy("combobox"))
        self.assertTrue(fc.has_remedy("react_select"))
        self.assertTrue(fc.has_remedy("password"))
        self.assertEqual(fc.get_remedy("text_input"), "FORCE_SELECT_ALL_BACKSPACE_CLEAR")
        self.assertEqual(fc.get_remedy("combobox"), "FILTER_ACTIVE_NON_LEAVING_CONTAINER_AND_EXACT_MATCH")
        self.assertEqual(fc.get_remedy("react_select"), "REACT_SELECT_CLEAR_AND_SELECT")

    def test_calculate_diff_uk_phone_formats(self):
        # National without leading 0 vs space-separated
        self.assertEqual(self.engine.calculate_diff("7787442404", "7787 442404"), 0)
        # UK local (07...) vs international (+44 7...)
        self.assertEqual(self.engine.calculate_diff("07787442404", "+44 7787 442404"), 0)
        # Full international with punctuation
        self.assertEqual(self.engine.calculate_diff("+44 7787 442404", "+44 (0) 7787-442404"), 0)
        # Different country code should mismatch
        self.assertEqual(self.engine.calculate_diff("+44 7787 442404", "+1 7787 442404"), 1)

    def test_calculate_diff_leading_zero_preservation(self):
        # Numeric coercion must not equate string IDs with leading zeros
        self.assertEqual(self.engine.calculate_diff("0123", "123"), 1)
        # But normal numeric strings should match
        self.assertEqual(self.engine.calculate_diff("2028", 2028), 0)

    def test_async_execute_and_reconcile(self):
        import asyncio

        mock_state = {"pref": "Jeff"}

        async def mock_writer(field, val, remedy):
            mock_state[field] = val
            return True

        async def mock_reader(field):
            return mock_state.get(field)

        async def run_test():
            ok, rec = await self.engine.async_execute_and_reconcile(
                field_name="pref",
                expected_value="",
                field_type="text_input",
                writer_fn=mock_writer,
                reader_fn=mock_reader,
            )
            return ok, rec

        ok, rec = asyncio.run(run_test())
        self.assertTrue(ok)
        self.assertEqual(rec.status, "MATCH")
        self.assertEqual(mock_state["pref"], "")


if __name__ == "__main__":
    unittest.main()
