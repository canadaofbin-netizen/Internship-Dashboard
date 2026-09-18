---
name: Workspace Linter
description: Enforces the Cookiecutter Data Science structure and lints Python code.
command: lint
---

# Instructions

When the user types `/lint` in the chat, you must perform the following actions to clean up and organize the workspace according to our strict rules.

## Step 1: Directory Structure Verification
1. List the files and folders in the project directory (`g:\My Drive\Kyubin_Yun_Workspace\04_Internship\2027_Summer2_Internship`).
2. Identify any files or folders that do NOT belong in the root directory according to the [Workspace Linting Guidelines](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/2027_Summer2_Internship/.agents/rules/workspace-linting.md) and [AGENTS.md Directives](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/AGENTS.md).

   - Allowed in root: `.agents`, `Templates`, `data`, `notebooks`, `src`, `reports`, `README.md`, `requirements.txt`, `.gitignore`, `2027_BCI_Internship_Tracker.xlsx`.
3. If you find orphaned scripts, datasets, or notebooks in the root directory, MOVE them to their appropriate subdirectories automatically:
   - Raw datasets (.csv, .edf, .bdf) -> `data/raw/`
   - Exploratory Notebooks (.ipynb) -> `notebooks/`
   - Python preprocessing scripts (.py) -> `src/features/`
   - Python modeling scripts (.py) -> `src/models/`

## Step 2: Code Linting
1. Identify any Python (`.py`) files in the workspace (specifically inside the `src/` directory).
2. If Python files are found, check if they conform to PEP 8 standards, have type hints, and have docstrings.
3. Automatically format the code using the `replace_file_content` tool to ensure PEP 8 compliance, add missing type hints, and insert Google-style docstrings. (If `ruff` or `black` is available in the environment, you may also run them via the terminal).

## Step 3: Summary Report
1. Output a short, friendly summary in Korean to the user.
2. Tell them exactly which files were moved (and to where).
3. Tell them which Python files were linted and formatted.
4. If the workspace is already perfectly clean, praise the user for maintaining a clean Cookiecutter Data Science structure!
