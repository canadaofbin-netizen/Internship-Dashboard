---
name: research
description: "Master skill for researching Global BCI, Neurotech, and Tech Companies, enforcing the Zero-Hallucination Protocol, and injecting verified data into the Internship Tracker."
command: research
---

# Instructions

When the user invokes `/research`, you must execute the end-to-end BCI & Tech internship research pipeline. This pipeline ensures that no hallucinated data enters the tracker and strictly aligns with the user's undergraduate background.

## 1. Undergraduate & Role Constraints ([AGENTS.md Compliance](file:///g:/My%20Drive/Kyubin_Yun_Workspace/04_Internship/AGENTS.md))
- **Target Persona**: UCL PALS Undergraduate Student with skills in Python EEG Data Pipelines, Web Scraping, and ML Optimization.
- **Target Roles**: Prioritize Data Science Intern, UX Researcher (UXR) Intern, and Machine Learning Intern.
- **Banned Roles**: Strictly avoid "Research Scientist" roles, as they require a PhD.
- **Strategy Hook Generation**: For every targeted PI or recruiter, draft a hook explaining how the user's practical EEG/ML pipeline skills can directly solve bottlenecks in their specific lab/wearable team.

## 2. Research Execution Pipeline
1. **Target Selection**: BCI Startups (Neuralink, Synchron, Precision Neuroscience) & Global Big Tech (Meta Reality Labs, Snap Lab, Apple Biosignals, DeepMind).
2. **Agent Deep Research**: Find official filtered careers portal URLs, estimated opening periods, and verified contacts.
3. **Zero-Hallucination Verification**: Must verify URLs with `read_url_content` or `search_web` to ensure HTTP 200 OK and relevancy.
4. **Excel Database Injection**: Inject data into `2027_BCI_Internship_Tracker.xlsx` or `Korea_Internship_Research_2026_2027.xlsx` with clean clickable hyperlinks.
