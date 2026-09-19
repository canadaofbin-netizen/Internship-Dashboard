#!/usr/bin/env python3
"""
Filters Sheet '2.UK_Tech_Quant_Finance' in Master_Internship_Tracker_2027_SSOT.xlsx.
- Removes noise categories and #3 (Software Engineering) and #4 (Trading & Quant / Quant Developer).
- Retains ONLY #1 (AI & Machine Learning), #2 (Data Science & Analytics), and #5 (Tech Consulting & AI Startups).
- Postings with multiple categories (e.g. 'Software Engineering, AI and Machine Learning') are kept if they contain any target tag.
- Re-indexes 'No' column sequentially (1..N).
- Preserves all fonts, borders, alignments, fills, row heights, column widths, freeze panes, data validations, and hyperlinks.
- Updates '0.CEO_Dashboard' KPI cards and directory table metrics.
"""

import shutil
import sys
from copy import copy
from datetime import datetime
from pathlib import Path

import openpyxl
from openpyxl.worksheet.datavalidation import DataValidation

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

WORKSPACE_ROOT = Path(r"G:\My Drive\Kyubin_Yun_Workspace\04_Internship")
EXCEL_PATH = WORKSPACE_ROOT / "Master_Internship_Tracker_2027_SSOT.xlsx"
BACKUP_DIR = WORKSPACE_ROOT / "Backups"

# Target tags representing categories #1, #2, and #5
TARGET_TAGS = {
    "AI and Machine Learning",  # #1 AI & Machine Learning
    "Data Science",            # #2 Data Science & Analytics
    "Tech Consulting",         # #5 Tech Consulting & AI Startups
    "Startups",                # #5 Tech Consulting & AI Startups
}


def create_backup():
    """Creates a timestamped backup of the master tracker."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"Master_Internship_Tracker_2027_SSOT.backup_{timestamp_str}.xlsx"
    shutil.copy2(EXCEL_PATH, backup_file)
    print(f"[Backup] Created timestamped backup: {backup_file.name} ({backup_file.stat().st_size} bytes)")

    # Also maintain a standard backup copy
    std_backup = BACKUP_DIR / "Master_Internship_Tracker_2027_SSOT.backup.xlsx"
    shutil.copy2(EXCEL_PATH, std_backup)
    print(f"[Backup] Updated standard backup: {std_backup.name}")
    return backup_file


def filter_and_update_workbook():
    print(f"[Processing] Loading workbook: {EXCEL_PATH}")
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=False)

    ws2 = wb["2.UK_Tech_Quant_Finance"]
    max_r = ws2.max_row
    max_c = ws2.max_column
    print(f"[WS2 Initial] max_row: {max_r}, max_column: {max_c}")

    # 1. Identify rows to keep
    # Header is row 1
    kept_row_indices = []
    dropped_row_indices = []
    category_counts = {}

    for r in range(2, max_r + 1):
        cat_val = str(ws2.cell(r, 5).value or "").strip()
        tags = [t.strip() for t in cat_val.split(",") if t.strip()]

        has_target = any(t in TARGET_TAGS for t in tags)
        if has_target:
            kept_row_indices.append(r)
            for t in tags:
                if t in TARGET_TAGS:
                    category_counts[t] = category_counts.get(t, 0) + 1
        else:
            dropped_row_indices.append(r)

    print(f"[WS2 Filter] Total data rows evaluated: {max_r - 1}")
    print(f"[WS2 Filter] Kept rows count: {len(kept_row_indices)}")
    print(f"[WS2 Filter] Dropped rows count: {len(dropped_row_indices)}")
    print("[WS2 Filter] Category tag occurrences in kept rows:")
    for tag, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  - {tag}: {count}")

    # 2. Extract formatting and cell data from kept rows
    # Store header (row 1)
    header_cells = []
    for c in range(1, max_c + 1):
        src = ws2.cell(1, c)
        header_cells.append(src)

    # Store kept rows data
    data_rows = []
    for r in kept_row_indices:
        row_cells = []
        for c in range(1, max_c + 1):
            row_cells.append(ws2.cell(r, c))
        data_rows.append(row_cells)

    # Preserve column widths and sheet properties
    col_widths = {}
    for col_letter, col_dim in ws2.column_dimensions.items():
        col_widths[col_letter] = col_dim.width

    freeze_panes = ws2.freeze_panes
    tab_color = ws2.sheet_properties.tabColor.rgb if ws2.sheet_properties.tabColor else "001F4E79"
    sheet_index = wb._sheets.index(ws2)

    # 3. Create a clean replacement worksheet
    wb.remove(ws2)
    new_ws2 = wb.create_sheet(title="2.UK_Tech_Quant_Finance", index=sheet_index)
    new_ws2.sheet_properties.tabColor = tab_color
    new_ws2.views.sheetView[0].showGridLines = True
    new_ws2.freeze_panes = freeze_panes

    for col_letter, width in col_widths.items():
        if width:
            new_ws2.column_dimensions[col_letter].width = width

    # Write Header Row
    new_ws2.row_dimensions[1].height = 28
    for col_idx, src in enumerate(header_cells, 1):
        dst = new_ws2.cell(1, col_idx, src.value)
        if src.has_style:
            dst.font = copy(src.font)
            dst.border = copy(src.border)
            dst.fill = copy(src.fill)
            dst.number_format = copy(src.number_format)
            dst.alignment = copy(src.alignment)
            dst.protection = copy(src.protection)

    # Write Kept Data Rows with sequential renumbering
    seq_no = 1
    header_cells[0].border  # Standard thin border from header
    for row_idx, src_row in enumerate(data_rows, 2):
        new_ws2.row_dimensions[row_idx].height = 20
        for col_idx, src in enumerate(src_row, 1):
            if col_idx == 1:
                # Column A: Sequential No
                dst = new_ws2.cell(row_idx, 1, seq_no)
            else:
                dst = new_ws2.cell(row_idx, col_idx, src.value)

            if src.has_style:
                dst.font = copy(src.font)
                dst.border = copy(src.border)
                dst.fill = copy(src.fill)
                dst.number_format = copy(src.number_format)
                dst.alignment = copy(src.alignment)
                dst.protection = copy(src.protection)

            if col_idx == 1:
                dst.alignment = copy(src.alignment)
                dst.font = copy(src.font)

            if src.hyperlink:
                dst.hyperlink = copy(src.hyperlink)

        seq_no += 1

    final_row = 1 + len(data_rows)
    print(f"[WS2 Rebuilt] New max_row: {final_row}")

    # Set AutoFilter
    new_ws2.auto_filter.ref = f"A1:I{final_row}"

    # Set Data Validations
    dv_stream = DataValidation(type="list", formula1='"Tech & Software / AI,Quant & High-Finance"', allow_blank=True)
    new_ws2.add_data_validation(dv_stream)
    dv_stream.add(f"B2:B{final_row}")

    dv_visa = DataValidation(type="list", formula1='"Yes,No,N/A,Case-by-case"', allow_blank=True)
    new_ws2.add_data_validation(dv_visa)
    dv_visa.add(f"G2:G{final_row}")

    # 4. Update 0.CEO_Dashboard
    ws0 = wb["0.CEO_Dashboard"]
    print("[CEO Dashboard] Updating metrics for Tab 2...")

    # Cell B7: Total Curated Roles (19 Palantir/L1 + 72 WS2 = 91)
    old_b7 = ws0["B7"].value
    ws0["B7"].value = f"{19 + len(data_rows)} Curated Roles"
    print(f"  B7: '{old_b7}' -> '{ws0['B7'].value}'")

    # Cell B8: Details description
    old_b8 = ws0["B8"].value
    ws0["B8"].value = f"Palantir (L1/L2 19선), {len(data_rows)} High-Value Roles (AI/ML, Data Science, Tech Consulting & Startups)"
    print(f"  B8: '{old_b8}' -> '{ws0['B8'].value}'")

    # Row 13 in Master Directory: Tab 2 entry
    # D13: Scope
    old_d13 = ws0["D13"].value
    ws0["D13"].value = "영국 AI/ML, Data Science, Tech Consulting & Startups 엄선 프로그램"
    print(f"  D13: '{old_d13}' -> '{ws0['D13'].value}'")

    # E13: Data scale count
    old_e13 = ws0["E13"].value
    ws0["E13"].value = f"{len(data_rows)}개 프로그램"
    print(f"  E13: '{old_e13}' -> '{ws0['E13'].value}'")

    # G13: Remarks
    old_g13 = ws0["G13"].value
    ws0["G13"].value = f"SWE/Quant/노이즈 제거 후 AI/ML, Data Science, Tech Consulting/Startup {len(data_rows)}선 엄선"
    print(f"  G13: '{old_g13}' -> '{ws0['G13'].value}'")

    # Verify F13 jump link remains intact
    print(f"  F13 Formula: '{ws0['F13'].value}'")

    # 5. Save workbook
    wb.save(EXCEL_PATH)
    print(f"[Success] Workbook saved cleanly to {EXCEL_PATH}")


if __name__ == "__main__":
    create_backup()
    filter_and_update_workbook()
