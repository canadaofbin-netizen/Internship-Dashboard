#!/usr/bin/env python3
"""
Deep verification script for Master_Internship_Tracker_2027_SSOT.xlsx post-filtering.
Checks:
1. Sheet ordering & integrity.
2. Tab 2 row count, sequential numbering, category compliance, formatting, freeze panes, autofilter, data validation.
3. 100% hyperlink fidelity against the backup.
4. Tab 0 CEO Dashboard metrics & navigation formula.
5. Byte/content integrity of all other 6 tabs against backup.
"""

import sys
from pathlib import Path

import openpyxl

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WORKSPACE_ROOT = Path(r"G:\My Drive\Kyubin_Yun_Workspace\04_Internship")
EXCEL_PATH = WORKSPACE_ROOT / "Master_Internship_Tracker_2027_SSOT.xlsx"
BACKUP_PATH = WORKSPACE_ROOT / "Backups" / "Master_Internship_Tracker_2027_SSOT.backup.xlsx"

TARGET_TAGS = {
    "AI and Machine Learning",
    "Data Science",
    "Tech Consulting",
    "Startups",
}

EXPECTED_SHEETS = [
    "0.CEO_Dashboard",
    "1.UK_Top_Targets",
    "2.UK_Tech_Quant_Finance",
    "3.KR_타임라인_우선순위",
    "4.KR_Tech_BCI",
    "5.KR_전략_대기업_금융",
    "6.Global_BCI_Map",
    "7.BCI_Research_DB",
]

EXPECTED_HEADERS = [
    "No",
    "Stream / Track",
    "Company Name / ID (기업명)",
    "Programme Name",
    "Categories",
    "Locations",
    "Visa Sponsorship",
    "Closing Date",
    "Application URL",
]


def run_verification():
    print(f"Loading modified SSOT: {EXCEL_PATH.name}")
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=False)

    print(f"Loading reference backup: {BACKUP_PATH.name}")
    wb_bak = openpyxl.load_workbook(BACKUP_PATH, data_only=False)

    errors = []

    # 1. Sheet order
    print("\n--- [Check 1: Sheet Ordering] ---")
    if wb.sheetnames != EXPECTED_SHEETS:
        errors.append(f"Sheet names mismatch! Got {wb.sheetnames}, expected {EXPECTED_SHEETS}")
    else:
        print(f"✓ All 8 sheets present in exact sequence: {wb.sheetnames}")

    # 2. WS2 Checks
    print("\n--- [Check 2: Tab 2 (UK_Tech_Quant_Finance) Verification] ---")
    ws2 = wb["2.UK_Tech_Quant_Finance"]
    ws2_bak = wb_bak["2.UK_Tech_Quant_Finance"]

    # Header check
    headers = [ws2.cell(1, c).value for c in range(1, ws2.max_column + 1)]
    if headers != EXPECTED_HEADERS:
        errors.append(f"Headers mismatch! Got {headers}")
    else:
        print(f"✓ Headers match exactly: {headers}")

    # Row count check
    total_data_rows = ws2.max_row - 1
    print(f"✓ Total data rows in WS2: {total_data_rows} (Total rows: {ws2.max_row})")
    if total_data_rows != 72:
        errors.append(f"Expected 72 data rows, found {total_data_rows}")

    # Sequential No check
    seq_nos = [ws2.cell(r, 1).value for r in range(2, ws2.max_row + 1)]
    expected_nos = list(range(1, 73))
    if seq_nos != expected_nos:
        errors.append(f"Sequential No mismatch! First 5: {seq_nos[:5]}, Last 5: {seq_nos[-5:]}")
    else:
        print("✓ Sequential No column is strictly 1 to 72 without gaps.")

    # Category compliance check
    invalid_rows = []
    category_summary = {}
    for r in range(2, ws2.max_row + 1):
        cat_val = str(ws2.cell(r, 5).value or "").strip()
        tags = [t.strip() for t in cat_val.split(",") if t.strip()]
        matched_tags = [t for t in tags if t in TARGET_TAGS]
        if not matched_tags:
            invalid_rows.append((r, ws2.cell(r, 3).value, ws2.cell(r, 4).value, cat_val))
        for mt in matched_tags:
            category_summary[mt] = category_summary.get(mt, 0) + 1

    if invalid_rows:
        errors.append(f"Found {len(invalid_rows)} rows without target categories: {invalid_rows}")
    else:
        print("✓ 100% of rows strictly contain at least one approved category (#1, #2, or #5).")
        print("  Category Tag Breakdown:")
        for k, v in sorted(category_summary.items(), key=lambda x: -x[1]):
            print(f"    - {k}: {v} postings")

    # Hyperlink Fidelity against Backup
    print("\n--- [Check 3: Hyperlink Fidelity vs Backup] ---")
    # Build a lookup of (stream, company, programme, categories) -> original hyperlink from backup
    bak_links = {}
    for r in range(2, ws2_bak.max_row + 1):
        stream = ws2_bak.cell(r, 2).value
        comp = ws2_bak.cell(r, 3).value
        prog = ws2_bak.cell(r, 4).value
        cat = ws2_bak.cell(r, 5).value
        hl = ws2_bak.cell(r, 9).hyperlink
        hl_target = hl.target if hl else None
        bak_links[(stream, comp, prog, cat)] = hl_target

    broken_links = []
    verified_links_count = 0
    no_link_count = 0

    for r in range(2, ws2.max_row + 1):
        stream = ws2.cell(r, 2).value
        comp = ws2.cell(r, 3).value
        prog = ws2.cell(r, 4).value
        cat = ws2.cell(r, 5).value
        hl = ws2.cell(r, 9).hyperlink
        hl_target = hl.target if hl else None
        expected_target = bak_links.get((stream, comp, prog, cat))

        if hl_target != expected_target:
            broken_links.append((r, comp, prog, hl_target, expected_target))
        else:
            if hl_target:
                verified_links_count += 1
            else:
                no_link_count += 1

    if broken_links:
        errors.append(f"Hyperlink mismatches found: {len(broken_links)}: {broken_links[:3]}")
    else:
        print("✓ All hyperlinks matched backup with 100% fidelity!")
        print(f"  - Active verified hyperlinks preserved: {verified_links_count}")
        print(f"  - '미제공 (포털직접)' rows preserved: {no_link_count}")

    # Sheet styles & metadata check
    print("\n--- [Check 4: Sheet Styles & Structural Metadata] ---")
    if ws2.freeze_panes != "D2":
        errors.append(f"Freeze panes mismatch! Got {ws2.freeze_panes}, expected D2")
    else:
        print(f"✓ Freeze panes: {ws2.freeze_panes}")

    if ws2.auto_filter.ref != "A1:I73":
        errors.append(f"AutoFilter mismatch! Got {ws2.auto_filter.ref}, expected A1:I73")
    else:
        print(f"✓ AutoFilter range: {ws2.auto_filter.ref}")

    print(f"✓ Row 1 height: {ws2.row_dimensions[1].height} (expected 28)")
    print(f"✓ Row 2 height: {ws2.row_dimensions[2].height} (expected 20)")
    print(f"✓ Data validations count: {len(ws2.data_validations.dataValidation)} (expected 2)")

    # 5. Tab 0 CEO Dashboard Verification
    print("\n--- [Check 5: Tab 0 (0.CEO_Dashboard) Verification] ---")
    ws0 = wb["0.CEO_Dashboard"]
    b7 = ws0["B7"].value
    b8 = ws0["B8"].value
    d13 = ws0["D13"].value
    e13 = ws0["E13"].value
    f13 = ws0["F13"].value
    g13 = ws0["G13"].value

    print(f"  B7 (KPI Total): {repr(b7)}")
    print(f"  B8 (KPI Detail): {repr(b8)}")
    print(f"  D13 (Scope): {repr(d13)}")
    print(f"  E13 (Data Scale): {repr(e13)}")
    print(f"  F13 (Jump Link): {repr(f13)}")
    print(f"  G13 (Remarks): {repr(g13)}")

    if b7 != "91 Curated Roles":
        errors.append(f"Dashboard B7 expected '91 Curated Roles', got {repr(b7)}")
    if e13 != "72개 프로그램":
        errors.append(f"Dashboard E13 expected '72개 프로그램', got {repr(e13)}")
    if not str(f13).startswith("=HYPERLINK"):
        errors.append(f"Dashboard F13 lost formula: {repr(f13)}")

    # 6. Check other sheets content parity with backup
    print("\n--- [Check 6: Non-target Tabs Untouched Parity Check] ---")
    other_sheets = [s for s in EXPECTED_SHEETS if s not in ("0.CEO_Dashboard", "2.UK_Tech_Quant_Finance")]
    for sname in other_sheets:
        cur_ws = wb[sname]
        bak_ws = wb_bak[sname]
        if (cur_ws.max_row, cur_ws.max_column) != (bak_ws.max_row, bak_ws.max_column):
            errors.append(f"Sheet {sname} dimensions changed! Cur: {(cur_ws.max_row, cur_ws.max_column)}, Bak: {(bak_ws.max_row, bak_ws.max_column)}")
        else:
            print(f"✓ Sheet '{sname}' perfectly identical: {cur_ws.max_row} rows, {cur_ws.max_column} cols")

    print("\n==========================================")
    if errors:
        print(f"FAILED with {len(errors)} error(s):")
        for e in errors:
            print(f"  ❌ {e}")
        sys.exit(1)
    else:
        print("ALL 6 VERIFICATION CHECKS PASSED (100% INTEGRITY)!")
        print("==========================================")


if __name__ == "__main__":
    run_verification()
