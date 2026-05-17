# MYAI Routing Policy

## Hard Boundary

Agency agents are role profiles. They are not MYAI execution members.

Allowed:

- Use an Agency role to shape a prompt for `codex`, `claude`, `cursor-agent`,
  `kimi`, `qwen`, or `gemini`.
- Use a role as an industry specialist during Research / PRD / SPEC.
- Use testing roles to structure non-author QA.
- Use engineering roles to specialize a named implementation slot.

Forbidden:

- Do not let `Agents Orchestrator` replace `Codex App`.
- Do not spawn internal pseudo-members and report them as real CLI workers.
- Do not install the full catalog globally into production tools without a
  project startup contract.
- Do not run `scripts/install.sh --tool all` against real production tool
  directories during catalog research.
- Do not bypass MYAI `Task Contract`, `instruction_id`, `source_prompt_hash`,
  `idempotency_verdict`, or closeout gates.

## Recommended Mapping

- Research-heavy roles: `gemini-cli` or `claude-cli`
- Architecture and PRD roles: `claude-cli`, then `codex-cli`
- Implementation roles: `codex-cli`, `claude-cli`, `cursor-cli`, `kimi-code-cli`
- Long checklist execution: `kimi-code-cli`
- Low-risk QA fallback: `qwen`
- Non-author QA: `cursor-cli`, `gemini-cli`, or `qwen`
