<!-- Published from the Webflow monorepo: packages/systems/ix3/schema/agent-pack/references/trigger-click.md
     Do not edit here. Edit the source and re-publish. -->

# `wf:click`

Read with [`envelope-and-targets.md`](envelope-and-targets.md).

|             |                                                    |
| ----------- | -------------------------------------------------- |
| controlType | `standard` (omit and the host stamps it)           |
| Standalone  | No — may share an interaction with other triggers  |
| Target      | `[REQUIRED]` — class, selector, attribute, or inst |
| Roles       | None                                               |
| Playback    | `control`, `delay`, `jump`, `speed` allowed        |

## Accept

```js
{
  pageId,
  name: 'Click',
  triggers: [{
    extensionKey: 'wf:click',
    config: {control: 'play'},
    target: {extensionKey: 'wf:class', value: [STYLE_BLOCK_ID]},
  }],
  timelines: [{actions: [ACTION]}],
}
```

Action targets may use `wf:trigger-only` here, unlike load and custom.

## Control

The allowed set depends on `pluginConfig.click`. Generated table:
[`capabilities.generated.md`](capabilities.generated.md) → Triggers.

`none` is never offered — a click always does something.

When `pluginConfig.click` is anything other than `'each'` (first, odd, even, or a
count), the trigger fires at most once per state, so the toggle controls have
nothing to alternate between and are also dropped.

`[REJECTED]` A control outside the trigger's allowed set.
Guard: `findTriggerControlAllowedError`

## Rejected

`[REJECTED]` No target. Guard: `findTriggerTargetContextError`

`[REJECTED]` Target `wf:body` or `wf:viewport` — those are trigger-context keys
for other triggers, not click.

`[REJECTED]` `scrollTriggerConfig` on a click trigger. Guard:
`findScrollTriggerError` · fragment: `must not set "scrollTriggerConfig"`

`[REJECTED]` `jump` when `control` is `none`, `restart`, `resume`,
`togglePlayReverse`, or `togglePlayReverseFlipEase` — the panel clears it for
those. Guard: `findTriggerJumpError` · fragment: `must not set a jump when control is`

`[REJECTED]` `speed` when `control` is `pause`, `stop`, or `none`.
Guard: `findTriggerSpeedError`

`[REJECTED]` Any `control` other than `play` once the interaction has two or more
grouped timelines. The panel offers only Play there.
Guard: `findGroupedTriggerControlError` · fragment:
`must use control "play" when the interaction has multiple action groups`

See [`timelines-and-groups.md`](timelines-and-groups.md) for what counts as a
group.

## Note

`reverseFlipEase` is in the accepted control set but the panel filters it out of
the default dropdown as a guard against stale-CDN GSAP versions that silently
ignore the `easeReverse` tween var. Prefer not to author it.
