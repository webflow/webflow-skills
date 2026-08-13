<!-- Published from the Webflow monorepo: packages/systems/ix3/schema/agent-pack/references/conditional-playback.md
     Do not edit here. Edit the source and re-publish. -->

# `conditionalPlayback`

Interaction-level field. **This is authorable.** Do not confuse it with
trigger-level `conditionalLogic`, which is gated off entirely — see
[`gated-capabilities.md`](gated-capabilities.md).

## Shape

An **array** of rule objects, not a keyed object:

```js
conditionalPlayback: [
  {type: 'prefers-reduced-motion', behavior: 'dont-animate'},
];
```

Two forms:

```js
{type: 'prefers-reduced-motion', behavior: 'dont-animate' | 'skip-to-end'}
{type: 'breakpoint', breakpoints: ['main' | 'medium' | 'small' | 'tiny'], behavior}
```

A shape like `{reducedMotion: 'skip'}` is not the wire format and has never been.

On update, `null` clears the field; omitting it leaves the stored value alone.

## Rejected

`[REJECTED]` Duplicate condition `type` values in the list.
Guard: `findConditionalPlaybackError`

`[REJECTED]` `behavior: 'skip-to-end'` while a continuous trigger
(`wf:mouse-move`) is present. Use `dont-animate` instead.

`[LEGACY-OK-ON-UPDATE]` The duplicate-type check is skipped on the update path
when the field is not being replaced, so stored data with duplicates is not forced
through a migration.

## A deliberate carve-out

Scroll scrub is **not** covered by the skip-to-end restriction. The panel's own
filter checks `controlType === 'continuous'` only, and still offers `skip-to-end`
on scroll. The guard matches that deliberately, so the API is not stricter than
the panel.

Read that as the guard stopping where the panel stops, not as an oversight. If a
future change tightens it, this note becomes incomplete rather than wrong.
