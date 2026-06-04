# Contributing

Guidelines for adding and improving Webflow skills. Internal and external contributions are both welcome.

## Designing skills (start here)

New to writing skills? Use Anthropic's guidance and tooling before you start — it's the fastest way to get a skill right the first time:

- **[The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)** — how to scope, structure, and name a skill, write descriptions with strong trigger keywords, apply progressive disclosure, and include effective examples.
- **[`skill-creator` skill](https://github.com/anthropics/skills/blob/main/skills/skill-creator)** — install it and let it scaffold and refine your `SKILL.md` instead of starting from a blank file.

Then follow the structure and conventions below.

## Adding a New Skill

### 1. Create the Skill Directory

```
plugins/webflow-skills/skills/
└── my-skill/
    └── SKILL.md
```

### 2. Write SKILL.md

Use YAML frontmatter followed by markdown content:

```markdown
---
name: my-skill
description: Clear description of what this skill does and when to use it. Include keywords that help agents identify when this skill is relevant.
---

# My Skill Name

## Instructions

Step-by-step guidance for the agent.

## Examples

Concrete examples showing expected input/output.

## Guidelines

- Specific rules to follow
- Edge cases to handle
```

### Naming Conventions

- `name`: 1-64 characters, lowercase alphanumeric with hyphens only
- `description`: Up to 1024 characters, include trigger keywords
- Keep `SKILL.md` under 500 lines

### Optional Fields

```yaml
---
name: my-skill
description: What this skill does
license: MIT
model: sonnet
allowed-tools: Read Grep Glob
---
```

## Quality Checklist

- [ ] `SKILL.md` has name and description in frontmatter
- [ ] Instructions section explains how to perform the task
- [ ] Examples show realistic prompts and responses
- [ ] Guidelines cover edge cases

## Pull Requests

1. Test the skill with Claude
2. Title format: `feat(skills): Add [skill-name]`
3. Explain what the skill does and why

## Issues

**Bug reports**: Skill name, steps to reproduce, expected vs actual

**Feature requests**: Proposed skill, use case, expected behavior
