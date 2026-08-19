<!-- Published from the Webflow monorepo: packages/systems/ix3/schema/agent-pack/references/trigger-scroll.md
     Do not edit here. Edit the source and re-publish. -->

# `wf:scroll`

Read with [`envelope-and-targets.md`](envelope-and-targets.md).

|                       |                                                                    |
| --------------------- | ------------------------------------------------------------------ |
| controlType           | `scroll` (omit and the host stamps it)                             |
| Standalone            | **Yes** — must be the only trigger on the interaction              |
| Target                | `[REQUIRED]` — class, selector, attribute, inst, or `wf:body`      |
| `scrollTriggerConfig` | `[REQUIRED]` — object with `start` and `end`                       |
| `enter`               | `[REQUIRED]` in practice without scrub — omit it and nothing plays |
| Roles                 | None. A scrub percent timeline must be roleless.                   |
| Playback              | `[OMIT]` all of `control`, `delay`, `jump`, `speed`                |

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
      scrollTriggerConfig: {
        start: 'top 90%',
        end: 'bottom 25%',
        enter: 'play', // without this the timeline never plays
      },
    },
    target: {extensionKey: 'wf:body', value: ''},
  }],
  timelines: [{actions: [ACTION]}],
}
```

## Send `enter` without scrub, or nothing plays

`enter`, `leave`, `enterBack`, and `leaveBack` are `.optional()` with no schema
default, so an omitted key stays omitted. `buildGSAPConfig` then coerces each one:

```ts
const actions = [
  stConfig.enter || 'none',
  stConfig.leave || 'none',
  stConfig.enterBack || 'none',
  stConfig.leaveBack || 'none',
];
```

Without scrub those four **are** the playback. The timeline is not attached to the
ScrollTrigger; `createToggleActionHandlers` builds one callback per action and skips
any that is `'none'`, so a config carrying none of them installs no `onEnter` at all.
The ScrollTrigger is created, the target resolves, `get_interaction` echoes the
config back, and the timeline never runs. Nothing errors.

With scrub on this cannot happen — the timeline is attached as `gsapConfig.animation`
and driven by scroll position, so the toggle actions are unread. The same omission is
therefore harmless on a scrub payload and fatal on a play-once reveal. Do not carry a
working scrub config over to a reveal and assume it plays.

The panel never reaches that state: `defaultScrollTriggerConfig` and
`createBaseTriggerConfig` both seed `enter: 'play'` with the other three `'none'`, so
every scroll trigger it writes carries all four. Match it and send at least
`enter: 'play'`.

Values are `play`, `pause`, `resume`, `reverse`, `restart`, `reset`, `complete`,
`none`. Add `leaveBack: 'reset'` when the user expects a reveal to replay on the way
back up.

The worst version of this pairs with a From or FromTo whose start value hides the
element (`opacity: '0%'`, `width: 0`). The build-time immediate render applies that
start value, the timeline never plays, and the element stays hidden — which reads to
the user as "the animation ran before I scrolled to it" rather than "it never ran".
See [`actions-and-properties.md`](actions-and-properties.md).

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
timelines: [{
  canvasDuration: 1, // no role
  actions: [{...ACTION, timing: {duration: 1}}],
}],
```

With scrub on, action `timing` is authored as a percent of the canvas rather than
in seconds. See [`timelines-and-groups.md`](timelines-and-groups.md).

### The tween has to span the canvas

Set action `timing.duration` to the same number as `canvasDuration`, almost always
`1`, so the tween occupies the whole scroll pass. `duration: 0.01` on a
`canvasDuration: 1` timeline is legal and plays in roughly 1% of the range, which is
indistinguishable from nothing happening.

And omitting `scrub` is not a scrub — that shape is a one-shot play when the range is
crossed, which also needs `enter` (above). If the user asked to scrub, pin to scroll,
or parallax, send a numeric `scrub` and a roleless `canvasDuration`.

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

## Choosing `start` and `end`

Both offsets are measured on the **trigger element**, not on the action target. The
first word is the edge of the trigger; the second is where that edge meets the
viewport.

On a play-once reveal, `start: 'top 90%'` fires as the element's top crosses 90% down
the viewport, while it is still entering. A start well up the screen (`'top 35%'`)
fires late, and on a short section that can be after the user has scrolled past the
thing the animation was meant to draw attention to. Nothing is wrong with the payload
in that case, so there is no error to chase — only a reveal the user never saw.

On a scrub the distance between `start` and `end` **is** the scroll range the
animation is spread across, so the range needs enough travel to be watchable.
`top bottom` → `top 10%` (the element enters from below and finishes near the top of
the viewport) and `top top` → `bottom bottom` both give a visible sweep — the second
is the pinned-track pattern and assumes a trigger tall enough to scroll through, as
the sample above does. Give a short element that same pair and the range is only as
tall as the element, so the sweep is over before the user registers it. Widen the
range, or put the trigger on a taller wrapper and animate a child.

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
