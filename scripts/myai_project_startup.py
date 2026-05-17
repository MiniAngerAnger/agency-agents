#!/usr/bin/env python3
"""Generate a MYAI project startup pack from an Agency role catalog."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


DEFAULT_DOCS = [
    "README.md",
    "docs/00_PROJECT_OVERVIEW.md",
    "docs/03_PRD.md",
    "docs/04_SPEC.md",
    "docs/05_TASKS.md",
    "docs/06_ACCEPTANCE.md",
]

CORE_ROLE_IDS = [
    "product-manager",
    "ux-architect",
    "software-architect",
    "codebase-onboarding-engineer",
    "technical-writer",
    "code-reviewer",
    "evidence-collector",
    "reality-checker",
    "test-results-analyzer",
]

KEYWORD_ROLE_RULES = [
    (("music", "song", "lyric", "story", "film", "director", "animation"), ["narratologist", "visual-storyteller", "image-prompt-engineer", "content-creator"]),
    (("douyin", "tiktok", "short-video", "video", "content"), ["douyin-strategist", "short-video-editing-coach", "video-optimization-specialist"]),
    (("copyright", "rights", "license", "risk", "ip", "肖像", "版权", "完整歌词"), ["legal-compliance-checker", "security-engineer"]),
    (("json", "schema", "fixture", "export", "cli", "local-first"), ["backend-architect", "data-engineer", "devops-automator"]),
    (("ui", "workbench", "html", "form", "preview"), ["frontend-developer", "ui-designer", "accessibility-auditor"]),
    (("culture", "period", "background", "visual lexicon", "年代", "文化"), ["cultural-intelligence-strategist", "historian", "anthropologist"]),
]

CLI_SLOT_ORDER = {
    "gemini-cli": "GeminiQA-1",
    "claude-cli": "ClaudeCLI-1",
    "codex-cli": "CodexCLI-1",
    "cursor-cli": "CursorQA-1",
    "kimi-code-cli": "KimiCLI-1",
    "qwen": "QwenQA-1",
}


def load_project_text(project_root: Path) -> tuple[str, list[str]]:
    chunks: list[str] = []
    docs_read: list[str] = []
    for rel in DEFAULT_DOCS:
        path = project_root / rel
        if path.is_file():
            docs_read.append(rel)
            chunks.append(path.read_text(encoding="utf-8", errors="ignore"))
    return "\n\n".join(chunks), docs_read


def load_catalog(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def select_role_ids(project_text: str) -> list[str]:
    normalized = project_text.lower()
    selected = list(CORE_ROLE_IDS)
    for keywords, role_ids in KEYWORD_ROLE_RULES:
        if any(keyword.lower() in normalized for keyword in keywords):
            for role_id in role_ids:
                if role_id not in selected:
                    selected.append(role_id)
    return selected


def role_map(catalog: dict[str, object]) -> dict[str, dict[str, object]]:
    agents = catalog.get("agents", [])
    if not isinstance(agents, list):
        return {}
    return {str(agent["id"]): agent for agent in agents if isinstance(agent, dict) and "id" in agent}


def bind_slot(agent: dict[str, object], index: int) -> dict[str, object]:
    recommended = agent.get("recommended_cli_slots")
    cli = "claude-cli"
    if isinstance(recommended, list) and recommended:
        cli = str(recommended[0])
    slot_prefix = CLI_SLOT_ORDER.get(cli, f"{cli}-slot")
    return {
        "slot_id": f"{slot_prefix}-{index:02d}",
        "owner": cli,
        "cli": cli,
        "role_profile_id": agent["id"],
        "role_profile_name": agent["name"],
        "task_id": "PROJECT-STARTUP-ROLE-MAPPING",
        "worktree": "<project worktree required before execution>",
        "branch": "<project branch required before execution>",
        "files_or_modules": "project docs, task contract, and scoped implementation files only",
        "reviewer": "non-author CLI slot required",
        "acceptance_commands": [
            "project-specific tests from docs/06_ACCEPTANCE.md",
            "git diff --check",
        ],
        "expected_duration": "30-90m depending on project phase",
        "first_check_after": "10m",
        "max_silent_grace": "30m",
        "stop_conditions": [
            "scope change",
            "missing credentials or provider blocker",
            "protected rule file edit required",
            "copyright/IP/legal uncertainty needs MOODY decision",
        ],
    }


def build_startup_pack(catalog: dict[str, object], project_root: Path, project_id: str) -> dict[str, object]:
    project_text, docs_read = load_project_text(project_root)
    agents_by_id = role_map(catalog)
    selected_ids = select_role_ids(project_text)
    selected_agents = [agents_by_id[role_id] for role_id in selected_ids if role_id in agents_by_id]
    missing_ids = [role_id for role_id in selected_ids if role_id not in agents_by_id]
    prompt_hash = hashlib.sha256(project_text.encode("utf-8")).hexdigest()

    return {
        "project_id": project_id,
        "project_root": str(project_root),
        "phase": "Execution/QA pilot",
        "source_prompt_hash": prompt_hash,
        "docs_read": docs_read,
        "catalog_name": catalog.get("catalog_name"),
        "catalog_source_commit": catalog.get("source_commit"),
        "normalized_goal": "Test MYAI Agency role catalog selection against a real industry project without editing the project.",
        "allowed_scope": [
            "read project docs",
            "select role profiles",
            "bind selected roles to real CLI slot templates",
            "produce startup mapping and QA notes",
        ],
        "forbidden_scope": [
            "do not edit the target project",
            "do not run global agency-agents install.sh",
            "do not treat role profiles as real CLI workers",
            "do not bypass MYAI Task Contract, QA, or closeout",
        ],
        "selected_role_count": len(selected_agents),
        "selected_roles": selected_agents,
        "missing_role_ids": missing_ids,
        "role_to_slot_mapping": [bind_slot(agent, index + 1) for index, agent in enumerate(selected_agents)],
        "qa_owner": "GeminiQA-1 or CursorQA-1",
        "verification_commands": [
            "python3 scripts/myai_project_startup.py --catalog myai/agent_catalog.json --project-root <project> --project-id <id> --out-json <out.json> --out-md <out.md>",
            "python3 -m json.tool <out.json>",
        ],
    }


def write_markdown(pack: dict[str, object]) -> str:
    lines = [
        f"# MYAI Agency Startup Pilot: {pack['project_id']}",
        "",
        f"- Project root: `{pack['project_root']}`",
        f"- Phase: `{pack['phase']}`",
        f"- Source prompt hash: `{pack['source_prompt_hash']}`",
        f"- Selected roles: `{pack['selected_role_count']}`",
        "",
        "## Docs Read",
        "",
    ]
    for doc in pack["docs_read"]:
        lines.append(f"- `{doc}`")

    lines.extend(["", "## Boundary", ""])
    lines.append("Allowed scope:")
    for item in pack["allowed_scope"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Forbidden scope:")
    for item in pack["forbidden_scope"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Selected Roles", ""])
    for role in pack["selected_roles"]:
        lines.append(f"- `{role['id']}` · {role['name']} · `{role['category']}` · `{role['command_deck_status']}`")

    lines.extend(["", "## Role To Slot Mapping", ""])
    for slot in pack["role_to_slot_mapping"]:
        lines.append(f"- `{slot['slot_id']}` -> `{slot['role_profile_id']}` via `{slot['cli']}`")

    lines.extend(["", "## QA", ""])
    lines.append(f"- Owner: `{pack['qa_owner']}`")
    lines.append("- This pilot is read-only against the target project.")
    lines.append("- Any real implementation must open a project worktree and generate a fresh MYAI Task Contract.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    parser.add_argument("--out-md", type=Path, required=True)
    args = parser.parse_args()

    catalog = load_catalog(args.catalog)
    pack = build_startup_pack(catalog, args.project_root, args.project_id)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(pack, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.write_text(write_markdown(pack), encoding="utf-8")
    print(f"selected_role_count={pack['selected_role_count']}")
    print(f"docs_read={len(pack['docs_read'])}")
    print(f"out_json={args.out_json}")
    print(f"out_md={args.out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
