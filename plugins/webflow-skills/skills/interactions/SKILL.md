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
- **No Designer or MCP Bridge required.** `data_interactions_tool` is headless, the same way `data_element_tool` is. Designer is only useful afterward, to inspect the Interactions panel or Preview. Do not ask the user to open the Bridge app in order to list or write interactions.
- After Webflow monorepo PR #117284 ships: if the Webflow Filesystem (WFS) interactions lane is `built`, prefer `site/interactions/interactions.ix3.json` — `data_interactions_tool` is then unregistered. **Until that PR lands, the tool is still registered even in WFS sessions.** This skill is the MCP CRUD path.

## Tool surface (beta dogfood)

These tools are **not on stable MCP**.

- **Server:** `https://mcp.webflow.com/beta/mcp`
- **Flag:** `ff-ix3-interaction-apis`
- **Scopes:** `pages:read` / `pages:write`
- **Compound tool:** `data_interactions_tool`
- **Actions:** `list_interactions`, `get_interaction`, `create_interaction`, `update_interaction`, `delete_interaction`
- `siteId` and `pageId` are **top-level** tool arguments (page context / create bookkeeping). They are **not** inside `create_interaction` args.
- **There is no `guide` action and no `webflow://guides/interactions` resource yet.** Both are planned. Until they ship, the `references/` files in this skill are the contract — do not try to call `guide` and do not wait for it.
- `create_interaction` args: `name` (required), `scope` (optional, default site), `triggers` (required array), `timelines` (required array), optional `timelineDefaults`, optional `conditionalPlayback`

## Instructions

### Phase 1: Discovery

1. **Call `webflow_guide_tool` first** — always the first MCP tool call
2. **Get the site**: `data_sites_tool` with `list_sites`. If only one site exists, use it.
3. **Get the page**: `data_pages_tool` with `list_pages`. You need that page's ID as top-level `pageId` on every `data_interactions_tool` call.
4. **Confirm the gate**: beta MCP endpoint and `ff-ix3-interaction-apis` covering the caller's identity. If `data_interactions_tool` is unregistered, stop and tell the user. The likely causes are the stable MCP endpoint instead of beta, or the flag not covering that identity. Do not treat a missing tool as a missing Bridge session, and do not ask the user to open Designer or the MCP Bridge. Do not work around it. `ff-ix3-interaction-de-api` is a **different** flag, for the Designer Extension iframe surface; it is not what this tool needs.

### Phase 2: Read the contract for what you are building

5. **Read the reference file for your trigger, plus `references/envelope-and-targets.md`.** That pair is enough to author any single-trigger interaction. See the Reference map below. Do this before your first write on anything beyond the five inline examples in this file.
6. Do not invent `+=` / `<` / `>` `timing.position` strings or `{reducedMotion:"skip"}`. A bare number for `timing.duration` is seconds (`0.4`, not `400`).

#### Reference map

| User asks for                                 | Read                                                                         |
| --------------------------------------------- | ---------------------------------------------------------------------------- |
| Click                                         | [references/trigger-click.md](references/trigger-click.md)                   |
| Hover, mouse enter/leave                      | [references/trigger-hover.md](references/trigger-hover.md)                   |
| Page load                                     | [references/trigger-load.md](references/trigger-load.md)                     |
| Scroll, scrub, parallax                       | [references/trigger-scroll.md](references/trigger-scroll.md)                 |
| Mouse move, cursor follow                     | [references/trigger-mouse-move.md](references/trigger-mouse-move.md)         |
| Custom JS event                               | [references/trigger-custom.md](references/trigger-custom.md)                 |
| Navbar, dropdown, conditions, Rive, variables | [references/gated-capabilities.md](references/gated-capabilities.md)         |
| Envelope, IDs, scope, targets, filters        | [references/envelope-and-targets.md](references/envelope-and-targets.md)     |
| Properties, values, `tt`, timing, splitText   | [references/actions-and-properties.md](references/actions-and-properties.md) |
| Roles, groups, percent canvas                 | [references/timelines-and-groups.md](references/timelines-and-groups.md)     |
| Reduced motion, breakpoint playback           | [references/conditional-playback.md](references/conditional-playback.md)     |
| Editing an existing interaction               | [references/updating-interactions.md](references/updating-interactions.md)   |
| Size and count limits                         | [references/limits-and-budgets.md](references/limits-and-budgets.md)         |
| A write succeeded but the user cannot edit it | [references/panel-traps.md](references/panel-traps.md)                       |
| A write succeeded but nothing animates        | [references/rejects-index.md](references/rejects-index.md) → "nothing to decode" |
| Decoding a rejection message                  | [references/rejects-index.md](references/rejects-index.md)                   |
| Which triggers and properties exist at all    | [references/capabilities.generated.md](references/capabilities.generated.md) |

Start at [references/index.md](references/index.md) if you are unsure. It also
explains the enforcement tags — in particular `[PANEL-TRAP]`, which means the
write will succeed but leave the user with something they cannot edit in the
Designer, and `[LEGACY-OK-ON-UPDATE]`, which means you must pass a stored value
through untouched rather than "fixing" it.

### Phase 3: Plan (before any write)

7. Resolve class targets: prefer style-block id arrays from `data_style_tool`; class name strings are accepted. **Confirm with `query_styles` that the class resolves to exactly one style block** — a name reused as the leaf of several combo chains returns several, and each targets a different element. When an element needs its own class, create it with `create_style` naming the full `parent_style_names` chain you intend to apply, then apply that same chain with `data_element_tool` `set_style`; a chain that does not already exist as a style block is refused
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
15. **A successful write is not proof the animation runs.** Several legal payloads save, read back byte-identical, and do nothing: a scroll reveal with no `enter`, a `[from, to]` pair on a To tween, a class array that is not one combo chain, a grouped interaction, `control: "reverse"` on a first click. `get_interaction` cannot detect any of them. Check the payload against the Guidelines below before reporting success, and if the user says nothing happens, start at [references/rejects-index.md](references/rejects-index.md) → "When there is nothing to decode" instead of rewriting the interaction.

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
          "targets": [
            { "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }
          ]
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
          "targets": [
            { "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }
          ]
        }
      ]
    }
  ]
}
```

### Example 3: Scroll scrub

**User:** "Scrub a fade as the user scrolls"

Scroll is **standalone**. A scrub needs a numeric `scrub` (not `true`), a roleless timeline with `canvasDuration: 1`, and action `timing.duration` equal to that canvas so the tween spans the full pass. **Omit** playback `control` / `delay` / `jump` / `speed`. Omitting `scrub` is a one-shot play when the range is crossed — not a scrub.

```json
{
  "name": "Scroll scrub fade",
  "triggers": [
    {
      "extensionKey": "wf:scroll",
      "config": {
        "scrollTriggerConfig": {
          "start": "top bottom",
          "end": "top 10%",
          "scrub": 0.3
        }
      },
      "target": { "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }
    }
  ],
  "timelines": [
    {
      "canvasDuration": 1,
      "actions": [
        {
          "id": "act-scroll-scrub",
          "name": "Fade",
          "timing": { "duration": 1 },
          "properties": {
            "wf:transform": { "opacity": ["0%", "100%"], "xPercent": [-40, 0] }
          },
          "targets": [
            { "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }
          ]
        }
      ]
    }
  ]
}
```

**Play-once variant (a reveal, not a scrub).** Drop `scrub` and `canvasDuration`, put `timing.duration` back in seconds — and **send `enter: "play"`**. Omitted toggle actions become `none`, and without scrub those toggles are the only playback, so a reveal with no `enter` binds successfully and never runs. Nothing errors.

```json
{
  "extensionKey": "wf:scroll",
  "config": {
    "scrollTriggerConfig": {
      "start": "top 90%",
      "end": "bottom 15%",
      "enter": "play",
      "leaveBack": "reset"
    }
  },
  "target": { "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }
}
```

`leaveBack: "reset"` is optional and replays the reveal when the user scrolls back up. Use a From (`tt: 1`) for the reveal itself so the element starts hidden.

### Example 4: Hover enter / leave

**User:** "Fade in on hover enter and out on leave"

Use the **role form**: one `wf:hover` trigger with `multiTimeline: true`, and two timelines tagged `mouseEnter` and `mouseLeave` via `triggerMetadata`. Roles must be exactly those strings and unique per timeline. Do not mix this with legacy hover `type` / `hover` / `custom`.

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
          "targets": [
            { "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }
          ]
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
          "targets": [
            { "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }
          ]
        }
      ]
    }
  ]
}
```

**Tell the user one caveat:** the panel will animate this correctly but will not offer a remove button for either action group, because it never writes hover this way itself.

**Do not** author the two-trigger split the panel prefers (two `wf:hover` triggers with `eventMode` plus `assignedGroupId`, and `groupId` on the timelines). The MCP timeline input has no `groupId` field, so Zod strips it and the triggers end up pointed at groups no timeline claims. The runtime then skips both triggers and the interaction silently does nothing. Nothing rejects and `get_interaction` still echoes your triggers back. See [references/trigger-hover.md](references/trigger-hover.md).

For enter only, send one trigger with `pluginConfig: { "multiTimeline": false }` and a single timeline.

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
          "targets": [
            { "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }
          ]
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
          "targets": [
            { "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }
          ]
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
- **A `wf:class` id array is ANDed into one compound selector**, not a list of alternatives: `["a","b"]` resolves to `.a.b`. The host expands a combo class's parents for you, so pass the one leaf id. Ids from two different combo chains produce a selector no element carries, and the target resolves to nothing with no error. One target means one class or one combo chain — animate two different sets of elements with two actions.
- **A leaf class name reused across chains** (`.btn.lift` and `.btn.cta.lift` are two style blocks both named `lift`) is rejected when passed as a name string and matches the wrong element when passed as ids. Give each element its own class instead.
- **Send only what the Interactions panel can author.** Worker Zod is lenient; illegal shapes fail on the Designer write path.
- **`conditionalPlayback`** is an **array** of `{ type, behavior }` (and breakpoint form), not `{reducedMotion:"skip"}`. Example: `[{ "type": "prefers-reduced-motion", "behavior": "dont-animate" }]`.
- **Load** omits trigger `target` and `pluginConfig`.
- **Scroll** and **mouse-move** omit playback `control` / `delay` / `jump` / `speed`.
- **A scroll without `scrub` needs `enter: "play"`.** Omitted toggle actions become `none`, so the ScrollTrigger binds and the timeline never plays. The panel always writes all four toggles; match it.
- **Scroll scrub:** send numeric `scrub`, `canvasDuration: 1`, and action `timing.duration: 1`. A tiny duration occupies ~1% of the scroll range and looks like nothing happened.
- **`control: "reverse"` is a no-op on the first click** (the playhead starts at 0). For a reverse the user can try in Preview, use `togglePlayReverse` (`pluginConfig.click` omitted or `"each"`).
- **A To tween reads only its `to` slot.** `[from, to]` on `tt: 0` is half discarded and GSAP animates from the element's live value, so `scale: [0.55, 1.15]` on an unscaled element goes 1 → 1.15 and `opacity: ["20%","100%"]` on an opaque element does nothing at all. Use `tt: 2` whenever the animation needs a start value.
- **Do not put a click or hover trigger on an element its own from-state collapses** (`scaleX: 0`, `width: 0`). No box is left to click. Trigger on a parent and animate the child.
- **Grouped interactions are not authorable through MCP.** The timeline input drops `groupId`, so the triggers persist pointed at groups no timeline claims and the runtime skips them. Author a single group, or say the capability is unavailable.
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
- Scopes: `pages:read` / `pages:write`
