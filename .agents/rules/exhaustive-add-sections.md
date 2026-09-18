---
description: "Exhaustive Add-Section Exploration & Population Protocol (모듈형 폼 내 추가(Add) 섹션 전수 탐색 및 후보자 데이터 완전 입력 규칙)"
globs: ["**/*"]
alwaysApply: true
---

# Exhaustive Add-Section Exploration & Population Protocol

- **Workspace Directives**: [AGENTS.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/AGENTS.md)
- **Baseline Data**: [Candidate Ground Truth Baseline](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/candidate-ground-truth.md)

이 규칙은 Workday, TikTok Careers, Greenhouse, Lever 등 채용 플랫폼에서 `+ Add` / `Add Another` 버튼 뒤에 숨겨진 동적 모듈을 누락 없이 전수 발굴하고 지원자의 모든 경력, 어학, 웹사이트, 기술, 프로젝트를 100% 기입하도록 강제하는 시스템 프로토콜입니다.

---

## 1. 전수 탐색 게이트 (Add-Section Discovery Gate)

에이전트는 폼의 각 스텝에서 'Next', 'Save', 'Continue', 'Submit' 버튼을 누르기 전, 반드시 다음 탐색 게이트를 통과해야 한다:
1. **DOM 내 모든 추가 트리거 전수 검색**:
   - `button`, `a`, `div` 중 텍스트가 `Add`, `+ Add`, `Add Another`, `Add New`, `Add More`인 모든 엘리먼트와 그 상위 섹션 컨텍스트(H2~H4, legend, aria-label)를 추출한다.
2. **누락 불인정 원칙 (Zero Omission)**:
   - 지원자의 이력서(Resume) 또는 Ground Truth에 존재하는 데이터 항목이 해당 폼의 Add 섹션과 매칭될 경우, 필수가 아닌 '선택(Optional)' 사항이라 할지라도 **반드시 `Add`를 클릭하여 전수 입력**해야 한다.
   - 단 하나의 매칭 가능한 Add 섹션이라도 비워둔 채 단계를 통과하는 행위는 심각한 결함(Critical Defect)으로 규정한다.

---

## 2. 6대 모듈형 섹션별 입력 기준 (Exhaustive Mapping Baseline)

### 2.1 Work Experience (경력 사항)
- **트리거**: `Add` / `Add Another` (Work Experience)
- **입력 데이터**:
  - **Item 1 (Research Assistant Intern)**:
    - Title: `Research Assistant Intern`
    - Company: `University of Oklahoma`
    - Location: `London, United Kingdom` (or `Hybrid` / `Norman, OK`)
    - Dates: `2026-06` – `Present` (또는 `2026-08`)
    - Role Description: [Form Text Normalization Protocol](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/form-text-normalization.md)에 따라 정제된 불릿(`• `) 4개 항목:
      ```text
      • Engineered an LLM classification pipeline to evaluate 700+ papers against screening criteria, achieving high inter-rater reliability (κ = 0.98) while resolving complex edge cases through iterative QA refinement.
      • Automated the collection and deduplication of 600+ papers by linking journal APIs to Zotero via MCP, programmatically archiving citation metadata and full-text PDFs.
      • Operationalized a 2x3 psychometric study in Qualtrics (N=680), configuring TIRT blocks and latency telemetry to objectively quantify cognitive load across Likert and MFC formats.
      • Collaborated with PhD researchers to formulate a moderated-mediation model examining how situational strength buffers AI-induced Counterproductive Work Behaviors (CWBs).
      ```
  - **Item 2 (Server, 선택적)**: `WooJung Korean Restaurant` | `London, UK` | `2026-02` – `2026-06`.
  - **Item 3 (Military Service, 선택적)**: `Republic of Korea Army` (Sergeant / Culinary Specialist) | `2022-06` – `2023-12`.

### 2.2 Languages (어학 능력)
- **트리거**: `Add` / `Add Another` (Languages)
- **필수 등록 2종 (복수 등록 의무)**:
  - **Language 1 (English)**:
    - Native 체크박스: **반드시 체크** (Review 화면에서 "Fluent: Yes" 보장)
    - 모든 유창성(Comprehension, Overall, Reading, Speaking, Writing): `Fluent`, `Native`, 또는 `Superior`
  - **Language 2 (Korean)**:
    - `Add Another` 클릭 후 `Korean` 선택
    - Native 체크박스: **반드시 체크**
    - 모든 유창성: `Fluent`, `Native`, 또는 `Superior`

### 2.3 Websites & Portfolio (웹사이트 및 포트폴리오)
- **트리거**: `Add` / `Add Another` (Websites / Portfolio / Links)
- **입력 데이터**:
  - **GitHub URL**: `https://github.com/canadaofbin-netizen`
  - 카테고리/유형: `Portfolio`, `Personal Website` 또는 `Other`

### 2.4 Social Network URLs / SNS (소셜 링크)
- **트리거**: LinkedIn, GitHub, X 필드 또는 `Add SNS`
- **입력 데이터**:
  - **LinkedIn**: `https://www.linkedin.com/in/kyubin-yun-495a33301/`
  - **GitHub**: `https://github.com/canadaofbin-netizen`

### 2.5 Skills (보유 기술 및 도구)
- **트리거**: Skills 멀티선택 인풋 또는 `Add Skill`
- **입력 데이터**:
  - `Python`, `SQL`, `Machine Learning`, `Data Analysis`, `R`, `Tableau`, `Qualtrics`, `Research` 등 핵심 키워드 전수 태깅.

### 2.6 Projects / Honors & Awards / Certificates (프로젝트 및 수상/자격증)
- **트리거**: `Add Project`, `Add Honor/Award`, `Add Certificate`
- **입력 데이터**:
  - **Project**: `Personalized LLM Knowledge Graph (Obsidian)` (설명: 불릿 `• ` 정제 3개 항목).
  - **Certificate 1**: `Google Data Analytics Professional Certificate` (Coursera).
  - **Certificate 2**: `Python for Data Science and Machine Learning` (LinkedIn Learning).

---

## 3. 입력 후 사후 검증 (Post-Add Verification)

1. **카드 생성 검증**: `Add` 클릭 후 생성된 입력 폼에 값이 정상 주입되고, 카드(Card/Row) 형태로 저장되었는지 독립 검독(Read-After-Write)을 수행한다.
2. **에러 배제 확인**: 추가 항목 내에 빨간색 경고 메시지나 누락된 하위 필드(예: 직무 설명, 날짜 포맷 오류)가 0건인지 검증한 후에만 다음 단계로 진행한다.
