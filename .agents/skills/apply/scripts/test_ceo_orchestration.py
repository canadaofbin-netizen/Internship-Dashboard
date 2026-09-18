#!/usr/bin/env python3
"""
Unit tests for the CEO Control Tower Orchestration System,
including session registration, handoff brief generation,
return synchronization, and Master SSOT Excel integrity.
"""

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
    save_registry,
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
            # Cleanup ephemeral test room
            clean_reg = load_registry()
            clean_reg["chatrooms"] = [r for r in clean_reg.get("chatrooms", []) if r.get("session_id") != test_sid]
            save_registry(clean_reg)

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
            "1.UK_Top_Targets",
            "2.UK_Tech_Quant_Finance",
            "3.KR_타임라인_우선순위",
            "4.KR_Tech_BCI",
            "5.KR_전략_대기업_금융",
            "6.Global_BCI_Map",
            "7.BCI_Research_DB",
        ]
        self.assertEqual(len(wb.sheetnames), 8, f"Expected exactly 8 sheets, got {len(wb.sheetnames)}: {wb.sheetnames}")
        for sheet_name in expected_sheets:
            self.assertIn(sheet_name, wb.sheetnames, f"Sheet {sheet_name} missing from Master SSOT Excel!")

        # Verify Tab Colors
        expected_tab_colors = {
            "0.CEO_Dashboard": "D4AF37",
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

        # Verify 7.BCI_Research_DB telemetry columns are hidden
        ws_db = wb["7.BCI_Research_DB"]
        for col_letter in ["G", "H", "I", "J", "K"]:
            self.assertTrue(
                ws_db.column_dimensions[col_letter].hidden,
                f"Telemetry column {col_letter} in 7.BCI_Research_DB must be hidden in SSOT",
            )

        # Verify 6.Global_BCI_Map hyperlinks point to 7.BCI_Research_DB
        ws_bci = wb["6.Global_BCI_Map"]
        self.assertIn("7.BCI_Research_DB", str(ws_bci["E2"].value))

        # Verify noise removal in 2.UK_Tech_Quant_Finance
        ws_uk_tqf = wb["2.UK_Tech_Quant_Finance"]
        self.assertGreater(ws_uk_tqf.max_row, 500)
        for r in range(2, ws_uk_tqf.max_row + 1):
            cat = str(ws_uk_tqf.cell(r, 5).value or "")
            self.assertNotIn("Pensions and Insurance", cat)
            self.assertNotIn("Accounting and Audit", cat)
            self.assertNotIn("Real Estate", cat)
            self.assertNotIn("Big 4", cat)

        # Verify sections exist in 4.KR_Tech_BCI and 5.KR_전략_대기업_금융
        ws_kr_tech = wb["4.KR_Tech_BCI"]
        self.assertGreaterEqual(ws_kr_tech.max_row, 30)
        ws_kr_corp = wb["5.KR_전략_대기업_금융"]
        self.assertGreaterEqual(ws_kr_corp.max_row, 20)

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


if __name__ == "__main__":
    unittest.main()
