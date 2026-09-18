# Original User Request

## Initial Request — 2026-08-06T16:31:19Z

Design a zero-hallucination methodology and protocol for extracting and verifying URLs and emails for an Excel research database, through a rigorous 10-round multi-agent debate.

Working directory: ~/teamwork_projects/zero_hallucination_protocol
Integrity mode: exploration

## Requirements

### R1. Multi-Round Red-Teaming Debate
Conduct a rigorous, multi-agent debate consisting of at least 10 distinct rounds. Agents must aggressively challenge each other's proposed verification methods to find loopholes, hallucinations, and edge cases in URL and email extraction.

### R2. Comprehensive Verification Protocol
Deliver a final "Zero-Hallucination Protocol" document. It must specify exact programmatic or deterministic verification steps (e.g., HTTP status code checking for URLs, SMTP/MX record validation for emails, cross-referencing LinkedIn vs Lab directories).

### R3. Component Coverage
The protocol must explicitly cover all Excel components: Company Career Portals, Personnel Profile URLs, Personnel Emails, and recent publication URLs.

## Acceptance Criteria

### Objective Verification
- [ ] A final Markdown report is produced containing a summary of the 10-round debate and the finalized verification protocol.
- [ ] The protocol explicitly requires objective, non-LLM-based checks (e.g. HTTP 200 OK, valid MX records) for every URL and email.
- [ ] The protocol contains zero assumptions that an LLM can "guess" an email format without external validation.
