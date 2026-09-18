---
description: "Rules for interacting with, formatting, and updating the Master Internship Tracker Excel file."
globs: ["**/*.xlsx", "**/*tracker*"]
alwaysApply: false
---

# Excel Tracker Architecture & Anti-Hallucination Rules

- **Workspace Directives**: [AGENTS.md](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/AGENTS.md)

This rule file dictates how AI agents must interact with, format, and populate the Master Internship Tracker (`2027_BCI_Internship_Tracker.xlsx` / `Korea_Internship_Research_2026_2027.xlsx`).

## 1. Map & Database Architecture (Strict Compliance)
Agents must NEVER break the Map & Database structure of the Excel file.

### A. `1.Overview_Map` (The Anchor Sheet)
- **Purpose**: A clean, high-level dashboard.
- **Rules**:
  - **Do NOT** add detailed networking contacts, hooks, or multiple URLs to this sheet.
  - **Do NOT** use emojis in the `Opening Period` or `Priority` columns (keep it clean text).
  - **Sorting**: Must always be sorted by `Priority` in this specific order: `Global Big Tech` -> `UK Startup` -> `US Startup` -> `KR Startup` -> `KR Conglomerate`.
  - **Freeze Panes**: Must always be frozen at `B2` (Only `Company Name` and Row 1 are anchored).
  - **Deep Dive Link**: Column E must contain a clickable internal hyperlink `➡️ Go to DB` that points to the exact row in `2.Research_Database`.

### B. `2.Research_Database` (The Deep Dive Sheet)
- **Purpose**: A vertical-expansion sheet designed to bypass Excel's "one link per cell" limitation.
- **Rules**:
  - **Merged Rows**: Every company MUST be allocated exactly 3 rows. The `Company Anchor` (Col A) and `Core Research Fit` (Col C) must be merged across these 3 rows.
  - **Hyperlinks (CRITICAL)**: To ensure emails and URLs are clickable, they MUST be placed in individual rows (Row 1 for Target 1, Row 2 for Target 2, etc.) under the `Target Email (Clickable)` column.
  - **Do NOT** combine multiple emails into a single cell using line breaks (`\n`), as this breaks the clickable hyperlink functionality.

## 2. Anti-Hallucination & Research Verification
When an agent is tasked with researching a new company and adding it to the tracker:
1. **Fact-Check URLs**: Ensure the `Careers Portal` URL actually exists and is active. Do not hallucinate dummy URLs.
2. **Target Profiles**: Verify that the extracted `Target 1/2/3` individuals actually work at the specified organization via a Web Search before adding them to the CRM.
3. **Undergraduate Constraint**: Double-check the job requirements. If a role is labeled "Research Scientist," implicitly verify if it requires a PhD. If it does, automatically pivot the target position to "Data Science Intern", "UX Researcher Intern", or "Research Assistant". 

## 3. Styling Constraints
- Always use the predefined pastel colors for Priority rows in the Map.
- Do not use generic, high-contrast Zebra striping (black/white). Keep the corporate, minimalistic aesthetic (Soft Grays, Dark Navy Headers `FF2C3E50`, White font).
