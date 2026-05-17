# MYAI Agency Startup Pilot: TRADING_LAB

- Project root: `/Users/moody/Downloads/MYAI/PROJECTS/TRADING_LAB`
- Phase: `Execution/QA pilot`
- Source prompt hash: `d17ac5f91ab3a86898a00558a3a2f443793b376023a088bc37bb9670b373bf1b`
- Selected roles: `14`

## Docs Read

- `README.md`

## Boundary

Allowed scope:
- read project docs
- select role profiles
- bind selected roles to real CLI slot templates
- produce startup mapping and QA notes

Forbidden scope:
- do not edit the target project
- do not run global agency-agents install.sh
- do not treat role profiles as real CLI workers
- do not bypass MYAI Task Contract, QA, or closeout

## Selected Roles

- `product-manager` · Product Manager · `product` · `available-as-project-role`
- `ux-architect` · UX Architect · `design` · `available-as-project-role`
- `software-architect` · Software Architect · `engineering` · `available-as-project-role`
- `codebase-onboarding-engineer` · Codebase Onboarding Engineer · `engineering` · `available-as-project-role`
- `technical-writer` · Technical Writer · `engineering` · `available-as-project-role`
- `code-reviewer` · Code Reviewer · `engineering` · `available-as-project-role`
- `evidence-collector` · Evidence Collector · `testing` · `qa-role-profile`
- `reality-checker` · Reality Checker · `testing` · `qa-role-profile`
- `test-results-analyzer` · Test Results Analyzer · `testing` · `qa-role-profile`
- `legal-compliance-checker` · Legal Compliance Checker · `support` · `available-as-project-role`
- `security-engineer` · Security Engineer · `engineering` · `available-as-project-role`
- `frontend-developer` · Frontend Developer · `engineering` · `available-as-project-role`
- `ui-designer` · UI Designer · `design` · `available-as-project-role`
- `accessibility-auditor` · Accessibility Auditor · `testing` · `qa-role-profile`

## Role To Slot Mapping

- `ClaudeCLI-1-01` -> `product-manager` via `claude-cli`
- `ClaudeCLI-1-02` -> `ux-architect` via `claude-cli`
- `CodexCLI-1-03` -> `software-architect` via `codex-cli`
- `CodexCLI-1-04` -> `codebase-onboarding-engineer` via `codex-cli`
- `CodexCLI-1-05` -> `technical-writer` via `codex-cli`
- `CodexCLI-1-06` -> `code-reviewer` via `codex-cli`
- `CursorQA-1-07` -> `evidence-collector` via `cursor-cli`
- `CursorQA-1-08` -> `reality-checker` via `cursor-cli`
- `CursorQA-1-09` -> `test-results-analyzer` via `cursor-cli`
- `QwenQA-1-10` -> `legal-compliance-checker` via `qwen`
- `CodexCLI-1-11` -> `security-engineer` via `codex-cli`
- `CodexCLI-1-12` -> `frontend-developer` via `codex-cli`
- `ClaudeCLI-1-13` -> `ui-designer` via `claude-cli`
- `CursorQA-1-14` -> `accessibility-auditor` via `cursor-cli`

## QA

- Owner: `GeminiQA-1 or CursorQA-1`
- This pilot is read-only against the target project.
- Any real implementation must open a project worktree and generate a fresh MYAI Task Contract.
