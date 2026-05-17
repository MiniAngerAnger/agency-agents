# MYAI Agency Startup Pilot: MUSIC_FILM_DIRECTOR

- Project root: `/Users/moody/Downloads/MYAI/PROJECTS/MUSIC_FILM_DIRECTOR`
- Phase: `Execution/QA pilot`
- Source prompt hash: `4640188f7c09b304b0f7c687b801c904d7adaff686d3935af9e9ecee9863cd1f`
- Selected roles: `27`

## Docs Read

- `README.md`
- `docs/00_PROJECT_OVERVIEW.md`
- `docs/03_PRD.md`
- `docs/04_SPEC.md`
- `docs/05_TASKS.md`
- `docs/06_ACCEPTANCE.md`

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
- `narratologist` · Narratologist · `academic` · `available-as-project-role`
- `visual-storyteller` · Visual Storyteller · `design` · `available-as-project-role`
- `image-prompt-engineer` · Image Prompt Engineer · `design` · `available-as-project-role`
- `content-creator` · Content Creator · `marketing` · `available-as-project-role`
- `douyin-strategist` · Douyin Strategist · `marketing` · `available-as-project-role`
- `short-video-editing-coach` · Short-Video Editing Coach · `marketing` · `available-as-project-role`
- `video-optimization-specialist` · Video Optimization Specialist · `marketing` · `available-as-project-role`
- `legal-compliance-checker` · Legal Compliance Checker · `support` · `available-as-project-role`
- `security-engineer` · Security Engineer · `engineering` · `available-as-project-role`
- `backend-architect` · Backend Architect · `engineering` · `available-as-project-role`
- `data-engineer` · Data Engineer · `engineering` · `available-as-project-role`
- `devops-automator` · DevOps Automator · `engineering` · `available-as-project-role`
- `frontend-developer` · Frontend Developer · `engineering` · `available-as-project-role`
- `ui-designer` · UI Designer · `design` · `available-as-project-role`
- `accessibility-auditor` · Accessibility Auditor · `testing` · `qa-role-profile`
- `cultural-intelligence-strategist` · Cultural Intelligence Strategist · `specialized` · `available-as-project-role`
- `historian` · Historian · `academic` · `available-as-project-role`
- `anthropologist` · Anthropologist · `academic` · `available-as-project-role`

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
- `GeminiQA-1-10` -> `narratologist` via `gemini-cli`
- `ClaudeCLI-1-11` -> `visual-storyteller` via `claude-cli`
- `ClaudeCLI-1-12` -> `image-prompt-engineer` via `claude-cli`
- `GeminiQA-1-13` -> `content-creator` via `gemini-cli`
- `GeminiQA-1-14` -> `douyin-strategist` via `gemini-cli`
- `GeminiQA-1-15` -> `short-video-editing-coach` via `gemini-cli`
- `GeminiQA-1-16` -> `video-optimization-specialist` via `gemini-cli`
- `QwenQA-1-17` -> `legal-compliance-checker` via `qwen`
- `CodexCLI-1-18` -> `security-engineer` via `codex-cli`
- `CodexCLI-1-19` -> `backend-architect` via `codex-cli`
- `CodexCLI-1-20` -> `data-engineer` via `codex-cli`
- `CodexCLI-1-21` -> `devops-automator` via `codex-cli`
- `CodexCLI-1-22` -> `frontend-developer` via `codex-cli`
- `ClaudeCLI-1-23` -> `ui-designer` via `claude-cli`
- `CursorQA-1-24` -> `accessibility-auditor` via `cursor-cli`
- `ClaudeCLI-1-25` -> `cultural-intelligence-strategist` via `claude-cli`
- `GeminiQA-1-26` -> `historian` via `gemini-cli`
- `GeminiQA-1-27` -> `anthropologist` via `gemini-cli`

## QA

- Owner: `GeminiQA-1 or CursorQA-1`
- This pilot is read-only against the target project.
- Any real implementation must open a project worktree and generate a fresh MYAI Task Contract.
