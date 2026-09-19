#!/usr/bin/env python3
"""
Unit tests for the CEO Control Tower Orchestration System,
including session registration, handoff brief generation,
return synchronization, and Master SSOT Excel integrity.
"""

import re
import unittest

import openpyxl
from ceo_hub import (
    BRIEFS_DIR,
    REGISTRY_PATH,
    RETURNS_DIR,
    SSOT_EXCEL_PATH,
    WORKSPACE_ROOT,
    generate_handoff,
    list_rooms,
    load_registry,
    register_room,
    sync_return,
)


class TestCEOOrchestration(unittest.TestCase):
    def test_registry_structure_and_schema(self):
        self.assertTrue(REGISTRY_PATH.exists(), f"Registry file must exist at {REGISTRY_PATH}")
        reg = load_registry()

        self.assertEqual(reg.get("candidate"), "Kyubin Yun")
        self.assertIn("University College London", reg.get("university", ""))

        tracks = reg.get("tracks", {})
        self.assertIn("TRACK-A", tracks)
        self.assertIn("TRACK-B", tracks)
        self.assertIn("TRACK-C", tracks)
        self.assertIn("TRACK-D", tracks)

        rooms = reg.get("chatrooms", [])
        self.assertGreaterEqual(len(rooms), 3)
        for r in rooms:
            self.assertIn("session_id", r)
            self.assertIn("track", r)
            self.assertIn("status", r)
            self.assertIn("priority", r)
            self.assertIn("title", r)

    def test_room_registration_and_sync_lifecycle(self):
        test_sid = "ROOM-TEST-TEMP-999"
        original_registry_bytes = REGISTRY_PATH.read_bytes()
        reg = load_registry()
        initial_count = len(reg.get("chatrooms", []))

        try:
            # Register room
            new_room = register_room(
                session_id=test_sid,
                track="TRACK-B",
                title="Unit Test Ephemeral Room",
                priority="MEDIUM",
                target_companies=["TestCorp UK"],
                outcome_summary="Testing registration lifecycle.",
            )
            self.assertEqual(new_room["session_id"], test_sid)
            self.assertEqual(new_room["status"], "READY_FOR_DISPATCH")

            # Verify it shows up in list_rooms
            rooms = list_rooms(track_filter="TRACK-B")
            found = [r for r in rooms if r["session_id"] == test_sid]
            self.assertEqual(len(found), 1)

            # Generate handoff
            brief_path = generate_handoff(test_sid)
            self.assertTrue(brief_path.exists())
            brief_text = brief_path.read_text(encoding="utf-8")
            self.assertIn("Kyubin Yun", brief_text)
            self.assertIn("zcjtyun@ucl.ac.uk", brief_text)
            self.assertIn("+44 7787 442404", brief_text)
            self.assertIn("Zero Auto-Submit", brief_text)
            self.assertIn("Visible Naver Whale Browser", brief_text)

            # Sync return
            sync_return(
                session_id=test_sid,
                status="COMPLETED",
                summary="Ephemeral task completed with 100% verification.",
            )
            updated_reg = load_registry()
            updated_room = [r for r in updated_reg["chatrooms"] if r["session_id"] == test_sid][0]
            self.assertEqual(updated_room["status"], "COMPLETED")
            self.assertIn("Ephemeral task completed", updated_room["outcome_summary"])

        finally:
            # Restore exact original registry bytes to avoid leaving git tree dirty
            REGISTRY_PATH.write_bytes(original_registry_bytes)

            # Clean up generated brief/return files if created
            test_brief = BRIEFS_DIR / f"{test_sid}_brief.md"
            if test_brief.exists():
                test_brief.unlink()
            test_return = RETURNS_DIR / f"{test_sid}_return.md"
            if test_return.exists():
                test_return.unlink()

            final_reg = load_registry()
            self.assertEqual(len(final_reg["chatrooms"]), initial_count)

    def test_master_ssot_excel_integrity(self):
        self.assertTrue(SSOT_EXCEL_PATH.exists(), f"Master SSOT Excel must exist at: {SSOT_EXCEL_PATH}")
        wb = openpyxl.load_workbook(SSOT_EXCEL_PATH, data_only=False)

        expected_sheets = [
            "0.CEO_Dashboard",
            "UK_BCI",
            "1.UK_Top_Targets",
            "2.UK_Tech_Quant_Finance",
            "3.KR_타임라인_우선순위",
            "4.KR_Tech_BCI",
            "5.KR_전략_대기업_금융",
            "6.Global_BCI_Map",
            "7.BCI_Research_DB",
        ]
        self.assertEqual(len(wb.sheetnames), 9, f"Expected exactly 9 sheets, got {len(wb.sheetnames)}: {wb.sheetnames}")
        for sheet_name in expected_sheets:
            self.assertIn(sheet_name, wb.sheetnames, f"Sheet {sheet_name} missing from Master SSOT Excel!")

        # Verify Tab Colors
        expected_tab_colors = {
            "0.CEO_Dashboard": "D4AF37",
            "UK_BCI": "1F4E79",
            "1.UK_Top_Targets": "1F4E79",
            "2.UK_Tech_Quant_Finance": "1F4E79",
            "3.KR_타임라인_우선순위": "C00000",
            "4.KR_Tech_BCI": "C00000",
            "5.KR_전략_대기업_금융": "C00000",
            "6.Global_BCI_Map": "7030A0",
            "7.BCI_Research_DB": "7030A0",
        }
        for sname, expected_hex in expected_tab_colors.items():
            ws = wb[sname]
            self.assertIsNotNone(ws.sheet_properties.tabColor, f"Tab color not set for {sname}")
            actual_color = ws.sheet_properties.tabColor.rgb
            self.assertTrue(
                actual_color.endswith(expected_hex),
                f"Tab color mismatch for {sname}: expected ending with {expected_hex}, got {actual_color}",
            )

        # Verify Executive Dashboard links to all 7 sub-sheets
        ws_dash = wb["0.CEO_Dashboard"]
        self.assertGreater(ws_dash.max_row, 20)
        found_subsheet_links = set()
        for row in ws_dash.iter_rows(values_only=False):
            for cell in row:
                cell_str = str(cell.value or "")
                if cell_str.startswith("=HYPERLINK"):
                    for target_sheet in expected_sheets[1:]:
                        if target_sheet in cell_str:
                            found_subsheet_links.add(target_sheet)

        self.assertEqual(
            found_subsheet_links,
            set(expected_sheets[1:]),
            f"Executive Dashboard must link to all 7 sub-sheets! Found: {found_subsheet_links}",
        )

        # Verify 7.BCI_Research_DB telemetry columns are hidden and exact row count
        ws_db = wb["7.BCI_Research_DB"]
        self.assertEqual(ws_db.max_row, 85, "7.BCI_Research_DB must have exactly 85 rows (1 header + 84 contacts)")
        for col_letter in ["G", "H", "I", "J", "K"]:
            self.assertTrue(
                ws_db.column_dimensions[col_letter].hidden,
                f"Telemetry column {col_letter} in 7.BCI_Research_DB must be hidden in SSOT",
            )

        # Verify all 28 companies in 6.Global_BCI_Map have hyperlinks pointing to 7.BCI_Research_DB
        ws_bci = wb["6.Global_BCI_Map"]
        self.assertEqual(ws_bci.max_row, 29, "6.Global_BCI_Map must have exactly 29 rows (1 header + 28 companies)")
        for r in range(2, ws_bci.max_row + 1):
            comp = str(ws_bci.cell(r, 1).value or "").strip().lower()
            val = str(ws_bci.cell(r, 5).value or "")
            match = re.search(r"#'7\.BCI_Research_DB'!A(\d+)", val)
            self.assertIsNotNone(match, f"Row {r} invalid formula: {val}")
            target_row = int(match.group(1))
            db_comp = str(ws_db.cell(target_row, 1).value or "").strip().lower()
            self.assertTrue(
                comp in db_comp or db_comp in comp,
                f"Row {r} company '{comp}' does not match DB row {target_row} company '{db_comp}'",
            )

        # Verify noise removal, expired purging, and exact role counts in 2.UK_Tech_Quant_Finance
        ws_uk_tqf = wb["2.UK_Tech_Quant_Finance"]
        self.assertEqual(
            ws_uk_tqf.max_row, 73, "2.UK_Tech_Quant_Finance must have exactly 73 rows (1 header + 72 roles)"
        )
        tech_cnt = sum(
            1 for r in range(2, ws_uk_tqf.max_row + 1) if ws_uk_tqf.cell(r, 2).value == "Tech & Software / AI"
        )
        fin_cnt = sum(
            1 for r in range(2, ws_uk_tqf.max_row + 1) if ws_uk_tqf.cell(r, 2).value == "Quant & High-Finance"
        )
        self.assertEqual(tech_cnt, 72, f"Expected 72 Tech roles, got {tech_cnt}")
        self.assertEqual(fin_cnt, 0, f"Expected 0 Finance roles, got {fin_cnt}")

        target_tags = {"AI and Machine Learning", "Data Science", "Tech Consulting", "Startups"}
        for r in range(2, ws_uk_tqf.max_row + 1):
            cat = str(ws_uk_tqf.cell(r, 5).value or "")
            tags = [t.strip() for t in cat.split(",") if t.strip()]
            self.assertTrue(
                any(t in target_tags for t in tags),
                f"Row {r} category '{cat}' does not contain #1, #2, or #5 tags",
            )
            self.assertNotIn("Pensions and Insurance", cat)
            self.assertNotIn("Accounting and Audit", cat)
            self.assertNotIn("Real Estate", cat)
            self.assertNotIn("Big 4", cat)
            cdate = str(ws_uk_tqf.cell(r, 8).value or "")
            if "T" in cdate:
                dt_part = cdate.split("T")[0]
                self.assertGreaterEqual(dt_part, "2026-09-18", f"Expired role found at row {r}: {cdate}")

        # Verify exact counts and sections in remaining sheets
        ws_uk_targets = wb["1.UK_Top_Targets"]
        self.assertEqual(ws_uk_targets.max_row, 20, "1.UK_Top_Targets must have 20 rows (19 targets)")
        for r in range(2, ws_uk_targets.max_row + 1):
            cell_k = ws_uk_targets.cell(r, 11)
            comp_name = ws_uk_targets.cell(r, 3).value
            self.assertIsNotNone(cell_k.hyperlink, f"Row {r} ({comp_name}) in 1.UK_Top_Targets must have a valid hyperlink")
            target_url = cell_k.hyperlink.target or ""
            self.assertTrue(
                target_url.startswith("http://") or target_url.startswith("https://"),
                f"Row {r} ({comp_name}) hyperlink must start with http/https, got '{target_url}'",
            )
        # Verify specific critical mappings that must not be shifted
        self.assertIn("virtu", (ws_uk_targets.cell(18, 11).hyperlink.target or "").lower())
        self.assertIn("mavensecurities", (ws_uk_targets.cell(19, 11).hyperlink.target or "").lower())
        self.assertIn("smartrecruiters.com/ttp1", (ws_uk_targets.cell(20, 11).hyperlink.target or "").lower())

        self.assertEqual(
            wb["3.KR_타임라인_우선순위"].max_row, 64, "3.KR_타임라인_우선순위 must have 64 rows (63 opportunities)"
        )
        ws_kr_tech = wb["4.KR_Tech_BCI"]
        self.assertEqual(ws_kr_tech.max_row, 49, "4.KR_Tech_BCI must have 49 rows")
        ws_kr_corp = wb["5.KR_전략_대기업_금융"]
        self.assertEqual(ws_kr_corp.max_row, 30, "5.KR_전략_대기업_금융 must have 30 rows")

        wb.close()

    def test_company_name_headers_dropdowns_and_freeze_panes(self):
        """Verifies company name visibility, prominent headers, AutoFilters, DataValidations,
        freeze panes, and non-truncated column widths across all sheets in Master SSOT Excel.
        """
        wb = openpyxl.load_workbook(SSOT_EXCEL_PATH, data_only=False)

        # 0. Sheet 0: CEO Dashboard - Directory AutoFilter & generous widths
        ws0 = wb["0.CEO_Dashboard"]
        self.assertEqual(ws0.auto_filter.ref, "B11:G18")
        self.assertGreaterEqual(ws0.column_dimensions["B"].width, 28.0)
        self.assertGreaterEqual(ws0.column_dimensions["D"].width, 48.0)

        # 1. Sheet 1: UK Top Targets - Company Name prominent, D2 freeze, full AutoFilter (A1:L), DataValidation
        ws1 = wb["1.UK_Top_Targets"]
        self.assertIn("기업명", str(ws1["C1"].value))
        self.assertIn("Company Name", str(ws1["C1"].value))
        self.assertEqual(ws1.freeze_panes, "D2")
        self.assertIsNotNone(ws1.auto_filter.ref)
        self.assertEqual(ws1.auto_filter.ref, f"A1:L{ws1.max_row}")
        self.assertGreaterEqual(ws1.column_dimensions["C"].width, 36.0)
        self.assertGreaterEqual(ws1.column_dimensions["D"].width, 60.0)
        self.assertGreaterEqual(len(ws1.data_validations.dataValidation), 2)

        # 2. Sheet 2: UK Tech Quant Finance - Company Name prominent, D2 freeze, AutoFilter, DataValidation
        ws2 = wb["2.UK_Tech_Quant_Finance"]
        self.assertIn("기업명", str(ws2["C1"].value))
        self.assertIn("Company Name", str(ws2["C1"].value))
        self.assertEqual(ws2.freeze_panes, "D2")
        self.assertIsNotNone(ws2.auto_filter.ref)
        self.assertEqual(ws2.auto_filter.ref, f"A1:I{ws2.max_row}")
        self.assertGreaterEqual(ws2.column_dimensions["C"].width, 40.0)
        self.assertGreaterEqual(ws2.column_dimensions["D"].width, 80.0)
        self.assertGreaterEqual(len(ws2.data_validations.dataValidation), 2)

        # 3. Sheet 3: KR Timeline - Company Name prominent, B2 freeze, AutoFilter, DataValidation
        ws3 = wb["3.KR_타임라인_우선순위"]
        self.assertIn("기업명", str(ws3["A1"].value))
        self.assertIn("Company Name", str(ws3["A1"].value))
        self.assertEqual(ws3.freeze_panes, "B2")
        self.assertIsNotNone(ws3.auto_filter.ref)
        self.assertEqual(ws3.auto_filter.ref, f"A1:K{ws3.max_row}")
        self.assertGreaterEqual(ws3.column_dimensions["A"].width, 38.0)
        self.assertGreaterEqual(ws3.column_dimensions["C"].width, 60.0)
        self.assertGreaterEqual(len(ws3.data_validations.dataValidation), 4)

        # 4. Sheet 4: KR Tech BCI - Company Name prominent, B3 freeze, AutoFilter, DataValidation
        ws4 = wb["4.KR_Tech_BCI"]
        self.assertIn("기업명", str(ws4["A2"].value))
        self.assertEqual(ws4.freeze_panes, "B3")
        self.assertIsNotNone(ws4.auto_filter.ref)
        self.assertEqual(ws4.auto_filter.ref, f"A2:I{ws4.max_row}")
        self.assertGreaterEqual(ws4.column_dimensions["A"].width, 36.0)
        self.assertGreaterEqual(len(ws4.data_validations.dataValidation), 1)

        # 5. Sheet 5: KR Strategy Corp Finance - Company Name prominent, B3 freeze, AutoFilter, DataValidation
        ws5 = wb["5.KR_전략_대기업_금융"]
        self.assertIn("기업명", str(ws5["A2"].value))
        self.assertEqual(ws5.freeze_panes, "B3")
        self.assertIsNotNone(ws5.auto_filter.ref)
        self.assertEqual(ws5.auto_filter.ref, f"A2:I{ws5.max_row}")
        self.assertGreaterEqual(ws5.column_dimensions["A"].width, 38.0)
        self.assertGreaterEqual(len(ws5.data_validations.dataValidation), 1)

        # 6. Sheet 6: Global BCI Map - Company Name prominent, B2 freeze, AutoFilter, DataValidation
        ws6 = wb["6.Global_BCI_Map"]
        self.assertIn("Company Name", str(ws6["A1"].value))
        self.assertIn("기업명", str(ws6["A1"].value))
        self.assertEqual(ws6.freeze_panes, "B2")
        self.assertIsNotNone(ws6.auto_filter.ref)
        self.assertEqual(ws6.auto_filter.ref, f"A1:E{ws6.max_row}")
        self.assertGreaterEqual(ws6.column_dimensions["A"].width, 48.0)
        self.assertGreaterEqual(ws6.column_dimensions["C"].width, 54.0)
        self.assertGreaterEqual(ws6.column_dimensions["D"].width, 46.0)
        self.assertGreaterEqual(len(ws6.data_validations.dataValidation), 1)

        # 7. Sheet 7: BCI Research DB - Company Name prominent, B2 freeze, full AutoFilter (A1:K), DataValidation
        ws7 = wb["7.BCI_Research_DB"]
        self.assertIn("Company Name", str(ws7["A1"].value))
        self.assertIn("기업명", str(ws7["A1"].value))
        self.assertEqual(ws7.freeze_panes, "B2")
        self.assertIsNotNone(ws7.auto_filter.ref)
        self.assertEqual(ws7.auto_filter.ref, f"A1:K{ws7.max_row}")
        self.assertGreaterEqual(ws7.column_dimensions["A"].width, 48.0)
        self.assertGreaterEqual(len(ws7.data_validations.dataValidation), 1)

        wb.close()

    def test_register_room_validation_errors(self):
        # 1. Test invalid session IDs (traversal, invalid chars, too short/empty)
        invalid_sids = [
            "ROOM/INVALID/001",
            "ROOM\\INVALID\\001",
            "ROOM:BAD:001",
            "../ROOM-TRAVERSAL",
            "ROOM WITH SPACES",
            "",
            "AB",
        ]
        for sid in invalid_sids:
            with self.assertRaises(ValueError, msg=f"Should reject invalid session_id: {sid}"):
                register_room(
                    session_id=sid,
                    track="TRACK-B",
                    title="Test Title",
                )

        # 2. Test invalid tracks
        invalid_tracks = ["INVALID_TRACK", "TRACK-Z", "TRACK-E", ""]
        for trk in invalid_tracks:
            with self.assertRaises(ValueError, msg=f"Should reject invalid track: {trk}"):
                register_room(
                    session_id="ROOM-TEST-VALID-001",
                    track=trk,
                    title="Test Title",
                )

        # 3. Test invalid priorities
        invalid_priorities = ["SUPER_URGENT", "EXTREME", "INVALID"]
        for prio in invalid_priorities:
            with self.assertRaises(ValueError, msg=f"Should reject invalid priority: {prio}"):
                register_room(
                    session_id="ROOM-TEST-VALID-001",
                    track="TRACK-B",
                    title="Test Title",
                    priority=prio,
                )

        # 4. Test duplicate session_id
        with self.assertRaises(ValueError, msg="Should reject duplicate session_id"):
            register_room(
                session_id="ROOM-GLOBAL-BCI-001",
                track="TRACK-A",
                title="Duplicate Room",
            )

    def test_sync_return_and_handoff_validation_errors(self):
        # 1. Non-existent session ID
        with self.assertRaises(ValueError, msg="handoff should reject unknown session"):
            generate_handoff("NON-EXISTENT-SESSION-999")

        with self.assertRaises(ValueError, msg="sync_return should reject unknown session"):
            sync_return("NON-EXISTENT-SESSION-999", status="COMPLETED", summary="Test")

        # 2. Invalid status
        with self.assertRaises(ValueError, msg="sync_return should reject invalid status"):
            sync_return("ROOM-UK-PALANTIR-002", status="NOT_A_STATUS", summary="Test")

        # 3. Non-existent return_file path
        with self.assertRaises(FileNotFoundError, msg="sync_return should raise FileNotFoundError for missing file"):
            sync_return(
                "ROOM-UK-PALANTIR-002",
                status="COMPLETED",
                summary="Test",
                return_file="definitely_does_not_exist_9999.md",
            )

    def test_source_trackers_archival_completeness(self):
        """Verifies that all three original source trackers are preserved in data/source_trackers/."""
        source_dir = WORKSPACE_ROOT / "data" / "source_trackers"
        expected_sources = [
            "2027_BCI_Internship_Tracker.xlsx",
            "UK_2027_Summer_Internship_Trackr_Master.xlsx",
            "Korea_Internship_Research_2026_2027.xlsx",
        ]
        for src_name in expected_sources:
            src_file = source_dir / src_name
            self.assertTrue(src_file.is_file(), f"Expected source tracker missing in data/source_trackers: {src_name}")
            self.assertGreater(src_file.stat().st_size, 10000, f"Source tracker file too small: {src_name}")

    def test_build_ssot_import_resilience(self):
        """Ensures ceo_hub.build_ssot can resolve consolidate_excel_ssot even without scripts in sys.path."""
        import sys

        scripts_str = str(WORKSPACE_ROOT / ".agents" / "skills" / "apply" / "scripts")
        original_path = list(sys.path)
        try:
            sys.path = [p for p in sys.path if p != scripts_str]
            from ceo_hub import build_ssot

            self.assertTrue(callable(build_ssot))
        finally:
            sys.path = original_path

    def test_control_tower_documentation_and_rules(self):
        hub_md = WORKSPACE_ROOT / "00_CEO_Control_Tower" / "CEO_ORCHESTRATION_HUB.md"
        handoff_md = WORKSPACE_ROOT / "00_CEO_Control_Tower" / "HANDOFF_PROTOCOLS.md"
        rule_md = WORKSPACE_ROOT / ".agents" / "rules" / "ceo-orchestration-protocol.md"

        self.assertTrue(hub_md.exists(), "CEO_ORCHESTRATION_HUB.md must exist")
        self.assertTrue(handoff_md.exists(), "HANDOFF_PROTOCOLS.md must exist")
        self.assertTrue(rule_md.exists(), "ceo-orchestration-protocol.md must exist")

        rule_content = rule_md.read_text(encoding="utf-8")
        self.assertTrue(rule_content.startswith("---\n"), "Rule must have YAML frontmatter")
        self.assertIn("description:", rule_content)
        self.assertIn("AGENTS.md", rule_content)

    def test_is_uk_expired_comprehensive_edge_cases(self):
        """Tests that is_uk_expired robustly handles datetime objects, date objects,
        ISO strings without 'T', Korean deadline strings, and rolling indicators.
        """
        from datetime import date, datetime

        from consolidate_excel_ssot import is_uk_expired

        # Cases strictly before 2026-09-18 (should return True)
        self.assertTrue(is_uk_expired(datetime(2026, 9, 15, 0, 0)))
        self.assertTrue(is_uk_expired(date(2026, 9, 15)))
        self.assertTrue(is_uk_expired("2026-09-15"))
        self.assertTrue(is_uk_expired("2026-09-15 00:00:00"))
        self.assertTrue(is_uk_expired("2026.09.15"))
        self.assertTrue(is_uk_expired("2026-09-13 마감"))
        self.assertTrue(is_uk_expired("2026-09-17T23:59:59.000Z"))

        # Cases on or after 2026-09-18 (should return False)
        self.assertFalse(is_uk_expired("2026-09-18T00:00:00.000Z"))
        self.assertFalse(is_uk_expired("2026-09-18"))
        self.assertFalse(is_uk_expired(datetime(2026, 9, 18, 0, 0)))
        self.assertFalse(is_uk_expired("2026-09-19T00:00:00.000Z"))
        self.assertFalse(is_uk_expired("2026-10-21 마감"))
        self.assertFalse(is_uk_expired("2026-12-31 마감"))

        # Rolling, unspecified, None (should return False)
        self.assertFalse(is_uk_expired("Rolling / Unspecified"))
        self.assertFalse(is_uk_expired("Rolling"))
        self.assertFalse(is_uk_expired("Rolling (조기마감 주의)"))
        self.assertFalse(is_uk_expired(None))
        self.assertFalse(is_uk_expired(""))


if __name__ == "__main__":
    unittest.main()
