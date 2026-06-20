---
name: ui-workflow-memory
description: Store and retrieve verified UI workflow selectors, recipes, and failures for DCC-MCP legacy UI automation.
license: MIT
compatibility: "dcc-mcp-core 0.18+"
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
    search-hint: "ui workflow memory, remember selector, workflow recipe, failed selector, legacy tool automation memory"
    tools: tools.yaml
---

# UI Workflow Memory

Use this skill to persist verified selector chains, UI recipes, and failures.
Memory is advisory: workflow tools must still verify their final result.
