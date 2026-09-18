---
description: "Cookiecutter Data Science directory structure and Python code linting standards."
globs: ["**/*.py", "**/*.ipynb"]
alwaysApply: false
---

# Workspace Linting & Structure Guidelines (Cookiecutter Data Science)

- **Workspace Directives**: [AGENTS.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/AGENTS.md)

To prevent the workspace from becoming messy as projects and research tasks grow, the AI must strictly enforce the **Cookiecutter Data Science (CCDS)** directory structure, which is the gold standard for ML and Data Science projects on GitHub. 

## 1. Directory Structure Enforcements
When generating new code, downloading datasets, or creating notebooks, the AI must place them in the following structured directories. Do NOT clutter the root directory.

```text
.
├── data/
│   ├── raw/             # The original, immutable data dump (Do NOT edit these files)
│   ├── interim/         # Intermediate data that has been transformed or filtered
│   └── processed/       # The final, canonical data sets for modeling
├── notebooks/           # Jupyter notebooks for exploration
├── src/                 # Source code for use in this project
│   ├── data/            # Scripts to download or generate data
│   ├── features/        # Scripts to extract features
│   ├── models/          # Scripts to train models and make predictions
│   └── visualization/   # Scripts to create visualizations
├── reports/             # Generated analysis
└── Templates/           # Templates for research and outreach
```

## 2. Code Linting & Formatting Rules
To ensure Python code remains professional and readable:
1. **PEP 8 Compliance**: All Python code generated must adhere to PEP 8 standard formatting.
2. **Type Hinting**: Use Python type hints (`def process_data(df: pd.DataFrame) -> np.ndarray:`) to make code readable and robust.
3. **Docstrings**: Use standard docstrings (Google or NumPy style) for all functions.
4. **Imports**: Group imports properly (Standard library -> Third party -> Local imports).
