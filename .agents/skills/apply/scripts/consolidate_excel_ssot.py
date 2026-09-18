#!/usr/bin/env python3
"""
Consolidates all fragmented internship trackers into a single, unified Master SSOT workbook:
Master_Internship_Tracker_2027_SSOT.xlsx

Sources:
1. 2027_Summer2_Internship/2027_BCI_Internship_Tracker.xlsx
2. UK_2027_Summer_Internship_Trackr_Master.xlsx (or data/source_trackers/)
3. Korea_Internship_Research_2026_2027.xlsx (or data/source_trackers/)
"""

import sys
from copy import copy
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

WORKSPACE_ROOT = Path(r"G:\My Drive\Kyubin_Yun_Workspace\04_Internship")


def find_source_file(candidates: list[Path]) -> Path:
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError(f"None of the candidate source paths exist: {candidates}")


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
    """Builds the 0.CEO_Executive_Dashboard tab with navigation, KPIs, and ground truth."""
    ws.title = "0.CEO_Executive_Dashboard"
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
        "C": 24,  # Track / Category
        "D": 45,  # Focus Scope / Description
        "E": 14,  # Count / Status
        "F": 25,  # Jump Link
        "G": 30,  # Notes / Remarks
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
    cell_sub.value = "Candidate: Kyubin Yun (UCL BSc Psychology and Language Sciences, Class of 2028, Penultimate Year) | Zero Auto-Submit | SSOT Single Source of Truth"
    cell_sub.font = font_sub
    cell_sub.fill = navy_fill
    cell_sub.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[3].height = 20

    # Row 5: Section Header - Executive KPI Overview
    ws.merge_cells("B5:G5")
    s1 = ws["B5"]
    s1.value = "  📊 EXECUTIVE PORTFOLIO SUMMARY (850+ TRACKED OPPORTUNITIES)"
    s1.font = font_sec_head
    s1.fill = dark_header_fill
    s1.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[5].height = 24

    # Rows 6-8: KPI Metric Cards
    kpis = [
        ("B", "C", "GLOBAL BCI & NEUROTECH", "28 Firms / 84 Contacts", "Apple, Google, Meta, Neuralink"),
        ("D", "D", "UK 2027 TECH & FINANCE", "783 Roles (20 Curated)", "Palantir, Trackr UK Tech & Finance"),
        ("E", "E", "KOREA TOP ROLES", "55 Verified Positions", "KAIST BCI, Daangn, Bain/McK, Samsung"),
        ("F", "G", "SYSTEM STATUS", "SSOT READY / 100% AUDIT", "Zero Auto-Submit & Whale Browser Active"),
    ]

    for start_col, end_col, title, main_val, sub_text in kpis:
        # Title row 6
        cell_k_t = ws[f"{start_col}6"]
        cell_k_t.value = title
        cell_k_t.font = font_kpi_label
        cell_k_t.fill = kpi_card_fill
        cell_k_t.alignment = Alignment(horizontal="center", vertical="center")

        # Main val row 7
        cell_k_v = ws[f"{start_col}7"]
        cell_k_v.value = main_val
        cell_k_v.font = font_kpi_num
        cell_k_v.fill = kpi_card_fill
        cell_k_v.alignment = Alignment(horizontal="center", vertical="center")

        # Sub text row 8
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
    s2.value = "  🧭 MASTER SHEET DIRECTORY & INSTANT NAVIGATION (클릭 시 해당 시트로 이동)"
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
    # (Sheet Name, Target Sheet, Category, Scope, Count, Remarks)
    nav_data = [
        (
            "1.Global_BCI_Map",
            "1.Global_BCI_Map",
            "Global BCI / Neurotech",
            "글로벌 BCI & 테크 우선순위 맵 대시보드",
            "28개사",
            "Pastel Priority & Go to DB 링크",
        ),
        (
            "2.Research_Database",
            "2.Research_Database",
            "Global BCI / Neurotech",
            "기업별 리서치 적합도, 핵심 컨택 및 전략 훅",
            "84행 (3행/사)",
            "텔레메트리 G~K 은닉 준수",
        ),
        (
            "3.Global_BCI_Filtered",
            "3.Global_BCI_Filtered",
            "Global BCI / Neurotech",
            "석박사 전용 / 지원 조건 불일치 필터아웃 기업",
            "10개사",
            "추후 재검토용 아카이브",
        ),
        (
            "4.UK_Target_Master",
            "4.UK_Target_Master",
            "UK 2027 Summer Tech",
            "영국 하계인턴 1순위 타깃 (Palantir, Amazon 등)",
            "20개 타깃",
            "공식포털 단독발굴 및 L1 우선순위",
        ),
        (
            "5.UK_Trackr_Tech",
            "5.UK_Trackr_Tech",
            "UK 2027 Summer Tech",
            "영국 테크/SW/AI 하계인턴 전수 데이터",
            "286개 프로그램",
            "Trackr UK 검증 전수 DB",
        ),
        (
            "6.UK_Trackr_Finance",
            "6.UK_Trackr_Finance",
            "UK 2027 Summer Finance",
            "영국 퀀트/트레이딩/IB/컨설팅 하계인턴 전수 DB",
            "477개 프로그램",
            "Trackr UK 금융/컨설팅 전수",
        ),
        (
            "7.KR_통합일정_타임라인",
            "7.KR_통합일정_타임라인",
            "Korea Career 2026-2027",
            "국내 55개 타깃 기회 통합 타임라인 및 마감일",
            "55개 기회",
            "다가오는 순 정렬 및 역량 매칭",
        ),
        (
            "8.KR_종합요약_우선순위",
            "8.KR_종합요약_우선순위",
            "Korea Career 2026-2027",
            "국내 핵심 18대 우선순위 기회 행동 계획",
            "18개 타깃",
            "플랫폼 공고 직결 링크 탑재",
        ),
        (
            "9.KR_EEG_BCI_연구실",
            "9.KR_EEG_BCI_연구실",
            "Korea Research Labs",
            "KAIST/서울대/고려대 뇌공학·BCI 랩 인턴십",
            "11개 랩",
            "해외대 TrYBBE / 컨택 가이드",
        ),
        (
            "10.KR_데이터사이언스_DA",
            "10.KR_데이터사이언스_DA",
            "Korea Tech / Data Science",
            "당근/토스/네이버/카카오 DA 및 DS 인턴",
            "14개 포지션",
            "SQL, Python, A/B Test 매칭",
        ),
        (
            "11.KR_전략컨설팅_RA",
            "11.KR_전략컨설팅_RA",
            "Korea Strategy Consulting",
            "Bain, McKinsey, BCG, LEK 등 리서치 어시스턴트",
            "11개 포지션",
            "케이스 투입 및 정량분석",
        ),
        (
            "12.KR_대기업_해외대하계",
            "12.KR_대기업_해외대하계",
            "Korea Conglomerate",
            "삼성전자 DX/DS, SK하이닉스 해외대 인턴십",
            "5대 전형",
            "정규직 전환 특전 (2~3월 접수)",
        ),
        (
            "13.KR_외국계금융_IB",
            "13.KR_외국계금융_IB",
            "Korea Global Finance",
            "모건스탠리, 골드만삭스, BofA 서울 오피스 인턴",
            "6개 프로그램",
            "영/국문 이중언어 & 정량모델링",
        ),
        (
            "14.KR_AI_Agent_LLM",
            "14.KR_AI_Agent_LLM",
            "Korea AI Startups",
            "뤼튼, 스캐터랩 등 AI Agent 및 LLM 엔지니어",
            "8개 포지션",
            "Agentic 프레임워크 실무 매칭",
        ),
        (
            "15.UK_Overview_Dashboard",
            "15.UK_Overview_Dashboard",
            "UK Roadmap Summary",
            "영국 2027 하계 마스터 로드맵 원본 대시보드",
            "종합 요약",
            "기지원 21개사 배제 필터",
        ),
    ]

    curr_row = 12
    for s_name, target_s, cat, scope, count_str, remark in nav_data:
        # Col B: Sheet Name
        cb = ws[f"B{curr_row}"]
        cb.value = s_name
        cb.font = font_bold
        cb.border = table_border
        cb.alignment = Alignment(horizontal="left", vertical="center")

        # Col C: Category
        cc = ws[f"C{curr_row}"]
        cc.value = cat
        cc.font = font_regular
        cc.border = table_border
        cc.alignment = Alignment(horizontal="left", vertical="center")

        # Col D: Scope
        cd = ws[f"D{curr_row}"]
        cd.value = scope
        cd.font = font_regular
        cd.border = table_border
        cd.alignment = Alignment(horizontal="left", vertical="center")

        # Col E: Count
        ce = ws[f"E{curr_row}"]
        ce.value = count_str
        ce.font = font_bold
        ce.border = table_border
        ce.alignment = Alignment(horizontal="center", vertical="center")

        # Col F: Jump Link Formula
        cf = ws[f"F{curr_row}"]
        cf.value = f'=HYPERLINK("#\'{target_s}\'!A1", "➡️ {target_s} 바로가기")'
        cf.font = font_link
        cf.border = table_border
        cf.alignment = Alignment(horizontal="center", vertical="center")

        # Col G: Remark
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


def build_master_ssot():
    """Main orchestration function compiling the SSOT Excel workbook."""
    print("🚀 Starting Master SSOT Excel Compilation...")

    # Locate source files
    bci_candidates = [
        WORKSPACE_ROOT / "2027_Summer2_Internship" / "2027_BCI_Internship_Tracker.xlsx",
        WORKSPACE_ROOT / "data" / "source_trackers" / "2027_BCI_Internship_Tracker.xlsx",
    ]
    uk_candidates = [
        WORKSPACE_ROOT / "UK_2027_Summer_Internship_Trackr_Master.xlsx",
        WORKSPACE_ROOT / "data" / "source_trackers" / "UK_2027_Summer_Internship_Trackr_Master.xlsx",
    ]
    kr_candidates = [
        WORKSPACE_ROOT / "Korea_Internship_Research_2026_2027.xlsx",
        WORKSPACE_ROOT / "data" / "source_trackers" / "Korea_Internship_Research_2026_2027.xlsx",
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

    # Sheet 0: Executive Dashboard
    ws_dash = wb_master.active
    create_master_dashboard(ws_dash)

    # Sheet mapping: (Destination Sheet Name, Source Workbook, Source Sheet Name)
    sheet_mappings = [
        ("1.Global_BCI_Map", wb_bci, "1.Overview_Map"),
        ("2.Research_Database", wb_bci, "2.Research_Database"),
        ("3.Global_BCI_Filtered", wb_bci, "X.Filtered_Out"),
        ("4.UK_Target_Master", wb_uk, "2.Target_Applications_Master"),
        ("5.UK_Trackr_Tech", wb_uk, "3.Trackr_UK_Tech_Full"),
        ("6.UK_Trackr_Finance", wb_uk, "4.Trackr_UK_Finance_Full"),
        ("7.KR_통합일정_타임라인", wb_kr, "통합일정_타임라인"),
        ("8.KR_종합요약_우선순위", wb_kr, "종합요약_우선순위"),
        ("9.KR_EEG_BCI_연구실", wb_kr, "EEG_뇌공학_BCI_생체신호"),
        ("10.KR_데이터사이언스_DA", wb_kr, "데이터사이언티스트_분석가"),
        ("11.KR_전략컨설팅_RA", wb_kr, "전략컨설팅_RA"),
        ("12.KR_대기업_해외대하계", wb_kr, "대기업_해외대하계인턴_2027"),
        ("13.KR_외국계금융_IB", wb_kr, "외국계금융_IB_서울"),
        ("14.KR_AI_Agent_LLM", wb_kr, "AI_Agent_LLM_엔지니어"),
        ("15.UK_Overview_Dashboard", wb_uk, "1.Overview_Dashboard"),
    ]

    for dst_name, src_wb, src_name in sheet_mappings:
        print(f"  -> Copying [{src_name}] into [{dst_name}]...")
        dst_ws = wb_master.create_sheet(title=dst_name)
        copy_worksheet(src_wb[src_name], dst_ws)

    # Ensure telemetry columns G-K remain hidden in 2.Research_Database
    ws_db = wb_master["2.Research_Database"]
    for col_letter in ["G", "H", "I", "J", "K"]:
        ws_db.column_dimensions[col_letter].hidden = True

    # Save to Master SSOT file at root
    output_path = WORKSPACE_ROOT / "Master_Internship_Tracker_2027_SSOT.xlsx"
    print(f"💾 Saving unified Master SSOT workbook to: {output_path}...")
    wb_master.save(output_path)

    # Close all workbooks
    wb_master.close()
    wb_bci.close()
    wb_uk.close()
    wb_kr.close()

    print("✅ Master SSOT Workbook compilation completed successfully!")
    return output_path


if __name__ == "__main__":
    build_master_ssot()
