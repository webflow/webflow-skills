<!-- Published from the Webflow monorepo: packages/systems/ix3/schema/agent-pack/references/trigger-mouse-move.md
     Do not edit here. Edit the source and re-publish. -->

# `wf:mouse-move`

Read with [`envelope-and-targets.md`](envelope-and-targets.md).

|             |                                                                                         |
| ----------- | --------------------------------------------------------------------------------------- |
| controlType | `continuous` (omit and the host stamps it)                                              |
| Standalone  | **Yes** — must be the only trigger                                                      |
| Target      | `wf:viewport` with `value: ''` recommended; class/selector/attribute/inst also accepted |
| Roles       | `[REQUIRED]` on every timeline, unique                                                  |
| Playback    | `[OMIT]` all of `control`, `delay`, `jump`, `speed`                                     |

## Roles

Exactly `'mouseX'`, `'mouseY'`, or `'interval'`.

| Role                | `canvasDuration` | `wf:mouse-follow` action          |
| ------------------- | ---------------- | --------------------------------- |
| `mouseX` / `mouseY` | allowed          | allowed, at most one per timeline |
| `interval`          | not allowed      | not allowed                       |

## Accept

```js
{
  pageId,
  name: 'Mouse',
  triggers: [{
    extensionKey: 'wf:mouse-move',
    config: {},  // optional pluginConfig: {restingState: {x: 0, y: 0}}
    target: {extensionKey: 'wf:viewport', value: ''},
  }],
  timelines: [
    {triggerMetadata: {role: 'mouseX'}, actions: [ACTION]},
    {triggerMetadata: {role: 'mouseY'}, actions: [ACTION2]},
  ],
}
```

## Interval metadata

`distance` and `axes` are authored only on an `interval` timeline.

`[PENDING]` Either field on a timeline whose role is not `interval`. Part of
DES-7448, **not on `dev` yet** — today the write may succeed silently.
Guard once landed: `findOffIntervalMetadataError` · fragment:
`distance and axes are only authored on interval`

`[PENDING]` Interval metadata on an interaction with no mouse-move trigger. Same
ticket, same status.
Guard once landed: `findIntervalMetadataTriggerError`

`[PANEL-TRAP]` `distance` is clamped by the panel to 1–10000 and rounded, but the
write path has no numeric bound. A value outside that range is stored and then
silently rewritten the next time the user edits the field.

## Rejected

`[REJECTED]` A missing, duplicate, or invalid role on any timeline.
Guard: `findTimelineRoleError` · fragment: `Expected one of: mouseX, mouseY, interval`

`[REJECTED]` Combined with any other trigger.
Guard: `findStandaloneTriggerError`

`[REJECTED]` Any of `control`, `delay`, `jump`, `speed`.
Guard: `findUneditablePlaybackFieldError`

`[REJECTED]` `wf:viewport` as a target on any trigger other than mouse-move.

`[REJECTED]` A `wf:mouse-follow` action outside a mouseX/mouseY timeline, or more
than one per timeline. Guard: `findMouseFollowContextError`

`[REJECTED]` `conditionalLogic` — conditions are unavailable and continuous
triggers are additionally excluded.
Guards: `findConditionsCapabilityError`, `findContinuousConditionsError`

`[REJECTED]` `conditionalPlayback` with `behavior: 'skip-to-end'` while a
continuous trigger is present. Use `dont-animate`.
Guard: `findConditionalPlaybackError`

## Panel trap

`[PANEL-TRAP]` `timing.repeat` and `timing.yoyo` are hidden by the panel on a
continuous interaction, but only the **scroll-scrub** variant is rejected by the
write path — `findScrollScrubActionTimingError` keys off scrub, not continuous. A
value set here is stored, ignored by the runtime, and invisible in the panel.
