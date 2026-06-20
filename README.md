# DCC-MCP UI Workflow Memory

Structured workflow memory for DCC-MCP UI automation.

Use this skill to remember selector chains, workflow recipes, and verified
failures for legacy UI tools. It stores local JSON by default and is meant to
make repeated UI automation less exploratory over time.

## Install

```bash
dcc-mcp-cli marketplace add dcc-mcp/dcc-ui-workflow-memory
dcc-mcp-cli marketplace install dcc-ui-workflow-memory
```

## Tools

- `remember_ui_workflow`
- `find_ui_workflows`
- `record_ui_workflow_failure`

Set `DCC_MCP_UI_WORKFLOW_MEMORY` to override the default store path.
