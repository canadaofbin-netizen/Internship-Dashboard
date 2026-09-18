---
name: BCI Zero-Hallucination Researcher
description: Master skill for researching Global BCI Tech Companies, enforcing the Zero-Hallucination Protocol, and injecting verified data into the 2027 Internship Tracker.
command: research
---

# Instructions

When the user invokes `/research`, you must execute the end-to-end BCI internship research pipeline. This pipeline ensures that no hallucinated data enters the tracker and strictly aligns with the user's undergraduate background.

## 1. Undergraduate & Role Constraints ([AGENTS.md Compliance](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/AGENTS.md))
- **Target Persona**: UCL PALS Undergraduate Student with skills in Python EEG Data Pipelines (Motor Imagery channel reduction), Web Scraping, and ML Optimization.
- **Target Roles**: Prioritize Data Science Intern, UX Researcher (UXR) Intern, and Machine Learning Intern.
- **Banned Roles**: Strictly avoid "Research Scientist" roles, as they require a PhD.
- **Strategy Hook Generation**: For every targeted PI or recruiter, you must draft a hook explaining how the user's practical EEG/ML pipeline skills can directly solve bottlenecks in their specific lab/wearable team.

## 2. Research Execution Pipeline
You must execute the research in the following order:

### Phase 1: Target Selection
- Ask the user which companies they want to research, or propose a mix of:
  - **BCI Startups**: Neuralink, Synchron, Precision Neuroscience, Paradromics, Kernel.
  - **Global Big Tech**: Meta Reality Labs, Snap Lab, Apple Biosignals, DeepMind.

### Phase 2: Agent Deep Research
- Spawn multiple `CompanyResearcher` subagents concurrently using the `invoke_subagent` tool.
- Instruct subagents to find:
  1. The official filtered careers portal URL for internships.
  2. The estimated opening period for Summer 2027 internships.
  3. 1-3 specific academic/industry targets (PIs, Researchers, Recruiters) on LinkedIn or lab directories.

### Phase 3: Zero-Hallucination Verification
- You MUST NOT guess URLs or emails. All data must be subjected to the **Zero-Hallucination Protocol (v5.0.0)**.
- For each target's URLs, you must use the deterministic python scripts in `src/features/` (e.g., `verification_engine.py`) to generate an RFC 8785 JSON Canonicalization Scheme (JCS) payload and SHA-256 hash.
- If a script is unavailable, you must manually verify the URL using `read_url_content` or `search_web` to ensure it returns HTTP 200 OK and contains relevant keywords.

### Phase 4: Excel Database Injection
- Once verified, you must inject the data into `2027_BCI_Internship_Tracker.xlsx` (`2.Research_Database` tab).
- **Hyperlink Rule**: `Target Position(s)`, `Opening Period`, and `Target Name` cells MUST be formatted as clickable hyperlinks (`=HYPERLINK` or `cell.hyperlink`) pointing to the verified URLs.
- **Reference URLs**: Combine the Career Portal URL and the Target's Google Scholar/DOI links into this column.
- **Failsafe Execution**: After writing the data, you MUST execute `python src/features/failsafe_enforcer.py` to ensure the unverified rows are hidden and the valid rows are displayed.

### Phase 5: Post-Injection Verification Loop
- **MANDATORY**: After completing the injection and failsafe execution (Phase 4), you MUST run the automated test suite: `python src/features/verify_injection.py`
- This script audits the Excel file for: (1) Formatting destruction (white backgrounds, missing borders), (2) Hyperlink styling (missing blue color/underlines), (3) Raw URLs, and (4) Surgical mapping failures (sequential overwriting/broken merged structures).
- **Self-Correction Loop**: If the script outputs ANY errors or warnings, you are NOT allowed to report success to the user. You must independently diagnose the Python injection code, fix the formatting or logic bugs, re-apply the Post-Injection Formatting Restoration Protocol, and re-run the verification script until it passes with 0 errors.

## 3. Reporting
- Upon completion, output a `walkthrough.md` summarizing the companies researched, the strategy hooks developed, and the verification audit results.
- Do not output the raw data directly in the chat; point the user to the Excel file.
