---
name: webflow-mcp:interactions
version: 2026.08.26
description: Create, update, list, and delete Webflow IX3 interactions (GSAP animations) through Webflow MCP. Use when the user wants click/hover/load/scroll/mouse-move animations, interaction timelines, or data_interactions_tool / create_interaction payloads. Requires beta MCP + ff-ix3-interaction-apis during dogfood.
---

<!--
CHANGELOG
2026.08.30 — Three corrections found by re-reading our own claims against merged PRs.
  * The role-form hover remove-button warning was true when written and was fixed by
    webflow#117817 on 2026-08-19. Reattributed to that PR rather than called false.
  * `playInReverse` is not an authorable replacement for `autoReverse`. webflow#118489
    rejects it; there is no API-side replacement. The earlier entry below is wrong.
  * Advanced eases are simply authorable. No write-boundary guard exists and the gate
    is 100% public and stale, so the `[FLAG]` framing promised a refusal that cannot
    happen.
2026.08.26 — Corrections from a 135-interaction stress run (197 write attempts,
31 browser assertions). The gaps were almost all in the positive direction —
not "which payloads are refused", which measured 46/48 accurate, but "what
shape does this accepted field take".
  * `wf:any-element` value is `'*'`, not `''`. It does not share a value with the
    other two action-only keys. Highest-cost error in the run: eight relationship
    rows sent as a batch on the documented value, all refused.
  * `wf:attribute` also takes a full selector. A bare name matches every element
    carrying the attribute, which is ambiguous when several do.
  * The hover recommendation is now one weak preference (prefer the split because
    the panel writes it) instead of opposite defaults here and in the pack. A
    Designer check then disproved the remove-button penalty the role form was
    said to carry: both forms show a delete control on both action groups, so
    there is no editability tradeoff to trade against.
  * `webflow_guide_tool` returns nothing about interactions; said so rather than
    letting the mandated first step imply otherwise.
  * References re-published from the corrected pack, which also adds the
    `wf:lottie` / `wf:spline` value shapes, the `ix3-*` wrapper shapes, the
    `{from,to}` exception for plugin namespaces, `playInReverse`'s location, a
    `[FLAG]` tag distinct from `[GATED]`, and the MCP-vs-host ordering on the
    conditions guard.
2026.08.25 — Dogfood corrections against Webflow MCP 2.0.1.
  * Added the silent-strip rule for unknown `config` keys (the single most
    expensive trap on this surface — it cost a dogfood run three misfiled bugs).
  * Documented `timing.ease` / `timing.stagger.ease` as an integer index into
    EASING_NAMES, with the full 0–30 table, plus the advanced-ease object union.
    Previously undocumented in every file.
  * Documented the `wf:class` `{operation, selectors}` shape.
  * Documented the `stagger` object, the `filterContext.relationship` enum,
    `wf:selector`, the `wf:inst` `[componentId, elementId]` shape, `wf:attribute`,
    and the per-interaction caps.
  * Added `"tt": 2` to Examples 1–3. As written they paired a [from,to] array with
    an omitted tween type, which is a measured no-op on a default element. Example 1
    also gained the rest-state note: a FromTo holds its from-state, so the click
    example renders at `opacity: 0` until clicked, which reads as a failed write
    unless the agent says so.
  * Corrected the hover-split section: `eventMode` is `pluginConfig.eventMode`
    with values 'enter'/'leave'.
  * Added Example 6 (custom JS event) including the Webflow.require('ix3').emit()
    firing call, which appears nowhere else in the pack.
  * Noted the tool-schema errata for conditionalPlayback and the siteId/site_id
    placement split across the tool family.
-->


# Interactions

Create and edit IX3 interactions (GSAP animations) through Webflow MCP.

## Important Note

**ALWAYS use Webflow MCP tools for all operations:**

- Use Webflow MCP's `webflow_guide_tool` to get best practices **before any other tool call** — it covers general MCP conventions and returns nothing about interactions; the IX3 contract lives in `references/`
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
- **The `guide` action and the `webflow://guides/interactions` resource are not live yet.** They are in review as `mcp-remote-cloudflare-server` #399. Until that ships, the `references/` files in this skill are the contract — do not try to call `guide` and do not wait for it. Once it is live, prefer it for payload shapes and use this skill for the workflow around them.
- `create_interaction` args: `name` (required), `scope` (optional, default site), `triggers` (required array), `timelines` (required array), optional `timelineDefaults`, optional `conditionalPlayback`
- **Component and variant scope work.** `{type:"component", componentId, variants?}` is accepted on create and update. `variants` holds variant **option ids** from `data_component_variants_tool` — omitting it or passing `[]` both mean every variant. Do not set `libraryProfileId`; it marks the interaction library-owned. A component or variant id that does not exist is rejected. See [references/envelope-and-targets.md](references/envelope-and-targets.md).

## Instructions

### Phase 1: Discovery

1. **Call `webflow_guide_tool` first** — always the first MCP tool call. Be clear
   about what it gives you: general MCP tool conventions, and **nothing about
   interactions**. Its response contains no occurrence of `interaction`, `ix3`,
   `wf:click`, or `scrollTrigger` today. Call it for the site/page/element
   conventions, then get the IX3 contract from `references/` — do not read its
   silence on interactions as "there is nothing to know."
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
15. **A successful write is not proof the animation runs.** Several legal payloads save, read back byte-identical, and do nothing: a `[from, to]` pair on a To tween, a class array that is not one combo chain, a mouse-move trigger with no target, `control: "reverse"` on a first click. `get_interaction` cannot detect any of them. Check the payload against the Guidelines below before reporting success, and if the user says nothing happens, start at [references/rejects-index.md](references/rejects-index.md) → "When there is nothing to decode" instead of rewriting the interaction.

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
          "tt": 2,
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

A FromTo holds its from-state at rest, so this element renders at **`opacity: 0` until the first click** — measured on a published page. That is what fading in means, but **tell the user**, because an element they cannot see reads as a failed write rather than a working interaction. If it should be visible before the click, animate a property whose rest value is already visible (an `x` offset, a colour) or use a To.

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
          "tt": 2,
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
          "tt": 2,
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

**Play-once variant (a reveal, not a scrub).** Drop `scrub` and `canvasDuration`, put `timing.duration` back in seconds — and **send `enter: "play"`**. The host stamps absent toggle keys on create and on trigger replacement (`enter: "play"`, the other three `"none"`) and leaves an explicit `"none"` alone, so an omission is repaired rather than left inert. Send `enter` anyway: it is what the panel writes, and it is correct on both sides of that rollout.

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
          "tt": 2,
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
          "tt": 2,
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

**No caveat needed any more.** An earlier version of this skill warned that the panel would not offer a remove button for either action group. That was true when written, and [webflow#117817](https://github.com/webflow/webflow/pull/117817) fixed it on 2026-08-19 — Remove now renders for this shape when a Hover owner exists. Confirmed in the Designer afterwards: a role-form hover authored through MCP animates correctly *and* shows a delete control on both Actions groups, the same as the split form.

The two-trigger split the panel prefers **is** authorable, but the discriminator
is **`config.pluginConfig.eventMode`**, with the values **`'enter'` / `'leave'`** —
not `mouseEnter`/`mouseLeave`, and **not** at `config` level, where it is silently
discarded (see the first Guidelines section). `eventMode` also requires a boolean
`multiTimeline` beside it, and the interaction needs `control: "play"` once it has
two or more action groups.

**Use `multiTimeline: false` on the split**, not `true`. The runtime branches on
that flag: `true` is two-group *role* mode, which emits `mouseEnter` / `mouseLeave`
role callbacks and is the role form above; `false` is single-group mode, where each
trigger drives its own group and `eventMode` gates which event binds
(`bindEnter = eventMode !== 'leave'`). The split routes by `groupId`, so it wants
`false`.

```json
"triggers": [
  {
    "extensionKey": "wf:hover",
    "config": {
      "control": "play",
      "assignedGroupId": "grp-in",
      "pluginConfig": { "multiTimeline": false, "eventMode": "enter" }
    },
    "target": { "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }
  },
  {
    "extensionKey": "wf:hover",
    "config": {
      "control": "play",
      "assignedGroupId": "grp-out",
      "pluginConfig": { "multiTimeline": false, "eventMode": "leave" }
    },
    "target": { "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }
  }
]
```

with `groupId: "grp-in"` / `"grp-out"` on the two timelines. `groupId` survives to
the host, and an `assignedGroupId` matching no timeline group is rejected rather
than stored inert. Note multi-timeline hover routes by timeline **role** first,
then by group.

**Both forms work, and neither costs the user anything measurable.** Verified
side by side in the Designer, both authored through MCP against the same element:
identical playback (`y` `0 → -24` on enter, `-24 → 0` on leave) and a delete
control on both action groups in **both** forms.

So this is a weak preference: **prefer the split form above**, because it is the
shape the panel writes itself and the user sees what they would have built by
hand. The role form (Example 4) is equally valid — the panel does not write it,
but it does edit it.

Earlier versions of this skill told agents to trade playback fidelity against a
missing remove button. There is no such tradeoff. See
[references/trigger-hover.md](references/trigger-hover.md).

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
          "tt": 2,
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
          "tt": 2,
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

### Example 6: Custom JS event

**User:** "Play this when my script fires an event"

Three non-obvious requirements, all mandatory:

1. The trigger target must be **`wf:body`** (`value: ""`). Any other key is rejected.
2. The event name lives at **`config.pluginConfig.eventName`**. At `config` level
   it is silently discarded and the trigger can never fire.
3. It is **not** a DOM `CustomEvent`. Dispatching one does nothing. The site fires
   it through the IX3 module.

```json
{
  "name": "Custom event flash",
  "triggers": [
    {
      "extensionKey": "wf:custom",
      "config": {
        "control": "play",
        "pluginConfig": { "eventName": "my-event" }
      },
      "target": { "extensionKey": "wf:body", "value": "" }
    }
  ],
  "timelines": [
    {
      "actions": [
        {
          "id": "act-custom-flash",
          "name": "Flash",
          "tt": 2,
          "timing": { "duration": 0.4 },
          "properties": { "wf:transform": { "opacity": ["100%", "20%"] } },
          "targets": [
            { "extensionKey": "wf:class", "value": ["STYLE_BLOCK_ID"] }
          ]
        }
      ]
    }
  ]
}
```

**Tell the user how to fire it.** This is the part that looks broken otherwise:

```js
const wfIx = Webflow.require('ix3');
wfIx.emit('my-event');
```

`emit` is the only firing method — the module exposes
`{getInstance, emit, destroy, ready, instance}`. There is no `trigger`, `dispatch`,
or `fire`. A non-string or whitespace-only `eventName` is rejected at the write
boundary; an **absent** one is accepted for backward compatibility and yields a
trigger that never fires. See [references/trigger-custom.md](references/trigger-custom.md).

## Guidelines

### Read this one first: unknown `config` keys are silently discarded

`triggerConfigSchema` is a non-strict Zod object, so **any key you put on
`trigger.config` that is not a declared field is dropped without an error.** The
write succeeds, the response looks clean, `get_interaction` round-trips
byte-identically, and your field is gone.

Declared `config` fields: `control`, `delay`, `jump`, `speed`, `controlType`,
`scrollTriggerConfig`, `pluginConfig`, `assignedGroupId`, `assignedTimelineRole`,
`conditionalLogic`.

**Everything plugin-specific goes inside `config.pluginConfig`** — `eventName`,
`eventMode`, `multiTimeline`, `smoothness`, and anything else a plugin defines.
Putting one of those at `config` level is the single most expensive mistake on
this surface, because nothing tells you:

```jsonc
// WRONG — silently discarded, trigger never fires
"config": { "eventName": "my-event" }
// RIGHT
"config": { "pluginConfig": { "eventName": "my-event" } }
```

A dogfood run lost three fields this way (`eventName`, `eventMode`, and a
mistyped `easing`) and misfiled all three as missing API features. If a field you
sent is absent from the response, assume you addressed it wrong before you
conclude it is unsupported.

### Easing: `timing.ease` is a number, not a string

`ease` is either a **non-negative integer index** into the built-in easing table
or an advanced-ease object. A string is rejected with a bare `Invalid input` that
does not tell you this.

| Index | Name | | Index | Name | | Index | Name |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | `none` (Linear) | | 11 | `power4.out` | | 22 | `elastic.in` |
| 1 | `power1.in` | | 12 | `power4.inOut` | | 23 | `elastic.out` |
| 2 | `power1.out` | | 13 | `back.in` | | 24 | `elastic.inOut` |
| 3 | `power1.inOut` | | 14 | `back.out` | | 25 | `expo.in` |
| 4 | `power2.in` | | 15 | `back.inOut` | | 26 | `expo.out` |
| 5 | `power2.out` | | 16 | `bounce.in` | | 27 | `expo.inOut` |
| 6 | `power2.inOut` | | 17 | `bounce.out` | | 28 | `sine.in` |
| 7 | `power3.in` | | 18 | `bounce.inOut` | | 29 | `sine.out` |
| 8 | `power3.out` | | 19 | `circ.in` | | 30 | `sine.inOut` |
| 9 | `power3.inOut` | | 20 | `circ.out` | | | |
| 10 | `power4.in` | | 21 | `circ.inOut` | | | |

The panel's "Power 1 out" is `2`; its "Linear" is `0`.

```json
"timing": { "duration": 0.4, "ease": 2 }
```

Advanced eases are objects discriminated on `type`. **Just write one** — no guard
rejects an advanced ease at the write boundary, and
`ff-styl-1612-ix3-advanced-easing` is public at 100% and classified stale, so it
gates the panel's Adaptive Easing control rather than the API:
`back {curve,power}`, `elastic {curve,amplitude,period}`, `steps {stepCount}`,
`rough {templateCurve,points,strength,taper,randomizePoints,clampPoints}`,
`slowMo {linearRatio,power,yoyoMode}`, `expoScale {startingScale,endingScale,templateCurve}`,
`customWiggle {wiggles,wiggleType}`, `customBounce {strength,squash,endAtStart}`,
`customEase {bezierCurve}`. `curve` is `in` / `out` / `inOut`.

```json
"timing": { "duration": 0.4, "ease": { "type": "back", "curve": "out", "power": 1.7 } }
```

`timing.stagger.ease` takes the same shape. A 4-number bezier array is **not**
accepted — use `{type: "customEase", bezierCurve: "..."}`.

### Class change: `wf:class`

One property, named `class`, Set-only (`tt: 3`):

```json
"tt": 3,
"properties": {
  "wf:class": {
    "class": { "operation": "addClass", "selectors": ["STYLE_BLOCK_ID"] }
  }
}
```

`operation` is `addClass` / `removeClass` / `toggleClass`. A bare array, a bare
string, or `{add: [...]}` are all rejected.

### `stagger` is an object

`{amount?, axis?, each?, ease?, from?, grid?}`. A bare number is rejected.

- `each` / `amount` — seconds, or a `"250ms"` string
- `axis` — `'x'` / `'y'`
- `ease` — the same index-or-object shape as `timing.ease`
- `from` — `'start' | 'center' | 'end' | 'edges' | 'random'`, a number, or `null`
- `grid` — `'auto'`, a `[columns, rows]` number pair, or `null`. `'none'` is rejected.

```json
"timing": { "duration": 0.5, "stagger": { "each": 0.05, "from": "start", "grid": [2, 2] } }
```

### `filterContext.relationship` enum

`none` · `within` · `direct-child-of` · `contains` · `direct-parent-of` ·
`next-to` · `next-sibling-of` · `prev-sibling-of`. CSS-flavoured guesses like
`descendants` are rejected.

### Target value shapes

| Key | Value |
| --- | --- |
| `wf:class` | style-block id array, or a class name string |
| `wf:inst` | **`[componentId, elementId]`** — for a page-level element the componentId slot is the **page id**. Which form is legal follows `scope`: component scope takes the component-definition id, site and pages scope require the page id |
| `wf:selector` | a CSS selector string, e.g. `"body"`. This is how you target the body from an action; `wf:body` is trigger-context-only |
| `wf:body`, `wf:viewport` | `""` — **trigger targets only** |
| `wf:any-element` | `"*"` — **not** `""`. Action targets only |
| `wf:trigger-only`, `wf:trigger-only-parent` | `""`. Action targets only |
| `wf:attribute` | an attribute name **or a full selector**. `"data-thing"` is stored as `[data-thing]` and matches every element carrying it; pass `'[data-thing="x"]'` when several elements share the attribute |
| `wf:id` | element DOM id |

**`wf:any-element` is the one key whose value is a wildcard, not a placeholder.**
The three action-only keys look interchangeable and are not: `""` on
`wf:any-element` is refused with `"wf:any-element" value must be "*"`. Because
these are usually authored one row per `filterContext` relationship, getting it
wrong loses the whole batch rather than one row.

`wf:inst` and `wf:trigger-only` reject an *active* `filterContext`; the stamped
`relationship: 'none'` placeholder is fine.

### Caps

Triggers per interaction **20** · timelines per interaction **5** · actions per
timeline **200** · targets per action **20** · `canvasDuration` **≤ 12s** ·
`groupId` **1–64 chars** · random-array sets **2–12 values** · IX3 value total
**65,536 bytes**.

**MCP applies these as Zod `.max()` on create *and* update.** The Designer host
raises the ceiling for already-stored over-cap interactions; MCP does not. So
reading a 200+-action timeline and resubmitting it to change one action **fails
over MCP**.

### Tool-schema errata

The `data_interactions_tool` JSON Schema currently describes
`conditionalPlayback` as `{"type": "object"}` with the example
`{reducedMotion:"skip"}`. **Both are wrong.** The server validator requires an
**array**; see the `conditionalPlayback` bullet below. Trust this skill over the
tool description on that field.

Also note `siteId`/`pageId` placement differs across the tool family: **top-level**
for `data_interactions_tool`, `data_style_tool`, and `data_element_tool`; nested
**`site_id` inside the action** for `data_pages_tool`, `data_assets_tool`, and
`data_agent_instructions_tool`.

### Everything else

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
- **A scroll without `scrub` needs `enter: "play"`.** The host stamps absent toggle keys on persist (`enter: "play"`, the rest `"none"`) and keeps an explicit `"none"`, but send `enter` yourself: the panel always writes all four toggles, and being explicit is correct regardless of where that stamp has rolled out. `scrollTriggerConfig` itself is never invented — missing or null is rejected.
- **Scroll scrub:** send numeric `scrub`, `canvasDuration: 1`, and action `timing.duration: 1`. A tiny duration occupies ~1% of the scroll range and looks like nothing happened.
- **`control: "reverse"` is a no-op on the first click** (the playhead starts at 0). For a reverse the user can try in Preview, use `togglePlayReverse` (`pluginConfig.click` omitted or `"each"`).
- **A To tween reads only its `to` slot.** `[from, to]` on `tt: 0` is half discarded and GSAP animates from the element's live value, so `scale: [0.55, 1.15]` on an unscaled element goes 1 → 1.15 and `opacity: ["20%","100%"]` on an opaque element does nothing at all. Use `tt: 2` whenever the animation needs a start value.
- **Do not put a click or hover trigger on an element its own from-state collapses** (`scaleX: 0`, `width: 0`). No box is left to click. Trigger on a parent and animate the child.
- **Grouped timelines are authorable.** `groupId` (1–64 characters) is accepted on the MCP timeline input, and `config.assignedGroupId` on a click or hover trigger routes to it. An `assignedGroupId` that matches no timeline `groupId` is rejected rather than stored inert, so mismatches surface as an error instead of a dead interaction. Load, scroll, and continuous triggers ignore `assignedGroupId`.
- **`wf:navbar` and `wf:dropdown` are not authorable, and neither are `wf:focus`, `wf:blur`, or `wf:change`.** The guards take no flag or session argument, so this holds for every caller regardless of Statsig state — no flag turns it on for you. Navbar and dropdown are registered in the Designer and excluded pending GA; focus, blur, and change have no Designer schema at all. Tell the user the trigger is unavailable rather than attempting a write. See [references/gated-capabilities.md](references/gated-capabilities.md).
- **No GSAP position operators** (`+=`, `<`, `>`) in `timing.position`. Use a finite number (seconds) or `'500ms'`.
- **Duration is seconds.** `timing.duration: 0.4` is 400ms. `400` is 400 seconds. Use `"400ms"` if you think in milliseconds.
- **From / FromTo (`tt: 1` / `2`) sit at the from-state until the trigger fires.** Prefer To (`tt: 0` or omit) when the element should be visible at rest.
- **`splitText` needs a target that already contains copy** — in itself or a descendant. The element *type* is not the constraint: a Block / Div whose text is a child node splits fine (verified on a published page: a `.pg-card` Block containing "Card one" produced two `gsap_split_word` spans). What fails silently is a target with no text anywhere inside it — that saves and animates nothing.
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
