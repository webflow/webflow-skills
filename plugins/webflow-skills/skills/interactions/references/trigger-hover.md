<!-- Published from the Webflow monorepo: packages/systems/ix3/schema/agent-pack/references/trigger-hover.md
     Do not edit here. Edit the source and re-publish. -->

# `wf:hover`

Read with [`envelope-and-targets.md`](envelope-and-targets.md).

|             |                                                    |
| ----------- | -------------------------------------------------- |
| controlType | `standard`                                         |
| Standalone  | No                                                 |
| Target      | `[REQUIRED]` — class, selector, attribute, or inst |
| Roles       | Required only in multi-timeline mode               |
| Playback    | Allowed, same rules as click                       |

## Pick one config model

Hover is the only trigger with two mutually exclusive `pluginConfig` shapes. Mixing
them is refused.

| Model  | Fields                                         | Must not also send        |
| ------ | ---------------------------------------------- | ------------------------- |
| New    | `multiTimeline: boolean`, optional `eventMode` | `type`, `hover`, `custom` |
| Legacy | `type`, `hover`, optional `custom`             | boolean `multiTimeline`   |

Prefer the new model. Guard: `findHoverConfigModelError`

`[REJECTED]` Boolean `multiTimeline` alongside any legacy field.

`[REJECTED]` `eventMode` without a boolean `multiTimeline`.

`[REJECTED]` A timeline with no role, or a role outside the registered set, once
`multiTimeline: true` is set. Note the guard checks the timelines you send, not the
full set: a single `mouseEnter` timeline is accepted, so an enter-only hover is
legal and you do not need to invent a second timeline to satisfy validation.
Guard: `findTimelineRoleError`

## Accept — single timeline

```js
{
  pageId,
  name: 'Hover',
  triggers: [{
    extensionKey: 'wf:hover',
    config: {},
    target: {extensionKey: 'wf:class', value: [STYLE_BLOCK_ID]},
  }],
  timelines: [{actions: [ACTION]}],
}
```

## Accept — enter and leave

```js
{
  pageId,
  name: 'Hover in/out',
  triggers: [{
    extensionKey: 'wf:hover',
    config: {pluginConfig: {multiTimeline: true}},
    target: {extensionKey: 'wf:class', value: [STYLE_BLOCK_ID]},
  }],
  timelines: [
    {triggerMetadata: {role: 'mouseEnter'}, actions: [ACTION]},
    {triggerMetadata: {role: 'mouseLeave'}, actions: [ACTION2]},
  ],
}
```

Roles are exactly `'mouseEnter'` and `'mouseLeave'`, and each must be unique across
timelines. Both are shown here because a hover in and out is the common request,
not because the guard demands the pair. Guard: `findTimelineRoleError`

## Legacy pass-through

`[PENDING]` `pluginConfig.type: 'mouseover'`. The Designer's Type dropdown only
offers mouseenter and mouseleave, so `mouseover` is not something the panel can
produce. The rejection — and the matching allowance that lets an already-stored
`mouseover` survive an unrelated update — are part of DES-7448 and are **not on
`dev` yet**, so today the write may succeed silently.

Do not author it. When reading an interaction that already stores it, pass it
through untouched rather than rewriting it.

Guard once landed: `findHoverConfigModelError` (scoped allowance on the update path)

## Rejected

Same target and playback rejects as [`trigger-click.md`](trigger-click.md).
