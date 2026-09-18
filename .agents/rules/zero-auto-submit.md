---
description: "Zero Auto-Submit Rule: Strictly prohibits automated clicking of final application submit buttons."
globs: ["**/*"]
alwaysApply: true
---

# Zero Auto-Submit Rule (최종 제출 버튼 자동 클릭 절대 금지)

- **Workspace Directives**: [AGENTS.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/AGENTS.md)

이 규칙은 지원자의 취업 기회 보호 및 시스템 안전을 위해 **절대적인 우선순위(Zero Tolerance)**를 갖는 가드레일입니다.

---

## 1. 제출 통제 가드레일

- **핵심 원칙:**
  - 에이전트는 어떠한 채용 사이트(Greenhouse, Workday, Lever, Taleo, 기업 자체 포털 등)에서도 **최종 지원서 제출 버튼(`Submit Application`, `Submit`, `제출하기` 등)을 프로그램이나 스크립트로 자동 클릭해서는 안 됩니다.**
- **정지 지점:**
  - 반드시 최종 **`Review / Pre-submit`** 화면(모든 입력값과 첨부파일이 올바르게 채워진 상태)까지만 진행하고 즉시 멈추어야 합니다.
- **보고 및 인계:**
  - Review 화면에 도달하면 작성된 주요 항목 요약과 함께 "최종 확인 후 사용자가 직접 [Submit] 버튼을 눌러 제출을 완료해 주십시오"라고 안내해야 합니다.

---

## 2. 폼 내부 엔터(Enter) 키 발송 원천 금지 및 이중 차단 장치

1. **엔터 키(Enter) 발송 전면 금지**:
   - HTML `<form>` 내부의 드롭다운 선택이나 입력란 조작 시 `page.keyboard.press("Enter")`를 절대 전송해서는 안 됩니다. 드롭다운이 닫혀 있거나 포커스가 입력 필드에 있을 경우, 브라우저가 기본 동작으로 `form.submit()`을 트리거하여 원치 않는 조기 제출이 발생하기 때문입니다.
   - 모든 드롭다운 선택은 DOM 옵션 엘리먼트(`.select__option`, `[role="option"]`)를 직접 탐색하여 `.click()` 하거나 네이티브 프로토타입 세터를 통해서만 수행해야 합니다.

2. **클라이언트 사이드 이중 제출 차단 가드 (Form Submit Interceptor)**:
   - 폼 자동화 스크립트 실행 시 첫 번째 조치로 페이지 내 모든 폼에 아래의 제출 차단 가드를 주입하여 돌발 엔터 키나 이벤트 버블링으로 인한 제출을 원천 차단해야 합니다:
   ```javascript
   document.querySelectorAll('form').forEach(f => {
     f.addEventListener('submit', (e) => {
       if (!window.__user_manual_submit_allowed) {
         e.preventDefault();
         e.stopPropagation();
         console.warn('[Zero Auto-Submit Guard] Blocked automatic form submission!');
       }
     }, true);
   });
   ```
