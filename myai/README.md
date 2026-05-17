# MYAI Command Deck Adapter

This directory makes `agency-agents` usable as a MYAI AI CODER project-role
catalog.

It does not turn the 169 Agency agents into real MYAI team members. Real work
still routes through MYAI Command Deck:

```text
Codex App controller
  -> Task Contract
  -> named real CLI slot
  -> project-scoped role profile from this catalog
  -> verification
  -> non-author QA
  -> closeout
```

## Files

- `agent_catalog.json`: full generated inventory for all 169 project roles.
- `agent_catalog.md`: human-readable generated inventory.
- `project_startup_contract.md`: project kickoff template for selecting and
  adapting roles per industry project.
- `routing_policy.md`: rules that prevent role profiles from bypassing MYAI
  Command Deck governance.
- `pilots/`: read-only startup pilot outputs against real MYAI projects.

Regenerate the catalog:

```bash
python3 scripts/myai_catalog.py --check \
  --out-json myai/agent_catalog.json \
  --out-md myai/agent_catalog.md
```

Run a read-only project startup pilot:

```bash
python3 scripts/myai_project_startup.py \
  --catalog myai/agent_catalog.json \
  --project-root /Users/moody/Downloads/MYAI/PROJECTS/MUSIC_FILM_DIRECTOR \
  --project-id MUSIC_FILM_DIRECTOR \
  --out-json myai/pilots/music_film_director/startup_pack.json \
  --out-md myai/pilots/music_film_director/startup_pack.md
```
