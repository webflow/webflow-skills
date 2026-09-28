---
name: webflow-designer-api:interactions
description: Create and edit Webflow interactions from Designer Extension code with webflow.interactions. Use when writing TypeScript that calls create, set, get, getAll, or remove, or that builds click, hover, page load, scroll, mouse move, or custom event timelines, targets, and action properties.
---

# Interactions in a Designer Extension

If you are changing interactions with Webflow MCP, use the `webflow-mcp:interactions` skill instead of this one.

You are writing TypeScript for a Designer Extension. The methods are `webflow.interactions.get`, `getAll`, `create`, `set`, and `remove`. This surface has no `update` and no `delete`.

`value`, `properties`, `pluginConfig`, and `triggerMetadata` are open in the typings. A misspelled field still typechecks. After every write, read the interaction back with `get` and compare it with what you sent.

Reference:

- [Interactions](https://developers.webflow.com/designer/reference/interactions-overview)
- [Get all interactions](https://developers.webflow.com/designer/reference/get-all-interactions)
- [Get interaction](https://developers.webflow.com/designer/reference/get-interaction)
- [Create interaction](https://developers.webflow.com/designer/reference/create-interaction)
- [Set interaction](https://developers.webflow.com/designer/reference/set-interaction)
- [Remove interaction](https://developers.webflow.com/designer/reference/remove-interaction)

Per-trigger examples and the field rules live in [references/index.md](references/index.md).

## Workflow

### 1. Check that the user can change interactions

Writes need the Designer Ability `canModifyInteractions`: any locale, the main branch, the canvas workflow, and Design mode. Reads need `canReadInteractions`: any locale, the main branch, any workflow, and any mode.

Before `get` or `getAll`:

```ts
const ability = await webflow.canForAppMode([
  webflow.appModes.canReadInteractions,
  webflow.appModes.canModifyInteractions,
]);

if (!ability.canReadInteractions) {
  throw new Error('This user cannot read interactions in the current Designer mode.');
}
```

Before `create`, `set`, or `remove`:

```ts
const ability = await webflow.canForAppMode([
  webflow.appModes.canReadInteractions,
  webflow.appModes.canModifyInteractions,
]);

if (!ability.canModifyInteractions) {
  throw new Error('This user cannot change interactions in the current Designer mode.');
}
```

A write the user cannot make fails with `User does not have permission to modify interactions.` A read fails with `User does not have permission to access interactions.`

### 2. Get the current page

```ts
const page = await webflow.getCurrentPage();
```

`page.id` is the `pageId` you pass to `create`, and the page id inside a pages scope and a `wf:inst` pair.

### 3. Resolve class targets

`wf:class` accepts a class slug string or a non-empty array of style-block ids. A slug is saved only when it matches exactly one class on the site.

```ts
const style = await webflow.getStyleByName('hero-btn');
```

`getStyleByName` returns one style or `null`. When a slug might match more than one class, list styles with `webflow.getAllStyles()` and pass the style-block id array. Zero matches fails with `wf:class value "hero-btn" does not match a style block on this site.` More than one match fails with `wf:class value "hero-btn" matches multiple style blocks; use a style-block id array instead.`

### 4. Build the payload and call `create`

`pageId` belongs on the create argument. Omitting `scope` stores `{type: 'site'}`, so the interaction runs on every page. It does not limit the interaction to `pageId`. Pass a pages scope to keep it on the current page.

```ts
const page = await webflow.getCurrentPage();
const created = await webflow.interactions.create({
  pageId: page.id,
  name: 'Fade in on click',
  scope: {type: 'pages', value: [page.id]},
  triggers: [
    {
      extensionKey: 'wf:click',
      config: {control: 'play'},
      target: {extensionKey: 'wf:class', value: 'hero-btn'},
    },
  ],
  timelines: [
    {
      name: 'Fade',
      actions: [
        {
          id: 'fade',
          name: 'Fade',
          tt: 2,
          timing: {duration: 0.4, ease: 2},
          properties: {'wf:transform': {opacity: ['0%', '100%']}},
          targets: [{extensionKey: 'wf:class', value: 'hero-btn'}],
        },
      ],
    },
  ],
});
```

Omit keys whose value is `undefined`. Sending `undefined` can leave the call pending. Do not send `timelineDefaults`.

Open the matching file in [references/index.md](references/index.md) before you pick a trigger. Each file has one complete example.

### 5. Read the result back with `get`

Pass `created.id` from `create`.

```ts
async function readInteraction(id: string) {
  const saved = await webflow.interactions.get(id);
  if (saved) {
    console.log(saved.name, saved.timelines.length);
  }
  return saved;
}
```

`get` returns `null` when the id is missing. A resolved `create` means the call was accepted. It does not mean every field you sent was stored. Compare `saved` with the payload. Expect these rewrites, and treat any other missing field as a mistake:

- A class slug comes back as a style-block id array. A combo class includes its parent ids.
- A bare attribute name comes back as `[name]`.
- `"500ms"` comes back as `0.5`. `delay: null` comes back as `0.25`.
- An omitted filter comes back as `{relationship: 'none', filterBy: ['wf:class', []], firstMatchOnly: false}`.

The full list is in [references/traps.md](references/traps.md).

### 6. Edit with `set` and delete with `remove`

`set` leaves omitted keys unchanged, replaces provided keys, and accepts `null` for `conditionalPlayback` and `timelineDefaults`. A `timelines` array replaces the whole set. Keep the `id` of every timeline you still want. Omit the id only when you want a new timeline.

Pass `created.id` from `create`.

```ts
async function renameAndRemove(id: string) {
  const existing = await webflow.interactions.get(id);
  if (!existing) return;
  await webflow.interactions.set({
    id: existing.id,
    name: 'Fade in (slower)',
  });
  await webflow.interactions.remove(existing.id);
}
```

Removing an already deleted interaction succeeds and returns `{deleted: true}`. Removing an id that never existed fails. If a write fails with `The write may or may not have been applied; read the interaction before retrying.`, call `get` before you try again.

### 7. Check the result in Preview or on the published page

Ask the user to play the interaction in Preview, or on the published page. `hidden: true` on an action excludes that action from both. `getAll` returning a row does not prove the animation is visible.

## What a write accepts

Trigger `extensionKey`: `wf:click`, `wf:hover`, `wf:load`, `wf:scroll`, `wf:custom`, `wf:mouse-move`.

Action property keys: `wf:transform`, `wf:style`, `wf:class`, `wf:lottie`, `wf:spline`, `wf:mouse-follow`, `wf:variable`, `wf:rive`, `wf:animate-rive`.

Property names, tween types, ease, stagger, split text, class changes, and variable and Rive actions are in [references/actions.md](references/actions.md). Target shapes are in [references/targets.md](references/targets.md).

`getAll()` lists IX3 interactions on the site. `getAll({pageId: page.id})` lists the ones visible on that page, including site-wide interactions. `getAll` does not return Classic Interactions. An empty list is not proof the site has no motion. `getAll({pageId: ''})` returns no rows. Pass a real page id.

## What a write does not accept

These trigger types fail on every `create` and on every `set` that includes `triggers`:

- `wf:navbar`
- `wf:dropdown`
- `wf:focus`
- `wf:blur`
- `wf:change`
- Any other `extensionKey`

These options fail on every write that includes them:

- `conditionalLogic` on a trigger. Use `conditionalPlayback` for reduced motion and breakpoints. See [references/traps.md](references/traps.md).
- `assignedTimelineRole` on a trigger you are adding. Route a trigger with `assignedGroupId` and a matching timeline `groupId`.
- A `timelineDefaults` object. Omit it on `create`. On `set`, omit it to keep a stored value, or pass `null` to clear it.
- `scrollTriggerConfig` on any trigger other than `wf:scroll`.
- `endTrigger`, `scroller`, and `horizontal: true` inside `scrollTriggerConfig`. `pin` is a boolean when you set it.
- `control`, `delay`, `jump`, and `speed` on `wf:scroll` and `wf:mouse-move`.
- A target, or any `pluginConfig` key, on `wf:load`.
- `wf:id` as a target. Use `wf:selector`, `wf:class`, or `wf:inst`.
- `timing.delay` on an action. Sequence with `timing.position`, or put delay on the trigger or on `timeline.settings`.
- `autoReverse`. Use `repeat` and `yoyo`, or a second action for the reverse.
- `actionPresetIds`, `previewSpeed`, `playInReverse`, and `immediate` on a timeline.
- `duration`, `ease`, `repeatDelay`, `stagger`, and `position` on `timeline.settings`.
- A second `wf:load` trigger, or a `wf:scroll` or `wf:mouse-move` trigger combined with any other trigger.
- More than 20 triggers, 5 timelines, 200 actions on one timeline, or 20 targets on one action. The target error tells you to use a class or selector target.

## Traps

Three groups, with the error text and the fix, are in [references/traps.md](references/traps.md).

- **Rejected with an error.** The call throws. Fix the payload and send it again.
- **Accepted but changed.** The call resolves, and `get` is missing a field you sent or has rewritten it. The usual cause is a plugin field placed on `config` instead of `config.pluginConfig`. `config: {eventMode: 'leave'}` saves without `eventMode`.
- **Saved but never animates.** `get` matches the stored interaction, and Preview does not move. A custom event with no `eventName`, an action with `hidden: true`, and an ease index above 30 are in this group.

## References

| File | Open it for |
| --- | --- |
| [references/index.md](references/index.md) | Which file to open |
| [references/trigger-click.md](references/trigger-click.md) | Click |
| [references/trigger-hover.md](references/trigger-hover.md) | Hover enter and leave |
| [references/trigger-load.md](references/trigger-load.md) | Page load |
| [references/trigger-scroll.md](references/trigger-scroll.md) | Scroll, play once and scrub |
| [references/trigger-mouse-move.md](references/trigger-mouse-move.md) | Mouse move |
| [references/trigger-custom.md](references/trigger-custom.md) | Custom event and the page code that fires it |
| [references/actions.md](references/actions.md) | Action properties, tweens, ease, stagger, split text, class, variable, Rive |
| [references/targets.md](references/targets.md) | Target values and filters |
| [references/traps.md](references/traps.md) | Errors, dropped fields, and animations that never play |
