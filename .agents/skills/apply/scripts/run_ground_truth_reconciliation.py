#!/usr/bin/env python3
"""
Ground-Truth Integrity & Auto-Correction Engine: Comprehensive Live Verification Runner.
Executes the 4-step loop (Payload Parsing, Action Execution, Read-After-Write Inspection,
and Strict Diff Reconciliation) across live Naver Whale browser tabs:
1. Scale AI Greenhouse
2. TikTok Careers
3. LSEG Workday

Enforces the Zero Auto-Submit safety protocol and outputs the formal [Verification Audit] table.
"""

import asyncio
import re
import sys

from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8")

from reconciliation_engine import (
    SSOT_CANDIDATE_BASELINE,
    AuditRecord,
    FailureCache,
    ReconciliationEngine,
)
from text_normalizer import normalize_text


class LiveBrowserReconciler:
    def __init__(self):
        self.engine = ReconciliationEngine(failure_cache=FailureCache.with_standard_remedies(), max_retries=3)

    async def run(self):
        print("================================================================================")
        print("[System Protocol: Ground-Truth Integrity & Auto-Correction Engine Active]")
        print("Connecting to live Naver Whale browser CDP on http://localhost:9222...")
        print("================================================================================")

        async with async_playwright() as p:
            try:
                browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            except Exception as e:
                print(f"FATAL: Unable to connect to Naver Whale CDP on port 9222: {e}")
                return False

            context = browser.contexts[0]
            pages = context.pages

            scale_page = next((pg for pg in pages if "greenhouse.io" in pg.url or "scaleai" in pg.url), None)
            tiktok_page = next((pg for pg in pages if "lifeattiktok.com" in pg.url), None)
            workday_page = next((pg for pg in pages if "myworkdayjobs.com" in pg.url), None)

            print("Detected tabs on port 9222:")
            print(f" - Scale AI Greenhouse: {'FOUND' if scale_page else 'MISSING'}")
            print(f" - TikTok Careers:      {'FOUND' if tiktok_page else 'MISSING'}")
            print(f" - LSEG Workday:        {'FOUND' if workday_page else 'MISSING'}")

            # -------------------------------------------------------------------------
            # TAB 1: SCALE AI GREENHOUSE AUDIT & RECONCILIATION
            # -------------------------------------------------------------------------
            if scale_page:
                print("\n>>> AUDITING TAB 1: Scale AI Greenhouse (Software Engineering Intern Summer 2027)...")
                await self.audit_scale_ai(scale_page)

            # -------------------------------------------------------------------------
            # TAB 2: TIKTOK CAREERS AUDIT & RECONCILIATION
            # -------------------------------------------------------------------------
            if tiktok_page:
                print("\n>>> AUDITING TAB 2: TikTok Careers (Graduate/Internship Application)...")
                await self.audit_tiktok(tiktok_page)

            # -------------------------------------------------------------------------
            # TAB 3: LSEG WORKDAY AUDIT & RECONCILIATION
            # -------------------------------------------------------------------------
            if workday_page:
                print("\n>>> AUDITING TAB 3: LSEG Workday (Engineering Summer Internship Programme)...")
                await self.audit_workday(workday_page)

            # -------------------------------------------------------------------------
            # STEP 3: SUBMISSION GATE & FORMAL AUDIT TABLE
            # -------------------------------------------------------------------------
            print("\n================================================================================")
            print("EVALUATING SUBMISSION GATE ACROSS ALL TARGET FORMS...")
            print("================================================================================")
            passed, audit_report = self.engine.verify_submission_gate()
            print(audit_report)

            # -------------------------------------------------------------------------
            # STEP 4: ZERO AUTO-SUBMIT SAFETY ENFORCEMENT
            # -------------------------------------------------------------------------
            print("\n[Zero Auto-Submit Enforcement]")
            print("  - Scale AI Greenhouse: Halted at form completion (Submit application NOT clicked).")
            print("  - TikTok Careers: Halted at form completion (Submit NOT clicked).")
            print(
                "  - LSEG Workday: Halted at credential/registration review (Create Account / Next NOT auto-submitted)."
            )
            print("  - System Status: Execution safely suspended at Review stage for user manual action.")

            return passed

    async def audit_scale_ai(self, page):
        fields = [
            ("Scale AI: First Name", "first_name", SSOT_CANDIDATE_BASELINE["first_name"], "text_input"),
            ("Scale AI: Last Name", "last_name", SSOT_CANDIDATE_BASELINE["last_name"], "text_input"),
            ("Scale AI: Preferred First Name (Strictly Blank)", "preferred_name", "", "text_input"),
            ("Scale AI: Email", "email", SSOT_CANDIDATE_BASELINE["email"], "text_input"),
            ("Scale AI: Phone Prefix (Country)", "country", SSOT_CANDIDATE_BASELINE["phone_prefix"], "text_input"),
            ("Scale AI: Phone Number", "phone", SSOT_CANDIDATE_BASELINE["phone"], "text_input"),
            ("Scale AI: Location (City)", "candidate-location", "London, England, United Kingdom", "text_input"),
            ("Scale AI: Resume Attachment", "resume_attachment", "Kyubin_Yun_Resume_2027.pdf", "file_attached"),
            ("Scale AI: School", "school--0", "UCL (University College London)", "react_select"),
            ("Scale AI: Degree", "degree--0", "Bachelor's Degree", "react_select"),
            ("Scale AI: Discipline", "discipline--0", "Psychology", "react_select"),
            ("Scale AI: Graduation Year", "end-year--0", SSOT_CANDIDATE_BASELINE["graduation_year"], "text_input"),
            ("Scale AI: LinkedIn Profile", "question_9044247005", SSOT_CANDIDATE_BASELINE["linkedin"], "text_input"),
            ("Scale AI: GitHub / Website", "question_9044248005", SSOT_CANDIDATE_BASELINE["github"], "text_input"),
            (
                "Scale AI: When do you graduate?",
                "question_9086086005",
                SSOT_CANDIDATE_BASELINE["graduation_year"],
                "text_input",
            ),
            ("Scale AI: Summer 2027 Availability", "question_9044249005", "Yes", "react_select"),
            ("Scale AI: Located in London", "question_9044250005", "Yes", "react_select"),
            ("Scale AI: Work Authorization", "question_9044251005", "Yes", "react_select"),
            ("Scale AI: Requires Sponsorship", "question_9044252005", "Yes", "react_select"),
            ("Scale AI: Gender", "gender", SSOT_CANDIDATE_BASELINE["gender"], "react_select"),
            ("Scale AI: Hispanic / Latino", "hispanic_ethnicity", "No", "react_select"),
            ("Scale AI: Race", "race", SSOT_CANDIDATE_BASELINE["race"], "react_select"),
            ("Scale AI: Veteran Status", "veteran_status", "I am not a protected veteran", "react_select"),
            ("Scale AI: Disability Status", "disability_status", "I do not want to answer", "react_select"),
        ]

        for field_name, dom_id, expected_val, field_type in fields:
            attempts = 0
            while attempts < self.engine.max_retries:
                attempts += 1
                # Step 3: Read-After-Write Inspection (independent DOM query)

                actual_val = await page.evaluate(
                    """(id) => {
                    if (id === 'resume_attachment') {
                        const els = Array.from(document.querySelectorAll('.file-upload__filename, p.body__secondary, [data-qa="uploaded-filename"], .chosen'));
                        const pdfEl = els.find(e => e.innerText && e.innerText.trim().endsWith('.pdf'));
                        return pdfEl ? pdfEl.innerText.trim() : '';
                    }
                    const el = document.getElementById(id);
                    if (!el) return '';
                    const ctrl = el.closest('.select__control');
                    if (ctrl) {
                        const sv = ctrl.querySelector('.select__single-value');
                        if (sv) return sv.innerText.trim();
                    }
                    return (el.value || '').trim();
                }""",
                    dom_id,
                )

                # Step 4: Strict Diff Reconciliation
                diff = self.engine.calculate_diff(expected_val, actual_val)
                if diff == 0:
                    self.engine.audit_log.append(
                        AuditRecord(
                            field_name=field_name,
                            expected_value=expected_val,
                            actual_value=actual_val,
                            status="MATCH",
                            attempts=attempts,
                        )
                    )
                    break
                else:
                    defect = self.engine._diagnose_defect(expected_val, actual_val, field_type)
                    remedy_action = self.engine._determine_remedy(defect)
                    self.engine.failure_cache.record_failure(field_type, defect, remedy_action, field_name=field_name)
                    print(
                        f"  [RECONCILING] {field_name}: Actual '{actual_val}' != Expected '{expected_val}'. Applying {remedy_action}..."
                    )

                    # Remedial action
                    if field_type == "react_select":
                        await page.evaluate(
                            """async ({id, val}) => {
                            const el = document.getElementById(id);
                            if (!el) return;
                            const ctrl = el.closest('.select__control');
                            if (!ctrl) return;
                            const clearBtn = ctrl.querySelector('.select__clear-indicator');
                            if (clearBtn) {
                                clearBtn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                                clearBtn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                            }
                            ctrl.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                            el.focus();
                            el.value = val;
                            el.dispatchEvent(new Event('input', { bubbles: true }));
                            await new Promise(r => setTimeout(r, 200));
                            const menu = ctrl.parentElement ? ctrl.parentElement.querySelector('.select__menu') : null;
                            if (menu) {
                                const options = Array.from(menu.querySelectorAll('.select__option, [role="option"]'));
                                const match = options.find(o => o.innerText && o.innerText.trim().toLowerCase() === val.toLowerCase());
                                if (match) {
                                    match.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                                    match.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                                }
                            }
                        }""",
                            {"id": dom_id, "val": expected_val},
                        )
                    else:
                        await page.evaluate(
                            """({id, val}) => {
                            const el = document.getElementById(id);
                            if (el) {
                                el.focus();
                                const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                                setter.call(el, val);
                                el.dispatchEvent(new Event('input', { bubbles: true }));
                                el.dispatchEvent(new Event('change', { bubbles: true }));
                                el.dispatchEvent(new Event('blur', { bubbles: true }));
                            }
                        }""",
                            {"id": dom_id, "val": expected_val},
                        )
                    await page.wait_for_timeout(300)
            else:
                self.engine.audit_log.append(
                    AuditRecord(
                        field_name=field_name,
                        expected_value=expected_val,
                        actual_value=actual_val,
                        status="MISMATCH",
                        attempts=attempts,
                        diagnostics=f"Exhausted retries on {dom_id}",
                    )
                )

    async def audit_tiktok(self, page):
        # 1. Contact & Identity
        contact_fields = [
            ("TikTok: Candidate Name", "name", SSOT_CANDIDATE_BASELINE["legal_name"], "text_input"),
            ("TikTok: Phone Country Code", "phonePrefix", SSOT_CANDIDATE_BASELINE["phone_prefix"], "combobox"),
            ("TikTok: Mobile Number", "mobile", SSOT_CANDIDATE_BASELINE["phone_national"], "text_input"),
            ("TikTok: Email", "email", SSOT_CANDIDATE_BASELINE["email"], "text_input"),
            ("TikTok: Resume Attachment", "resume", "Kyubin_Yun_Resume_2027.pdf", "file_attached"),
        ]

        for field_name, key, expected_val, field_type in contact_fields:
            attempts = 0
            while attempts < self.engine.max_retries:
                attempts += 1
                actual_val = await page.evaluate(
                    """(k) => {
                    if (k === 'phonePrefix') {
                        const el = document.querySelector('[data-cy="selectedValue"]');
                        return el ? el.innerText.trim() : '';
                    }
                    if (k === 'resume') {
                        return document.body.innerText.includes('Kyubin_Yun_Resume_2027.pdf') ? 'Kyubin_Yun_Resume_2027.pdf' : '';
                    }
                    if (k === 'mobile') {
                        const inps = Array.from(document.querySelectorAll('input'));
                        const mob = inps.find(i => i.value && i.closest('.atsx-form-item') && i.closest('.atsx-form-item').innerText.includes('Mobile'));
                        return mob ? mob.value.trim() : '';
                    }
                    const el = document.getElementById(k);
                    return el ? (el.value || '').trim() : '';
                }""",
                    key,
                )

                diff = self.engine.calculate_diff(expected_val, actual_val)
                if diff == 0:
                    self.engine.audit_log.append(
                        AuditRecord(
                            field_name=field_name,
                            expected_value=expected_val,
                            actual_value=actual_val,
                            status="MATCH",
                            attempts=attempts,
                        )
                    )
                    break
                else:
                    defect = self.engine._diagnose_defect(expected_val, actual_val, field_type)
                    remedy = self.engine._determine_remedy(defect)
                    self.engine.failure_cache.record_failure(field_type, defect, remedy, field_name=field_name)
                    print(
                        f"  [RECONCILING] {field_name}: Actual '{actual_val}' != Expected '{expected_val}'. Applying remedy {remedy}..."
                    )
                    if key == "phonePrefix":
                        await page.click('[data-cy="phonePrefix"]')
                        await page.wait_for_timeout(300)
                        await page.evaluate("""() => {
                            const items = document.querySelectorAll('.atsx-select-dropdown-menu-item, [role="option"]');
                            for (const item of items) {
                                if (item.innerText.includes('United Kingdom') && item.innerText.includes('+44')) {
                                    item.scrollIntoView();
                                    item.click();
                                    break;
                                }
                            }
                        }""")
                    await page.wait_for_timeout(300)
            else:
                self.engine.audit_log.append(
                    AuditRecord(
                        field_name=field_name,
                        expected_value=expected_val,
                        actual_value=actual_val,
                        status="MISMATCH",
                        attempts=attempts,
                    )
                )

        # 2. Education & Experience structured inputs (with 4-step reconciliation loop)
        struct_fields = [
            ("TikTok: Education 1 School", "education[3].school", "Kwangwoon University"),
            ("TikTok: Education 1 Major", "education[3].fieldOfStudy", "Industrial-Organizational Psychology"),
            ("TikTok: Education 2 School", "education[4].school", "University College London (UCL)"),
            ("TikTok: Education 2 Major", "education[4].fieldOfStudy", "Psychology and Language Sciences"),
            ("TikTok: Experience 1 Company", "career[1].company", "Republic of Korea Army"),
            ("TikTok: Experience 1 Title", "career[1].title", "Sergeant (Culinary Specialist)"),
            ("TikTok: Experience 2 Company", "internship[1].company", "University of Oklahoma"),
            ("TikTok: Experience 2 Title", "internship[1].title", "Research Assistant Intern"),
            ("TikTok: Experience 3 Company", "internship[2].company", "WooJung Korean Restaurant"),
            ("TikTok: Experience 3 Title", "internship[2].title", "Server"),
        ]

        for field_name, dom_id, expected_val in struct_fields:
            attempts = 0
            while attempts < self.engine.max_retries:
                attempts += 1
                actual_val = await page.evaluate(
                    """(id) => {
                    const inps = Array.from(document.querySelectorAll('input'));
                    const matchedInp = inps.find(i => i.id === id);
                    if (matchedInp && matchedInp.value) return matchedInp.value.trim();
                    const el = document.getElementById(id);
                    if (!el) return '';
                    if (el.value !== undefined && el.value !== '') return el.value.trim();
                    return (el.innerText || '').trim();
                }""",
                    dom_id,
                )

                diff = self.engine.calculate_diff(expected_val, actual_val)
                if diff == 0:
                    self.engine.audit_log.append(
                        AuditRecord(
                            field_name=field_name,
                            expected_value=expected_val,
                            actual_value=actual_val,
                            status="MATCH",
                            attempts=attempts,
                        )
                    )
                    break
                else:
                    defect = self.engine._diagnose_defect(expected_val, actual_val, "text_input")
                    remedy = self.engine._determine_remedy(defect)
                    self.engine.failure_cache.record_failure("text_input", defect, remedy, field_name=field_name)
                    print(
                        f"  [RECONCILING] {field_name}: Actual '{actual_val}' != Expected '{expected_val}'. Applying remedy {remedy}..."
                    )
                    await page.evaluate(
                        """({id, val}) => {
                        const inps = Array.from(document.querySelectorAll('input'));
                        const el = inps.find(i => i.id === id) || document.getElementById(id);
                        if (el) {
                            el.focus();
                            const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                            setter.call(el, val);
                            el.dispatchEvent(new Event('input', { bubbles: true }));
                            el.dispatchEvent(new Event('change', { bubbles: true }));
                            el.dispatchEvent(new Event('blur', { bubbles: true }));
                        }
                    }""",
                        {"id": dom_id, "val": expected_val},
                    )
                    await page.wait_for_timeout(300)
            else:
                self.engine.audit_log.append(
                    AuditRecord(
                        field_name=field_name,
                        expected_value=expected_val,
                        actual_value=actual_val,
                        status="MISMATCH",
                        attempts=attempts,
                    )
                )

        # 3. Textareas - Validate bullet formatting and unwrap (with 4-step reconciliation loop)
        textarea_checks = [
            ("TikTok: Experience 1 Description (ROK Army)", "career[1].desc", 2),
            ("TikTok: Experience 2 Description (Univ of Oklahoma)", "internship[1].desc", 4),
            ("TikTok: Experience 3 Description (WooJung Restaurant)", "internship[2].desc", 1),
        ]

        for field_name, dom_id, expected_bullet_count in textarea_checks:
            attempts = 0
            while attempts < self.engine.max_retries:
                attempts += 1
                # Step 3: Independent Read-After-Write Inspection from DOM
                actual_val = await page.evaluate(
                    """(id) => {
                    const el = document.getElementById(id);
                    return el ? el.value : '';
                }""",
                    dom_id,
                )

                lines = [line_item for line_item in actual_val.split("\n") if line_item.strip()]
                all_standard_bullets = all(line_item.startswith("• ") for line_item in lines)
                has_no_mid_sentence_breaks = not bool(re.search(r"[a-zA-Z0-9,]\n[a-zA-Z0-9]", actual_val))
                correct_count = len(lines) == expected_bullet_count
                is_clean = all_standard_bullets and has_no_mid_sentence_breaks and correct_count

                if is_clean:
                    summary_exp = f"{expected_bullet_count} standard bullets ('• '), normalized unwrapped text"
                    summary_act = f"{len(lines)} bullets ('• '), 0 mid-sentence line breaks"
                    self.engine.audit_log.append(
                        AuditRecord(
                            field_name=field_name,
                            expected_value=summary_exp,
                            actual_value=summary_act,
                            status="MATCH",
                            attempts=attempts,
                        )
                    )
                    break
                else:
                    print(f"  [RECONCILING] {field_name}: Textarea requires normalization (attempt {attempts})...")
                    normalized = normalize_text(actual_val)
                    await page.evaluate(
                        """({id, val}) => {
                        const el = document.getElementById(id);
                        if (el) {
                            el.focus();
                            const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
                            setter.call(el, val);
                            el.dispatchEvent(new Event('input', { bubbles: true }));
                            el.dispatchEvent(new Event('change', { bubbles: true }));
                            el.dispatchEvent(new Event('blur', { bubbles: true }));
                        }
                    }""",
                        {"id": dom_id, "val": normalized},
                    )
                    await page.wait_for_timeout(300)
            else:
                # Step 3 independent read after retry exhaustion
                final_val = await page.evaluate(
                    """(id) => {
                    const el = document.getElementById(id);
                    return el ? el.value : '';
                }""",
                    dom_id,
                )
                final_lines = [line_item for line_item in final_val.split("\n") if line_item.strip()]

                final_breaks = len(re.findall(r"[a-zA-Z0-9,]\n[a-zA-Z0-9]", final_val))
                self.engine.audit_log.append(
                    AuditRecord(
                        field_name=field_name,
                        expected_value=f"{expected_bullet_count} standard bullets ('• '), normalized unwrapped text",
                        actual_value=f"{len(final_lines)} bullets ('• '), {final_breaks} mid-sentence line breaks",
                        status="MISMATCH",
                        attempts=attempts,
                        diagnostics=f"Failed to normalize textarea {dom_id}",
                    )
                )

        # 4. Demographics & Right to Work Dropdowns (with 4-step reconciliation loop)
        dropdown_checks = [
            ("TikTok: Gender Identity", 0, SSOT_CANDIDATE_BASELINE["gender_tiktok"]),
            ("TikTok: Disability Status", 1, SSOT_CANDIDATE_BASELINE["disability"]),
            ("TikTok: Race/Ethnicity", 2, SSOT_CANDIDATE_BASELINE["race_tiktok"]),
            ("TikTok: Work Authorization (Right to Work)", 3, SSOT_CANDIDATE_BASELINE["work_authorization"]),
            ("TikTok: Visa Sponsorship Required", 4, SSOT_CANDIDATE_BASELINE["sponsorship_required"]),
            ("TikTok: Referral Source", 5, "School career development office"),
        ]

        for field_name, idx, expected_opt in dropdown_checks:
            attempts = 0
            while attempts < self.engine.max_retries:
                attempts += 1
                actual_val = await page.evaluate(
                    """(idx) => {
                    const selects = document.querySelectorAll('.ud__select');
                    const target = selects[idx];
                    const selector = target ? (target.querySelector('.ud__select__selector') || target) : null;
                    return selector ? (selector.innerText || '').trim() : '';
                }""",
                    idx,
                )

                diff = 0 if expected_opt in actual_val else 1
                if diff == 0:
                    self.engine.audit_log.append(
                        AuditRecord(
                            field_name=field_name,
                            expected_value=expected_opt,
                            actual_value=actual_val,
                            status="MATCH",
                            attempts=attempts,
                        )
                    )
                    break
                else:
                    defect = "DROPDOWN_MISMATCH_OR_STALE_CONTAINER"
                    remedy = "FILTER_ACTIVE_NON_LEAVING_CONTAINER_AND_EXACT_MATCH"
                    self.engine.failure_cache.record_failure("ud_select", defect, remedy, field_name=field_name)
                    print(
                        f"  [RECONCILING] {field_name}: Actual '{actual_val}' != Expected '{expected_opt}'. Applying {remedy}..."
                    )
                    await page.evaluate(
                        """async ({idx, opt}) => {
                        const selects = document.querySelectorAll('.ud__select');
                        const target = selects[idx];
                        if (!target) return;
                        target.click();
                        await new Promise(r => setTimeout(r, 200));
                        const options = Array.from(document.querySelectorAll('.ud__select__options__item, .atsx-select-dropdown-menu-item, [role="option"]'));
                        const match = options.find(o => o.innerText && o.innerText.trim().includes(opt));
                        if (match) {
                            match.scrollIntoView();
                            match.click();
                        }
                    }""",
                        {"idx": idx, "opt": expected_opt},
                    )
                    await page.wait_for_timeout(300)
            else:
                self.engine.audit_log.append(
                    AuditRecord(
                        field_name=field_name,
                        expected_value=expected_opt,
                        actual_value=actual_val,
                        status="MISMATCH",
                        attempts=attempts,
                    )
                )

        # 5. Privacy Policy Checkbox (with 4-step reconciliation loop)
        attempts = 0
        while attempts < self.engine.max_retries:
            attempts += 1
            cb_val = await page.evaluate("""() => {
                const cb = document.querySelector('input[type="checkbox"]');
                return cb ? (cb.checked ? 'Checked (True)' : 'Unchecked (False)') : 'Not found';
            }""")
            diff_cb = self.engine.calculate_diff(True, cb_val)
            if diff_cb == 0:
                self.engine.audit_log.append(
                    AuditRecord(
                        field_name="TikTok: Privacy Policy Consent",
                        expected_value="Checked (True)",
                        actual_value=cb_val,
                        status="MATCH",
                        attempts=attempts,
                    )
                )
                break
            else:
                print("  [RECONCILING] TikTok Privacy Policy: Checkbox not checked. Clicking...")
                await page.evaluate("""() => {
                    const cb = document.querySelector('input[type="checkbox"]');
                    if (cb && !cb.checked) {
                        cb.click();
                        cb.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                }""")
                await page.wait_for_timeout(300)
        else:
            self.engine.audit_log.append(
                AuditRecord(
                    field_name="TikTok: Privacy Policy Consent",
                    expected_value="Checked (True)",
                    actual_value=cb_val,
                    status="MISMATCH",
                    attempts=attempts,
                )
            )

    async def audit_workday(self, page):
        workday_fields = [
            ("LSEG Workday: Account Email", "input-4", SSOT_CANDIDATE_BASELINE["email"], "text_input"),
            ("LSEG Workday: Account Password", "input-5", SSOT_CANDIDATE_BASELINE["workday_password"], "password"),
            ("LSEG Workday: Verify Password", "input-6", SSOT_CANDIDATE_BASELINE["workday_password"], "password"),
            ("LSEG Workday: Privacy Policy Consent", "input-9", True, "checkbox"),
            (
                "LSEG Workday: Honeypot Robot Input (Must be blank)",
                "28a2af4d-41e4-43b5-9024-87d106a82a54",
                "",
                "text_input",
            ),
        ]

        for field_name, dom_id, expected_val, field_type in workday_fields:
            attempts = 0
            while attempts < self.engine.max_retries:
                attempts += 1
                actual_val = await page.evaluate(
                    """(id) => {
                    const el = document.getElementById(id);
                    if (!el) return '';
                    if (el.type === 'checkbox') return el.checked ? 'Checked (True)' : 'Unchecked (False)';
                    return (el.value || '').trim();
                }""",
                    dom_id,
                )

                diff = self.engine.calculate_diff(expected_val, actual_val)
                if diff == 0:
                    self.engine.audit_log.append(
                        AuditRecord(
                            field_name=field_name,
                            expected_value="Checked (True)" if expected_val is True else expected_val,
                            actual_value=actual_val,
                            status="MATCH",
                            attempts=attempts,
                        )
                    )
                    break
                else:
                    defect = self.engine._diagnose_defect(expected_val, actual_val, field_type)
                    remedy = self.engine._determine_remedy(defect)
                    self.engine.failure_cache.record_failure(field_type, defect, remedy, field_name=field_name)
                    print(
                        f"  [RECONCILING] {field_name}: Actual '{actual_val}' != Expected '{expected_val}'. Applying remedy {remedy}..."
                    )

                    if field_type == "checkbox":
                        await page.evaluate(
                            """({id}) => {
                            const el = document.getElementById(id);
                            if (el && !el.checked) {
                                el.click();
                                el.dispatchEvent(new Event('change', { bubbles: true }));
                            }
                        }""",
                            {"id": dom_id},
                        )
                    else:
                        await page.evaluate(
                            """({id, val}) => {
                            const el = document.getElementById(id);
                            if (el) {
                                el.focus();
                                const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                                setter.call(el, val);
                                el.dispatchEvent(new Event('input', { bubbles: true }));
                                el.dispatchEvent(new Event('change', { bubbles: true }));
                                el.dispatchEvent(new Event('blur', { bubbles: true }));
                            }
                        }""",
                            {"id": dom_id, "val": expected_val},
                        )
                    await page.wait_for_timeout(300)
            else:
                self.engine.audit_log.append(
                    AuditRecord(
                        field_name=field_name,
                        expected_value="Checked (True)" if expected_val is True else expected_val,
                        actual_value=actual_val,
                        status="MISMATCH",
                        attempts=attempts,
                    )
                )


if __name__ == "__main__":
    reconciler = LiveBrowserReconciler()
    success = asyncio.run(reconciler.run())
    sys.exit(0 if success else 1)
