---
description: "Protocol for the CEO Chatroom orchestrating specialized child chatrooms, session handoffs, and SSOT synchronization."
globs: ["00_CEO_Control_Tower/**/*", "**/*ceo*"]
alwaysApply: false
---

# CEO Chatroom Orchestration & Multi-Session Protocol

- **Workspace Directives**: [AGENTS.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/AGENTS.md)
- **Central Hub**: [CEO_ORCHESTRATION_HUB.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/00_CEO_Control_Tower/CEO_ORCHESTRATION_HUB.md)
- **Handoff Protocols**: [HANDOFF_PROTOCOLS.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/00_CEO_Control_Tower/HANDOFF_PROTOCOLS.md)
- **Session Registry**: [CHATROOM_REGISTRY.json](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/00_CEO_Control_Tower/CHATROOM_REGISTRY.json)
- **Master SSOT Tracker**: [Master_Internship_Tracker_2027_SSOT.xlsx](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/Master_Internship_Tracker_2027_SSOT.xlsx)

이 규칙은 본 채팅방(CEO Control Tower)이 향후 생성될 복수의 전문 하위 채팅방(Specialized Child Chatrooms)을 총괄 지휘하고, 단일 진실 공급원(SSOT) 원칙을 집행하는 표준 운영 지침을 정의합니다.

---

## 1. CEO 챗룸 및 하위 챗룸의 역할 분담 원칙 (Authority Separation)

1. **CEO 채팅방 (Executive Control Tower)**:
   - 전체 커리어 트랙(Global BCI, UK Tech & Finance, Korea Careers, DS Technical Prep)의 우선순위와 일정을 총괄합니다.
   - 모든 기회의 공식 기록인 `Master_Internship_Tracker_2027_SSOT.xlsx` 및 `00_CEO_Control_Tower/CHATROOM_REGISTRY.json`의 상태를 갱신할 배타적 권한을 가집니다.
   - 하위 채팅방으로 전달할 **미션 디스패치 브리프(Mission Handoff Brief)**를 발행합니다.
2. **하위 채팅방 (Specialized Child Chatrooms)**:
   - 디스패치된 단일 미션(지원서 작성, 포털 탐색, 랩 리서치 등)을 독립적으로 실행합니다.
   - 실행 전 [Rule: Context-Driven Architectural Blueprint & Gap Analysis](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/context-driven-architecture-gap-analysis.md)을 준수합니다.
   - 지원 작업 시 [Rule: Zero Auto-Submit](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/zero-auto-submit.md) 및 [Rule: Visible Browser Protocol](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/visible-browser-protocol.md)을 100% 강제 적용합니다.
   - 작업 완료 시 반드시 규격화된 [Mission Completion Dossier]를 작성하여 CEO 채팅방으로 복귀 보고합니다.

---

## 2. 4단계 미션 라이프사이클 (Mission Lifecycle)

| 단계 (Phase) | 수행 주체 | 핵심 행동 (Core Action) | 산출물 및 기준 |
| :--- | :--- | :--- | :--- |
| **Phase 1: Registration** | CEO Chatroom | 세션 ID 부여 및 `CHATROOM_REGISTRY.json` 등록 | Session ID, 트랙 분류, 목표 기업 설정 |
| **Phase 2: Handoff** | CEO Chatroom | Ground Truth와 대상 포지션 데이터 결합 브리프 생성 | `sessions/briefs/<ID>_brief.md` |
| **Phase 3: Execution** | Child Room | 가시 브라우저 조작 및 지원서 검토(Review) 도달 | Review URL, 불일치율 0% 검증 |
| **Phase 4: Reconciliation**| CEO Chatroom | 결과 도시에 인입, SSOT 엑셀 및 레지스트리 상태 갱신 | `Master_Internship_Tracker_2027_SSOT.xlsx` |

---

## 3. 컨텍스트 무손실 핸드오프 규칙 (Zero-Loss Context Handoff)

- CEO 챗룸에서 하위 챗룸으로 컨텍스트를 인계할 때, 지원자의 인적사항이나 자격증명을 모호하게 지시하지 않고 [Rule: Candidate Ground Truth Baseline](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/candidate-ground-truth.md)에 기반한 확정된 값을 100% 명시적으로 주입합니다.
- 하위 챗룸은 전달받은 Ground Truth 값을 임의로 변경하거나 대체할 수 없습니다.

---

## 4. 단일 진실 공급원(SSOT) 엑셀 관리 원칙

- 개별 엑셀 파일이 파편화되는 것을 방지하기 위해, 모든 지원 현황과 신규 발굴 정보는 오직 `Master_Internship_Tracker_2027_SSOT.xlsx`에 집약됩니다.
- 하위 챗룸에서 리크루터 연락처나 지원 상태 변경이 발생하면, CEO 챗룸을 통해 `build_ssot` 또는 동기화 명령을 실행하여 엑셀에 최종 반영합니다.
