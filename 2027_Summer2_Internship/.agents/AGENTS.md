# Agent Directives for UCL Summer Intern / Job Hunt

This file defines the AI's behavior, constraints, and contextual knowledge for this workspace, based on the user's strategic goals and background.
- **Parent Workspace Directives**: [04_Internship AGENTS.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/AGENTS.md)

## 1. User Profile & Core Competencies
- **Education & Background**: 
  - UCL PALS (Psychology and Language Sciences) student.
  - Completed PALS0011 module (EEG, fMRI, fNIRS).
- **Core Technical Skills & Experience**:
  - **BCI & EEG Signal Processing**: Conducting a side project on left/right motor imagery classification. Goal is >95% accuracy on full channels, then testing lateral channels (T3, T4, F7, F8) to mimic smart glasses frames.
  - **Data Engineering & Web Scraping**: Built an AI-automated data pipeline to bypass bot-detection (CAPTCHAs, IP blocking) and bulk-download over 600 full-text academic papers for a Boundary Spanning Meta-Analysis (BSMA) project under an I/O Psychology professor.
  - **Machine Learning (ML) & Data Science**: Feature extraction, channel reduction, and statistical database construction.
  - **Wearable Sensors & Smart Glasses**: Strong vision for integrating non-invasive EEG sensors directly into glasses' frames without external peripherals.
- **Key Strengths**: Bridging the gap between raw biological/psychological phenomena and practical, automated computational pipelines (e.g., HCI, UX).

## 2. Strategic Job Targeting Rules
- **Undergraduate-Exclusive Filtering**: The user is currently an undergraduate student. Therefore, strictly filter and prioritize programs open to undergraduates (e.g., *Summer Internships, 12-month Industrial Placements, Student Researcher, or Undergraduate RA/Lab Shadowing*).
- **Target Roles**: Always prioritize job titles like **Data Science Intern**, **Data Analyst**, **UX Researcher (UXR) Intern**, **Machine Learning Intern**, or **Research Assistant**.
- **Roles to Avoid**: Do NOT target **Research Scientist** roles, as these typically require a completed PhD and extensive publication records, and will lead to automatic rejection.
- **Target Organizations**:
  - **Academic Labs**: Focus on groups combining computational modeling with neuroscience/psychiatry (e.g., UCL TCP Lab, UCL Centre for Consciousness Research, Imperial, Oxford).
  - **Tech Companies / Startups**: Focus on companies working on AR/VR, Neural Interfaces, Wearables, and on-device AI (e.g., Meta, Snap, Apple, Arm, DeepMind, Samsung AI Center).

## 3. Communication & Cold Email Strategy
- **Value Proposition**: Focus on *practical implementation* and *problem-solving*. Highlight how the user can build large-scale data pipelines, optimize noisy data, or integrate hardware/sensors to accelerate their research.
- **Portfolio First**: Ensure applications and emails are backed by tangible proof. Always remind the user to attach or prepare GitHub portfolios, Colab notebooks, or project links that demonstrate their pipelines and ML optimization skills.
- **Tone**: Professional, proactive, and highly focused on technical execution and problem-solving.

## 4. AI Assistant Guidelines (Behavioral Constraints)
- **Target Analysis**: When the user asks to analyze a new lab, company, or researcher, strictly use the dimensions outlined in `Research_Template.md` (Overview, Tech, Fit, Strategy, Timeline).
- **Mapping Skills**: Always explicitly map the target organization's technical needs or bottlenecks back to the user's specific skills (EEG pipelines, ML optimization, wearables).
- **Role Enforcement**: If the user asks for application advice, strictly enforce the rule to target Data Science/UXR/Engineering roles over Research Scientist roles.
- **Action-Oriented Prompts**: Continually prompt the user to prepare, polish, or link specific GitHub repositories or portfolios before they apply or send cold emails.

## 5. Research Verification Loop (Self-Correction)
- **Mandatory Verification**: Whenever tasked with researching a target (lab, company, or professor) or extracting contacts, the AI must implement an internal **Verification Loop**.
- **Verification Checklist**:
  1. **Reality Check**: Does this lab/company/professor actually exist and are they still active?
  2. **Contact Accuracy**: Are the emails and names formatted correctly and logically consistent?
  3. **Undergrad Fit**: Is the extracted role genuinely accessible to an undergraduate? (If it secretly requires a PhD, it must be flagged or discarded).
- **Loop Trigger**: If the AI detects any missing, contradictory, or potentially hallucinated information during the research phase, it MUST NOT output the result immediately. Instead, it must trigger a loop: run additional `search_web` tools or re-read documents until the information is definitively verified or explicitly marked as "Needs Manual Verification by User."

---

## 6. 2027 Summer Internship Application QA Verification & Ground Truth Baseline
- **Candidate**: Kyubin Yun (UCL BSc Psychology and Language Sciences, Class of 2028)
- **Strict Safety Rule**: **Zero Auto-Submit (최종 제출 버튼 자동 클릭 절대 금지)** — 모든 지원서는 반드시 Review / Pre-submit 단계까지만 작성하고 대기. 최종 Submit 버튼은 사용자가 직접 검토 후 수동으로 클릭합니다.

### 6.1 Candidate Ground Truth Baseline (검증 기준 데이터)

#### A. 인적사항 및 포털 계정 자격증명 (Credentials)
| 항목 | 기준 입력값 (Ground Truth) | 비고 및 주의사항 |
| :--- | :--- | :--- |
| **Legal Name** | Kyubin Yun (First Name: Kyubin / Last Name: Yun) | 여권 영문명 일치 |
| **Preferred Name** | *(None / Blank)* | 선호명 없음 (Jeff 등 입력 금지, 필드 반드시 공란 유지) |
| **Korean Name** | 윤규빈 | 국문 서류 매칭용 |
| **Portal ID / Email** | `zcjtyun@ucl.ac.uk` | UCL 공식 학적 이메일 (모든 포털 공통 계정 ID) |
| **Standard Password** | `Jeff0825!!` | 일반 지원 플랫폼 (Greenhouse, Lever, TikTok 등) |
| **Workday Password** | `Jeff0825!!!!` | Workday 전용 (12자 이상 특수문자 조건 필수 충족) |
| **Mobile Phone** | `+44 7787 442404` (Country Code: `+44`, Number: `7787442404`) | UK Mobile (Workday: Telephone/Mobile 구분) |
| **UK Address** | 40 Merchant St, Brent Cross, Suite 638, London, NW2 8BB | 영국 런던 현지 거주지 주소 |
| **Address Line 1** | 40 Merchant St, Brent Cross, Suite 638 | 번지 및 상세주소 |
| **City / Town** | London | 도시 |
| **Postal Code** | NW2 8BB | 영국 우편번호 |
| **Country** | United Kingdom | 영국 |

#### B. 학력 및 영국 취업 비자 자격 (Education & Visa Status)
| 항목 | 기준 입력값 (Ground Truth) | 비고 및 주의사항 |
| :--- | :--- | :--- |
| **University** | University College London (UCL) | Penultimate Year (재학 중) |
| **Degree & Major** | Bachelor of Science (BSc) in Psychology and Language Sciences | Workday 입력 시 BSc 코드 정밀 매칭 |
| **Study Period** | September 2025 – June 2028 | 2027 하계 인턴 Penultimate 자격 완벽 부합 |
| **Expected Graduation** | June 2028 | 2028년 6월 졸업 예정 |
| **Academic Grade** | Honours (Achieved/Predicted: 70.5/100) | 학위 등급 표기 |
| **UK Work Authorization** | Yes (UK Student Route Visa) | 방학 기간 중 주 40시간 Full-time 근무 법적 보장 |
| **Visa Sponsorship** | Yes (스폰서십 필요) | 정규직/졸업 후 전환 시 Skilled Worker 스폰서십 필요 |
| **Sponsorship Explanation** | "I am an undergraduate student at University College London (UCL) holding a valid UK Student Route visa, legally permitting full-time employment during university vacations for this internship without sponsorship. Upon graduation in June 2028, I am eligible for the 2-year unsponsored Graduate Route visa, granting full working rights with zero employer sponsorship required. I would only require Skilled Worker visa sponsorship thereafter for subsequent long-term permanent employment." | 비자 서술형 표준 문안 (Graduate Route 2년 무스폰서십 혜택 명시) |

#### C. 프로필 링크 및 제출 서류 (Links & Documents)
| 항목 | 기준 입력값 (Ground Truth) | 비고 및 주의사항 |
| :--- | :--- | :--- |
| **Resume PDF** | `g:\My Drive\Kyubin_Yun_Workspace\04_Internship\01_Resumes\Kyubin_Yun_Resume_2027.pdf` | 최신 2027 버전 이력서 파일 경로 |
| **LinkedIn** | `https://www.linkedin.com/in/kyubin-yun-495a33301/` | 링크드인 프로필 |
| **GitHub** | `https://github.com/canadaofbin-netizen` | **최신 깃허브 URL** (구 링크 사용 금지) |

### 6.2 핵심 플랫폼별 기입 지침 및 오류 방지 규칙 (Critical Rules & Fix Log)
1. **Workday 계정 생성 시 비밀번호 길이 규칙:**
   - 일반 포털 비밀번호(`Jeff0825!!`, 10자리) 사용 시 Workday는 최소 12자 이상 요건으로 인해 계정 생성이 거절됩니다.
   - 반드시 `Jeff0825!!!!` (12자리)를 사용하여 계정을 생성/로그인해야 합니다.
2. **Workday 어학(Languages) 유창성 표시 메커니즘:**
   - Workday 입력 폼에서 영어를 Fluent로 선택하더라도, "Native" 체크박스를 체크하지 않으면 Review 화면에서 "I am fluent in this language: No"로 오표기됩니다.
   - 따라서 영어를 입력할 때도 반드시 Native 체크박스를 체크해야 최종 Review 화면에서 **"I am fluent in this language: Yes"**로 정상 검증됩니다.
   - 한국어(Korean)와 영어(English) 모두 등록하여 Reading, Speaking, Writing 전부 Fluent/Native로 기입합니다.
3. **영국 HESA 인종(Ethnicity) 분류 선택 규칙:**
   - Workday 검색창에 "Asian"을 검색할 경우 알파벳 순으로 첫 번째 항목인 `Asian / Asian British - Chinese (United Kingdom)`가 기본 선택될 수 있습니다.
   - 한국 국적 지원자는 반드시 `Asian / Asian British - Any other Asian background (United Kingdom)` 항목을 명시적으로 검색하여 선택해야 하며, Chinese 항목은 삭제(Delete charm)해야 합니다.
4. **학위(Degree) 매칭 규칙:**
   - Workday 학위 선택 시 일반 Bachelor's가 아닌 세부 코드 `BSc (Bachelor of Science)`를 선택해야 전공명(`Psychology and Language Sciences`)과 충돌 없이 정상 통과됩니다.
5. **국가 전화 코드 확인:**
   - 폼 기본값(미국 `+1` 등)을 방치하지 말고, 지원자의 영국 휴대전화 국가코드인 **`+44` (United Kingdom)**를 정확히 선택합니다.
6. **지원서 텍스트 정제 의무 (Text Normalization):**
   - PDF 자동 파싱이나 복사 시 유입되는 아티팩트(`⚫`, `●`, `⬤`, mid-sentence `\n`, trailing hyphens)를 원천 차단하기 위해 [Rule: Form Field Text Normalization Protocol](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/form-text-normalization.md)을 준수하여 정제 텍스트만 주입합니다.
7. **최종 제출 절대 금지 (Zero Auto-Submit):**
   - 모든 지원 프로세스는 마지막 Review / Pre-submit 단계에서 멈추어야 하며, 최종 Submit 버튼은 사용자가 직접 검토 후 수동으로 클릭합니다.

### 6.3 Automated Application Protocol & Slash Commands (/browser, /goal, /boost)
지원서 작성 및 포털 정보 입력은 AI 에이전트가 `/browser`, `/goal`, `/boost` 세 가지 핵심 기능을 결합하여 전담 대행합니다:
1. **/browser (가시 브라우징 및 폼 입력 대행)**:
   - 채용 포털 접속, 계정 로그인/생성, 이력서 업로드 및 인적사항·학력·비자·문항 답변 입력을 수행.
   - **실시간 화면 가시성 원칙 (Visible First)**:
     - 백그라운드 가상 크롬(`headless=True`, `Temp` 프로필)으로 숨어서 작업하는 행위를 엄격히 금지.
     - 사용자가 실시간으로 입력 과정을 육안으로 볼 수 있도록, **사용자가 실행 중인 네이버 웨일 브라우저(CDP 포트 9222)에 직접 연결하여 제어**하거나, **화면 전면에 독립된 브라우저 창(`headless=False`)을 띄워 작업**.
   - **지원서 텍스트 정제 의무**: `normalize_text()`를 거쳐 불릿(`• `), 줄바꿈, 띄어쓰기가 완벽히 정제된 텍스트만 주입.
   - **Zero Auto-Submit 준수**: 최종 'Review / Pre-submit' 화면까지만 진행하고 작업을 멈춘 뒤 사용자 검토 대기.
2. **/goal (자율 완결형 엔드투엔드 파이프라인)**:
   - 다단계 지원서 입력 및 리서치 전 과정을 중단 없이 최종 목표(Review 화면 도달)까지 철저하게 완수.
   - 폼 입력 검증 실패나 세션 오류 발생 시 스스로 원인을 찾아 교정.
3. **/boost (심층 문항 분석 및 사전 아키텍처/갭 분석 Gate)**:
   - 지원 동기(Motivation), 에세이, 기술 질문 등 서술형 문항 작성 시 심층 전략 추론을 발동.
   - 지원자의 연구/기술 역량(UCL BSc, EEG/BCI 파이프라인, Data Science/UXR)과 직무 요구 역량을 정확히 매칭하고 일관성 및 무환각 교차 검증 수행.
   - 복합 작업 및 시스템 구축 착수 전 [Rule: Context-Driven Architectural Blueprint & Gap Analysis](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/context-driven-architecture-gap-analysis.md)에 따라 목적 분해 → 아키텍처 설계 → 5대 영역 갭 분석(Pre-Flight Architecture Gate)을 통과한 후 실행.
4. **브라우저 세션 안전성 유지**:
   - 단일 가시 브라우저(Whale CDP 9222) 제어 시 포트 충돌이나 불필요한 백그라운드 프로세스가 발생하지 않도록 탭 단위로 안정적으로 조작하고 세션을 관리합니다.

---

## 7. 컨텍스트 기반 아키텍처 설계 및 갭 분석 프로토콜 (Context-Driven Architectural Blueprint & Gap Analysis)

### 7.1 목적 및 작동 원칙 (Pre-Flight Architecture Gate)
에이전트는 사용자의 요청을 접수했을 때 즉시 코드를 작성하거나 툴(브라우저 제어, CLI, 파일 편집 등)을 실행하지 않는다. 작업의 근본적인 목적을 분해하고, 그 목적을 달성하기 위한 최적의 시스템 아키텍처를 정의하며, 누락된 필수 요건이 없는지 사전에 전수 점검하는 **"Pre-Flight Architecture Gate"**를 반드시 통과해야 한다.

### 7.2 3단계 사전 분석 및 설계 파이프라인
1. **Phase 1: Intent & Outcome Deconstruction (목적 및 완료 조건 정의)**
   - **Core Objective**: 이 작업의 최종 비즈니스/운영 목적은 무엇인가? (단순 행위가 아닌 '달성하고자 하는 결과 상태')
   - **Definition of Done (DoD)**: 어떤 조건이 충족되어야 이 작업이 100% 성공했다고 객관적으로 판단할 수 있는가?
   - **Hard Constraints**: 건드려서는 안 되는 영역, 허용되지 않는 부작용, 보장해야 할 자원/시간/규격 한계는 무엇인가? (SSOT 불변, Zero Auto-Submit, Visible Whale Browser 준수)

2. **Phase 2: Tailored System Architecture Design (맞춤형 시스템 설계)**
   - **Data Flow**: 입력 데이터 → 가공/변환(불릿 표준화 `• ` 등) → 중간 검증 → 최종 출력/반영 단계 정의.
   - **State & Error Management**: 중단 발생 시 복구 전략(Idempotency, 롤백, 캐싱, Failure Cache) 설계.
   - **Interface/Tool Mapping**: 어떤 도구(Playwright CDP, CLI, 스크립트 등)를 어느 순서와 의존성으로 연결할지 구조화.

3. **Phase 3: Exhaustive Gap Analysis (필수/누락 요소 전수 점검)**
   설계된 아키텍처를 실행하기 전, 다음 5개 영역에서 누락된 것이 없는지 자가 감사(Self-Audit)를 수행한다:

| 점검 영역 (Dimension) | 핵심 검증 질문 (Audit Question) | 누락 시 조치 (Defensive Action) |
| :--- | :--- | :--- |
| **Dependencies & Prerequisites** | 런타임 환경, 라이브러리, 인증 토큰, 접근 권한, 파일 경로 등이 사전에 준비되었는가? | 작업 전 사전 설치/검증 스크립트 선행 |
| **Input Completeness** | 사용자가 제공한 원본 데이터에 빈 값, 비정형 포맷, 모호한 명칭이 없는가? | 기본값(Fallback) 규칙 정의 또는 사용자 확인 |
| **Edge Cases & Failure Modes** | 네트워크 지연, UI 요소 미로딩, 데이터 중복, 예외 규격 인입 시 어떻게 처리할 것인가? | 재시도(Retry) 및 예외 분기 로직 삽입 |
| **Verification Loop** | 작업이 의도대로 끝났음을 사후 검증할 메커니즘(Diff 검사, 상태 체크)이 포함되었는가? | 독립 검증 절차(Read-After-Write) 필수 편입 |
| **Side Effects & Reversibility** | 기존 시스템 상태, DB 레코드, 로컬 파일을 비가역적으로 훼손할 위험이 없는가? | 백업 생성 또는 안전 모드 드라이런(Dry-run) 실행 |

### 7.3 Execution Gate (실행 전환 기준)
- **Gap Score = 0 (결함 없음)**: 위 5개 영역의 누락 요소가 모두 식별되고 방어 로직이 아키텍처에 포함된 경우에만 실행(Execution) 단계로 진입한다.
- **Ambiguity Detected (모호성/누락 발견)**:
  - 시스템 구축에 치명적인 정보가 누락되었다면, 임의로 추측하여 실행하지 말고 **부족한 정보와 위험 요소를 정리하여 즉시 질문**한다.
  - 경미하거나 합리적 기본값 적용이 가능한 경우, **"적용한 가정(Assumptions)"을 명시**하고 시스템 내에 방어 장치를 둔 상태로 진행한다.

### 7.4 보고 및 출력 규격 (Pre-Flight Review Output Format)
복잡한 작업 수행 전, 사용자에게 다음 구조로 아키텍처 점검 결과를 요약 보고한 뒤 실행한다:
```text
[Architecture & Pre-Flight Review]

작업 목적 및 DoD: <정의>

제안 시스템 구조: <파이프라인 요약>

식별된 잠재 누락/위험 요소:
- <위험/누락 1> -> [대응 방안: ...]
- <위험/누락 2> -> [대응 방안: ...]

실행 여부: [Ready / Awaiting Clarification]
```

### 7.5 슬래시 커맨드 연계 (/boost 발동 지침)
사용자가 `/boost` 명령이나 복합 엔지니어링을 지시할 때 본 프로토콜이 자동 발동되며, 단독 주입 시 [Rule: Meta-Prompt Architecture & Gap Analysis](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/meta-prompt-architecture-gap-analysis.md) 지시문을 활용합니다.

---

## Agent Customizations Index

### Rules (`.agents/rules/`)
- [Rule: Candidate Ground Truth Baseline](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/candidate-ground-truth.md) - 지원자 Ground Truth 데이터 및 5대 플랫폼 오류 방지 가이드.
- [Rule: Ground-Truth Integrity & Auto-Correction Engine](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/ground-truth-integrity.md) - SSOT 4단계 입력-독립검독-불일치교정 루프 및 제출 차단선 규칙.
- [Rule: Meta-Prompt Ground-Truth Audit](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/meta-prompt-ground-truth-audit.md) - /boost 및 폼 자동화 시 에이전트 자체 교정 강제 주입용 메타 프롬프트.
- [Rule: Context-Driven Architectural Blueprint & Gap Analysis](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/context-driven-architecture-gap-analysis.md) - 작업 착수 전 목적 분석, 맞춤형 아키텍처 설계 및 5대 핵심 영역 갭 분석(Gap Analysis) 프로토콜.
- [Rule: Meta-Prompt Architecture & Gap Analysis](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/meta-prompt-architecture-gap-analysis.md) - /boost 및 복합 작업 시작 전 아키텍처 설계 및 결함 점검 강제 주입용 메타 프롬프트.
- [Rule: Form Field Text Normalization Protocol](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/form-text-normalization.md) - 지원서 텍스트 정제, PDF 불릿 치환 및 문장 중간 임의 줄바꿈 제거 표준.
- [Rule: Visible Browser Protocol](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/visible-browser-protocol.md) - 화면 가시 브라우저(네이버 웨일) 의무 규칙.
- [Rule: Zero Auto-Submit](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/zero-auto-submit.md) - 최종 제출 버튼 자동 클릭 금지 원칙.
- [Rule: Excel Tracker Architecture](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/2027_Summer2_Internship/.agents/rules/excel-tracker-architecture.md) - Master Internship Tracker (`2027_BCI_Internship_Tracker.xlsx`) 아키텍처 및 안티 환각 규칙.
- [Rule: Workspace Linting](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/2027_Summer2_Internship/.agents/rules/workspace-linting.md) - Cookiecutter Data Science 디렉터리 구조 및 Python 코드 린팅 규칙.

### Skills (`.agents/skills/`)
- [Skill: Visible Application Automation](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/skills/apply/SKILL.md) - 네이버 웨일 브라우저 지원서 작성 및 자동 텍스트 정제 스킬 (`/apply`).
- [Skill: Workspace Linter](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/2027_Summer2_Internship/.agents/skills/lint/SKILL.md) - 디렉터리 구조 검증 및 코드 자동 린팅 (`/lint`).
- [Skill: BCI Zero-Hallucination Researcher](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/2027_Summer2_Internship/.agents/skills/research/SKILL.md) - 글로벌 BCI 테크 기업 리서치 및 엑셀 트래커 주입 파이프라인 (`/research`).
