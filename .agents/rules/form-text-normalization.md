---
description: "Form Field Text Normalization & Clean Formatting Protocol: Strictly mandates removal of raw PDF bullets, unwrapping of mid-sentence line breaks, and professional formatting across all job application forms."
globs: ["**/*"]
alwaysApply: true
---

# Form Field Text Normalization & Clean Formatting Protocol (지원서 텍스트 정제 및 줄바꿈/불릿 표준화 규칙)

- **Workspace Directives**: [AGENTS.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/AGENTS.md)

이 규칙은 이력서(PDF) 파싱, 텍스트 복사, 또는 자동 폼 입력 시 발생하는 **3대 추악한 아티팩트(Ugly Artifacts)**를 원천 차단하고, 채용 담당자(Recruiter/Hiring Manager)에게 제출되는 모든 지원서 텍스트를 사람이 직접 공들여 작성한 수준의 최고급 포맷으로 완성하기 위한 **절대 강제 규칙**입니다.

---

## 1. 도입 배경 및 차단 대상 (Target Artifacts)

PDF 자동 파싱 모듈이나 단순 텍스트 추출기를 통해 추출된 텍스트는 브라우저 폼(Textarea, Input)에 들어갈 때 다음과 같은 심각한 품질 결함을 동반합니다:
1. **원시 불릿 기호 및 공백 누락**:
   - PDF 내부 폰트 글리프인 `⚫`, `●`, `⬤` (\u2b24), `▪`, `▫`, `◆`, `◇`, `⁃`, `◦`, `‣`, `∙` 등이 그대로 복사됨.
   - 불릿 기호와 본문 단어 사이에 공백이 누락되어 `⚫Engineered`, `⬤Automated` 처럼 단어가 붙어버리는 현상.
2. **문장 중간 임의 줄바꿈 (Mid-Sentence Hard Breaks)**:
   - PDF의 좁은 열(Column) 너비에 맞춰 시각적으로 강제 개행된 줄바꿈(`\n`)이 그대로 텍스트 필드에 삽입됨.
   - 예: `achieving high\ninter-rater reliability`, `Zotero via MCP,\nprogrammatically`, `situational strength\nbuffers AI-induced...`
   - 행 끝 하이픈 줄바꿈(`inter-\nrater`)이 부자연스러운 공백(`inter- rater`)으로 치환되는 현상.
   - 브라우저 텍스트 필드는 자체적으로 자동 줄바꿈(Word Wrap)을 수행하므로, 이러한 임의 줄바꿈이 들어가면 문장이 뚝뚝 끊겨 극도로 어색하고 비전문적으로 보임.
3. **불규칙한 띄어쓰기 및 구두점 오류**:
   - 쉼표(`,`), 세미콜론(`;`), 콜론(`:`) 뒤 공백 누락, 불필요한 이중 공백, 줄 끝 트레일링 공백.
   - 문장 끝 마침표(`.`) 뒤에 공백 없이 대문자로 시작하는 문장이 연결되는 현상 (`QA.Refined` -> `QA. Refined`).

---

## 2. 텍스트 정제 5대 표준 규격 (5 Normalization Mandates)

모든 지원서 폼의 서술형 문항, 경력 설명(Experience Description), 프로젝트 설명(Project Description)에 텍스트를 기입할 때는 다음 5대 규격을 반드시 충족해야 합니다:

### [원칙 1] 표준 불릿 통일 (`• ` 또는 `- `)
- 모든 원시 불릿 기호(`⚫`, `●`, `⬤`, `▪`, `▫`, `◆`, `◇`, `⁃`, `◦`, `‣`, `∙`, `o `, `* `, `- `)는 표준 유니코드 불릿 **`• `** (`\u2022` + 반각 공백 1칸)으로 통일 변환합니다.
- 불릿 기호 바로 뒤에는 반드시 1칸의 공백을 두어 단어와 붙는 현상을 원천 방지합니다 (`• Engineered` O / `•Engineered` X).
- **주의**: 영단어 'of', 'on', 'our' 등 일반 단어가 불릿으로 오인식되어 앞 글자가 잘리는 오류(`f 500k`, `n AWS`)가 발생하지 않도록, ASCII 및 알파벳 마커는 반드시 뒤에 공백이 수반된 경우(`o `)에만 불릿으로 판별합니다.

### [원칙 2] 문장 내 임의 줄바꿈 완전 제거 (Unwrap Mid-Sentence Breaks)
- 동일한 불릿 포인트 또는 단락 내에서 문장이 끝나지 않았는데 PDF 레이아웃 때문에 발생한 모든 줄바꿈(`\n`)을 제거하고 단일 공백(` `)으로 이어 붙입니다.
- 행 끝 하이픈 단어(`inter-\nrater`, `high-\nperformance`)는 공백 없이 매끄럽게 연결합니다 (`inter-rater`, `high-performance`).
- **오직 별개의 불릿 항목 사이(`\n`)** 또는 **서로 다른 문단 사이(`\n\n`)**에만 의도적인 개행을 유지합니다.

### [원칙 3] 구두점 및 공백 정규화 (Punctuation & Whitespace Cleanup)
- 쉼표(`,`), 세미콜론(`;`), 콜론(`:`) 뒤에 영문자가 바로 오는 경우 단일 공백을 자동 보정합니다 (`MCP,programmatically` -> `MCP, programmatically`, `Skills:Python` -> `Skills: Python`).
- 마침표(`.`) 뒤에 대문자가 바로 붙는 경우 단일 공백을 보정하되 약어(`Ph.D.`, `U.S.A.`)는 안전하게 보존합니다.
- 탭(`\t`) 및 2개 이상의 연속된 공백은 단일 공백(` `)으로 축소합니다.
- 각 줄의 시작과 끝에 위치한 무의미한 여백(Leading/Trailing whitespace)을 제거합니다.

### [원칙 4] 프레임워크 폼 상태 동기화 (DOM & State Sync)
- React, Vue, Angular 등 현대 SPA 기반 채용 포털(TikTok Careers, Workday, Greenhouse 등)은 DOM 프로퍼티만 변경하면 컴포넌트 내부 State가 갱신되지 않습니다.
- 따라서 텍스트를 입력하거나 교정할 때는 Playwright의 `fill()` 메서드를 사용하거나, 프로토타입 세터와 함께 `input`, `change`, `blur` 이벤트를 강제 디스패치해야 합니다:
  ```javascript
  const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
  setter.call(textarea, normalizedText);
  textarea.dispatchEvent(new Event('input', { bubbles: true }));
  textarea.dispatchEvent(new Event('change', { bubbles: true }));
  textarea.dispatchEvent(new Event('blur', { bubbles: true }));
  ```

### [원칙 5] 사전 검증 및 자동 후처리 의무 (Post-Parsing Clean Hook)
- 이력서 PDF 파싱 결과를 폼에 입력할 때는 반드시 공용 정제 모듈(`.agents/skills/apply/scripts/text_normalizer.py`)을 통과시킨 정제 텍스트만 주입합니다.
- 지원서가 최종 Review 단계에 도달하기 전, 에이전트는 페이지 내 모든 `textarea`를 재점검하여 위 아티팩트가 남아있지 않은지 자체 전수 검사를 완결해야 합니다.

---

## 3. 정제 전/후 비교 예시 (Ground Truth Reference)

| 구분 | 정제 전 (Ugly / Raw PDF Artifacts) | 정제 후 (Clean / Professional Standard) |
| :--- | :--- | :--- |
| **사례 A** | `⬤Engineered an LLM classification pipeline to evaluate 700+ papers against screening criteria, achieving high`<br>`inter-rater reliability (κ = 0.98) while resolving complex edge cases through iterative QA refinement.` | `• Engineered an LLM classification pipeline to evaluate 700+ papers against screening criteria, achieving high inter-rater reliability (κ = 0.98) while resolving complex edge cases through iterative QA refinement.` |
| **사례 B** | `● Automated the collection and deduplication of 600+ papers by linking journal APIs to Zotero via MCP,`<br>`programmatically archiving citation metadata and full-text PDFs.` | `• Automated the collection and deduplication of 600+ papers by linking journal APIs to Zotero via MCP, programmatically archiving citation metadata and full-text PDFs.` |
| **사례 C** | `● Led and supervised a squad of 25+ personnel, managing daily operations, performance evaluation, and conflict`<br>`resolution to maintain high morale and operational effectiveness.` | `• Led and supervised a squad of 25+ personnel, managing daily operations, performance evaluation, and conflict resolution to maintain high morale and operational effectiveness.` |
