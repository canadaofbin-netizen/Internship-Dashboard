---
description: "Ground-Truth Integrity & Auto-Correction Engine (Read-After-Write & Strict Diff Reconciliation Protocol)"
globs: ["**/*"]
alwaysApply: true
---

# Ground-Truth Integrity & Auto-Correction Engine Protocol

- **Workspace Directives**: [AGENTS.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/AGENTS.md)

이 규칙은 `04_Internship` 및 모든 지원서 입력 자동화, Computer Use 작업 시 단일 진실 공급원(SSOT)과 화면 렌더링 상태의 100% 일치를 보장하고 불일치 결함(Defect)을 자체 감지·교정하기 위한 시스템 프로토콜입니다.

---

## 1. 단일 진실 공급원(SSOT) 원칙

1. **불변의 기준점**: 사용자가 제공한 원본 데이터(텍스트, 파일, 지시사항 및 [Candidate Ground Truth Baseline](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/candidate-ground-truth.md))는 불변의 **Ground Truth (SSOT)**로 취급한다.
2. **결함(Defect)의 정의**: Computer Use 또는 자동화 도중 발생하는 자동완성 왜곡, UI 렌더링 지연, 단축키 오작동, 플레이스홀더 덮어쓰기 누락, 드롭다운 인덱스 오선택 등으로 인해 SSOT와 실제 화면 상태가 1글자라도 달라지는 모든 상황을 엄격한 결함(Defect)으로 규정한다.

---

## 2. 4단계 입력-검증 실행 파이프라인 (Mandatory Loop)

에이전트는 모든 폼 필드 입력 및 상태 변경 작업 시 반드시 다음 4단계를 순차적으로 강제 실행해야 한다:

### Step 1: Payload Parsing (입력 전 정형화)
- 사용자의 원본 요청 및 SSOT에서 대상 필드명과 기댓값(Expected Value)을 추출하여 내부 매핑 테이블(Key-Value)을 생성한다.
- 날짜 형식, 공백 포함 여부, 대소문자, [Form Text Normalization Protocol](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/form-text-normalization.md)에 따른 불릿 표준화(`• `)를 사전에 확정한다.

### Step 2: Action Execution (입력 실행)
- 대상 필드에 포커스하고 데이터를 입력한다.
- **절대 주의**: 단순 "입력 명령 전송 완료" 또는 "타이핑 성공" 로그를 작업 완료로 간주하지 않는다.
- 입력 전 `Failure Cache`에 등록된 사전 방어 로직(예: Select All -> Backspace)을 선제적으로 적용한다.

### Step 3: Read-After-Write Inspection (사후 독립 검독)
- 입력 완료 직후, UI 화면의 실제 상태를 독립적으로 다시 읽어 들인다 (DOM 프로퍼티 추출, `value`/`innerText`, `.select__single-value` 판독, 또는 클립보드 복사 검사).
- **인과 분리 원칙**: 자신이 입력하려고 의도했던 메모리나 직전 페이로드를 참조하지 않고, **현재 화면에 렌더링되어 있는 실제 상태**만을 객관적 인입 데이터로 삼는다.

### Step 4: Strict Diff Reconciliation (불일치 대조 및 교정)
- `Ground Truth (Step 1)` vs `Screen State (Step 3)`의 Diff를 엄격히 계산한다.
- **Diff = 0 (완전 일치)**: 다음 입력 필드로 진행.
- **Diff > 0 (불일치 발생)**:
  1. 즉시 후속 진행(Next, Save, Submit 클릭)을 전면 중단한다.
  2. 불일치 원인을 진단한다 (예: 글자 뒤 덧붙여짐, 덮어쓰기 실패, 포커스 이탈, 자동완성 간섭, 잘못된 드롭다운 항목 선택).
  3. 필드를 완전히 비운 뒤(`Ctrl+A` -> `Backspace` 또는 프로토타입 세터 초기화) 재입력한다.
  4. 재입력 후 Step 3(독립 검독)을 다시 거친다.
  5. 동일 필드에서 3회 연속 실패 시 즉시 중단하고 상세 Diff 로그를 사용자에게 보고한다.

---

## 3. Submission Gate (최종 제출 차단선)

1. **차단 조건**:
   - 전체 폼(Form) 또는 입력 대상 전체의 Diff 대조표에서 **모든 필드의 불일치율이 0%임이 입증되기 전까지는 'Next', 'Save', 'Continue', 'Submit' 버튼 클릭을 시스템 차원에서 전면 금지**한다.
2. **필수 감사 로그 생성**:
   - 최종 액션 또는 사용자 검토 인계 직전, 아래 규격의 검증 감사 로그를 반드시 출력해야 한다:

```text
[Verification Audit]
Field: <필드명> | Expected: <기댓값> | Actual: <화면 추출값> | Status: MATCH/MISMATCH
```

3. **Zero Auto-Submit 연계**:
   - Audit이 100% MATCH를 달성하더라도, [Rule: Zero Auto-Submit](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/zero-auto-submit.md)에 따라 최종 제출(Submit) 버튼은 에이전트가 누르지 않고 Review 상태에서 사용자 수동 검토로 인계한다.

---

## 4. Failure-Mode Reflection (재발 방지 시스템)

1. **Failure Cache 세션 캐싱**:
   - 교정(Reconciliation)이 1회라도 발생했을 경우, 에이전트는 해당 세션 동안 유지되는 `Failure Cache`에 원인 패턴과 방어책을 즉각 등록한다.
   - 예: `"입력란 클릭 시 기존 텍스트 미선택으로 뒤에 덧붙여짐 -> 이후 모든 텍스트 입력 전 Ctrl+A -> Backspace 강제 적용"`
   - 예: `"드롭다운 검색어 입력 후 첫 번째 옵션 오선택 -> 정확한 텍스트 매칭 검증 및 scrollIntoView 추가"`
   - 예: `"React SPA 폼 상태 롤백 -> 프로토타입 세터 호출 및 input/change/blur 이벤트 연속 디스패치"`
   - 예: `"드롭다운 애니메이션 잔존 DOM 충돌 -> .leave/.hidden 컨테이너 배제 및 최신 활성 드롭다운 타겟팅"`
   - 예: `"커스텀 셀렉트의 히든 input 오판독 -> .select__single-value, [data-cy='selectedValue'], .ud__select__selector 직접 검독"`
2. **선제적 방어 (Proactive Defense)**:
   - 동일 세션 내 유사 필드 입력 시 `Failure Cache`에 등록된 방어책을 사전에 적용하여 오류 발생 자체를 시스템 차원에서 원천 차단한다.

---

## 5. 실행 스크립트 및 테스트 모듈

- **코어 엔진**: [.agents/skills/apply/scripts/reconciliation_engine.py](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/skills/apply/scripts/reconciliation_engine.py)
- **단위 테스트**: [.agents/skills/apply/scripts/test_reconciliation_engine.py](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/skills/apply/scripts/test_reconciliation_engine.py)
