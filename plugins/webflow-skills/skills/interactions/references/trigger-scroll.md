<!-- Published from the Webflow monorepo: packages/systems/ix3/schema/agent-pack/references/trigger-scroll.md
     Do not edit here. Edit the source and re-publish. -->

# `wf:scroll`

Read with [`envelope-and-targets.md`](envelope-and-targets.md).

|                       |                                                               |
| --------------------- | ------------------------------------------------------------- |
| controlType           | `scroll` (omit and the host stamps it)                        |
| Standalone            | **Yes** — must be the only trigger on the interaction         |
| Target                | `[REQUIRED]` — class, selector, attribute, inst, or `wf:body` |
| `scrollTriggerConfig` | `[REQUIRED]` — object with `start` and `end`                  |
| Roles                 | None. A scrub percent timeline must be roleless.              |
| Playback              | `[OMIT]` all of `control`, `delay`, `jump`, `speed`           |

Both the target and the config are schema-optional but the Designer always writes
them. Without them the runtime resolves nothing and `ScrollTriggerStrategy.bind`
bails.

## Accept — minimal

```js
{
  pageId,
  name: 'Scroll',
  triggers: [{
    extensionKey: 'wf:scroll',
    config: {
      scrollTriggerConfig: {start: 'top 90%', end: 'bottom 25%'},
    },
    target: {extensionKey: 'wf:body', value: ''},
  }],
  timelines: [{actions: [ACTION]}],
}
```

## Accept — scrub with a percent canvas

```js
config: {
  scrollTriggerConfig: {
    start: 'top top',
    end: 'bottom bottom',
    scrub: 0.5,
    // pin: true | false
    // horizontal: false
  },
},
timelines: [{canvasDuration: 1, actions: [ACTION]}],  // no role
```

With scrub on, action `timing` is authored as a percent of the canvas rather than
in seconds. See [`timelines-and-groups.md`](timelines-and-groups.md).

### `scrub` takes a number, not a boolean

`scrub: z.number().nonnegative().nullable().optional()`.

| Form               | Meaning                       |
| ------------------ | ----------------------------- |
| omitted, or `null` | no scrubbing                  |
| `0`                | 1:1 scrubbing, no smoothing   |
| a positive number  | smoothing duration in seconds |

`[REJECTED]` at schema: `scrub: true` or `scrub: false`. A boolean is the shape
GSAP takes and the shape the panel's toggle suggests, so it is an easy payload to
reach for, but the schema refuses it before any guard runs. Use `0` to enable
without smoothing and omit the key to disable.

The JSDoc above the field still describes the old boolean behavior (`true` for 1:1,
`false` for off). The schema is the contract; that comment is stale.

`scrub != null` is also the predicate that makes a timeline scroll-scrub for
`findPercentTimelineError` and `findScrollScrubActionTimingError`, so `scrub: 0`
counts as scrubbing while an omitted `scrub` does not.

## What the panel writes

`IX3ScrollTriggerConfig` authors `start`, `end`, `scrub`, `showMarkers`, `clamp`,
the enter/leave/enterBack/leaveBack toggle actions, and `pin` as a boolean
checkbox. Nothing else.

## Rejected

`[REJECTED]` Missing trigger target.
Guard: `findScrollTriggerError` · fragment: `requires a trigger target`

`[REJECTED]` Missing, null, or non-object `scrollTriggerConfig`.
Fragments: `requires a "scrollTriggerConfig"` / `must be an object`

`[REJECTED]` `scrollTriggerConfig` on any non-scroll trigger. Publish-time target
collection walks `pin`/`endTrigger`/`scroller` without checking the trigger key, so
a click carrying that config would stamp `data-wf-target` and change published
behavior the panel can neither show nor clear.
Fragment: `must not set "scrollTriggerConfig"`

The next four have no exported constant behind them — they live inside
`findScrollTriggerConfigError`. If you are verifying this file, read that function
directly.

`[REJECTED]` `endTrigger`. The panel ends the scroll range on the trigger element
itself. Fragment: `endTrigger is not offered by the Designer`

`[REJECTED]` `scroller`. Scroll interactions always track the page scroller.
Fragment: `scroller is not offered by the Designer`

`[REJECTED]` `horizontal: true`. The panel only authors vertical ranges.
`horizontal: false` **is** accepted, because the panel's default config persists it
on the next edit. Fragment: `horizontal is not offered by the Designer`

`[REJECTED]` A non-boolean `pin` (for example a target tuple). The checkbox pins
the trigger element itself and cannot name another one; a tuple renders as a
checked box the user cannot restore.
Fragment: `pin must be a boolean`

`[REJECTED]` Combined with any other trigger.
Guard: `findStandaloneTriggerError` · fragment: `cannot be combined with other triggers`

`[REJECTED]` Any of `control`, `delay`, `jump`, `speed`. The panel shows no
playback settings for scroll, so the value could never be edited or cleared.
Guard: `findUneditablePlaybackFieldError` · fragment:
`the Designer shows no playback settings for it`

`[REJECTED]` Action `timing.repeat` or `timing.yoyo` while scrub is on. The runtime
ignores them in scrub mode and the panel clears them when scrub is enabled.
Guard: `findScrollScrubActionTimingError` · fragment:
`cannot be set on a scroll-scrub interaction`

`[REJECTED]` `canvasDuration` without scrub, or on a timeline that carries a role.
Guard: `findPercentTimelineError`

## Panel trap

`[PANEL-TRAP]` On a page-target scroll, the panel silently refuses a start offset
greater than the end offset — the change is dropped with no error. The write path
has no equivalent guard, so an API caller can store a start past its end and the
panel will show a state it would never have produced.
