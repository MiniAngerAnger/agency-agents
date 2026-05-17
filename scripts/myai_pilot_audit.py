#!/usr/bin/env python3
"""Audit MYAI startup pilots for context-size and routing guardrails."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


MAX_SELECTED_ROLES = 40
REQUIRED_SLOT_FIELDS = {
    "slot_id",
    "owner",
    "cli",
    "role_profile_id",
    "task_id",
    "worktree",
    "branch",
    "files_or_modules",
    "reviewer",
    "acceptance_commands",
    "expected_duration",
    "first_check_after",
    "max_silent_grace",
    "stop_conditions",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def audit_pack(path: Path) -> tuple[dict[str, Any], list[str]]:
    pack = load_json(path)
    errors: list[str] = []
    selected_roles = pack.get("selected_roles")
    role_to_slot = pack.get("role_to_slot_mapping")
    missing_role_ids = pack.get("missing_role_ids")

    if not isinstance(selected_roles, list):
        errors.append("selected_roles must be a list")
        selected_roles = []
    if not isinstance(role_to_slot, list):
        errors.append("role_to_slot_mapping must be a list")
        role_to_slot = []
    if not isinstance(missing_role_ids, list):
        errors.append("missing_role_ids must be a list")
        missing_role_ids = []

    selected_role_count = len(selected_roles)
    if selected_role_count == 0:
        errors.append("selected role list is empty")
    if selected_role_count > MAX_SELECTED_ROLES:
        errors.append(f"selected role count exceeds {MAX_SELECTED_ROLES}: {selected_role_count}")
    if selected_role_count == 169:
        errors.append("startup pack injected the full 169-role catalog")
    if pack.get("selected_role_count") != selected_role_count:
        errors.append("selected_role_count does not match selected_roles length")
    if missing_role_ids:
        errors.append(f"missing role ids present: {missing_role_ids}")
    if len(role_to_slot) != selected_role_count:
        errors.append("role_to_slot_mapping length does not match selected_roles length")

    reference_roles = [
        role.get("id")
        for role in selected_roles
        if isinstance(role, dict) and role.get("command_deck_status") == "reference-only"
    ]
    if reference_roles:
        errors.append(f"reference-only roles selected: {reference_roles}")

    for index, slot in enumerate(role_to_slot, start=1):
        if not isinstance(slot, dict):
            errors.append(f"slot {index} is not an object")
            continue
        missing_fields = sorted(REQUIRED_SLOT_FIELDS - set(slot))
        if missing_fields:
            errors.append(f"slot {index} missing fields: {missing_fields}")

    summary = {
        "path": str(path),
        "project_id": pack.get("project_id"),
        "docs_read": len(pack.get("docs_read", [])) if isinstance(pack.get("docs_read"), list) else 0,
        "selected_role_count": selected_role_count,
        "role_to_slot_count": len(role_to_slot),
        "missing_role_ids": len(missing_role_ids),
        "reference_only_selected": len(reference_roles),
        "context_guard": "passed" if not errors else "failed",
    }
    return summary, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pilots-root", type=Path, default=Path("myai/pilots"))
    args = parser.parse_args()

    pack_paths = sorted(args.pilots_root.glob("*/startup_pack.json"))
    summaries: list[dict[str, Any]] = []
    all_errors: dict[str, list[str]] = {}
    for path in pack_paths:
        summary, errors = audit_pack(path)
        summaries.append(summary)
        if errors:
            all_errors[str(path)] = errors

    result = {
        "pilot_count": len(pack_paths),
        "max_selected_roles": MAX_SELECTED_ROLES,
        "passed": len(pack_paths) - len(all_errors),
        "failed": len(all_errors),
        "summaries": summaries,
        "errors": all_errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if all_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
