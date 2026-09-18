# 2027 Summer Internship (BCI & Neurotech)

2027 하계 인턴십(Global BCI, Neurotech & AI Tech) 지원 및 마스터 트래커 프로젝트입니다.

- **Workspace Directives**: [AGENTS.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/AGENTS.md)
- **Subproject Directives**: [.agents/AGENTS.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/2027_Summer2_Internship/.agents/AGENTS.md)
- **Master Excel Tracker**: `2027_BCI_Internship_Tracker.xlsx`

---

## 📁 Directory Structure (Cookiecutter Data Science)

```text
.
├── .agents/                 # Subproject directives, rules, and skills
├── Backups/                 # Pristine and versioned Excel backups
├── data/                    # Data storage
│   ├── raw/                 # Original, immutable datasets
│   ├── interim/             # Intermediate processed data
│   └── processed/           # Canonical datasets for analysis
├── notebooks/               # Jupyter notebooks for exploratory analysis
├── reports/                 # Generated analysis and portfolio reports
├── src/                     # Source code for data pipelines and verification
│   ├── data/                # Data collection and download scripts
│   ├── features/            # Feature engineering, failsafe, and verification scripts
│   ├── models/              # Model training and prediction logic
│   └── visualization/       # Visualization scripts
├── Templates/               # Outreach and research markdown templates
├── 2027_BCI_Internship_Tracker.xlsx  # Master BCI Internship Tracker
└── README.md
```

## 🛠️ Verification & Pipeline Execution

```bash
# Verify headers in Research_Database
python src/features/check_headers.py

# Enforce zero-hallucination failsafe (hide unverified rows & telemetry columns G-K)
python src/features/failsafe_enforcer.py

# Run Excel injection formatting and structural integrity test
python src/features/verify_injection.py
```
