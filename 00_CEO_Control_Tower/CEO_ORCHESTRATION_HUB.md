# CEO Orchestration Hub & Central Control Tower (00_CEO_Control_Tower)

이 문서는 2027 하계 인턴십 및 커리어 전 과정을 지휘하는 **CEO 채팅방의 메인 관제 센터 대시보드**입니다. 앞으로 개설될 모든 전문 하위 채팅방(Child Chatrooms)은 본 허브의 통제를 받으며, 단일 진실 공급원(SSOT)인 `Master_Internship_Tracker_2027_SSOT.xlsx`와 완벽히 동기화됩니다.

---

## 📌 핵심 바로가기 및 마스터 자산 (Master Assets)

- **통합 마스터 엑셀 트래커 (SSOT)**: [Master_Internship_Tracker_2027_SSOT.xlsx](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/Master_Internship_Tracker_2027_SSOT.xlsx)
  - 글로벌 BCI 28개사, 영국 91개 엄선 프로그램(L1 19개 + AI/DS/Tech Consulting 72개), 영국 BCI 26선, 한국 63개 고영향 기회 등 208개 핵심 데이터 통합 및 직결 링크 탑재
- **세션 디스패치 및 복귀 프로토콜**: [HANDOFF_PROTOCOLS.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/00_CEO_Control_Tower/HANDOFF_PROTOCOLS.md)
- **머신러닝/에이전트 세션 레지스트리**: [CHATROOM_REGISTRY.json](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/00_CEO_Control_Tower/CHATROOM_REGISTRY.json)
- **CEO 오케스트레이션 거버넌스 규칙**: [Rule: CEO Orchestration Protocol](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/ceo-orchestration-protocol.md)
- **워크스페이스 총괄 행동 지침**: [AGENTS.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/AGENTS.md)
- **전체 워크스페이스 색인**: [INDEX.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/00_CEO_Control_Tower/INDEX.md)
- **심층 리서치 보고서 및 도시에**:
  - [글로벌 BCI 엔터프라이즈 도시에](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/00_CEO_Control_Tower/reports/Global_BCI_Enterprise_Internship_Dossier_2027.md)
  - [국내 55개 고영향 기회 종합 보고서](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/00_CEO_Control_Tower/reports/Korea_Internship_Research_Report_2026_2027.md)
  - [차기 지원 대상 및 현황 리스트](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/00_CEO_Control_Tower/reports/Next_Internship_Applications_List.md)

---

## 🗂️ 4대 전략 커리어 트랙 현황 (Strategic Tracks Overview)

| 트랙 ID | 트랙 명칭 (Track Name) | 대상 도메인 및 기업군 | 규모 및 데이터 현황 | 현재 운영 상태 | 담당 시트 (SSOT Sheet) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TRACK-A** | **Global BCI & Neurotech** | Apple, Google, Meta, Neuralink 등 글로벌 탑티어 BCI | 28개 타깃 기업, 84명 핵심 연구자 | 연구 및 네트워킹 대기 | `6.Global_BCI_Map` / `7.BCI_Research_DB` |
| **TRACK-B** | **UK 2027 Summer Tech & Fin** | Palantir, Tower Research, Man Group, AI/ML·Data Science·Startups 72선, 영국 BCI 26선 | 117개 기회 (L1 19개 타깃 + AI/DS/Tech Consulting 72개 + 영국 BCI 생태계 26개) | **즉시 지원 착수 (Palantir 등)** | `UK_BCI` / `1.UK_Top_Targets` / `2.UK_Tech_Quant_Finance` |
| **TRACK-C** | **Korea High-Impact Careers** | KAIST BCI 랩, 당근/토스 DA/Product, 베인/맥킨지 RA, 삼성전자, 네이버, 카카오 | 63개 전수 검증 기회 (6대 섹터) | 타임라인 모니터링 | `3.KR_타임라인_우선순위` / `4.KR_Tech_BCI` / `5.KR_전략_대기업_금융` |
| **TRACK-D** | **Data Science & Tech Prep** | 머신러닝 로드맵, 파이썬 DS, 코딩테스트/OA/SJT | 2대 핵심 로드맵 + 실전 프로젝트 | 상시 역량 강화 | `03_Data_Science_Roadmap` |

---

## 🛰️ 활성 및 등록 하위 채팅방 세션 레지스트리 (Active Chatroom Sessions)

CEO 채팅방에서 관리 및 관제 중인 세션 목록입니다:

| 세션 ID | 트랙 | 채팅방 명칭 및 미션 | 상태 (Status) | 우선순위 | 산출물 및 브리프 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ROOM-GLOBAL-BCI-001` | TRACK-A | Global BCI 타깃 도시에 및 네트워킹 리서치 | `COMPLETED` | HIGH | 28개사 리서치 완료 / 도시에 구축 |
| `ROOM-UK-PALANTIR-002` | TRACK-B | **Palantir Product Designer & FDSE 지원서 작성** | `READY_FOR_DISPATCH` | **URGENT** | 공식포털 단독발굴 / 디스패치 대기 |
| `ROOM-KR-RESEARCH-003` | TRACK-C | 국내 55개 타깃 전수 검증 및 종합 보고서 발행 | `COMPLETED` | HIGH | 8개 시트 대조 및 78KB 보고서 완성 |

---

## 🛠️ CEO Control Tower CLI 도구 가이드 (`ceo_hub.py`)

CEO 채팅방에서는 전용 CLI 툴을 통해 세션을 생성, 디스패치하고 엑셀을 재구축할 수 있습니다:

```bash
# 1. 전체 등록 세션 및 트랙 현황 조회
python .agents/skills/apply/scripts/ceo_hub.py list

# 2. 신규 하위 채팅방 등록
python .agents/skills/apply/scripts/ceo_hub.py register --session-id ROOM-UK-AMAZON-004 --track TRACK-B --title "Amazon SDE Intern Apply" --targets "Amazon UK" --priority HIGH

# 3. 하위 채팅방용 완결형 마크다운 브리프 자동 생성 (Ground Truth 자동 주입)
python .agents/skills/apply/scripts/ceo_hub.py handoff --session-id ROOM-UK-PALANTIR-002

# 4. 하위 채팅방 작업 완료 복귀 보고서 인입 및 레지스트리 동기화
python .agents/skills/apply/scripts/ceo_hub.py sync-return --session-id ROOM-UK-PALANTIR-002 --status SUCCESS_REVIEW_READY --summary "Review 화면 도달 완료. 사용자 최종 제출 대기."

# 5. Master SSOT Excel 동기화 및 재컴파일
python .agents/skills/apply/scripts/ceo_hub.py build-ssot
```

---

## 🎯 즉시 실행 우선순위 로드맵 (Immediate Action Queue)

1. **[L1 Tier] Palantir Technologies (London, UK)**:
   - 직무: Product Designer, Internship / Forward Deployed Software Engineer (FDSE) Intern
   - 조치: `ROOM-UK-PALANTIR-002` 하위 챗룸으로 디스패치하여 지원서 작성 및 Review 도달.
2. **[상시/ASAP] 당근 (Daangn) Data Analyst (Seoul, KR)**:
   - 직무: AI-Driven DA / Growth DA (인턴 3~6개월)
   - 조치: 국문 이력서 및 포트폴리오 정비 후 지원 준비.
3. **[가을 공채] Bain & Company / McKinsey & Company (Seoul / London)**:
   - 직무: Associate Consultant Trainee (ACT) / Summer Business Analyst
   - 조치: 문제해결 역량 및 케이스 인터뷰 대비.
4. **[2027년 2~3월 접수] 삼성전자 DX/DS부문 해외대 학부 하계 인턴십**:
   - 직무: Samsung Research, MX사업부, 빅데이터센터, 반도체 AI
   - 조치: 페널티메이트(2028년 6월 졸업) 지원 자격 완벽 부합 확인 완료, 정규직 전환 대비.
