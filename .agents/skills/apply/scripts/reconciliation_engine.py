#!/usr/bin/env python3
"""
Ground-Truth Integrity & Auto-Correction Engine (Reconciliation Engine)
Enforces a 4-step Read-After-Write & Strict Diff Reconciliation loop
between Single Source of Truth (SSOT) and live UI/screen state.
"""

import re
import sys
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


@dataclass
class AuditRecord:
    field_name: str
    expected_value: Any
    actual_value: Any
    status: str  # "MATCH" or "MISMATCH"
    attempts: int = 1
    diagnostics: str | None = None

    def to_audit_line(self) -> str:
        exp_str = str(self.expected_value).replace("\n", "\\n")
        act_str = str(self.actual_value).replace("\n", "\\n")
        return f"Field: {self.field_name} | Expected: {exp_str} | Actual: {act_str} | Status: {self.status}"


STANDARD_REMEDIES: dict[str, str] = {
    "text_input": "FORCE_SELECT_ALL_BACKSPACE_CLEAR",
    "combobox": "FILTER_ACTIVE_NON_LEAVING_CONTAINER_AND_EXACT_MATCH",
    "select": "GENERIC_DOM_SETTER_RETRY",
    "react_select": "REACT_SELECT_CLEAR_AND_SELECT",
    "checkbox": "FORCE_CLICK_AND_DISPATCH_CHANGE",
    "textarea": "DISPATCH_SYNTHETIC_EVENTS_AND_BLUR",
    "ud_select": "FILTER_ACTIVE_NON_LEAVING_CONTAINER_AND_EXACT_MATCH",
    "password": "FORCE_SELECT_ALL_BACKSPACE_CLEAR",
}


class FailureCache:
    """
    Session-level cache recording failure patterns and remedial actions.
    Enables Failure-Mode Reflection to prevent recurring errors.
    Supports both generic field_type remedies and field_name-specific remedies.
    """

    def __init__(self, populate_defaults: bool = True):
        self.cache: dict[str, str] = dict(STANDARD_REMEDIES) if populate_defaults else {}
        self.history: list[dict[str, Any]] = []

    @classmethod
    def with_standard_remedies(cls) -> "FailureCache":
        return cls(populate_defaults=True)

    def record_failure(self, field_type: str, failure_mode: str, remedy: str, field_name: str | None = None):
        if field_name:
            self.cache[f"{field_name}:{field_type}"] = remedy
        else:
            self.cache[field_type] = remedy
        self.history.append(
            {"field_name": field_name, "field_type": field_type, "failure_mode": failure_mode, "remedy": remedy}
        )

    def get_remedy(self, field_type: str, field_name: str | None = None) -> str | None:
        if field_name and f"{field_name}:{field_type}" in self.cache:
            return self.cache[f"{field_name}:{field_type}"]
        return self.cache.get(field_type)

    def has_remedy(self, field_type: str, field_name: str | None = None) -> bool:
        if field_name and f"{field_name}:{field_type}" in self.cache:
            return True
        return field_type in self.cache

    def clear(self):
        self.cache.clear()
        self.history.clear()


class ReconciliationEngine:
    """
    Coordinates Payload Parsing, Action Execution, Read-After-Write Inspection,
    and Strict Diff Reconciliation.
    """

    def __init__(self, failure_cache: FailureCache | None = None, max_retries: int = 3):
        self.failure_cache = failure_cache or FailureCache()
        self.max_retries = max_retries
        self.audit_log: list[AuditRecord] = []

    # Step 1: Payload Parsing (입력 전 정형화)
    def parse_payload(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """
        Extracts and normalizes target fields from raw user inputs / SSOT baseline.
        Standardizes bullets, whitespace, and formatting requirements.
        """
        normalized: dict[str, Any] = {}
        for k, v in raw_data.items():
            if isinstance(v, str):
                clean_v = v.replace("\r\n", "\n").strip()
                normalized[k] = clean_v
            else:
                normalized[k] = v
        return normalized

    # Step 2 & 3 & 4: Mandatory Execution & Verification Loop
    def execute_and_reconcile(
        self,
        field_name: str,
        expected_value: Any,
        field_type: str,
        writer_fn: Callable[[str, Any, str | None], bool],
        reader_fn: Callable[[str], Any],
        custom_comparator: Callable[[Any, Any], bool] | None = None,
    ) -> tuple[bool, AuditRecord]:
        """
        Executes an input action, performs independent Read-After-Write inspection,
        and enforces strict Diff Reconciliation with adaptive retry up to max_retries.
        """
        attempts = 0
        last_actual = None
        diagnostics = None

        while attempts < self.max_retries:
            attempts += 1
            # Check FailureCache for proactive remedy (field-specific or generic)
            active_remedy = self.failure_cache.get_remedy(field_type, field_name)

            # Step 2: Action Execution
            write_ok = writer_fn(field_name, expected_value, active_remedy)
            writer_failure_msg = None if write_ok else "Writer function returned failure"

            # Step 3: Read-After-Write Inspection
            # Independently read current rendered screen state
            actual_value = reader_fn(field_name)
            last_actual = actual_value

            # Step 4: Strict Diff Reconciliation
            if custom_comparator:
                is_match = custom_comparator(expected_value, actual_value)
            else:
                is_match = self.calculate_diff(expected_value, actual_value) == 0

            if is_match:
                record = AuditRecord(
                    field_name=field_name,
                    expected_value=expected_value,
                    actual_value=actual_value,
                    status="MATCH",
                    attempts=attempts,
                    diagnostics=None,
                )
                self.audit_log.append(record)
                return True, record

            # Diagnosing discrepancy
            defect_diag = self._diagnose_defect(expected_value, actual_value, field_type)
            diagnostics = f"{writer_failure_msg} | {defect_diag}" if writer_failure_msg else defect_diag
            remedy = self._determine_remedy(defect_diag)
            self.failure_cache.record_failure(field_type, defect_diag, remedy, field_name=field_name)

        # Retries exhausted -> record MISMATCH
        record = AuditRecord(
            field_name=field_name,
            expected_value=expected_value,
            actual_value=last_actual,
            status="MISMATCH",
            attempts=attempts,
            diagnostics=diagnostics,
        )
        self.audit_log.append(record)
        return False, record

    async def async_execute_and_reconcile(
        self,
        field_name: str,
        expected_value: Any,
        field_type: str,
        writer_fn: Callable[[str, Any, str | None], Any],
        reader_fn: Callable[[str], Any],
        custom_comparator: Callable[[Any, Any], bool] | None = None,
    ) -> tuple[bool, AuditRecord]:
        """
        Asynchronous variant of execute_and_reconcile for Playwright CDP automation.
        Executes action, independently inspects live DOM state, and reconciles diffs.
        """
        import inspect

        attempts = 0
        last_actual = None
        diagnostics = None

        while attempts < self.max_retries:
            attempts += 1
            active_remedy = self.failure_cache.get_remedy(field_type, field_name)

            # Step 2: Action Execution
            write_res = writer_fn(field_name, expected_value, active_remedy)
            if inspect.isawaitable(write_res):
                write_res = await write_res
            write_ok = bool(write_res)
            writer_failure_msg = None if write_ok else "Writer function returned failure"

            # Step 3: Read-After-Write Inspection
            actual_res = reader_fn(field_name)
            if inspect.isawaitable(actual_res):
                actual_res = await actual_res
            actual_value = actual_res
            last_actual = actual_value

            # Step 4: Strict Diff Reconciliation
            if custom_comparator:
                is_match = custom_comparator(expected_value, actual_value)
            else:
                is_match = self.calculate_diff(expected_value, actual_value) == 0

            if is_match:
                record = AuditRecord(
                    field_name=field_name,
                    expected_value=expected_value,
                    actual_value=actual_value,
                    status="MATCH",
                    attempts=attempts,
                    diagnostics=None,
                )
                self.audit_log.append(record)
                return True, record

            defect_diag = self._diagnose_defect(expected_value, actual_value, field_type)
            diagnostics = f"{writer_failure_msg} | {defect_diag}" if writer_failure_msg else defect_diag
            remedy = self._determine_remedy(defect_diag)
            self.failure_cache.record_failure(field_type, defect_diag, remedy, field_name=field_name)

        record = AuditRecord(
            field_name=field_name,
            expected_value=expected_value,
            actual_value=last_actual,
            status="MISMATCH",
            attempts=attempts,
            diagnostics=diagnostics,
        )
        self.audit_log.append(record)
        return False, record

    @staticmethod
    def _to_bool(val: Any) -> bool | None:
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            s = val.strip().lower()
            if s in ["true", "checked", "checked (true)", "1", "yes"]:
                return True
            if s in ["false", "unchecked", "unchecked (false)", "0", "no"]:
                return False
        return None

    @staticmethod
    def _normalize_phone_digits(val: str) -> str | None:
        if not isinstance(val, str):
            return None
        cleaned = val.replace("\u00a0", " ").strip()
        if not re.fullmatch(r"[\+\d\s\-\(\)\.]+", cleaned):
            return None
        digits = re.sub(r"\D", "", cleaned)
        if len(digits) < 7:
            return None
        # Handle UK mobile and international variations (+44 vs 0 vs bare national 7...)
        if digits.startswith("44"):
            core = digits[2:]
            core = core.removeprefix("0")
            return f"44{core}"
        if digits.startswith("0") and len(digits) == 11:
            return f"44{digits[1:]}"
        if len(digits) == 10 and digits.startswith("7"):
            return f"44{digits}"
        return digits

    def calculate_diff(self, expected: Any, actual: Any) -> int:
        """
        Strict diff comparison: returns 0 if exact match, >0 if mismatch.
        Handles:
        1. Exact equality.
        2. None vs empty string equivalence for empty fields.
        3. Boolean states ('Checked (True)' vs True, 'false' vs False).
        4. Integer/Float vs numeric strings (e.g. 2028 vs "2028") with leading zero protection.
        5. Phone number spacing/punctuation and UK international/national normalization.
        6. String whitespace normalization (trimming trailing spaces, normalized line endings).
        """
        if expected == actual:
            return 0

        # Empty field equivalence
        if (expected is None or expected == "") and (actual is None or actual == ""):
            return 0

        # Boolean comparison
        b_exp = self._to_bool(expected)
        b_act = self._to_bool(actual)
        if b_exp is not None and b_act is not None:
            return 0 if b_exp == b_act else 1

        # Number comparison (e.g. 2028 vs "2028"), preserving leading zeros for codes/IDs
        try:
            exp_is_num = isinstance(expected, (int, float)) or (
                isinstance(expected, str) and expected.strip().isdigit()
            )
            act_is_num = isinstance(actual, (int, float)) or (isinstance(actual, str) and actual.strip().isdigit())
            if exp_is_num and act_is_num:
                if isinstance(expected, str) and isinstance(actual, str):
                    s_exp = expected.strip()
                    s_act = actual.strip()
                    if (s_exp.startswith("0") or s_act.startswith("0")) and len(s_exp) != len(s_act):
                        pass
                    elif float(s_exp) == float(s_act):
                        return 0
                elif float(expected) == float(actual):
                    return 0
        except (ValueError, TypeError):
            pass

        # Phone number normalization
        if isinstance(expected, str) and isinstance(actual, str):
            p_exp = self._normalize_phone_digits(expected)
            p_act = self._normalize_phone_digits(actual)
            if p_exp is not None and p_act is not None:
                return 0 if p_exp == p_act else 1

            # Standard string normalization (line by line trimming, whitespace collapse, \r\n to \n)
            exp_clean = expected.replace("\u00a0", " ").strip()
            act_clean = actual.replace("\u00a0", " ").strip()
            norm_exp = "\n".join(
                re.sub(r"[ \t]+", " ", line.strip()) for line in exp_clean.replace("\r\n", "\n").split("\n")
            )
            norm_act = "\n".join(
                re.sub(r"[ \t]+", " ", line.strip()) for line in act_clean.replace("\r\n", "\n").split("\n")
            )
            return 0 if norm_exp == norm_act else 1

        return 1

    def _diagnose_defect(self, expected: Any, actual: Any, field_type: str) -> str:
        if actual is None or actual == "":
            return "FIELD_EMPTY_AFTER_WRITE"

        # Check boolean defects
        b_exp = self._to_bool(expected)
        b_act = self._to_bool(actual)
        if b_exp is not None and b_act is not None and b_exp != b_act:
            return "CHECKBOX_STATE_MISMATCH"

        if isinstance(expected, str) and isinstance(actual, str):
            if expected in actual and len(actual) > len(expected):
                return "TEXT_APPENDED_OVERWRITE_FAILED"
            if actual in expected and len(actual) < len(expected):
                return "TEXT_TRUNCATED_OR_CUTOFF"
            if actual != expected:
                if field_type in ["combobox", "select", "ud_select", "react_select"]:
                    return "DROPDOWN_MISMATCH_OR_STALE_CONTAINER"
                return "VALUE_INCORRECT_OR_AUTOSELF_SELECTED"

        return "UNKNOWN_MISMATCH"

    def _determine_remedy(self, failure_mode: str) -> str:
        if failure_mode == "TEXT_APPENDED_OVERWRITE_FAILED":
            return "FORCE_SELECT_ALL_BACKSPACE_CLEAR"
        if failure_mode == "FIELD_EMPTY_AFTER_WRITE":
            return "DISPATCH_SYNTHETIC_EVENTS_AND_BLUR"
        if failure_mode in ["VALUE_INCORRECT_OR_AUTOSELF_SELECTED", "DROPDOWN_MISMATCH_OR_STALE_CONTAINER"]:
            return "FILTER_ACTIVE_NON_LEAVING_CONTAINER_AND_EXACT_MATCH"
        if failure_mode == "CHECKBOX_STATE_MISMATCH":
            return "FORCE_CLICK_AND_DISPATCH_CHANGE"
        return "GENERIC_DOM_SETTER_RETRY"

    # Step 3: Submission Gate (최종 제출 차단선)
    def verify_submission_gate(self) -> tuple[bool, str]:
        """
        Evaluates the entire audit log.
        Returns (True, audit_table) if 100% of fields MATCH (0% defect).
        Returns (False, audit_table) and BLOCKS submission if any MISMATCH exists.
        """
        if not self.audit_log:
            return False, "[Verification Audit]\nERROR: No fields were audited. Submission BLOCKED."

        lines = ["[Verification Audit]"]
        all_passed = True

        for rec in self.audit_log:
            lines.append(rec.to_audit_line())
            if rec.status != "MATCH":
                all_passed = False

        audit_table = "\n".join(lines)
        if all_passed:
            verdict = "\n>>> SUBMISSION GATE: PASSED (100% Match, 0% Defect). Ready for User Final Review."
        else:
            verdict = "\n>>> SUBMISSION GATE: BLOCKED! Discrepancies detected. Manual/auto correction required."

        return all_passed, audit_table + verdict


# Candidate Ground Truth Baseline (SSOT) Reference Helper
SSOT_CANDIDATE_BASELINE = {
    # 1. Personal & Contact Credentials
    "legal_name": "Kyubin Yun",
    "first_name": "Kyubin",
    "last_name": "Yun",
    "preferred_name": "",  # Strictly Blank (None)
    "korean_name": "윤규빈",
    "email": "zcjtyun@ucl.ac.uk",
    "phone": "+44 7787 442404",
    "phone_prefix": "+44",
    "phone_national": "7787442404",
    "uk_address": "40 Merchant St, Brent Cross, Suite 638, London, NW2 8BB",
    "address_line1": "40 Merchant St, Brent Cross, Suite 638",
    "city": "London",
    "postal_code": "NW2 8BB",
    "country": "United Kingdom",
    # 2. Education & Visa Status
    "university": "University College London (UCL)",
    "degree": "BSc",
    "degree_general": "Bachelor's degree",
    "discipline": "Psychology and Language Sciences",
    "study_period": "September 2025 – June 2028",
    "graduation_year": "2028",
    "graduation_month": "06",
    "expected_graduation": "June 2028",
    "academic_grade": "Honours (Achieved/Predicted: 70.5/100)",
    "work_authorization": "Yes",
    "sponsorship_required": "Yes",
    "visa_status": "UK Student Route Visa",
    "sponsorship_explanation": (
        "I am an undergraduate student at University College London (UCL) holding a valid "
        "UK Student Route visa, legally permitting full-time employment during university "
        "vacations for this internship without sponsorship. Upon graduation in June 2028, "
        "I am eligible for the 2-year unsponsored Graduate Route visa, granting full working "
        "rights with zero employer sponsorship required. I would only require Skilled Worker "
        "visa sponsorship thereafter for subsequent long-term permanent employment."
    ),
    # 3. Demographics & Platform Specifics
    "gender": "Male",
    "gender_tiktok": "Man",
    "disability": "No",
    "race": "Asian",
    "race_tiktok": "East Asian / East Asian British",
    "ethnicity_hesa": "Asian / Asian British - Any other Asian background (United Kingdom)",
    "language_english_fluency": "Fluent",
    "language_english_native": True,
    "language_korean_fluency": "Fluent",
    "language_korean_native": True,
    # 4. Links, Passwords & Documents
    "linkedin": "https://www.linkedin.com/in/kyubin-yun-495a33301/",
    "github": "https://github.com/canadaofbin-netizen",
    "standard_password": "Jeff0825!!",
    "workday_password": "Jeff0825!!!!",
    "resume_path": r"g:\My Drive\Kyubin_Yun_Workspace\04_Internship\01_Resumes\Kyubin_Yun_Resume_2027.pdf",
}


if __name__ == "__main__":
    print("Ground-Truth Integrity & Auto-Correction Engine (Reconciliation Engine)")
    print(f"Loaded {len(SSOT_CANDIDATE_BASELINE)} SSOT baseline fields.")
    engine = ReconciliationEngine()
    print("Running baseline self-audit against SSOT...")
    for k, v in SSOT_CANDIDATE_BASELINE.items():
        ok, rec = engine.execute_and_reconcile(
            field_name=k,
            expected_value=v,
            field_type="text_input",
            writer_fn=lambda f, val, rem: True,
            reader_fn=lambda f: SSOT_CANDIDATE_BASELINE[f],
        )
    passed, audit_summary = engine.verify_submission_gate()
    print(audit_summary)
    sys.exit(0 if passed else 1)
