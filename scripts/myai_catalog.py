#!/usr/bin/env python3
"""Build a MYAI Command Deck catalog from Agency agent Markdown files.

The catalog treats Agency agents as project-scoped role profiles, not as real
MYAI executor members. Real execution remains owned by Codex App and the CLI
slots defined in MYAI Command Deck.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


AGENT_DIRS = [
    "academic",
    "design",
    "engineering",
    "finance",
    "game-development",
    "marketing",
    "paid-media",
    "product",
    "project-management",
    "sales",
    "spatial-computing",
    "specialized",
    "support",
    "testing",
]

CATEGORY_PHASES = {
    "academic": ["Research", "PRD", "SPEC"],
    "design": ["Research", "PRD", "SPEC", "Execution", "QA"],
    "engineering": ["SPEC", "TASKS", "Execution", "QA"],
    "finance": ["Research", "PRD", "SPEC", "QA"],
    "game-development": ["Research", "PRD", "SPEC", "Execution", "QA"],
    "marketing": ["Research", "PRD", "SPEC", "Execution", "QA"],
    "paid-media": ["Research", "PRD", "SPEC", "Execution", "QA"],
    "product": ["Research", "PRD", "SPEC", "TASKS"],
    "project-management": ["PRD", "SPEC", "TASKS", "Acceptance"],
    "sales": ["Research", "PRD", "SPEC", "Execution"],
    "spatial-computing": ["Research", "SPEC", "Execution", "QA"],
    "specialized": ["Research", "PRD", "SPEC", "Execution", "QA"],
    "support": ["Research", "PRD", "SPEC", "Acceptance"],
    "testing": ["QA", "Acceptance"],
}

CATEGORY_LAYER = {
    "academic": "industry-domain-specialist",
    "design": "product-design-specialist",
    "engineering": "implementation-specialist",
    "finance": "industry-domain-specialist",
    "game-development": "industry-implementation-specialist",
    "marketing": "growth-domain-specialist",
    "paid-media": "growth-domain-specialist",
    "product": "product-planning-specialist",
    "project-management": "planning-support-specialist",
    "sales": "go-to-market-specialist",
    "spatial-computing": "industry-implementation-specialist",
    "specialized": "industry-domain-specialist",
    "support": "operations-support-specialist",
    "testing": "qa-specialist",
}

CATEGORY_CLI = {
    "academic": ["gemini-cli", "claude-cli"],
    "design": ["claude-cli", "codex-cli", "cursor-cli"],
    "engineering": ["codex-cli", "claude-cli", "cursor-cli", "kimi-code-cli"],
    "finance": ["gemini-cli", "claude-cli"],
    "game-development": ["claude-cli", "codex-cli", "kimi-code-cli"],
    "marketing": ["gemini-cli", "claude-cli", "qwen"],
    "paid-media": ["gemini-cli", "claude-cli", "qwen"],
    "product": ["claude-cli", "gemini-cli", "codex-cli"],
    "project-management": ["codex-app-controller", "claude-cli"],
    "sales": ["gemini-cli", "claude-cli", "qwen"],
    "spatial-computing": ["claude-cli", "codex-cli", "kimi-code-cli"],
    "specialized": ["claude-cli", "codex-cli", "gemini-cli", "qwen"],
    "support": ["qwen", "cursor-cli", "gemini-cli"],
    "testing": ["cursor-cli", "gemini-cli", "qwen"],
}

CONTROLLER_BLOCKLIST = {
    "Agents Orchestrator": "reference-only: cannot replace Codex App or create internal pseudo-team members",
    "Studio Producer": "planning-support-only: cannot become MYAI controller",
    "Project Shepherd": "planning-support-only: cannot become MYAI controller",
    "Studio Operations": "operations-support-only: cannot own dispatch",
}


def slugify(value: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", value.lower())).strip("-")


def read_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return {}, path.read_text(encoding="utf-8")

    frontmatter: dict[str, str] = {}
    body_start = 0
    for idx, line in enumerate(lines[1:], start=1):
        if line == "---":
            body_start = idx + 1
            break
        if ":" in line:
            key, value = line.split(":", 1)
            frontmatter[key.strip()] = value.strip().strip('"')

    return frontmatter, "\n".join(lines[body_start:])


def agent_record(repo_root: Path, path: Path) -> dict[str, object] | None:
    frontmatter, body = read_frontmatter(path)
    name = frontmatter.get("name")
    if not name:
        return None

    category = path.relative_to(repo_root).parts[0]
    phases = CATEGORY_PHASES.get(category, ["Research"])
    recommended_cli = CATEGORY_CLI.get(category, ["claude-cli"])
    layer = CATEGORY_LAYER.get(category, "industry-domain-specialist")
    command_deck_status = "available-as-project-role"
    governance_note = "Use through a MYAI Task Contract; never as an autonomous executor identity."

    if name in CONTROLLER_BLOCKLIST:
        command_deck_status = "reference-only"
        governance_note = CONTROLLER_BLOCKLIST[name]
    elif category == "testing":
        command_deck_status = "qa-role-profile"
        governance_note = "Can guide non-author QA, but real QA ownership stays with a named CLI slot."
    elif category == "project-management":
        command_deck_status = "planning-support-role"
        governance_note = "Can shape task cards and acceptance notes, but cannot dispatch real CLI slots."

    return {
        "id": slugify(name),
        "name": name,
        "category": category,
        "source_path": str(path.relative_to(repo_root)),
        "description": frontmatter.get("description", ""),
        "layer": layer,
        "allowed_phases": phases,
        "recommended_cli_slots": recommended_cli,
        "command_deck_status": command_deck_status,
        "governance_note": governance_note,
        "body_word_count": len(body.split()),
    }


def build_catalog(repo_root: Path) -> dict[str, object]:
    agents: list[dict[str, object]] = []
    for dirname in AGENT_DIRS:
        for path in sorted((repo_root / dirname).glob("*.md")):
            record = agent_record(repo_root, path)
            if record:
                agents.append(record)

    categories: dict[str, int] = {}
    statuses: dict[str, int] = {}
    for agent in agents:
        categories[agent["category"]] = categories.get(agent["category"], 0) + 1
        statuses[agent["command_deck_status"]] = statuses.get(agent["command_deck_status"], 0) + 1

    return {
        "catalog_name": "agency-agents-myai-command-deck-catalog",
        "catalog_version": "2026-05-17",
        "source_repo": "https://github.com/msitarzewski/agency-agents",
        "source_commit": source_commit(repo_root),
        "myai_integration_rule": "Agency agents are project role profiles. Real execution must route through MYAI Command Deck Task Contracts and named CLI slots.",
        "agent_count": len(agents),
        "category_counts": dict(sorted(categories.items())),
        "status_counts": dict(sorted(statuses.items())),
        "agents": agents,
    }


def source_commit(repo_root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"
    return result.stdout.strip()


def validate_catalog(catalog: dict[str, object], repo_root: Path) -> list[str]:
    errors: list[str] = []
    agents = catalog.get("agents")
    if not isinstance(agents, list):
        return ["catalog.agents must be a list"]

    ids = [agent.get("id") for agent in agents if isinstance(agent, dict)]
    duplicate_ids = sorted({agent_id for agent_id in ids if ids.count(agent_id) > 1})
    for agent_id in duplicate_ids:
        errors.append(f"duplicate agent id: {agent_id}")

    for agent in agents:
        if not isinstance(agent, dict):
            errors.append("agent entry is not an object")
            continue
        source_path = agent.get("source_path")
        if not isinstance(source_path, str) or not (repo_root / source_path).is_file():
            errors.append(f"missing source_path: {source_path}")
        if agent.get("name") in CONTROLLER_BLOCKLIST and agent.get("command_deck_status") != "reference-only":
            errors.append(f"controller-like role is not reference-only: {agent.get('name')}")
        if agent.get("category") == "testing" and agent.get("command_deck_status") != "qa-role-profile":
            errors.append(f"testing role is not qa-role-profile: {agent.get('name')}")

    expected_statuses = {"available-as-project-role", "planning-support-role", "qa-role-profile", "reference-only"}
    seen_statuses = {agent.get("command_deck_status") for agent in agents if isinstance(agent, dict)}
    unknown_statuses = sorted(str(status) for status in seen_statuses - expected_statuses)
    for status in unknown_statuses:
        errors.append(f"unknown command_deck_status: {status}")

    return errors


def write_markdown(catalog: dict[str, object]) -> str:
    lines = [
        "# MYAI Command Deck Agent Catalog",
        "",
        f"- Source: {catalog['source_repo']}",
        f"- Source commit: `{catalog['source_commit']}`",
        f"- Agent count: `{catalog['agent_count']}`",
        "",
        "## Rule",
        "",
        str(catalog["myai_integration_rule"]),
        "",
        "## Category Counts",
        "",
    ]
    for category, count in catalog["category_counts"].items():
        lines.append(f"- `{category}`: {count}")

    lines.extend(["", "## Agents", ""])
    agents = catalog["agents"]
    assert isinstance(agents, list)
    for item in agents:
        lines.append(
            f"- `{item['id']}` · {item['name']} · `{item['category']}` · "
            f"`{item['command_deck_status']}` · phases: {', '.join(item['allowed_phases'])}"
        )

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out-json", type=Path)
    parser.add_argument("--out-md", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    catalog = build_catalog(args.repo)
    if args.check:
        errors = validate_catalog(catalog, args.repo)
        if catalog["agent_count"] != 169:
            errors.append(f"expected 169 agents, found {catalog['agent_count']}")
        if errors:
            raise SystemExit("\n".join(errors))

    if args.out_json:
        args.out_json.parent.mkdir(parents=True, exist_ok=True)
        args.out_json.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if args.out_md:
        args.out_md.parent.mkdir(parents=True, exist_ok=True)
        args.out_md.write_text(write_markdown(catalog), encoding="utf-8")

    if not args.out_json and not args.out_md:
        print(json.dumps(catalog, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
