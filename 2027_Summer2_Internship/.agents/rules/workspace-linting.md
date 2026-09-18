---
description: "Cookiecutter Data Science directory structure and Python code linting standards for 2027 Summer Internship."
globs: ["**/*.py", "**/*.ipynb"]
alwaysApply: false
---

# Workspace Linting & Structure Guidelines (Cookiecutter Data Science)

- **Workspace Directives**: [AGENTS.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/AGENTS.md) | [Subproject AGENTS.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/2027_Summer2_Internship/.agents/AGENTS.md)

To prevent the workspace from becoming messy as the BCI (Motor Imagery) side project and other research tasks grow, the AI must strictly enforce the **Cookiecutter Data Science (CCDS)** directory structure, which is the gold standard for ML and Data Science projects on GitHub. 

## 1. Directory Structure Enforcements
When generating new code, downloading datasets, or creating notebooks, the AI must place them in the following structured directories. Do NOT clutter the root directory.

```text
.
├── data/
│   ├── raw/             # The original, immutable EEG data dump (Do NOT edit these files)
│   ├── interim/         # Intermediate data that has been transformed or filtered
│   └── processed/       # The final, canonical data sets for modeling (e.g., T3/T4/F7/F8 only)
├── notebooks/           # Jupyter notebooks for exploration. 
│                        # Naming convention: <step>-<initials>-<description>.ipynb (e.g., 01-ky-eda.ipynb)
├── src/                 # Source code for use in this project
│   ├── data/            # Scripts to download or generate data
│   ├── features/        # Scripts to extract features (e.g., channel reduction, bandpass filtering)
│   ├── models/          # Scripts to train models and make predictions
│   └── visualization/   # Scripts to create exploratory and results-oriented visualizations
├── reports/             # Generated analysis (e.g., PDF portfolios for cold emails, figures)
└── Templates/           # Templates for research and outreach (e.g., Research_Template.md)
```
*Rule: If a user asks to write a script for preprocessing EEG, automatically place it in `src/features/`. If downloading raw open-source EEG, put it in `data/raw/`.*

## 2. Code Linting & Formatting Rules
To ensure the python code in this repository remains professional and readable (crucial when sharing a GitHub link in a cold email to tech companies):
1. **PEP 8 Compliance**: All Python code generated must adhere to PEP 8 standard formatting.
2. **Type Hinting**: Use Python type hints (`def process_eeg(data: pd.DataFrame) -> np.ndarray:`) to make the code highly readable and robust.
3. **Docstrings**: Use standard docstrings (Google or NumPy style) for all functions, especially in the `src/` directory.
4. **Imports**: Group imports properly (Standard library -> Third party -> Local `src` imports).
