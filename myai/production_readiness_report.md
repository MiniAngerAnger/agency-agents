# MYAI Command Deck Adapter Production Readiness

## Verdict

`Command Deck Agency Catalog` is ready for Phase 1 production use as a role catalog and project-startup routing input.

It is still not a standalone autonomous execution team. Real execution remains owned by `Codex App -> MYAI Task Contract -> real CLI slot -> verification -> non-author QA`.

## Blockers Closed

### 1. Upstream lint was not clean

Previous state:

```text
16 error(s), 81 warning(s) in 200 files
```

Current state:

```text
0 error(s), 0 warning(s) in 200 files
```

Command:

```bash
./scripts/lint-agents.sh
```

### 2. `install.sh` could write user-wide tool directories

Current behavior:

- `--dry-run` shows selected tools and writes nothing.
- User-wide installs are blocked by default.
- User-wide installs require explicit `--allow-global-install`.

Verified examples:

```text
./scripts/install.sh --tool gemini-cli --dry-run --no-interactive -> exit 0, writes none
./scripts/install.sh --tool gemini-cli --no-interactive -> exit 2, refused user-wide install
./scripts/install.sh --tool cursor --dry-run --no-interactive -> exit 0, project-scoped, writes none
```

### 3. `Agents Orchestrator / NEXUS` could conflict with MYAI control

Current behavior:

- Catalog marks `Agents Orchestrator` as `reference-only`.
- `Agents Orchestrator` cannot replace `Codex App`.
- NEXUS strategy and runbooks include `MYAI Control Boundary`.
- Any pipeline-controller language must be translated into:

```text
Codex App controller -> MYAI Task Contract -> real CLI slot -> verification -> non-author QA
```

### 4. Only one pilot existed

Current pilot count: `4`.

| Project | Docs read | Selected roles | Missing roles |
|---|---:|---:|---:|
| `MUSIC_FILM_DIRECTOR` | 6 | 27 | 0 |
| `PDLM` | 6 | 24 | 0 |
| `FREELANCE_INCOME_TOOLKIT` | 1 | 17 | 0 |
| `TRADING_LAB` | 1 | 14 | 0 |

### 5. Role selection could pollute prompt context

Current audit:

```text
pilot_count: 4
passed: 4
failed: 0
max_selected_roles: 40
```

Guards checked:

- selected roles must be non-empty.
- selected roles must be <= 40.
- selected roles must not equal the full 169-role catalog.
- `missing_role_ids` must be empty.
- no `reference-only` roles can be selected.
- `role_to_slot_mapping` length must match selected roles.
- each slot must include required MYAI slot contract fields.

Command:

```bash
python3 scripts/myai_pilot_audit.py --pilots-root myai/pilots
```

## Production Scope

Allowed now:

- Use `myai/agent_catalog.json` as a Command Deck role catalog.
- Generate project startup packs before work begins.
- Use selected role profiles to specialize real CLI slots.
- Use `myai_pilot_audit.py` before promoting a pilot.

Still forbidden:

- Do not install all agents globally into production tools by default.
- Do not call the 169 role profiles a real execution team.
- Do not let `Agents Orchestrator / NEXUS` replace Codex App.
- Do not bypass MYAI Task Contract, idempotency, real verification, or non-author QA.
