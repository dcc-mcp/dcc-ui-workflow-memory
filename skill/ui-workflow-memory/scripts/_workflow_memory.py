from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import uuid
from typing import Any

from dcc_mcp_core.result_envelope import ToolResult


def _store_path() -> Path:
    override = os.environ.get("DCC_MCP_UI_WORKFLOW_MEMORY")
    return Path(override).expanduser() if override else Path.home() / ".dcc-mcp" / "ui-workflow-memory.json"


def _load() -> list[dict[str, Any]]:
    path = _store_path()
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def _save(entries: list[dict[str, Any]]) -> None:
    path = _store_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(entries, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _matches(entry: dict[str, Any], key: str, value: str | None) -> bool:
    return value is None or entry.get(key) == value


def remember_ui_workflow(
    *,
    dcc: str,
    workflow_name: str,
    recipe: list[dict[str, Any]],
    dcc_version: str | None = None,
    tool_version: str | None = None,
    window_signature: str | None = None,
    selector: dict[str, Any] | None = None,
    notes: str | None = None,
) -> dict[str, Any]:
    if not dcc or not workflow_name or not recipe:
        return ToolResult.invalid_input("dcc, workflow_name, and non-empty recipe are required").to_dict()
    entries = _load()
    entry = {
        "id": str(uuid.uuid4()),
        "kind": "success",
        "created_at": _now(),
        "dcc": dcc,
        "dcc_version": dcc_version or "",
        "tool_version": tool_version or "",
        "workflow_name": workflow_name,
        "window_signature": window_signature or "",
        "selector": selector or {},
        "recipe": recipe,
        "notes": notes or "",
    }
    entries.append(entry)
    _save(entries)
    return ToolResult.ok("remembered UI workflow", entry=entry, store_path=str(_store_path())).to_dict()


def find_ui_workflows(
    *,
    dcc: str,
    workflow_name: str | None = None,
    dcc_version: str | None = None,
    tool_version: str | None = None,
    include_failures: bool = True,
    limit: int = 10,
) -> dict[str, Any]:
    cap = max(1, min(int(limit), 100))
    hits = []
    for entry in reversed(_load()):
        if entry.get("dcc") != dcc:
            continue
        if not include_failures and entry.get("kind") == "failure":
            continue
        if not _matches(entry, "workflow_name", workflow_name):
            continue
        if not _matches(entry, "dcc_version", dcc_version):
            continue
        if not _matches(entry, "tool_version", tool_version):
            continue
        hits.append(entry)
        if len(hits) >= cap:
            break
    return ToolResult.ok("found UI workflow memories", entries=hits, count=len(hits), store_path=str(_store_path())).to_dict()


def record_ui_workflow_failure(
    *,
    dcc: str,
    workflow_name: str,
    reason: str,
    dcc_version: str | None = None,
    tool_version: str | None = None,
    window_signature: str | None = None,
    selector: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if not dcc or not workflow_name or not reason:
        return ToolResult.invalid_input("dcc, workflow_name, and reason are required").to_dict()
    entries = _load()
    entry = {
        "id": str(uuid.uuid4()),
        "kind": "failure",
        "created_at": _now(),
        "dcc": dcc,
        "dcc_version": dcc_version or "",
        "tool_version": tool_version or "",
        "workflow_name": workflow_name,
        "window_signature": window_signature or "",
        "selector": selector or {},
        "reason": reason,
    }
    entries.append(entry)
    _save(entries)
    return ToolResult.ok("recorded UI workflow failure", entry=entry, store_path=str(_store_path())).to_dict()


def run_cli(fn: Any) -> None:
    import sys

    try:
        params = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else {}
    except ValueError:
        params = {}
    sys.stdout.write(json.dumps(fn(**params)) + "\n")
