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

## Which model the panel creates depends on a flag

Both models are accepted by the write path, and this page documents both. But which
one a _new_ hover gets in the panel is gated:
`defaultValue: {multiTimeline: false}` is only registered when
`isMultiTimelineHoverEnabled` is true, and that flag ships off today. With it off, a
hover created in the panel stays legacy and carries no `multiTimeline` key.

The affordance _registrations_ are not gated: `isMultiTimelineFor`,
`timelineGroupConfig`, and `triggerSplit` are declared unconditionally so a hover
already persisted as new-model keeps its enter/leave split flow after the flag rolls
off.

But a **second** flag, `IX3_TIMELINE_GROUPS`, gates both "add group" entry points in
the panel. That splits editability in two, and the distinction matters:

| Stored shape                          | `IX3_TIMELINE_GROUPS` off                                                                                                                                                 |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| New-model hover with **one** timeline | Cannot gain a separate hover out. The add button is not rendered.                                                                                                         |
| An existing **two-group** split       | Still editable, renameable, and removable. The remove control stays reachable on purpose so a rollback does not strand authors in a multi-timeline view they cannot exit. |

So authoring a single-timeline new-model hover through the API can produce something
the user cannot extend in the panel, depending on a flag you cannot see from the
payload. Authoring the full split avoids that, because two groups keep their
controls either way.

Practical guidance:

- **Read-modify-write: preserve the stored model.** Never add `multiTimeline` to
  legacy data or strip it from new-model data. Changing the discriminator moves the
  interaction between editors.
- **Creating something new:** the new model is the better shape and stays editable,
  but be aware it is not what a flag-off panel would have produced for that user. If
  matching the shipping panel exactly matters more than the enter/leave split, author
  legacy.

Flag state is not visible in the payload, so no rule here can decide this for you.

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

**Send `multiTimeline: false` explicitly to get this model.**
`HoverTriggerInput` decides which editor to show with
`typeof config?.multiTimeline === 'boolean'`. Omitting the key puts the interaction
on the legacy path, which defaults `type` to `mouseenter` and hides "Add separate
hover out", so an empty `config` produces an enter-only interaction the user cannot
extend rather than the editable single-timeline one this example is for.

Note the flag caveat above: the panel only seeds this boolean itself when
`isMultiTimelineHoverEnabled` is on. Authoring it explicitly is what puts new data on
the new model regardless.

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
