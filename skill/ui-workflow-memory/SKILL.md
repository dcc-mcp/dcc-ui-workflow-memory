---
name: ui-workflow-memory
description: Store and retrieve verified selectors, recipes, and failures for DCC-MCP CUA, UI Control, and dcc-cua automation.
license: MIT
compatibility: "dcc-mcp-core 0.20+"
metadata:
  dcc-mcp:
    version: v0.1.0
    dcc: python
    layer: infrastructure
    tags:
      - ui
      - workflow
      - memory
      - selectors
      - automation
    search-hint: "CUA, UI Control, dcc-cua, ui workflow memory, remember selector, workflow recipe, failed selector, UI automation memory"
    tools: tools.yaml
---

# UI Workflow Memory

Use this skill to persist verified selector chains, UI recipes, and failures.
Memory is advisory: workflow tools must still verify their final result.

For core 0.20, record current `ui_control__snapshot`, `ui_control__find`, and
single-step `ui_control__act` outcomes produced by dcc-cua 0.4. Do not store or
replay removed `app_ui__*` calls.
