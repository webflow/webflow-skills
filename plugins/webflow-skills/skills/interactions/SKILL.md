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
- Use Webflow MCP's `data_interactions_tool` for list / get / create / update / delete
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
- **Actions:** `list_interactions`, `get_interaction`, `create_interaction`, `update_interaction`, `delete_interaction`
- `siteId` and `pageId` are **top-level** tool arguments (session / create bookkeeping). They are **not** inside `create_interaction` args.
- **There is no `guide` action and no `webflow://guides/interactions` resource yet.** Both are planned. Until they ship, the `references/` files in this skill are the contract — do not try to call `guide` and do not wait for it.
- `create_interaction` args: `name` (required), `scope` (optional, default site), `triggers` (required array), `timelines` (required array), optional `timelineDefaults`, optional `conditionalPlayback`

## Instructions

### Phase 1: Discovery

1. **Call `webflow_guide_tool` first** — always the first MCP tool call
2. **Get the site**: `data_sites_tool` with `list_sites`. If only one site exists, use it.
3. **Get the page**: `data_pages_tool` with `list_pages`. You need that page's ID as top-level `pageId` on every `data_interactions_tool` call.
4. **Confirm the gate**: beta MCP endpoint, **both** `ff-aio-150-page-automation` (base page-automation gate) and `ff-ix3-interaction-apis` (checked in addition), and a connected Designer Bridge session. If `data_interactions_tool` is unregistered, stop and tell the user — the likely causes are the stable MCP endpoint instead of beta, one of the two gates being off for that identity, or no Bridge session. Do not work around it. Note `ff-ix3-interaction-de-api` is a separate flag for the Designer Extension iframe surface and is not what this tool needs.

### Phase 2: Read the contract for what you are building

5. **Read the reference file for your trigger, plus `references/envelope-and-targets.md`.** That pair is enough to author any single-trigger interaction. See the Reference map below. Do this before your first write on anything beyond the five inline examples in this file.
6. Do not invent `+=` / `<` / `>` `timing.position` strings or `{reducedMotion:"skip"}`. A bare number for `timing.duration` is seconds (`0.4`, not `400`).

#### Reference map

| User asks for | Read |
| --- | --- |
| Click | [references/trigger-click.md](references/trigger-click.md) |
| Hover, mouse enter/leave | [references/trigger-hover.md](references/trigger-hover.md) |
| Page load | [references/trigger-load.md](references/trigger-load.md) |
| Scroll, scrub, parallax | [references/trigger-scroll.md](references/trigger-scroll.md) |
| Mouse move, cursor follow | [references/trigger-mouse-move.md](references/trigger-mouse-move.md) |
| Custom JS event | [references/trigger-custom.md](references/trigger-custom.md) |
| Navbar, dropdown, conditions, Rive, variables | [references/gated-capabilities.md](references/gated-capabilities.md) |
| Envelope, IDs, scope, targets, filters | [references/envelope-and-targets.md](references/envelope-and-targets.md) |
| Properties, values, `tt`, timing, splitText | [references/actions-and-properties.md](references/actions-and-properties.md) |
| Roles, groups, percent canvas | [references/timelines-and-groups.md](references/timelines-and-groups.md) |
| Reduced motion, breakpoint playback | [references/conditional-playback.md](references/conditional-playback.md) |
| Editing an existing interaction | [references/updating-interactions.md](references/updating-interactions.md) |
| Size and count limits | [references/limits-and-budgets.md](references/limits-and-budgets.md) |
| A write succeeded but the user cannot edit it | [references/panel-traps.md](references/panel-traps.md) |
| Decoding a rejection message | [references/rejects-index.md](references/rejects-index.md) |
| Which triggers and properties exist at all | [references/capabilities.generated.md](references/capabilities.generated.md) |

Start at [references/index.md](references/index.md) if you are unsure. It also
explains the enforcement tags — in particular `[PANEL-TRAP]`, which means the
write will succeed but leave the user with something they cannot edit in the
Designer, and `[LEGACY-OK-ON-UPDATE]`, which means you must pass a stored value
through untouched rather than "fixing" it.

### Phase 3: Plan (before any write)

7. Resolve class targets: prefer style-block id arrays from `data_style_tool`; class name strings are accepted
8. Plan the payload against the reference you read in Phase 2: object format, legal trigger/target, fresh action ids
9. **Request explicit confirmation** before create/update/delete:
   - "Would you like me to create this click fade?"
   - "Before I write this interaction: [plan]. Confirm to proceed."

### Phase 4: Write (after confirmation only)

10. `create_interaction` or `update_interaction` on `data_interactions_tool`
11. `update_interaction` is a partial: omitted fields stay, provided values replace, `null` clears `timelineDefaults` / `conditionalPlayback`. `timelines` is a **full replace** when sent.

### Phase 5: Verify

12. `get_interaction` with the returned id
13. Report what was created/updated
14. **On reject:** read the error, look it up in [references/rejects-index.md](references/rejects-index.md), fix the payload. Do not invent GSAP position operators, and do not retry the same shape hoping for a different result — every rejection here is deterministic.

## Examples

Replace `STYLE_BLOCK_ID` with a style-block id. Mint a **fresh unique** `id` on every action.

### Example 1: Click fade

**User:** "Add a click fade interaction"

1. Call `webflow_guide_tool`
2. `list_sites` → `list_pages` → resolve `STYLE_BLOCK_ID` via `data_style_tool`
3. Read [references/trigger-click.md](references/trigger-click.md) and [references/envelope-and-targets.md](references/envelope-and-targets.md)
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

Same discovery, reference read, and confirmation. Load **omits the trigger target**. Action targets must not be `wf:trigger-only`.

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

Use the **trigger split**: two `wf:hover` triggers separated by `pluginConfig.eventMode`, each pinned to a timeline group, with `multiTimeline: false` on both. This is the shape the panel writes, so the user can edit and remove the groups afterwards.

Mint your own group ids and reuse each one on its trigger (`assignedGroupId`) and its timeline (`groupId`). `control: "play"` is required once two groups exist.

```json
{
  "name": "Hover fade",
  "triggers": [
    {
      "extensionKey": "wf:hover",
      "config": {
        "control": "play",
        "assignedGroupId": "grp-hover-in",
        "pluginConfig": { "multiTimeline": false, "eventMode": "enter" }
      },
      "target": { "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }
    },
    {
      "extensionKey": "wf:hover",
      "config": {
        "control": "play",
        "assignedGroupId": "grp-hover-out",
        "pluginConfig": { "multiTimeline": false, "eventMode": "leave" }
      },
      "target": { "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }
    }
  ],
  "timelines": [
    {
      "groupId": "grp-hover-in",
      "name": "Hover in actions",
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
      "groupId": "grp-hover-out",
      "name": "Hover out actions",
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

**Do not** author hover in/out as one trigger with `multiTimeline: true` plus `mouseEnter` / `mouseLeave` roles. The write succeeds and the runtime honors it, but the panel offers no remove button for either resulting group. See [references/trigger-hover.md](references/trigger-hover.md). Use the role form only to read or preserve data that already stores it.

If the user only wants an enter animation, send one trigger with `pluginConfig: { "multiTimeline": false }` — omitting the key drops to the legacy editor instead. Either way, the panel may not offer "Add separate hover out" on a single-timeline hover, so author the full split above whenever the user wants both directions.

### Example 5: Mouse-move

**User:** "Move this element with the cursor"

Mouse-move is **standalone**. It validates without a target but never fires without one, so **always send a target** — `wf:viewport` (`value: ""`) for page-wide tracking, or `wf:inst` / `wf:class` to scope it. Every timeline needs a unique role from `mouseX` / `mouseY` / `interval`. **Omit** playback `control` / `delay` / `jump` / `speed`. See [references/trigger-mouse-move.md](references/trigger-mouse-move.md).

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
- **Duration is seconds.** `timing.duration: 0.4` is 400ms. `400` is 400 seconds. Use `"400ms"` if you think in milliseconds.
- **From / FromTo (`tt: 1` / `2`) sit at the from-state until the trigger fires.** Prefer To (`tt: 0` or omit) when the element should be visible at rest.
- **`splitText` needs a Heading, Paragraph, or Text that already has copy**, not a Div / Block.
- **Roles live on `timelines[].triggerMetadata`**, not on the trigger. Mouse-move needs a unique `mouseX` / `mouseY` / `interval` per timeline.
- On reject: read the error, look it up in [references/rejects-index.md](references/rejects-index.md), do not invent fields.

## Install / gate

```
npx -y skills add webflow/webflow-skills --skill 'webflow-mcp:interactions' --yes
```

Optional `--agent claude-code` (or cursor). Testers also need:

- Beta MCP: `https://mcp.webflow.com/beta/mcp`
- Flag: `ff-ix3-interaction-apis`
- Designer MCP Bridge connected
- Scopes: `pages:read` / `pages:write`
