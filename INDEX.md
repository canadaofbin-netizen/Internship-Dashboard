---
type: hub_index
domain: internship
status: active
updated: 2026-09-17
---

# 04_Internship (인턴십 및 취업 마스터 워크스페이스)

2027 하계 인턴십 및 취업 지원 전 과정을 관리하는 종합 커리어 작업 공간입니다.

---

## 📌 핵심 바로가기 및 에이전트 가이드

- **에이전트 행동 지침 및 검증 기준**: [AGENTS.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/AGENTS.md)
- **CEO 관제 타워 및 세션 허브**: [CEO_ORCHESTRATION_HUB.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/00_CEO_Control_Tower/CEO_ORCHESTRATION_HUB.md)
- **CEO 오케스트레이션 규칙**: [Rule: CEO Orchestration Protocol](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/ceo-orchestration-protocol.md)
- **지원자 Ground Truth Baseline**: [Rule: Candidate Ground Truth](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/candidate-ground-truth.md)
- **입력 검증 및 자체 교정 프로토콜**: [Rule: Ground-Truth Integrity](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/ground-truth-integrity.md)
- **메타 프롬프트 템플릿 (/boost 입력 검증)**: [Rule: Meta-Prompt Ground-Truth Audit](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/meta-prompt-ground-truth-audit.md)
- **아키텍처 설계 및 갭 분석 프로토콜**: [Rule: Context-Driven Architecture & Gap Analysis](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/context-driven-architecture-gap-analysis.md)
- **메타 프롬프트 템플릿 (/boost 아키텍처/갭 분석)**: [Rule: Meta-Prompt Architecture & Gap Analysis](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/meta-prompt-architecture-gap-analysis.md)
- **지원서 텍스트 정제 프로토콜**: [Rule: Form Field Text Normalization Protocol](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/form-text-normalization.md)
- **가시 브라우저 실행 원칙**: [Rule: Visible Browser Protocol](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/visible-browser-protocol.md)
- **최종 제출 자동 클릭 금지 원칙**: [Rule: Zero Auto-Submit](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/zero-auto-submit.md)
- **마스터 엑셀 트래커 아키텍처 규칙**: [Rule: Excel Tracker Architecture](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/excel-tracker-architecture.md)
- **워크스페이스 린팅 규칙**: [Rule: Workspace Linting](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/rules/workspace-linting.md)
- **지원서 작성 자동화 스킬**: [Skill: Apply](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/skills/apply/SKILL.md)
- **글로벌 인턴십 리서치 스킬**: [Skill: Research](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/skills/research/SKILL.md)
- **워크스페이스 린터 스킬**: [Skill: Lint](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/.agents/skills/lint/SKILL.md)
- **하위 프로젝트 지침 (2027 Summer Internship)**: [Subproject AGENTS.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/2027_Summer2_Internship/.agents/AGENTS.md)
- **하위 프로젝트 개요 (README.md)**: [Subproject README.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/2027_Summer2_Internship/README.md)
- **영문 이력서 파일 (2027 최신)**: [Kyubin_Yun_Resume_2027.pdf](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/01_Resumes/Kyubin_Yun_Resume_2027.pdf)

---

## 🗂️ 디렉터리 구성

- `00_CEO_Control_Tower/`: CEO 채팅방 관제 센터, 세션 레지스트리(`CHATROOM_REGISTRY.json`) 및 미션 디스패치 브리프
- `01_Resumes/`: 최신 영문/국문 이력서 및 커버레터 원본
- `02_Interview_Prep/`: 기업별 면접 및 온라인 테스트(OA/SJT) 대비 자료
- `03_Data_Science_Roadmap/`: 데이터 사이언스 & 머신러닝 학습 로드맵 및 프로젝트
- `2027_Summer2_Internship/`: 2027 하계 인턴십 지원 서브프로젝트 및 BCI 트래커
- `Backups/`: 버전별 엑셀 및 데이터 백업 아카이브
- `data/source_trackers/`: 통합 이전 원본 엑셀 트래커 아카이브 (글로벌 BCI / 영국 / 한국 트래커 전수 보관)
- `.agents/`: AI 에이전트 공통 규칙(`rules/`) 및 스킬(`skills/`) 정의

---

## 📊 인턴십 트래커 및 현황 보고서

- **통합 단일 진실 공급원(SSOT) 마스터 엑셀**: [Master_Internship_Tracker_2027_SSOT.xlsx](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/Master_Internship_Tracker_2027_SSOT.xlsx) (글로벌 BCI, 영국 테크/금융, 한국 55개 고영향 기회 전수 통합)
- **차기 지원 대상 및 현황 리스트**: [Next_Internship_Applications_List.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/00_CEO_Control_Tower/reports/Next_Internship_Applications_List.md)
- **글로벌 BCI 엔터프라이즈 도시에**: [Global_BCI_Enterprise_Internship_Dossier_2027.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/00_CEO_Control_Tower/reports/Global_BCI_Enterprise_Internship_Dossier_2027.md)
- **국내외 인턴십 리서치 보고서**: [Korea_Internship_Research_Report_2026_2027.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/00_CEO_Control_Tower/reports/Korea_Internship_Research_Report_2026_2027.md)
- **서브프로젝트 BCI 엑셀 트래커**: `2027_Summer2_Internship/2027_BCI_Internship_Tracker.xlsx`
- **글로벌 BCI 원본 인턴십 데이터 엑셀 아카이브**: `data/source_trackers/2027_BCI_Internship_Tracker.xlsx`
- **국내 원본 인턴십 데이터 엑셀 아카이브**: `data/source_trackers/Korea_Internship_Research_2026_2027.xlsx`
- **영국 원본 인턴십 데이터 엑셀 아카이브**: `data/source_trackers/UK_2027_Summer_Internship_Trackr_Master.xlsx`
