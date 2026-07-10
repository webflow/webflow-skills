## Project Overview

Webflow Skills is a marketplace-ready collection of agent skills for Claude Code, Cursor, and compatible agents. Skills extend agents with specialized Webflow capabilities: CMS management, site auditing, safe publishing, Designer tools, code components, and CLI integration. **This is a pure documentation project** — no compiled code, just SKILL.md files that guide agent behavior.

## Repository Structure

One plugin family lives under `plugins/`:

- **webflow-skills/** — CMS operations, site/asset/link audits, Designer page/component tools, safe publish, FlowKit naming, React code component workflows, CLI wrappers for Cloud, DevLink, and designer extensions, and Webflow University guided onboarding skills

Skills are grouped in the README under Webflow MCP, Webflow CLI, Webflow Code Component, and Webflow University sections. Webflow University skills (e.g. `webflow-university:mcp-getting-started`) are educational, guided-activity skills.

Key config files:

- `.mcp.json` — MCP server config (Webflow MCP at https://mcp.webflow.com/mcp)
- `.claude-plugin/marketplace.json` — Claude marketplace entry listing the Webflow Skills plugin
- `.agents/plugins/marketplace.json` — Codex marketplace entry listing the Webflow Skills plugin
- `plugins/webflow-skills/.codex-plugin/plugin.json` — Codex plugin manifest
- `plugins/webflow-skills/.mcp.json` — Symlink to the root `.mcp.json` for Codex plugin MCP config
- `plugins/webflow-skills/assets/logo.svg` — Symlink to the root `assets/logo.svg` for Codex plugin branding
- `.cursor-plugin/plugin.json` + `marketplace.json` — Cursor plugin config
- `agents/webflow-agent.md` — Agent setup documentation

## CI Validation

CI runs on push/PR to main (`.github/workflows/ci.yml`):

```bash
# What CI checks:
# 1. Required root files: README.md, LICENSE, AGENTS.md, CLAUDE.md (must be symlink)
# 2. Marketplace and plugin configs exist
# 3. Every skill dir under plugins/webflow-skills/skills/ has SKILL.md with name: and description: frontmatter
```

There is no build step, test suite, or linter config — validation is purely structural.

## Skill Anatomy

Each skill is a single `SKILL.md` file in its own directory:

```
plugins/webflow-skills/skills/<skill-name>/SKILL.md
```

Required YAML frontmatter:

```yaml
---
name: namespace:skill-name # e.g. webflow-mcp:site-audit
description: ... # Up to 1024 chars, include trigger keywords
---
```

Optional frontmatter: `license`, `model`, `allowed-tools`

## Design Conventions

- **Phased workflows**: Discovery → Analysis → Validation → Preview → Confirmation → Execution → Reporting
- **Safety-first**: All mutating operations require explicit user confirmation (type "confirm" or "publish", not just "yes")
- **Batch operations**: Large datasets split into 50-item batches with progress reporting
- **MCP-routed**: Webflow operations use MCP tools, never direct API calls

## Adding/Editing Skills

Follow `CONTRIBUTING.md`. PR title format: `feat(skills): Add [skill-name]`. Keep SKILL.md under 500 lines. Every skill needs Instructions, Examples, and Guidelines sections.
