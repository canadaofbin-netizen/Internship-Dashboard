---
description: "Context-Driven Architectural Blueprint & Gap Analysis Protocol (Pre-Flight Architecture Gate)"
globs: ["**/*"]
alwaysApply: true
---

# Context-Driven Architectural Blueprint & Gap Analysis Protocol

- **Workspace Directives**: [AGENTS.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/AGENTS.md)

이 문서는 `04_Internship` 워크스페이스 내 모든 작업(시스템 구축, 스크립트 작성, 지원서 폼 자동화, 리서치 파이프라인, 문서 작성 등)에 착수하기 전, 즉각적인 실행을 지양하고 **작업 목적 분석 → 맞춤형 아키텍처/시스템 설계 → 필수/누락 요소 점검(Gap Analysis)**을 시스템 차원에서 강제하는 **"Pre-Flight Architecture Gate"** 프로토콜입니다.

---

## 1. 목적 및 핵심 원칙 (Core Objectives & Operating Principles)

1. **지연 실행 원칙 (No Immediate Blind Action)**:
   - 에이전트는 사용자의 요청을 접수했을 때 즉시 코드를 작성하거나 툴(Computer Use, CLI, 파일 편집 등)을 실행하지 않는다.
   - 요청의 표면적 지시어 이면에 내재된 근본적인 목적을 분해하고, 그 목적을 달성하기 위한 최적의 시스템 아키텍처를 사전에 정의해야 한다.

2. **사전 비행 점검 강제 (Pre-Flight Architecture Gate)**:
   - 모든 작업은 반드시 3단계 사전 분석 및 설계 파이프라인(목적 정의 → 아키텍처 설계 → 갭 분석)을 거쳐야 한다.
   - 갭 분석 결과 식별된 결함이나 모호성이 완전히 해소되기 전까지 실행 단계로의 전환을 엄격히 차단한다.

3. **시스템 멱등성 및 안전성 (System Idempotency & Safety)**:
   - 아키텍처 설계 시 중단 후 재시작, 롤백, 캐싱 및 기존 Ground Truth 데이터(SSOT)의 훼손 방지를 최우선 설계 원칙으로 삼는다.

---

## 2. 3단계 사전 분석 및 설계 파이프라인 (3-Phase Pipeline)

### Phase 1: Intent & Outcome Deconstruction (목적 및 완료 조건 정의)
작업에 착수하기 전, 다음 3가지 핵심 질문에 대한 답을 내부적으로 명확히 규정한다:
1. **Core Objective (핵심 목적)**:
   - 이 작업의 최종 비즈니스/운영 목적은 무엇인가?
   - 단순한 행위(예: "파일 생성", "버튼 클릭")가 아닌 **'달성하고자 하는 최종 결과 상태'**를 명확히 정의한다.
2. **Definition of Done (DoD / 성공 판정 기준)**:
   - 어떤 조건이 충족되어야 이 작업이 100% 성공했다고 객관적으로 판단할 수 있는가?
   - 수치화 가능한 검증 기준(예: Diff = 0, 테스트 통과율 100%, 렌더링 확인 완료)을 수립한다.
3. **Hard Constraints (절대 제약 조건)**:
   - 건드려서는 안 되는 영역, 허용되지 않는 부작용, 보장해야 할 자원/시간/규격 한계는 무엇인가?
   - 예: [Candidate Ground Truth Baseline](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/candidate-ground-truth.md) 불변 준수, [Zero Auto-Submit](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/zero-auto-submit.md) 준수, [Visible Browser Protocol](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/visible-browser-protocol.md) 준수 등.

---

### Phase 2: Tailored System Architecture Design (맞춤형 시스템 설계)
목적에 맞춰 필요한 파이프라인과 아키텍처를 유기적으로 구성한다:
- **Data Flow (데이터 흐름)**:
  - 입력 데이터(SSOT, 사용자 프롬프트, 외부 소스) → 정형화 및 가공([Form Field Text Normalization](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/form-text-normalization.md)) → 중간 상태 검증 → 최종 출력/반영 단계 정의.
- **State & Error Management (상태 및 에러 제어)**:
  - 예기치 않은 중단 발생 시 복구 전략(Idempotency, 롤백, 캐싱, Failure Cache) 설계.
  - 비가역적 파괴 작업(파일 덮어쓰기, DB 수정) 전 백업 메커니즘 수립.
- **Interface & Tool Mapping (도구 및 인터페이스 맵핑)**:
  - 어떤 도구(Playwright CDP, CLI, Python 스크립트, Regex 등)를 어느 순서와 의존성으로 결합할지 명세화.

---

### Phase 3: Exhaustive Gap Analysis (필수/누락 요소 전수 점검)
설계된 아키텍처를 실행하기 전, 다음 5개 핵심 영역에서 결함이나 누락 요소가 없는지 자가 감사(Self-Audit)를 수행한다.

| 점검 영역 (Dimension) | 핵심 검증 질문 (Audit Questions) | 누락/결함 시 방어 조치 (Defensive Action) |
| :--- | :--- | :--- |
| **1. Dependencies & Prerequisites** | 런타임 환경, 필수 라이브러리, 인증 토큰, 접근 권한, 브라우저 가시성 상태, 파일 경로가 유효한가? | 작업 전 사전 설치/검증 스크립트 실행, 가시 브라우저 활성화 |
| **2. Input Completeness** | 입력 데이터에 빈 값, 비정형 포맷, 모호한 명칭, PDF 파싱 아티팩트가 없는가? | 정제 모듈(`normalize_text`) 선행, Fallback 기본값 설정 또는 사용자 명확화 질문 |
| **3. Edge Cases & Failure Modes** | 네트워크 지연, SPA DOM 상태 롤백, UI 요소 미로딩, 데이터 중복 인입 시 어떻게 대응할 것인가? | 재시도(최대 3회), 명시적 대기(`waitForSelector`), 이벤트 디스패치(`input/change/blur`) |
| **4. Verification Loop** | 작업이 의도대로 끝났음을 사후 검증할 독립적 수단(Diff 검사, Read-After-Write, 테스트)이 있는가? | 독립 검독 단계(Read-After-Write Inspection) 및 Diff 대조 의무화 |
| **5. Side Effects & Reversibility** | 기존 시스템 상태, 다른 설정 파일, DB 레코드, Git 히스토리를 비가역적으로 훼손할 위험이 없는가? | 백업 생성, 드라이런(Dry-run) 실행, 격리된 임시 영역 검증 후 이동 |

---

## 3. Execution Gate (실행 전환 기준)

1. **Gap Score = 0 (결함 없음)**:
   - 위 5개 영역의 누락 요소가 모두 식별되고, 대응 방어 로직이 아키텍처에 포함된 경우에만 실행(Execution) 단계로 진입한다.
2. **Ambiguity Detected (모호성/누락 발견)**:
   - **치명적 결핍 (Critical Gap)**: 시스템 구축이나 작업 완수에 치명적인 정보가 누락된 경우, 임의로 추측하거나 가정을 세워 실행하지 말고 **부족한 정보와 위험 요소를 명확히 정리하여 사용자에게 질문**한다.
   - **경미한 결핍 (Minor Gap)**: 합리적 기본값(Fallback) 적용이 가능한 경우, **"적용한 가정(Assumptions)"을 명시**하고 시스템 내에 방어 장치를 둔 상태로 진행한다.

---

## 4. 보고 및 출력 규격 (Pre-Flight Review Output Format)

복잡한 작업, 시스템 구축, 또는 `/boost` 발동 시 에이전트는 계획 수립 단계에서 다음 구조로 아키텍처 점검 결과를 요약 보고한다:

```text
[Architecture & Pre-Flight Review]

작업 목적 및 DoD: <달성 목표 상태 및 객관적 완료 판정 기준>

제안 시스템 구조: <파이프라인 단계 및 데이터 흐름 요약>

식별된 잠재 누락/위험 요소:
- <위험/누락 1> -> [대응 방안: ...]
- <위험/누락 2> -> [대응 방안: ...]

실행 여부: [Ready / Awaiting Clarification]
```

---

## 5. 타 시스템 프로토콜과의 상호 연계 (Interlinked Architecture)

- **데이터 진실성**: 모든 아키텍처 입력 데이터는 [Rule: Candidate Ground Truth Baseline](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/candidate-ground-truth.md)을 준수.
- **입력 검독 및 교정**: 폼 입력 파이프라인 설계 시 [Rule: Ground-Truth Integrity & Auto-Correction Engine](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/ground-truth-integrity.md)의 4단계 루프 편입.
- **텍스트 정제**: 텍스트 가공 단계는 [Rule: Form Field Text Normalization Protocol](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/form-text-normalization.md) 필수 연계.
- **가시 브라우징**: 브라우저 기반 도구 매핑 시 [Rule: Visible Browser Protocol](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/visible-browser-protocol.md) 준수.
- **최종 안전선**: 실행 파이프라인의 최종 단계는 [Rule: Zero Auto-Submit](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/zero-auto-submit.md)에 따라 수동 검토 대기 인계.
- **메타 프롬프트 템플릿**: 단독 주입 및 `/boost` 실행 시 [Rule: Meta-Prompt Architecture & Gap Analysis](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/meta-prompt-architecture-gap-analysis.md) 적용.

---

## 6. 실행 스크립트 및 테스트 모듈 (Execution Scripts & Unit Tests)

- **게이트 코어 엔진**: [.agents/skills/apply/scripts/architecture_gate.py](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/skills/apply/scripts/architecture_gate.py)
- **단위 테스트**: [.agents/skills/apply/scripts/test_architecture_gate.py](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/skills/apply/scripts/test_architecture_gate.py)
