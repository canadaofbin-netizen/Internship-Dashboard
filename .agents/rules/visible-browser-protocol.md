---
description: "Visible Browser Protocol: Prohibits hidden/headless background browsers and enforces visible browser execution in Naver Whale or foreground browser."
globs: ["**/*"]
alwaysApply: true
---

# Visible Browser Protocol Rule (화면 가시 브라우저 의무 규칙)

- **Workspace Directives**: [AGENTS.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/AGENTS.md)

이 규칙은 `04_Internship` 워크스페이스에서 채용 포털 접속 및 지원서 작성을 수행하는 모든 AI 에이전트에게 적용되는 **가시성 강제 규칙**입니다.

---

## 1. 백그라운드 가상 브라우저 금지 원칙 (No Hidden/Headless)

- **금지 행위:**
  - 사용자 화면에 뜨지 않는 백그라운드 가상 크롬(`headless=True`, `AppData\Local\Temp` 가상 프로필 등)을 실행하여 사용자 몰래 뒤편에서 작업하는 행위를 엄격히 금지합니다.
  - 사용자는 자신이 어떤 사이트에 무엇이 입력되고 있는지 실시간으로 모니터링할 수 있어야 합니다.

---

## 2. 가시 브라우저 실행 표준 (Visible Browser Standards)

에이전트는 브라우저 작업 시 다음 중 하나의 방법으로 **반드시 사용자의 화면에 창이 보이도록** 실행해야 합니다:

### 방법 A: 사용자 메인 브라우저인 네이버 웨일(Whale)로 탭 직접 열기 (최우선 권장)
- 웨일 실행 파일 경로:
  `C:\Program Files\Naver\Naver Whale\Application\whale.exe`
- 시스템 명령어:
  ```powershell
  Start-Process "C:\Program Files\Naver\Naver Whale\Application\whale.exe" "<지원URL>"
  ```
- 또는 Python 스크립트:
  `python .agents/skills/apply/scripts/open_visible_browser.py --url "<지원URL>" --browser whale`

### 방법 B: Playwright 자동화 시 가시 모드(`headless=False`) 강제
- Playwright 코드를 작성할 경우 반드시 `headless=False` 및 화면 위치/크기를 지정하여 사용자가 즉시 인지할 수 있는 새 창으로 띄워야 합니다:
  ```python
  browser = await p.chromium.launch(headless=False, args=["--start-maximized", "--window-position=100,100"])
  ```

---

## 3. 작업 화면 가시성 보고 의무

- 브라우저를 열 때 사용자에게 "현재 네이버 웨일(또는 전면 브라우저 창)에 해당 지원서 페이지를 열었습니다"라고 안내합니다.
- 자동 입력 완료 후 각 단계의 스크린샷 증빙 또는 직접 눈으로 확인 후 제출할 수 있도록 검토 단계를 명확히 전달합니다.
