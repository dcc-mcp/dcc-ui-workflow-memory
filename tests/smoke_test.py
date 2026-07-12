from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "ui-workflow-memory"
SCRIPTS = SKILL / "scripts"


def load(name: str):
    sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def validate_skill() -> None:
    from dcc_mcp_core import validate_skill

    report = validate_skill(str(SKILL))
    assert not report.has_errors, report


def memory_round_trip() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["DCC_MCP_UI_WORKFLOW_MEMORY"] = str(Path(tmp) / "memory.json")
        mod = load("_workflow_memory")
        result = mod.remember_ui_workflow(
            dcc="maya",
            dcc_version="2025",
            workflow_name="legacy_export",
            selector={"object_name": "ExportButton"},
            recipe=[{"tool": "click_widget", "object_name": "ExportButton"}],
        )
        assert result["success"], result
        found = mod.find_ui_workflows(dcc="maya", workflow_name="legacy_export")
        assert found["context"]["count"] == 1, found
        failed = mod.record_ui_workflow_failure(dcc="maya", workflow_name="legacy_export", reason="button renamed")
        assert failed["success"], failed


def wrapper_contract() -> None:
    for name in ("find_ui_workflows", "record_ui_workflow_failure", "remember_ui_workflow"):
        assert callable(load(name).main), f"{name}.py must expose main"


def main() -> None:
    validate_skill()
    memory_round_trip()
    wrapper_contract()


if __name__ == "__main__":
    main()
