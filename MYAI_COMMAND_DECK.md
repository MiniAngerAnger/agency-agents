# MYAI Command Deck Integration

## Conclusion

This fork treats `agency-agents` as a complete MYAI industry role catalog.
All 169 agents remain available, but they are not autonomous MYAI team members.

The MYAI execution boundary is:

```text
MOODY request
  -> Codex App controller
  -> MYAI Task Contract
  -> real CLI slot
  -> selected Agency role profile
  -> verification
  -> non-author QA
  -> closeout
```

## What Changed

- Added `myai/agent_catalog.json` with all 169 role profiles.
- Added `myai/agent_catalog.md` for human review.
- Added `myai/project_startup_contract.md` for per-project adaptation.
- Added `myai/routing_policy.md` to preserve MYAI Command Deck boundaries.
- Added `scripts/myai_catalog.py` to regenerate and verify the catalog.

## Operating Rule

Agency roles are domain and workflow profiles. They can shape how a real CLI
slot thinks about a project, but they cannot:

- replace `Codex App`,
- dispatch work,
- bypass Task Contract checks,
- bypass `instruction_id / source_prompt_hash / idempotency_verdict`,
- bypass real verification and non-author QA,
- report themselves as real `Codex CLI / Claude CLI / Cursor / Kimi / Qwen /
  Gemini` workers.

Do not run the upstream global installer against production tool directories
during MYAI catalog research. Use the generated `myai/agent_catalog.json` and a
project startup contract first.

## Project Startup Flow

1. Read the target project docs and determine phase.
2. Select role profiles from `myai/agent_catalog.json`.
3. Bind each selected role to a named real CLI slot.
4. Produce a MYAI Task Contract.
5. Run idempotency check before execution.
6. Execute in a project worktree.
7. Verify with real commands.
8. Run non-author QA.
9. Close out through MYAI Command Deck gates.

## Verification

```bash
python3 scripts/myai_catalog.py --check \
  --out-json myai/agent_catalog.json \
  --out-md myai/agent_catalog.md
python3 -m py_compile scripts/myai_catalog.py
```
