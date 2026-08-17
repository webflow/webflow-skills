<!-- Published from the Webflow monorepo: packages/systems/ix3/schema/agent-pack/references/trigger-mouse-move.md
     Do not edit here. Edit the source and re-publish. -->

# `wf:mouse-move`

Read with [`envelope-and-targets.md`](envelope-and-targets.md).

|             |                                                                                                                                                 |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| controlType | `continuous` (omit and the host stamps it)                                                                                                      |
| Standalone  | **Yes** — must be the only trigger                                                                                                              |
| Target      | `[REQUIRED]` in practice — validation accepts none, the runtime binds nothing. `wf:viewport` with `value: ''`, or class/selector/attribute/inst |
| Roles       | `[REQUIRED]` on every timeline, unique                                                                                                          |
| Playback    | `[OMIT]` all of `control`, `delay`, `jump`, `speed`                                                                                             |

## Send a target even though validation does not demand one

Mouse-move is absent from `TRIGGER_REQUIRES_TARGET_KEYS`, so a targetless payload
passes every guard and saves cleanly. It then never fires.

`bindTrigger` only resolves elements when a target is present:

```ts
const targetSchema = trigger[2];
let elements: HTMLElement[] = [];
if (targetSchema) {
  elements = this.resolveTargets(targetSchema, {}, interaction);
}
```

`ContinuousTriggerStrategy.bind` iterates that list, so an empty one means the
mouse-move handler is never invoked. There is no fallback to the viewport, body, or
document: `wf:viewport` binds to `window` only because the handler checks for that
extension key explicitly.

The same dead outcome applies when a target is present but resolves to nothing, for
example `wf:class` with an empty value.

**Send `{extensionKey: 'wf:viewport', value: ''}` unless you specifically want to
bind to elements.** Nothing will tell you otherwise: the write succeeds and the
interaction is silently inert.

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

`[REJECTED]` Either field on a timeline whose role is not `interval`. The interval
editor is the only place the Designer writes them.
Guard: `findOffIntervalMetadataError` · fragment:
`only authored on interval mouse-move timelines`

`[LEGACY-OK-ON-UPDATE]` An unchanged echo of a stored value on the same timeline id
passes, so a duration or target read-modify-write is not forced to strip it.

`[REJECTED]` Interval metadata on an interaction with no `wf:mouse-move` trigger.
Guard: `findIntervalMetadataTriggerError` · fragment:
`not write them without a "wf:mouse-move" trigger`

`[REJECTED]` A `distance` that is fractional, or outside 1 to 10000. Bounded in
`triggerMetadata`'s schema as `z.number().finite().int().min(1).max(10000)`, so
this fails schema validation before any guard runs. The bound exists to keep a
malicious payload from persisting `Infinity` or `NaN` into storage; the runtime
caps fires per update regardless.

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
