---
name: apply
description: "Assists the candidate in opening, filling, and reviewing 2027 internship application forms in a visible browser (Naver Whale or foreground browser) up to the final Review stage, with automated text normalization."
---

# Apply Skill (지원서 가시 작성 및 검토 스킬)

- **Workspace Directives**: [AGENTS.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/AGENTS.md)

이 스킬은 채용 포털(Greenhouse, Workday, Lever, TikTok, Taleo, 기업 자체 사이트)의 지원서 작성 전 과정을 **사용자 눈에 보이는 브라우저(네이버 웨일 또는 화면 전면 창)**를 활용하여 자동화하고 사전 검증을 완결하는 전담 스킬입니다.

---

## 1. 가시 브라우저 실행 원칙 (Visible First)

- **절대 금지:** 백그라운드 가상 크롬(`headless=True`, `AppData\Local\Temp` 임시 프로필)으로 숨어서 작업하는 행위.
- **실행 방법:**
  1. 지원 링크를 열 때 번들된 헬퍼 스크립트를 사용하여 사용자의 네이버 웨일 창에 탭을 직접 띄웁니다:
     ```bash
     python .agents/skills/apply/scripts/open_visible_browser.py --company scale_ai --browser whale
     # 또는 전체 탭 일괄 열기:
     python .agents/skills/apply/scripts/open_visible_browser.py --company all --browser whale
     ```
  2. 사용자가 실행 중인 네이버 웨일 브라우저(`http://localhost:9222`)에 CDP로 직접 연결하여 사용자가 보는 화면에서 실시간으로 탭을 조작하거나 검증합니다.
  3. 새 창으로 Playwright를 실행할 경우에도 반드시 `headless=False`를 명시하여 사용자의 화면 전면에 새 창이 뜨도록 합니다.

---

## 2. 필수 검증 기준 데이터 (Ground Truth)

모든 폼 입력 시 `.agents/rules/candidate-ground-truth.md`의 데이터를 100% 엄격 적용합니다:
- **Candidate**: Kyubin Yun (Korean: 윤규빈)
- **Email / ID**: `zcjtyun@ucl.ac.uk` (모든 포털 공통 ID)
- **일반 PW**: `Jeff0825!!` (Greenhouse, Lever, TikTok 등)
- **Workday PW**: `Jeff0825!!!!` (12자 이상 특수문자 필수 충족)
- **영국 주소**: `40 Merchant St, Brent Cross, Suite 638, London, NW2 8BB`
- **전화번호**: `+44 7787 442404` (국가코드: `+44`, 번호: `7787442404`)
- **학력**: UCL BSc Psychology and Language Sciences (September 2025 – June 2028, Penultimate Year, Honours)
- **비자 자격**: Student Route Visa (방학 중 주 40시간 Full-time 근무 법적 보장, 2028년 6월 졸업 후 2년 무스폰서십 Graduate Route 비자 취득 예정, 이후 장기 전환 시에만 Skilled Worker 필요)
- **이력서 PDF**: `g:\My Drive\Kyubin_Yun_Workspace\04_Internship\01_Resumes\Kyubin_Yun_Resume_2027.pdf`
- **LinkedIn**: `https://www.linkedin.com/in/kyubin-yun-495a33301/`
- **GitHub**: `https://github.com/canadaofbin-netizen`

---

## 3. 지원서 텍스트 정제 의무 (Text Normalization Protocol)

PDF 자동 파싱이나 텍스트 붙여넣기 시 발생하는 원시 불릿(`⚫`, `●`), 공백 누락(`⚫Engineered`), 문장 중간 임의 줄바꿈(`high\ninter-rater`)을 원천 방지하기 위해 **모든 Description 텍스트는 주입 전 정제 모듈을 반드시 통과**해야 합니다:
- **전용 정제 모듈**: `.agents/skills/apply/scripts/text_normalizer.py`
  ```python
  from text_normalizer import normalize_text

  clean_desc = normalize_text(raw_extracted_text)
  ```
- **정제 규격**:
  1. 원시 불릿 기호는 표준 불릿 `• ` (`\u2022` + 공백)으로 통일.
  2. 문장 도중의 불필요한 줄바꿈은 단일 공백으로 치환하여 매끄럽게 연결.
  3. 불릿 간의 구분과 의미 있는 문단 구분만 개행(`\n`) 유지.
  4. React/Vue 등 프레임워크 상태 동기화를 위해 프로토타입 세터와 `input`/`change`/`blur` 이벤트 디스패치 수행.

---

## 4. 포털별 핵심 오류 방지 가이드

- **Workday 비밀번호**: 반드시 `Jeff0825!!!!` (12자리) 사용.
- **Workday 언어 유창성**: 영어를 Fluent로 선택하더라도 반드시 "Native" 체크박스를 체크해야 최종 Review 화면에서 "I am fluent in this language: Yes"로 정상 판정.
- **영국 HESA 인종 분류**: 한국 국적은 기본값 Chinese가 아닌 `Asian / Asian British - Any other Asian background (United Kingdom)`를 명시적 검색/선택하고 Chinese 항목은 삭제.
- **학위 명칭**: 일반 Bachelor's가 아닌 세부 코드 `BSc` (Bachelor of Science) 선택.
- **국가 전화 코드**: 기본값(+1 등)이 아닌 영국 `+44` (United Kingdom) 선택 여부 철저 확인.

---

## 5. 최종 안전 가드레일 (Zero Auto-Submit)

- 어떠한 경우에도 최종 `Submit` 버튼을 자동으로 클릭하지 않습니다.
- 모든 입력, 텍스트 정제, 서류 첨부를 마친 뒤 최종 `Review / Pre-submit` 화면에서 정지하고, 사용자에게 직접 제출하도록 인계합니다.

---

## 6. 입력 검증 및 자체 교정 엔진 (Ground-Truth Integrity & Reconciliation Engine)

폼 필드 입력 및 Computer Use 도중 발생하는 자동완성 왜곡, 플레이스홀더 덮어쓰기 누락, 드롭다운 오선택을 사후 수동 지적 없이 시스템 차원에서 자동 감지·수정합니다:
- **전용 엔진 모듈**: `.agents/skills/apply/scripts/reconciliation_engine.py`
  ```bash
  python .agents/skills/apply/scripts/test_reconciliation_engine.py
  ```
- **4단계 실행 루프**:
  1. `Payload Parsing`: SSOT 기준 데이터 추출 및 정규화.
  2. `Action Execution`: 필드 포커스 및 입력 실행.
  3. `Read-After-Write Inspection`: 화면의 실제 렌더링 값 독립 추출 (`.select__single-value`, `value`, DOM 프로퍼티).
  4. `Strict Diff Reconciliation`: Diff > 0 감지 시 즉시 중단, 원인 분석, 필드 초기화 후 최대 3회 재시도.
- **Submission Gate**: 100% MATCH 확인 전 'Next'/'Submit' 클릭 전면 차단 및 `[Verification Audit]` 테이블 출력.
- **Failure Cache**: 세션 내 발생 결함 패턴을 캐싱하여 후속 필드 입력 시 선제적 방어 로직 적용.

---

## 7. 사전 아키텍처 설계 및 갭 분석 게이트 (Pre-Flight Architecture Gate)

지원서 작성 자동화, 브라우저 제어 세션 개시, 또는 복합 지원 파이프라인 가동 전 [Rule: Context-Driven Architectural Blueprint & Gap Analysis](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/context-driven-architecture-gap-analysis.md)에 따라 5대 갭 점검을 선행합니다:
1. **Dependencies & Prerequisites**: Whale 브라우저 CDP 포트(9222) 활성화 상태, 필요한 Python 라이브러리 확인.
2. **Input Completeness**: 타깃 채용 공고 URL 유효성, `text_normalizer.py` 사전 정제 파이프라인 통과 여부.
3. **Edge Cases & Failure Modes**: React/Vue SPA 상태 롤백, 드롭다운 지연 로딩, 활성 컨테이너 타겟팅 방어책.
4. **Verification Loop**: Read-After-Write 독립 검독 및 `reconciliation_engine.py` 결합 준비.
5. **Side Effects & Reversibility**: 엑셀 트래커 백업(`2027_BCI_Internship_Tracker.xlsx`), Zero Auto-Submit 차단선 확보.
- **전용 게이트 모듈**: [.agents/skills/apply/scripts/architecture_gate.py](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/skills/apply/scripts/architecture_gate.py)
  ```bash
  # 5대 갭 분석 및 [Architecture & Pre-Flight Review] 실행
  python .agents/skills/apply/scripts/architecture_gate.py --company scale_ai
  # 갭 점검 통과(Gap Score = 0) 시 가시 브라우저 자동 연계 론칭
  python .agents/skills/apply/scripts/architecture_gate.py --company scale_ai --launch
  ```
- **보고 의무**: 폼 자동화 착수 전 `[Architecture & Pre-Flight Review]` 요약을 출력하고 준비 상태를 확인합니다.
