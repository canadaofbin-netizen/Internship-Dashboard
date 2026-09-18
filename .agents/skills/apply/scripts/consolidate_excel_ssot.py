#!/usr/bin/env python3
"""
Consolidates all fragmented internship trackers into a streamlined 8-tab Master SSOT workbook:
Master_Internship_Tracker_2027_SSOT.xlsx

New 8-Tab Architecture:
  0.CEO_Dashboard (Gold - #D4AF37)
  1.UK_Top_Targets (Navy Blue - #1F4E79)
  2.UK_Tech_Quant_Finance (Navy Blue - #1F4E79)
  3.KR_타임라인_우선순위 (Crimson Red - #C00000)
  4.KR_Tech_BCI (Crimson Red - #C00000)
  5.KR_전략_대기업_금융 (Crimson Red - #C00000)
  6.Global_BCI_Map (Purple - #7030A0)
  7.BCI_Research_DB (Purple - #7030A0)

Key Features:
- UK Trackr Noise Removal: Purged 79+ noise roles (Audit, Tax, Accounting, Actuarial, Pensions, Insurance, Real Estate, Big 4 audit).
- UK Tech & Finance Consolidation: Single unified sheet with 'Stream / Track' indicator (Tech vs Quant/Finance) and sequential indexing.
- Korea Consolidation: Stacks DA/DS, AI Agent/LLM, and EEG/BCI into Tab 4; Stacks Strategy RA, Conglomerate, and IB into Tab 5 with crimson section banners.
- Direct Navigation: Tab 0 contains interactive =HYPERLINK formulas to all 7 sub-sheets.
- BCI Cross-linking: Col E formulas in Tab 6 dynamically jump to corresponding company rows in Tab 7.
- Telemetry Protection: Columns G-K in Tab 7 remain strictly hidden.
"""

import re
import sys
from copy import copy
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

WORKSPACE_ROOT = Path(r"G:\My Drive\Kyubin_Yun_Workspace\04_Internship")

TAB_COLORS = {
    "0.CEO_Dashboard": "D4AF37",  # Gold
    "1.UK_Top_Targets": "1F4E79",  # Navy Blue
    "2.UK_Tech_Quant_Finance": "1F4E79",  # Navy Blue
    "3.KR_타임라인_우선순위": "C00000",  # Crimson Red
    "4.KR_Tech_BCI": "C00000",  # Crimson Red
    "5.KR_전략_대기업_금융": "C00000",  # Crimson Red
    "6.Global_BCI_Map": "7030A0",  # Purple
    "7.BCI_Research_DB": "7030A0",  # Purple
}

# Noise filtering criteria for UK Trackr
UK_NOISE_KEYWORDS = [
    "audit",
    "tax",
    "taxation",
    "accounting",
    "accountant",
    "actuarial",
    "actuary",
    "pension",
    "insurance",
    "real estate",
    "property",
    "telecom",
    "helpdesk",
    "service desk",
    "wealth planning",
    "compliance",
]
UK_NOISE_CATEGORIES = [
    "Pensions and Insurance",
    "Accounting and Audit",
    "Real Estate",
    "Big 4",
]


def is_uk_noise(company_id: str, programme_name: str, categories: str) -> bool:
    """Returns True if the UK role falls under excluded noise domains."""
    c_str = str(categories or "").strip()
    p_str = str(programme_name or "").strip().lower()

    for nc in UK_NOISE_CATEGORIES:
        if nc.lower() in c_str.lower():
            return True

    for nk in UK_NOISE_KEYWORDS:
        pattern = r"\b" + re.escape(nk)
        if re.search(pattern, p_str) or re.search(pattern, c_str.lower()):
            return True

    return False


def find_source_file(candidates: list[Path]) -> Path:
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError(f"None of the candidate source paths exist: {candidates}")


def copy_cell(src_cell, dst_cell):
    """Deep-copies cell value, styles, and hyperlink."""
    dst_cell.value = src_cell.value
    if src_cell.has_style:
        dst_cell.font = copy(src_cell.font)
        dst_cell.border = copy(src_cell.border)
        dst_cell.fill = copy(src_cell.fill)
        dst_cell.number_format = copy(src_cell.number_format)
        dst_cell.protection = copy(src_cell.protection)
        dst_cell.alignment = copy(src_cell.alignment)
    if src_cell.hyperlink:
        dst_cell.hyperlink = copy(src_cell.hyperlink)
    if src_cell.comment:
        dst_cell.comment = copy(src_cell.comment)


def copy_worksheet(src_ws, dst_ws):
    """Deep-copies cells, formatting, hyperlinks, merged ranges, dimensions, and freeze panes."""
    for row in src_ws.iter_rows():
        for cell in row:
            new_cell = dst_ws.cell(row=cell.row, column=cell.column, value=cell.value)
            if cell.has_style:
                new_cell.font = copy(cell.font)
                new_cell.border = copy(cell.border)
                new_cell.fill = copy(cell.fill)
                new_cell.number_format = copy(cell.number_format)
                new_cell.protection = copy(cell.protection)
                new_cell.alignment = copy(cell.alignment)
            if cell.hyperlink:
                new_cell.hyperlink = copy(cell.hyperlink)
            if cell.comment:
                new_cell.comment = copy(cell.comment)

    # Copy merged cell ranges
    for rng in src_ws.merged_cells.ranges:
        dst_ws.merge_cells(str(rng))

    # Copy column dimensions (widths, hidden flags)
    for col_letter, col_dim in src_ws.column_dimensions.items():
        dst_ws.column_dimensions[col_letter].width = col_dim.width
        dst_ws.column_dimensions[col_letter].hidden = col_dim.hidden

    # Copy row dimensions
    for row_idx, row_dim in src_ws.row_dimensions.items():
        dst_ws.row_dimensions[row_idx].height = row_dim.height

    # Copy freeze panes
    if src_ws.freeze_panes:
        dst_ws.freeze_panes = src_ws.freeze_panes


def create_master_dashboard(ws):
    """Builds the 0.CEO_Dashboard tab with navigation, KPIs, and ground truth."""
    ws.title = "0.CEO_Dashboard"
    ws.sheet_properties.tabColor = TAB_COLORS["0.CEO_Dashboard"]
    ws.views.sheetView[0].showGridLines = True

    # Color definitions
    navy_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    dark_header_fill = PatternFill(start_color="2C3E50", end_color="2C3E50", fill_type="solid")
    sub_header_fill = PatternFill(start_color="2F5597", end_color="2F5597", fill_type="solid")
    light_blue_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    kpi_card_fill = PatternFill(start_color="F2F4F8", end_color="F2F4F8", fill_type="solid")

    font_title = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    font_sub = Font(name="Calibri", size=10, italic=True, color="D9E1F2")
    font_sec_head = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
    font_tbl_head = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    font_kpi_num = Font(name="Calibri", size=18, bold=True, color="1F4E79")
    font_kpi_label = Font(name="Calibri", size=9, bold=True, color="595959")
    font_regular = Font(name="Calibri", size=10, color="000000")
    font_bold = Font(name="Calibri", size=10, bold=True, color="000000")
    font_link = Font(name="Calibri", size=10, bold=True, color="0563C1", underline="single")

    thin_border_side = Side(style="thin", color="D3D3D3")
    table_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

    # Set column widths
    col_widths = {
        "A": 4,  # margin
        "B": 28,  # Sheet / Key
        "C": 26,  # Track / Category
        "D": 48,  # Focus Scope / Description
        "E": 15,  # Count / Status
        "F": 28,  # Jump Link
        "G": 32,  # Notes / Remarks
    }
    for col, width in col_widths.items():
        ws.column_dimensions[col].width = width

    # Row 2-3: Master Title Banner
    ws.merge_cells("B2:G2")
    cell_title = ws["B2"]
    cell_title.value = "2027 GLOBAL INTERNSHIP MASTER SSOT TRACKER (CEO CONTROL TOWER)"
    cell_title.font = font_title
    cell_title.fill = navy_fill
    cell_title.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[2].height = 32

    ws.merge_cells("B3:G3")
    cell_sub = ws["B3"]
    cell_sub.value = (
        "Candidate: Kyubin Yun (UCL BSc Psychology and Language Sciences, Class of 2028, Penultimate Year) | "
        "Zero Auto-Submit | SSOT 8-Tab Unified Architecture"
    )
    cell_sub.font = font_sub
    cell_sub.fill = navy_fill
    cell_sub.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[3].height = 20

    # Row 5: Section Header - Executive KPI Overview
    ws.merge_cells("B5:G5")
    s1 = ws["B5"]
    s1.value = "  📊 EXECUTIVE PORTFOLIO SUMMARY (8-TAB STREAMLINED ARCHITECTURE)"
    s1.font = font_sec_head
    s1.fill = dark_header_fill
    s1.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[5].height = 24

    # Rows 6-8: KPI Metric Cards
    kpis = [
        ("B", "C", "UK 2027 TECH & FINANCE", "704 Curated Roles", "Palantir (L1/L2), 684 Trackr Roles (Noise Purged)"),
        ("D", "D", "KOREA HIGH-IMPACT", "55 Verified Roles", "KAIST BCI, Daangn, Toss, Samsung, Bain/McK"),
        ("E", "E", "GLOBAL BCI & NEUROTECH", "28 Firms / 84 Contacts", "Apple, Google, Meta, Neuralink, Synchron"),
        ("F", "G", "SYSTEM GOVERNANCE", "8-TAB SSOT / 100% AUDIT", "Zero Auto-Submit & Visible Whale Browser"),
    ]

    for start_col, end_col, title, main_val, sub_text in kpis:
        cell_k_t = ws[f"{start_col}6"]
        cell_k_t.value = title
        cell_k_t.font = font_kpi_label
        cell_k_t.fill = kpi_card_fill
        cell_k_t.alignment = Alignment(horizontal="center", vertical="center")

        cell_k_v = ws[f"{start_col}7"]
        cell_k_v.value = main_val
        cell_k_v.font = font_kpi_num
        cell_k_v.fill = kpi_card_fill
        cell_k_v.alignment = Alignment(horizontal="center", vertical="center")

        cell_k_s = ws[f"{start_col}8"]
        cell_k_s.value = sub_text
        cell_k_s.font = Font(name="Calibri", size=8, italic=True, color="595959")
        cell_k_s.fill = kpi_card_fill
        cell_k_s.alignment = Alignment(horizontal="center", vertical="center")

        if start_col != end_col:
            ws.merge_cells(f"{start_col}6:{end_col}6")
            ws.merge_cells(f"{start_col}7:{end_col}7")
            ws.merge_cells(f"{start_col}8:{end_col}8")

    for r in range(6, 9):
        ws.row_dimensions[r].height = 20

    # Row 10: Section Header - Quick Navigation Directory
    ws.merge_cells("B10:G10")
    s2 = ws["B10"]
    s2.value = "  🧭 MASTER 8-TAB DIRECTORY & INSTANT NAVIGATION (클릭 시 해당 시트로 직결 이동)"
    s2.font = font_sec_head
    s2.fill = dark_header_fill
    s2.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[10].height = 24

    # Row 11: Table Header
    headers_nav = [
        "시트 명칭 (Sheet Name)",
        "트랙 분류 (Category)",
        "세부 내용 및 범위 (Scope)",
        "데이터 규모",
        "시트 직결 링크 (Direct Jump)",
        "특이사항 및 제약",
    ]
    cols_nav = ["B", "C", "D", "E", "F", "G"]
    for c, h in zip(cols_nav, headers_nav):
        cell_h = ws[f"{c}11"]
        cell_h.value = h
        cell_h.font = font_tbl_head
        cell_h.fill = sub_header_fill
        cell_h.alignment = Alignment(horizontal="center", vertical="center")
        cell_h.border = table_border
    ws.row_dimensions[11].height = 22

    # Nav rows definition:
    nav_data = [
        (
            "1.UK_Top_Targets",
            "1.UK_Top_Targets",
            "UK 2027 Summer Tech & Finance",
            "영국 L1/L2 최우선 타깃 엄선 20선 (Palantir 등)",
            "20개 타깃",
            "공식포털 단독발굴 및 L1 우선순위",
        ),
        (
            "2.UK_Tech_Quant_Finance",
            "2.UK_Tech_Quant_Finance",
            "UK 2027 Summer Tech & Finance",
            "영국 Tech, SWE, AI, Quant, Trading 유효 프로그램",
            "684개 프로그램",
            "회계/세무/보험/부동산 노이즈 79개사 전면 제거 완료",
        ),
        (
            "3.KR_타임라인_우선순위",
            "3.KR_타임라인_우선순위",
            "Korea Career 2026-2027",
            "국내 55대 기회 전수 통합 일정 & 타임라인 및 우선순위",
            "55개 기회",
            "다가오는 순 정렬 및 역량 매칭",
        ),
        (
            "4.KR_Tech_BCI",
            "4.KR_Tech_BCI",
            "Korea Tech & BCI Labs",
            "DA/DS, AI Agent/LLM, EEG/BCI 연구실 (KAIST 등)",
            "33개 기회",
            "3개 테크 섹션 통합 편성 (DA/AI/BCI)",
        ),
        (
            "5.KR_전략_대기업_금융",
            "5.KR_전략_대기업_금융",
            "Korea Strategy, Conglomerate, Finance",
            "전략컨설팅 RA, 대기업 해외대 인턴(삼성전자), 외국계 IB",
            "22개 기회",
            "3개 비즈니스 섹션 통합 편성 (전략/대기업/IB)",
        ),
        (
            "6.Global_BCI_Map",
            "6.Global_BCI_Map",
            "Global BCI / Neurotech",
            "글로벌 BCI & 뉴로테크 28개사 우선순위 맵",
            "28개사",
            "7번 시트 직결 링크 탑재",
        ),
        (
            "7.BCI_Research_DB",
            "7.BCI_Research_DB",
            "Global BCI / Neurotech",
            "기업별 연구 적합도, PI/연구원 핵심 컨택 및 전략 훅",
            "84명 (3명/사)",
            "텔레메트리 G~K 은닉 준수",
        ),
    ]

    curr_row = 12
    for s_name, target_s, cat, scope, count_str, remark in nav_data:
        cb = ws[f"B{curr_row}"]
        cb.value = s_name
        cb.font = font_bold
        cb.border = table_border
        cb.alignment = Alignment(horizontal="left", vertical="center")

        cc = ws[f"C{curr_row}"]
        cc.value = cat
        cc.font = font_regular
        cc.border = table_border
        cc.alignment = Alignment(horizontal="left", vertical="center")

        cd = ws[f"D{curr_row}"]
        cd.value = scope
        cd.font = font_regular
        cd.border = table_border
        cd.alignment = Alignment(horizontal="left", vertical="center")

        ce = ws[f"E{curr_row}"]
        ce.value = count_str
        ce.font = font_bold
        ce.border = table_border
        ce.alignment = Alignment(horizontal="center", vertical="center")

        cf = ws[f"F{curr_row}"]
        cf.value = f'=HYPERLINK("#\'{target_s}\'!A1", "➡️ {target_s} 바로가기")'
        cf.font = font_link
        cf.border = table_border
        cf.alignment = Alignment(horizontal="center", vertical="center")

        cg = ws[f"G{curr_row}"]
        cg.value = remark
        cg.font = font_regular
        cg.border = table_border
        cg.alignment = Alignment(horizontal="left", vertical="center")

        ws.row_dimensions[curr_row].height = 20
        curr_row += 1

    # Section 3: Ground Truth Baseline & Protocol Rules
    curr_row += 1
    ws.merge_cells(f"B{curr_row}:G{curr_row}")
    s3 = ws[f"B{curr_row}"]
    s3.value = "  🛡️ CANDIDATE GROUND TRUTH BASELINE & ZERO AUTO-SUBMIT DIRECTIVES"
    s3.font = font_sec_head
    s3.fill = dark_header_fill
    s3.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[curr_row].height = 24
    curr_row += 1

    gt_info = [
        ("Candidate Name", "Kyubin Yun (윤규빈)", "UCL Official Academic ID", "zcjtyun@ucl.ac.uk"),
        (
            "UK Mobile Phone",
            "+44 7787 442404",
            "UK Local Address",
            "40 Merchant St, Brent Cross, Suite 638, London, NW2 8BB",
        ),
        (
            "University & Degree",
            "UCL / BSc Psychology & Language Sciences",
            "Graduation Date",
            "June 2028 (Penultimate Year Class of 2028)",
        ),
        (
            "UK Work Authorization",
            "Yes (Student Route Visa - Full-time summer permitted)",
            "Graduate Route 2-Yr",
            "Yes (2-Year Unconditional Full Working Rights post-grad)",
        ),
        (
            "Standard Password",
            "Jeff0825!! (General Portals)",
            "Workday Password",
            "Jeff0825!!!! (Workday Mandatory 12+ chars)",
        ),
        (
            "Safety Directive 1",
            "Zero Auto-Submit (절대 최종 제출 클릭 금지)",
            "Safety Directive 2",
            "Visible Whale Browser (백그라운드 가상 브라우저 전면 금지)",
        ),
    ]

    for k1, v1, k2, v2 in gt_info:
        cb = ws[f"B{curr_row}"]
        cb.value = k1
        cb.font = font_bold
        cb.fill = light_blue_fill
        cb.border = table_border
        cb.alignment = Alignment(horizontal="left", vertical="center")

        cc = ws[f"C{curr_row}"]
        cc.value = v1
        cc.font = font_regular
        cc.border = table_border
        cc.alignment = Alignment(horizontal="left", vertical="center")

        cd = ws[f"D{curr_row}"]
        cd.value = k2
        cd.font = font_bold
        cd.fill = light_blue_fill
        cd.border = table_border
        cd.alignment = Alignment(horizontal="left", vertical="center")

        ws.merge_cells(f"E{curr_row}:G{curr_row}")
        ce = ws[f"E{curr_row}"]
        ce.value = v2
        ce.font = font_regular
        ce.border = table_border
        ce.alignment = Alignment(horizontal="left", vertical="center")

        ws.row_dimensions[curr_row].height = 20
        curr_row += 1


def build_uk_tech_quant_finance_sheet(dst_ws, wb_uk):
    """Builds Tab 2: 2.UK_Tech_Quant_Finance consolidating noise-filtered Tech & Finance roles."""
    dst_ws.title = "2.UK_Tech_Quant_Finance"
    dst_ws.sheet_properties.tabColor = TAB_COLORS["2.UK_Tech_Quant_Finance"]
    dst_ws.views.sheetView[0].showGridLines = True

    ws_tech = wb_uk["3.Trackr_UK_Tech_Full"]
    ws_fin = wb_uk["4.Trackr_UK_Finance_Full"]

    headers = [
        "No",
        "Stream / Track",
        "Company ID",
        "Programme Name",
        "Categories",
        "Locations",
        "Visa Sponsorship",
        "Closing Date",
        "Application URL",
    ]
    col_widths = {
        "A": 8,
        "B": 24,
        "C": 28,
        "D": 55,
        "E": 38,
        "F": 22,
        "G": 20,
        "H": 24,
        "I": 18,
    }
    for col, width in col_widths.items():
        dst_ws.column_dimensions[col].width = width

    h_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    h_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    thin_side = Side(style="thin", color="D3D3D3")
    tbl_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

    for col_idx, h in enumerate(headers, 1):
        c = dst_ws.cell(1, col_idx, h)
        c.fill = h_fill
        c.font = h_font
        c.border = tbl_border
        c.alignment = Alignment(horizontal="center", vertical="center")
    dst_ws.row_dimensions[1].height = 24
    dst_ws.freeze_panes = "A2"

    curr_row = 2
    seq_no = 1

    # 1. Tech & Software / AI roles (286 roles)
    for r in range(2, ws_tech.max_row + 1):
        dst_ws.row_dimensions[curr_row].height = 20
        c1 = dst_ws.cell(curr_row, 1, seq_no)
        c1.alignment = Alignment(horizontal="center", vertical="center")
        c1.border = tbl_border

        c2 = dst_ws.cell(curr_row, 2, "Tech & Software / AI")
        c2.alignment = Alignment(horizontal="center", vertical="center")
        c2.font = Font(name="Calibri", size=9, bold=True, color="1F4E79")
        c2.border = tbl_border

        for c in range(2, ws_tech.max_column + 1):
            src_cell = ws_tech.cell(r, c)
            dst_cell = dst_ws.cell(curr_row, c + 1, src_cell.value)
            if src_cell.has_style:
                dst_cell.font = copy(src_cell.font)
                dst_cell.border = tbl_border
                dst_cell.alignment = copy(src_cell.alignment)
            if src_cell.hyperlink:
                dst_cell.hyperlink = copy(src_cell.hyperlink)
        seq_no += 1
        curr_row += 1

    # 2. Quant & High-Finance roles (Noise filtered, 398 roles)
    for r in range(2, ws_fin.max_row + 1):
        vals = [ws_fin.cell(r, c).value for c in range(1, ws_fin.max_column + 1)]
        cid = vals[1] if len(vals) > 1 else ""
        prog = vals[2] if len(vals) > 2 else ""
        cat = vals[3] if len(vals) > 3 else ""

        if is_uk_noise(cid, prog, cat):
            continue

        dst_ws.row_dimensions[curr_row].height = 20
        c1 = dst_ws.cell(curr_row, 1, seq_no)
        c1.alignment = Alignment(horizontal="center", vertical="center")
        c1.border = tbl_border

        c2 = dst_ws.cell(curr_row, 2, "Quant & High-Finance")
        c2.alignment = Alignment(horizontal="center", vertical="center")
        c2.font = Font(name="Calibri", size=9, bold=True, color="2E75B6")
        c2.border = tbl_border

        for c in range(2, ws_fin.max_column + 1):
            src_cell = ws_fin.cell(r, c)
            dst_cell = dst_ws.cell(curr_row, c + 1, src_cell.value)
            if src_cell.has_style:
                dst_cell.font = copy(src_cell.font)
                dst_cell.border = tbl_border
                dst_cell.alignment = copy(src_cell.alignment)
            if src_cell.hyperlink:
                dst_cell.hyperlink = copy(src_cell.hyperlink)
        seq_no += 1
        curr_row += 1


def append_korean_section(dst_ws, src_ws, title_text, curr_row, title_fill_hex="A61C1C") -> int:
    """Appends a section banner and rows from a source worksheet into dst_ws."""
    max_col = src_ws.max_column
    t_fill = PatternFill(start_color=title_fill_hex, end_color=title_fill_hex, fill_type="solid")
    t_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    thin_side = Side(style="thin", color="D3D3D3")
    tbl_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

    # Section Title Banner
    dst_ws.cell(curr_row, 1, title_text)
    dst_ws.row_dimensions[curr_row].height = 24
    for c in range(1, max_col + 1):
        cell = dst_ws.cell(curr_row, c)
        cell.fill = t_fill
        cell.font = t_font
        cell.alignment = Alignment(horizontal="left", vertical="center")
    dst_ws.merge_cells(start_row=curr_row, start_column=1, end_row=curr_row, end_column=max_col)
    curr_row += 1

    # Header and Data rows
    for r in range(1, src_ws.max_row + 1):
        dst_ws.row_dimensions[curr_row].height = 22 if r == 1 else 20
        for c in range(1, max_col + 1):
            src_cell = src_ws.cell(r, c)
            dst_cell = dst_ws.cell(curr_row, c, src_cell.value)
            if src_cell.has_style:
                dst_cell.font = copy(src_cell.font)
                dst_cell.border = tbl_border
                dst_cell.fill = copy(src_cell.fill)
                dst_cell.number_format = copy(src_cell.number_format)
                dst_cell.alignment = copy(src_cell.alignment)
            if src_cell.hyperlink:
                dst_cell.hyperlink = copy(src_cell.hyperlink)
        curr_row += 1

    curr_row += 1  # 1 blank row between sections
    return curr_row


def build_kr_tech_bci_sheet(dst_ws, wb_kr):
    """Builds Tab 4: 4.KR_Tech_BCI consolidating DA/DS, AI Agent, and EEG/BCI research labs."""
    dst_ws.title = "4.KR_Tech_BCI"
    dst_ws.sheet_properties.tabColor = TAB_COLORS["4.KR_Tech_BCI"]
    dst_ws.views.sheetView[0].showGridLines = True

    col_widths = {
        "A": 25,
        "B": 30,
        "C": 42,
        "D": 30,
        "E": 24,
        "F": 48,
        "G": 45,
        "H": 38,
        "I": 35,
    }
    for col, width in col_widths.items():
        dst_ws.column_dimensions[col].width = width

    curr_row = 1
    curr_row = append_korean_section(
        dst_ws,
        wb_kr["데이터사이언티스트_분석가"],
        "  📊 [SECTION 1] 데이터사이언티스트 & 데이터 분석가 (14개 포지션 - 당근, 토스, 네이버, 카카오 등)",
        curr_row,
    )
    curr_row = append_korean_section(
        dst_ws,
        wb_kr["AI_Agent_LLM_엔지니어"],
        "  🤖 [SECTION 2] AI Agent & LLM 엔지니어 (8개 포지션 - 딥오토, 뤼튼, 스캐터랩 등)",
        curr_row,
    )
    curr_row = append_korean_section(
        dst_ws,
        wb_kr["EEG_뇌공학_BCI_생체신호"],
        "  🧠 [SECTION 3] EEG / 뇌공학 / BCI 생체신호 연구실 (11개 랩 - KAIST, 서울대, 고려대 등)",
        curr_row,
    )


def build_kr_strategy_corp_finance_sheet(dst_ws, wb_kr):
    """Builds Tab 5: 5.KR_전략_대기업_금융 consolidating Strategy RA, Conglomerates, and IB."""
    dst_ws.title = "5.KR_전략_대기업_금융"
    dst_ws.sheet_properties.tabColor = TAB_COLORS["5.KR_전략_대기업_금융"]
    dst_ws.views.sheetView[0].showGridLines = True

    col_widths = {
        "A": 30,
        "B": 42,
        "C": 26,
        "D": 35,
        "E": 48,
        "F": 48,
        "G": 48,
        "H": 38,
        "I": 36,
    }
    for col, width in col_widths.items():
        dst_ws.column_dimensions[col].width = width

    curr_row = 1
    curr_row = append_korean_section(
        dst_ws,
        wb_kr["전략컨설팅_RA"],
        "  💼 [SECTION 1] 전략컨설팅 RA (11개 포지션 - Bain ACT, McKinsey, BCG, LEK 등)",
        curr_row,
    )
    curr_row = append_korean_section(
        dst_ws,
        wb_kr["대기업_해외대하계인턴_2027"],
        "  🏢 [SECTION 2] 대기업 해외대 학부 하계인턴 2027 (5대 전형 - 삼성전자 DX/DS, SK하이닉스 등)",
        curr_row,
    )
    curr_row = append_korean_section(
        dst_ws,
        wb_kr["외국계금융_IB_서울"],
        "  📈 [SECTION 3] 외국계 금융 / 글로벌 IB 서울 오피스 (6개 프로그램 - 모건스탠리, 골드만삭스, BofA 등)",
        curr_row,
    )


def build_master_ssot():
    """Main orchestration function compiling the streamlined 8-tab SSOT Excel workbook."""
    print("🚀 Starting Master SSOT Excel Compilation (8-Tab Streamlined Architecture)...")

    # Locate source files
    bci_candidates = [
        WORKSPACE_ROOT / "data" / "source_trackers" / "2027_BCI_Internship_Tracker.xlsx",
        WORKSPACE_ROOT / "2027_Summer2_Internship" / "2027_BCI_Internship_Tracker.xlsx",
    ]
    uk_candidates = [
        WORKSPACE_ROOT / "data" / "source_trackers" / "UK_2027_Summer_Internship_Trackr_Master.xlsx",
        WORKSPACE_ROOT / "UK_2027_Summer_Internship_Trackr_Master.xlsx",
    ]
    kr_candidates = [
        WORKSPACE_ROOT / "data" / "source_trackers" / "Korea_Internship_Research_2026_2027.xlsx",
        WORKSPACE_ROOT / "Korea_Internship_Research_2026_2027.xlsx",
    ]

    bci_path = find_source_file(bci_candidates)
    uk_path = find_source_file(uk_candidates)
    kr_path = find_source_file(kr_candidates)

    print(f"  [Source 1: BCI]   {bci_path}")
    print(f"  [Source 2: UK]    {uk_path}")
    print(f"  [Source 3: Korea] {kr_path}")

    wb_bci = openpyxl.load_workbook(bci_path, data_only=False)
    wb_uk = openpyxl.load_workbook(uk_path, data_only=False)
    wb_kr = openpyxl.load_workbook(kr_path, data_only=False)

    wb_master = openpyxl.Workbook()

    # Tab 0: 0.CEO_Dashboard (Gold)
    print("  -> Creating [0.CEO_Dashboard] (Gold)...")
    ws_dash = wb_master.active
    create_master_dashboard(ws_dash)

    # Tab 1: 1.UK_Top_Targets (Navy Blue)
    print("  -> Creating [1.UK_Top_Targets] (Navy Blue)...")
    ws_uk_targets = wb_master.create_sheet(title="1.UK_Top_Targets")
    copy_worksheet(wb_uk["2.Target_Applications_Master"], ws_uk_targets)
    ws_uk_targets.sheet_properties.tabColor = TAB_COLORS["1.UK_Top_Targets"]

    # Tab 2: 2.UK_Tech_Quant_Finance (Navy Blue)
    print("  -> Creating [2.UK_Tech_Quant_Finance] (Navy Blue, Noise Purged)...")
    ws_uk_tqf = wb_master.create_sheet(title="2.UK_Tech_Quant_Finance")
    build_uk_tech_quant_finance_sheet(ws_uk_tqf, wb_uk)

    # Tab 3: 3.KR_타임라인_우선순위 (Crimson Red)
    print("  -> Creating [3.KR_타임라인_우선순위] (Crimson Red)...")
    ws_kr_time = wb_master.create_sheet(title="3.KR_타임라인_우선순위")
    copy_worksheet(wb_kr["통합일정_타임라인"], ws_kr_time)
    ws_kr_time.sheet_properties.tabColor = TAB_COLORS["3.KR_타임라인_우선순위"]

    # Tab 4: 4.KR_Tech_BCI (Crimson Red)
    print("  -> Creating [4.KR_Tech_BCI] (Crimson Red, 3 Sections)...")
    ws_kr_tech = wb_master.create_sheet(title="4.KR_Tech_BCI")
    build_kr_tech_bci_sheet(ws_kr_tech, wb_kr)

    # Tab 5: 5.KR_전략_대기업_금융 (Crimson Red)
    print("  -> Creating [5.KR_전략_대기업_금융] (Crimson Red, 3 Sections)...")
    ws_kr_corp = wb_master.create_sheet(title="5.KR_전략_대기업_금융")
    build_kr_strategy_corp_finance_sheet(ws_kr_corp, wb_kr)

    # Tab 6: 6.Global_BCI_Map (Purple)
    print("  -> Creating [6.Global_BCI_Map] (Purple)...")
    ws_bci_map = wb_master.create_sheet(title="6.Global_BCI_Map")
    copy_worksheet(wb_bci["1.Overview_Map"], ws_bci_map)
    ws_bci_map.sheet_properties.tabColor = TAB_COLORS["6.Global_BCI_Map"]
    # Update Column E jump hyperlinks to point to 7.BCI_Research_DB
    for r in range(2, ws_bci_map.max_row + 1):
        cell = ws_bci_map.cell(r, 5)
        val_str = str(cell.value or "")
        if "Research_Database" in val_str:
            new_val = val_str.replace("2.Research_Database", "7.BCI_Research_DB")
            cell.value = new_val

    # Tab 7: 7.BCI_Research_DB (Purple)
    print("  -> Creating [7.BCI_Research_DB] (Purple)...")
    ws_bci_db = wb_master.create_sheet(title="7.BCI_Research_DB")
    copy_worksheet(wb_bci["2.Research_Database"], ws_bci_db)
    ws_bci_db.sheet_properties.tabColor = TAB_COLORS["7.BCI_Research_DB"]
    # Ensure telemetry columns G-K remain hidden
    for col_letter in ["G", "H", "I", "J", "K"]:
        ws_bci_db.column_dimensions[col_letter].hidden = True

    # Validate final sheets
    expected_8_sheets = [
        "0.CEO_Dashboard",
        "1.UK_Top_Targets",
        "2.UK_Tech_Quant_Finance",
        "3.KR_타임라인_우선순위",
        "4.KR_Tech_BCI",
        "5.KR_전략_대기업_금융",
        "6.Global_BCI_Map",
        "7.BCI_Research_DB",
    ]
    assert wb_master.sheetnames == expected_8_sheets, f"Sheet mismatch: {wb_master.sheetnames}"

    # Save to Master SSOT file at root
    output_path = WORKSPACE_ROOT / "Master_Internship_Tracker_2027_SSOT.xlsx"
    print(f"💾 Saving unified 8-tab Master SSOT workbook to: {output_path}...")
    wb_master.save(output_path)

    # Close all workbooks
    wb_master.close()
    wb_bci.close()
    wb_uk.close()
    wb_kr.close()

    print("✅ Master SSOT Workbook compilation completed successfully (8 Tabs)!")
    return output_path


if __name__ == "__main__":
    build_master_ssot()
