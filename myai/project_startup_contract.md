# MYAI Project Startup Contract

Use this at the start of each industry project that wants to use the 169 Agency
role profiles.

## Required Inputs

- `project_id`:
- `industry`:
- `phase`: Research / PRD / SPEC / TASKS / Execution / QA / Acceptance
- `normalized_goal`:
- `allowed_scope`:
- `forbidden_scope`:
- `expected_outputs`:
- `verification_commands`:
- `stop_conditions`:

## Role Selection

Select roles from `myai/agent_catalog.json`.

Rules:

- Keep all 169 roles available in the catalog.
- Activate only the roles needed for the current project phase.
- A role profile can advise a real CLI slot; it cannot become a real executor.
- `Agents Orchestrator` is reference-only and cannot replace `Codex App`.
- QA roles guide review behavior; the reviewer must still be a named CLI slot.

## Slot Contract

Every active role must be bound to a real MYAI slot:

```yaml
slot_id:
owner:
cli:
role_profile_id:
task_id:
worktree:
branch:
files_or_modules:
reviewer:
acceptance_commands:
expected_duration:
first_check_after:
max_silent_grace:
stop_conditions:
```

## Startup Output

The project startup step must produce:

- selected role list
- role-to-slot mapping
- Task Contract
- verification commands
- QA owner
- explicit skipped roles with reason
