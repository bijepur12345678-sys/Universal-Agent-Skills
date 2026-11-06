# Defensive Security & Software Analysis

## Trigger
Use for secure code review, dependency audits, static analysis, defensive threat modeling, and authorized analysis of owned or permitted software.

## Workflow
1. Establish written scope, ownership/authorization, environment, and prohibited actions.
2. Prefer passive source review, dependency metadata, and safe static analysis.
3. Map assets, trust boundaries, sensitive data, and likely threat scenarios.
4. Use defensive scanners and document their versions, scope, and false-positive limits.
5. Validate findings non-destructively in a controlled environment.
6. Prioritize by impact, exposure, exploitability, and confidence; separate facts from hypotheses.
7. Recommend mitigations, secure defaults, tests, and patch verification.
8. Report scope, evidence, severity rationale, remediation, and residual risk.

Do not test systems without authorization or provide intrusion, persistence, evasion, or credential-theft instructions.
