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
    config: {pluginConfig: {multiTimeline: false}},
    target: {extensionKey: 'wf:class', value: [STYLE_BLOCK_ID]},
  }],
  timelines: [{actions: [ACTION]}],
}
```

**Send `multiTimeline: false` explicitly.** `HoverTriggerInput` decides which editor
to show with `typeof config?.multiTimeline === 'boolean'`, and the schema seeds the
boolean at creation. Omitting it puts the interaction on the legacy path, which
defaults `type` to `mouseenter` and makes the panel treat the data as legacy,
hiding "Add separate hover out". An empty `config` therefore produces an
enter-only interaction the user cannot extend, not the editable single-timeline one
this example is meant to show.

On a read-then-write, preserve whichever model the stored data already uses rather
than adding the discriminator to legacy data.

## Accept — separate hover out

Two shapes reach the runtime here and they are not equivalent. **Prefer the split
form**, because it is the one the panel produces and the one the panel can edit
afterwards.

### Split form — what the panel writes

"Add separate hover out" dispatches a trigger split: the panel writes **two**
`wf:hover` triggers distinguished by `pluginConfig.eventMode`, each pinned to an
action group, with `multiTimeline: false` on both.

```js
{
  pageId,
  name: 'Hover in/out',
  triggers: [
    {
      extensionKey: 'wf:hover',
      config: {
        control: 'play',
        assignedGroupId: GROUP_IN,
        pluginConfig: {multiTimeline: false, eventMode: 'enter'},
      },
      target: {extensionKey: 'wf:class', value: [STYLE_BLOCK_ID]},
    },
    {
      extensionKey: 'wf:hover',
      config: {
        control: 'play',
        assignedGroupId: GROUP_OUT,
        pluginConfig: {multiTimeline: false, eventMode: 'leave'},
      },
      target: {extensionKey: 'wf:class', value: [STYLE_BLOCK_ID]},
    },
  ],
  timelines: [
    {groupId: GROUP_IN, name: 'Hover in actions', actions: [ACTION]},
    {groupId: GROUP_OUT, name: 'Hover out actions', actions: [ACTION2]},
  ],
}
```

`control: 'play'` is not optional once two groups exist — see
`findGroupedTriggerControlError` in
[`timelines-and-groups.md`](timelines-and-groups.md).

### Role form — accepted, but leaves groups the panel cannot remove

```js
triggers: [{
  extensionKey: 'wf:hover',
  config: {pluginConfig: {multiTimeline: true}},
  target: {extensionKey: 'wf:class', value: [STYLE_BLOCK_ID]},
}],
timelines: [
  {triggerMetadata: {role: 'mouseEnter'}, actions: [ACTION]},
  {triggerMetadata: {role: 'mouseLeave'}, actions: [ACTION2]},
],
```

`[PANEL-TRAP]` The host accepts this and the runtime honors it, but the panel never
writes it for hover and cannot fully edit the result. The remove control keys off
`groupId` (absent here) or a `groupRoles` config, and hover declares `triggerSplit`
instead of `groupRoles` — so neither action group offers a remove button.

Use it only to read or preserve data that already stores it. Do not author it for a
new hover in/out.

Roles are exactly `'mouseEnter'` and `'mouseLeave'` and must be unique per timeline.
Guard: `findTimelineRoleError`

## Legacy pass-through

`[REJECTED]` `pluginConfig.type: 'mouseover'` on create. The Designer's Type
dropdown only offers mouseenter and mouseleave, so the panel cannot produce it.
Guard: `findHoverConfigModelError`

`[LEGACY-OK-ON-UPDATE]` A stored `mouseover` hover survives an update. The
allowance is counted one-for-one against the `wf:hover` triggers the stored
interaction already carried, so you cannot use one stored `mouseover` to authorize
a second. A non-hover trigger cannot inherit the allowance either.

Pass a stored `mouseover` through untouched. Do not author a new one.

## Rejected

`[REJECTED]` No target. Hover is in `TRIGGER_REQUIRES_TARGET_KEYS`, so the
missing-target branch in `findTriggerInvariantError` refuses it.
Fragment: `requires a target element`

Otherwise the same target and playback rejects as
[`trigger-click.md`](trigger-click.md).
