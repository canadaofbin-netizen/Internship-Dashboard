# CEO Chatroom Orchestration & Handoff Protocols (00_CEO_Control_Tower / HANDOFF_PROTOCOLS.md)

이 문서는 **CEO 채팅방(Executive Control Tower)**과 앞으로 생성될 **개별 전문 하위 채팅방(Specialized Child Chatrooms)** 간의 미션 디스패치, 컨텍스트 전달(Zero-Loss Context Handoff), 실행 거버넌스 및 결과 동기화 프로토콜을 정의합니다.

---

## 1. 아키텍처 개요 (Executive Hub & Execution Pods)

```text
                           ┌──────────────────────────────────────────────┐
                           │      👑 CEO CHATROOM (Control Tower)         │
                           │  - 전략 수립 및 우선순위 큐잉               │
                           │  - Master SSOT Excel 최종 변경 및 관리      │
                           │  - CHATROOM_REGISTRY.json 세션 관제          │
                           └──────────────────────┬───────────────────────┘
                                                  │
                ┌─────────────────────────────────┼─────────────────────────────────┐
                │ Mission Handoff Brief           │ Mission Handoff Brief           │ Mission Handoff Brief
                ▼                                 ▼                                 ▼
   ┌──────────────────────────┐      ┌──────────────────────────┐      ┌──────────────────────────┐
   │ 🎯 Pod A: BCI & Neurotech│      │ 🇬🇧 Pod B: UK Tech & Fin  │      │ 🇰🇷 Pod C: Korea Careers │
   │ - Apple, Google, Meta 등 │      │ - Palantir, Trackr UK 700│      │ - KAIST BCI, 당근, 삼성 │
   │ - 콜드 메일 및 네트워킹 │      │ - 지원서 작성 자동화     │      │ - 타임라인 및 오프라인   │
   └────────────┬─────────────┘      └────────────┬─────────────┘      └────────────┬─────────────┘
                │                                 │                                 │
                └─────────────────────────────────┼─────────────────────────────────┘
                                                  │ Return Completion Dossier
                                                  ▼
                                    [CEO Chatroom: SSOT Ingestion]
```

- **CEO 채팅방의 권한 및 책임**:
  1. **SSOT Master Excel 수호**: 모든 기회(글로벌 BCI, 영국 테크/금융, 한국 커리어)의 유일무이한 기준점인 `Master_Internship_Tracker_2027_SSOT.xlsx`의 상태 변경 및 동기화를 총괄합니다.
  2. **미션 디스패치(Dispatch)**: 하위 채팅방이 작업할 명확한 범위(기업명, 시트 행, 요구사항, 후보자 기준 데이터)를 담은 **Handoff Brief**를 생성합니다.
  3. **결과 인입(Reconciliation)**: 하위 채팅방이 완료 후 제출한 **Return Dossier**를 검토하고 레지스트리 및 엑셀에 반영합니다.

- **하위 채팅방(Child Chatroom)의 권한 및 책임**:
  1. 위임받은 단일 미션(예: "팔란티어 지원서 작성 및 검토")에만 100% 집중합니다.
  2. 시스템 전역 설정이나 다른 트랙의 엑셀 데이터를 임의로 변경하지 않습니다.
  3. [Rule: Zero Auto-Submit](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/zero-auto-submit.md) 및 [Rule: Visible Browser Protocol](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/visible-browser-protocol.md)을 철저히 준수합니다.

---

## 2. CEO -> 하위 채팅방 미션 디스패치 프로토콜 (Dispatch Protocol)

CEO 채팅방에서 신규 채팅방을 생성할 때 다음 단계를 거칩니다:

### Step 1: 세션 등록 및 브리프 생성
CEO 챗룸에서 CLI 도구를 실행하거나 에이전트에게 지시합니다:
```bash
python .agents/skills/apply/scripts/ceo_hub.py handoff --session-id <SESSION_ID>
```
이 명령어는 `CHATROOM_REGISTRY.json`의 정보와 `Master_Internship_Tracker_2027_SSOT.xlsx`의 해당 행 데이터를 결합하여 하위 챗룸용 완결형 마크다운 브리프를 생성합니다.

### Step 2: 신규 채팅방 개설 및 프롬프트 주입
사용자는 새 채팅방을 생성하고, 아래 표준 템플릿 형태로 출력된 브리프를 복사하여 첫 메시지로 붙여넣습니다.

#### [템플릿 A: CEO -> Child Chatroom Mission Dispatch Prompt]
```markdown
[MISSION DISPATCH FROM CEO CONTROL TOWER]
Session ID: <SESSION_ID>
Track: <TRACK_NAME> (e.g., TRACK-B: UK 2027 Summer Tech & Finance)
Target Organizations: <TARGET_COMPANIES>
Priority: <PRIORITY> (e.g., URGENT / HIGH)

1. Candidate Ground Truth Baseline (SSOT 불변 데이터):
- Legal Name: Kyubin Yun (윤규빈) | First: Kyubin / Last: Yun
- Email: zcjtyun@ucl.ac.uk
- Phone: +44 7787 442404 (UK Mobile, 국가코드 +44 필수)
- Address: 40 Merchant St, Brent Cross, Suite 638, London, NW2 8BB
- University: University College London (UCL)
- Degree: Bachelor of Science (BSc) in Psychology and Language Sciences
- Graduation: June 2028 (Penultimate Year Class of 2028)
- Grade: Honours (Achieved/Predicted: 70.5/100)
- UK Work Visa: Yes (Student Route Visa - 여름방학 주 40시간 풀타임 근무 법적 보장, 무스폰서)
- Standard Password: Jeff0825!! | Workday Password: Jeff0825!!!! (12자 이상)
- Resume: g:\My Drive\Kyubin_Yun_Workspace\04_Internship\01_Resumes\Kyubin_Yun_Resume_2027.pdf
- GitHub: https://github.com/canadaofbin-netizen
- LinkedIn: https://www.linkedin.com/in/kyubin-yun-495a33301/

2. Mission Objectives & Scope:
- Target Job / Lab: <TARGET_JOB_TITLE>
- Portal URL: <URL>
- Specific Requirements: <REQUIREMENTS>

3. Hard Governance Rules (위반 시 결함):
- [Zero Auto-Submit]: Review / Pre-submit 단계까지만 입력하고 멈출 것. 최종 제출 버튼 자동 클릭 절대 금지.
- [Visible Whale Browser]: 백그라운드 가상 브라우저 금지. 사용자 화면에 보이는 네이버 웨일 브라우저 조작.
- [Text Normalization]: PDF 파싱 아티팩트 방지 (불릿 `• ` 통일, 임의 줄바꿈 unwrap).

4. Deliverable:
작업 완료 후 CEO 채팅방에 보고할 표준 [Mission Completion Dossier]를 작성하여 출력할 것.
```

---

## 3. 하위 채팅방 -> CEO 결과 보고 프로토콜 (Return Protocol)

하위 채팅방에서 작업이 완료되면 에이전트는 다음 규격으로 보고서를 출력하며, 사용자는 이를 CEO 채팅방에 전달합니다.

#### [템플릿 B: Child Chatroom -> CEO Mission Completion Dossier]
```markdown
[MISSION COMPLETION DOSSIER]
Session ID: <SESSION_ID>
Track: <TRACK_NAME>
Target Organizations: <TARGET_COMPANIES>
Execution Status: [SUCCESS_REVIEW_READY / BLOCKED / IN_PROGRESS / REJECTED]

1. Execution Summary:
- 어떤 포털에 접속하여 어떤 입력 작업을 수행했는지 명시.
- Review 화면 도달 여부 및 최종 점검 결과.

2. Verification Audit & SSOT Delta:
- Ground Truth 데이터와의 일치율 (0% 불일치 확인).
- 텍스트 정제(불릿 `• ` 표준화, 문장 줄바꿈 복원) 적용 여부.
- 새로 발굴된 정보 (담당 리크루터 이메일, 마감 일정 변경, 특이 문항 답변 등).

3. Artifacts & Links:
- 지원서 검토 URL (Review URL) 또는 로컬 산출물 경로.
- 생성/보완된 에세이 또는 커버레터 파일 경로.

4. Action Required by Kyubin:
- 최종 사용자가 검토하고 직접 'Submit' 버튼을 눌러야 할 링크 및 주의사항 안내.
```

---

## 4. CEO 채팅방 동기화 및 엑셀 SSOT 반영 (Reconciliation)

CEO 채팅방에서 복귀 보고서를 접수하면:
1. `CHATROOM_REGISTRY.json`의 해당 세션 상태를 `COMPLETED`로 전환하고 결과 요약을 기록합니다.
2. `Master_Internship_Tracker_2027_SSOT.xlsx`의 해당 기업 상태(Status) 열을 갱신합니다 (예: `Review Ready`, `Applied`, `Interview Scheduled`).
3. 필요 시 `python .agents/skills/apply/scripts/consolidate_excel_ssot.py`를 실행하여 엑셀의 정합성을 동기화합니다.
4. 사용자에게 차기 우선순위 미션을 제안하고 새로운 하위 챗룸 브리프를 발급합니다.
