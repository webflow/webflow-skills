---
name: webflow-mcp:interactions
description: Create, update, list, and delete Webflow IX3 interactions (GSAP animations) through Webflow MCP. Use when the user wants click/hover/load/scroll/mouse-move animations, interaction timelines, or data_interactions_tool / create_interaction payloads. Requires beta MCP + ff-ix3-interaction-apis during dogfood.
---

# Interactions

Create and edit IX3 interactions (GSAP animations) through Webflow MCP.

## Important Note

**ALWAYS use Webflow MCP tools for all operations:**

- Use Webflow MCP's `webflow_guide_tool` to get best practices **before any other tool call**
- Use Webflow MCP's `data_sites_tool` with action `list_sites` to identify the target site
- Use Webflow MCP's `data_pages_tool` with action `list_pages` to find the target page by name or slug
- Use Webflow MCP's `data_interactions_tool` for list / get / create / update / delete (and `guide` when that action exists)
- Use Webflow MCP's `data_style_tool` to resolve class **style-block ids** before targeting `wf:class`
- DO NOT use any other tools or methods for Webflow interaction CRUD
- All tool calls must include the required `context` parameter (15-25 words, third-person perspective)
- **The Webflow Designer MCP Bridge must stay open.** `data_interactions_tool` is not headless the way `data_element_tool` is — it needs a live Designer session.
- After Webflow monorepo PR #117284 ships: if the Webflow Filesystem (WFS) interactions lane is `built`, prefer `site/interactions/interactions.ix3.json` — `data_interactions_tool` is then unregistered. **Until that PR lands, the tool is still registered even in WFS sessions.** This skill is the MCP CRUD path.

## Tool surface (beta dogfood)

These tools are **not on stable MCP**.

- **Server:** `https://mcp.webflow.com/beta/mcp`
- **Flag:** `ff-ix3-interaction-apis`
- **Scopes:** `pages:read` / `pages:write`
- **Compound tool:** `data_interactions_tool`
- **Actions:** `list_interactions`, `get_interaction`, `create_interaction`, `update_interaction`, `delete_interaction`, and `guide` (after the Cloudflare MCP guide PR). If `guide` is missing, follow **Guidelines** below and do not invent GSAP position strings.
- Before create/update: call `guide` **or** read MCP resource `webflow://guides/interactions` when those exist
- `siteId` and `pageId` are **top-level** tool arguments (session / create bookkeeping). They are **not** inside `create_interaction` args. They are still required when calling `guide`.
- `create_interaction` args: `name` (required), `scope` (optional, default site), `triggers` (required array), `timelines` (required array), optional `timelineDefaults`, optional `conditionalPlayback`

## Instructions

### Phase 1: Discovery

1. **Call `webflow_guide_tool` first** — always the first MCP tool call
2. **Get the site**: `data_sites_tool` with `list_sites`. If only one site exists, use it.
3. **Get the page**: `data_pages_tool` with `list_pages`. You need that page's ID as top-level `pageId` on every `data_interactions_tool` call.
4. **Confirm the gate**: beta MCP + `ff-ix3-interaction-apis` + Bridge connected. If `data_interactions_tool` is unregistered, stop and tell the user (stable MCP, flag off, or post-#117284 WFS built lane).

### Phase 2: Guide

5. Call `data_interactions_tool` action `guide` (same top-level `siteId` + `pageId`) **or** read `webflow://guides/interactions`
6. If neither exists yet, use **Guidelines** below. Do not invent `+=` / `<` / `>` timing.position strings or `{reducedMotion:"skip"}`

### Phase 3: Plan (before any write)

7. Resolve class targets: prefer style-block id arrays from `data_style_tool`; class name strings are accepted
8. Plan the payload from the guide: object format, legal trigger/target, fresh action ids
9. **Request explicit confirmation** before create/update/delete:
   - "Would you like me to create this click fade?"
   - "Before I write this interaction: [plan]. Confirm to proceed."

### Phase 4: Write (after confirmation only)

10. `create_interaction` or `update_interaction` on `data_interactions_tool`
11. `update_interaction` is a partial: omitted fields stay, provided values replace, `null` clears `timelineDefaults` / `conditionalPlayback`. `timelines` is a **full replace** when sent.

### Phase 5: Verify

12. `get_interaction` with the returned id
13. Report what was created/updated
14. **On reject:** read the error, call `guide` again, fix the payload. Do not invent GSAP position operators.

## Examples

Each example calls `guide` before `create_interaction` when that action exists. Replace `STYLE_BLOCK_ID` with a style-block id. Mint a **fresh unique** `id` on every action.

### Example 1: Click fade

**User:** "Add a click fade interaction"

1. Call `webflow_guide_tool`
2. `list_sites` → `list_pages` → resolve `STYLE_BLOCK_ID` via `data_style_tool`
3. Call `data_interactions_tool` action `guide` (or read `webflow://guides/interactions`)
4. Present the plan and wait for confirmation
5. After confirmation, `create_interaction`:

```json
{
  "name": "Click fade",
  "triggers": [
    {
      "extensionKey": "wf:click",
      "config": { "control": "play" },
      "target": { "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }
    }
  ],
  "timelines": [
    {
      "actions": [
        {
          "id": "act-click-fade",
          "name": "Fade",
          "timing": { "duration": 0.4 },
          "properties": { "wf:transform": { "opacity": ["0%", "100%"] } },
          "targets": [{ "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }]
        }
      ]
    }
  ]
}
```

6. `get_interaction` to verify

### Example 2: Page load fade

**User:** "Fade this section in when the page loads"

Same discovery + `guide` + confirm. Load **omits the trigger target**. Action targets must not be `wf:trigger-only`.

```json
{
  "name": "Load fade",
  "triggers": [{ "extensionKey": "wf:load", "config": { "control": "play" } }],
  "timelines": [
    {
      "actions": [
        {
          "id": "act-load-fade",
          "name": "Fade",
          "timing": { "duration": 0.4 },
          "properties": { "wf:transform": { "opacity": ["0%", "100%"] } },
          "targets": [{ "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }]
        }
      ]
    }
  ]
}
```

### Example 3: Scroll scrub

**User:** "Scrub a fade as the user scrolls"

Scroll is **standalone**. Include `scrollTriggerConfig` with `start` and `end`. **Omit** playback `control` / `delay` / `jump` / `speed`.

```json
{
  "name": "Scroll fade",
  "triggers": [
    {
      "extensionKey": "wf:scroll",
      "config": {
        "scrollTriggerConfig": { "start": "top 90%", "end": "bottom 25%" }
      },
      "target": { "extensionKey": "wf:body", "value": "" }
    }
  ],
  "timelines": [
    {
      "actions": [
        {
          "id": "act-scroll-fade",
          "name": "Fade",
          "timing": { "duration": 0.4 },
          "properties": { "wf:transform": { "opacity": ["0%", "100%"] } },
          "targets": [{ "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }]
        }
      ]
    }
  ]
}
```

### Example 4: Hover enter / leave

**User:** "Fade in on hover enter and out on leave"

Use `multiTimeline: true` with unique roles `mouseEnter` / `mouseLeave`. Do not mix this with legacy hover `type` / `hover` / `custom`.

```json
{
  "name": "Hover fade",
  "triggers": [
    {
      "extensionKey": "wf:hover",
      "config": { "pluginConfig": { "multiTimeline": true } },
      "target": { "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }
    }
  ],
  "timelines": [
    {
      "triggerMetadata": { "role": "mouseEnter" },
      "actions": [
        {
          "id": "act-hover-in",
          "name": "Fade in",
          "timing": { "duration": 0.3 },
          "properties": { "wf:transform": { "opacity": ["0%", "100%"] } },
          "targets": [{ "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }]
        }
      ]
    },
    {
      "triggerMetadata": { "role": "mouseLeave" },
      "actions": [
        {
          "id": "act-hover-out",
          "name": "Fade out",
          "timing": { "duration": 0.3 },
          "properties": { "wf:transform": { "opacity": ["100%", "0%"] } },
          "targets": [{ "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }]
        }
      ]
    }
  ]
}
```

### Example 5: Mouse-move

**User:** "Move this element with the cursor"

Mouse-move is **standalone**. Target `wf:viewport` (`value: ""`) is recommended. Every timeline needs a unique role from `mouseX` / `mouseY` / `interval`. **Omit** playback `control` / `delay` / `jump` / `speed`.

```json
{
  "name": "Mouse follow",
  "triggers": [
    {
      "extensionKey": "wf:mouse-move",
      "config": {},
      "target": { "extensionKey": "wf:viewport", "value": "" }
    }
  ],
  "timelines": [
    {
      "triggerMetadata": { "role": "mouseX" },
      "actions": [
        {
          "id": "act-mouse-x",
          "name": "Follow X",
          "timing": { "duration": 0.4 },
          "properties": { "wf:transform": { "x": ["0px", "40px"] } },
          "targets": [{ "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }]
        }
      ]
    },
    {
      "triggerMetadata": { "role": "mouseY" },
      "actions": [
        {
          "id": "act-mouse-y",
          "name": "Follow Y",
          "timing": { "duration": 0.4 },
          "properties": { "wf:transform": { "y": ["0px", "40px"] } },
          "targets": [{ "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }]
        }
      ]
    }
  ]
}
```

## Guidelines

- **Object format only:** `{ extensionKey, value, filterContext? }`. Nested `filterBy` is a **2-tuple** `["wf:class", ["STYLE_BLOCK_ID"]]`, never an object.
- **IDs:** omit timeline `id` on create (the host mints it). Every action needs a fresh unique `id`. Do not send trigger `id`.
- **Opacity** lives under `wf:transform` (e.g. `["0%","100%"]`), never `wf:style`.
- **Class targets:** style-block id arrays preferred; class name strings are accepted.
- **Send only what the Interactions panel can author.** Worker Zod is lenient; illegal shapes fail on the Designer write path.
- **`conditionalPlayback`** is an **array** of `{ type, behavior }` (and breakpoint form), not `{reducedMotion:"skip"}`. Example: `[{ "type": "prefers-reduced-motion", "behavior": "dont-animate" }]`.
- **Load** omits trigger `target` and `pluginConfig`.
- **Scroll** and **mouse-move** omit playback `control` / `delay` / `jump` / `speed`.
- **Navbar / dropdown are not authorable through this API today.** They are flag-gated and rejected on create for every caller. Tell the user the trigger is unavailable rather than attempting a write.
- **No GSAP position operators** (`+=`, `<`, `>`) in `timing.position`. Use a finite number (seconds) or `'500ms'`.
- On reject: read the error, call `guide` again, do not invent fields.

## Install / gate

```
npx -y skills add webflow/webflow-skills --skill 'webflow-mcp:interactions' --yes
```

Optional `--agent claude-code` (or cursor). Testers also need:

- Beta MCP: `https://mcp.webflow.com/beta/mcp`
- Flag: `ff-ix3-interaction-apis`
- Designer MCP Bridge connected
- Scopes: `pages:read` / `pages:write`
