<!-- Published from the Webflow monorepo: packages/systems/ix3/schema/agent-pack/references/actions-and-properties.md
     Do not edit here. Edit the source and re-publish. -->

# Actions, properties, and values

Which properties exist per extension key, and which support random or additive
values, is generated:
[`capabilities.generated.md`](capabilities.generated.md) → Actions.
This file covers the rules behind those tables.

## Action shape

```js
{
  id: 'act-...',                 // [REQUIRED] fresh unique string
  name: 'Fade',
  timing: {duration: 0.4},
  properties: {'wf:transform': {opacity: ['100%', '40%']}},
  targets: [{extensionKey: 'wf:class', value: [STYLE_BLOCK_ID]}],
}
```

## Tween type (`tt`)

| `tt` | Meaning |
| ---- | ------- |
| `0`  | To      |
| `1`  | From    |
| `2`  | FromTo  |
| `3`  | Set     |

Omit `tt` and the runtime treats it as To (`0`). `presetId` is optional — omit it
on a new action; the host does not require one.

From (`1`) and FromTo (`2`) apply their starting values as soon as the timeline is
built (GSAP immediate-render). That is the **default**, not a guarantee. The element
then sits at the from-state until the trigger plays, so a From fade of opacity `0%` →
`100%` looks missing on the canvas and on the published page until click, hover, or
load. If the element should be visible at rest and animate on trigger, author a To
(`tt: 0` or omit).

The exception: `buildTimeline` scans each timeline in order and records every
action's properties per target, including a To. When a later From or FromTo touches a
property an earlier action already recorded on the same target, that later action is
built with `immediateRender: false` so it cannot overwrite the earlier action's
starting value while the paused timeline is built. In that case the element keeps its
current state until playback, and the initial hidden state you expected at build time
does not appear.

So a From is only reliably at its start value at rest when no earlier action in the
same timeline targets the same property on the same target.

### The runtime reads only the slot your `tt` names

`buildTweensForAction` makes one GSAP call per tween type and hands it only the
matching half of the config:

| `tt` | Call                                          | Slots used  |
| ---- | --------------------------------------------- | ----------- |
| `0`  | `tl.to(els, {...vars, ...config.to})`         | `to` only   |
| `1`  | `tl.from(els, {...vars, ...config.from})`     | `from` only |
| `2`  | `tl.fromTo(els, config.from, {...config.to})` | both        |
| `3`  | `tl.set(els, {...vars, ...config.to})`        | `to` only   |

A `[from, to]` pair on a To is therefore built and then half discarded. GSAP animates
from the element's **live computed value** to `to`, not from the value you authored:
`scale: [0.55, 1.15]` with `tt: 0` on an unscaled element animates 1 → 1.15, and
`opacity: ['20%', '100%']` on an element that is already opaque animates nothing at
all. The write succeeds, `get_interaction` echoes both values back, and no error is
raised.

This is the most common reason a scroll-scrub payload looks inert: both endpoints are
authored, one is used, and the visible delta is whatever sits between the element's
current state and the `to` value. **Author `tt: 2` whenever the animation needs a
start value.** Reserve `tt: 0` for "from wherever it is now".

The mirror case is dropped rather than half-applied. A To carrying only a from value
(`y: [40, null]`) leaves `config.to` empty, and the action is skipped outright:
`if (tweenType === 0 && !hasToProps) continue`.

The panel disables the editor for the unused slot, so the user cannot clear a stored
value there either — see [`panel-traps.md`](panel-traps.md).

### A from-state that collapses the element can make it unclickable

When the trigger element and the action target are the same element, the from-state is
what the user has to interact with. A start value of `scaleX: 0` or `width: 0` leaves
no box to hit, so a click or hover trigger on that element never fires; `opacity: '0%'`
keeps the hit area but gives the user nothing to aim at. Both save cleanly and animate
correctly once triggered — they just cannot be triggered.

Put the trigger on a parent that keeps its box and animate the child.

Non-animatable properties are only valid inside a Set action. The Designer always
emits `tt: 3` for them.

`[REJECTED]` A non-animatable property on a non-Set action.
Guard: `validateActionPropertyShape` · fragment:
`is non-animatable and must only be used in a Set action`

`[LEGACY-OK-ON-UPDATE]` Exactly two pairs are grandfathered on the update path:
`wf:class.class` and `wf:transform.display`. Before Set actions shipped these
could sit on a `tt: 0` action mixed with animatable properties. An unchanged
stored value passes through; a new or altered one is refused. The eligibility
list is owned by the schema, so a caller flag cannot widen it to `zIndex` or
anything else.
Guard: `isLegacyNonAnimatableGrandfatherEligible` / `shouldAllowLegacyNonAnimatableOnUpdate`

## Property namespaces

`[REJECTED]` A property name that is not on the allowlist for its extension key.
Guard: `validateActionPropertyShape` · fragment: `is not a supported`

The message suggests the right namespace when you put a transform property under
`wf:style`. The most common instance: **opacity belongs under `wf:transform`, never
`wf:style`.**

Note `rotation`, not `rotate`.

`wf:lottie`, `wf:spline`, and `wf:mouse-follow` now carry their own property
allowlists and are checked like any other key. They are in the generated table with
their supported properties; do not assume a plugin namespace skips validation.

Every action key the API can author now has an entry, so in practice nothing skips
the property-name check today. The fallback still exists for a key added to the
registry before its allowlist, and the namespace gate handles unknown extension keys
either way.

## `timing.autoReverse` is not authorable

Covered in [`envelope-and-targets.md`](envelope-and-targets.md) alongside the other
fields the Designer never writes. Short version: `[REJECTED]` on both
`action.timing.autoReverse` and `timeline.settings.autoReverse`, with an unchanged
stored value allowed through on update.

## Value shapes

Accepted: a bare scalar, `[from]`, `[from, to]`, `[from, null]`, `[null, to]`, or a
random/additive wrapper.

`[REJECTED]` A plain `{from, to}` object. The Designer never stores one.
Guard: `validateActionPropertyShape` · fragment:
`must not be a plain {from, to} object`

## Random and additive

The Designer stores Random and Relative wrappers as the `to` leaf of a
`[from, to]` tuple, so capability checks run per authored leaf rather than only on
a top-level wrapper.

`[REJECTED]` `ix3-random-array` on a property that does not support random values.
Fragment: `does not support random values`

`[REJECTED]` `ix3-random` min/max on a property that supports only value sets.
Colors are value-set only. Fragment: `does not support random min/max range values`

`[REJECTED]` `ix3-additive` on a property that does not support it. Colors do not.
Fragment: `does not support additive values`

`[REJECTED]` A random-array outside the size bounds (see the generated file).
Fragment: `random-array must have between`

`[REJECTED]` A wrapper carrying a known `type` discriminator that fails its
structural guard. Fragment: `has a malformed`

## `timing.duration` — seconds, not milliseconds

`secondsOrMsSchema` stores a consistent number of **seconds**. Two input forms:

- A number is already seconds. `0.4` is four hundred milliseconds. `400` is four
  hundred seconds.
- A `"Nms"` string is converted: `"400ms"` becomes `0.4`.

The built-in presets use `0.3`. The panel's unit toggle writes either a number of
seconds or an `"Nms"` string; it never writes a millisecond number. The write
succeeds either way — nothing will tell you that `duration: 400` is six minutes
forty seconds.

`[REJECTED]` at schema: `'1.5s'`, a bare `'400'`, or any other string form.
Fragment: `Milliseconds must be in format "123ms" or "123.45ms"`

A third input form exists and is easy to miss: `secondsOrMsSchema` also accepts
`null`, and transforms it to **`0.25`**. That is not the same as omitting the field,
which leaves it unset and lets the runtime default apply. Do not send `null` expecting
"no duration".

### `timing.delay` on an action is accepted and then ignored

`timingConfigSchema` declares `delay: z.number()` but ends with
`.merge(playbackSettingsSchema)`, whose `delay` is the seconds-or-ms union, and a Zod
merge overrides the earlier key. So `"400ms"` is accepted on `delay` and normalizes to
`0.4`. Read the merge before trusting a field's declared type on this schema.

**But the value does nothing on an action.** `buildTweensForAction` builds its GSAP
tween vars from `position`, `duration`, `stagger`, `repeat`, and `repeatDelay`. It
never reads `action.timing.delay`. The write succeeds, `get_interaction` echoes the
value back, and the animation is unaffected. Nothing reports it.

Delay is real in the two other places it appears:

| Field                     | Effect                                                                        |
| ------------------------- | ----------------------------------------------------------------------------- |
| `trigger.config.delay`    | Delays trigger execution. Applied via `setTimeout` in the trigger strategies. |
| `timeline.settings.delay` | Timeline playback delay. Applied as GSAP `tl.delay()`.                        |
| `action.timing.delay`     | **Inert.** Accepted by the schema, never passed to GSAP.                      |

To stagger actions inside a timeline, use **`timing.position`**, not `timing.delay`.

On a percent canvas the same field is authored as a percent — see
[`timelines-and-groups.md`](timelines-and-groups.md).

## `timing.position` — the Start field

The panel treats `position` as an absolute start time. It writes either a number
of seconds or an `"Nms"` string, depending on the unit toggle, and Reset clears
it. There is no operator UI.

Two layers refuse different things here, and they return different errors.

**Schema first.** `timelinePositionSchema` accepts a number, an `"Nms"` string, a
GSAP alignment operator (`<`, `>`), a relative operator (`+=0.5`), or an alignment
with offset (`<+=1.5`). Anything else fails before a guard runs.

`[REJECTED]` at schema: `'1.5s'`, a bare `'500'`, or any other string form.
Fragment: `Absolute position must be a number or milliseconds string`

**Then the guard.** The operator forms the schema allows are the ones the panel
cannot author or display: `getTimelineEditorInputValue` returns null for them, so
the Start field renders empty and the next edit silently overwrites the operator
with an absolute time.

`[REJECTED]` at the guard: `<`, `>`, `+=0.5`, `<+=1`, and the other operator forms.
Guard: `findActionTimingPositionError` · fragment:
`is not a start time the Designer can author`

These two split across the layers as well, despite both being non-finite:

`[REJECTED]` at schema: `NaN`. Zod's `z.number()` refuses it during parsing, so it
never reaches the guard. Fragment: `Invalid input`

`[REJECTED]` at the guard: `Infinity` and `-Infinity`. Zod accepts both as numbers
because the position schema does not apply `.finite()`, so the guard is what stops
them. The Start field only writes finite seconds.
Guard: `findActionTimingPositionError`

The guard tests `!Number.isFinite`, which covers `NaN` too, but that branch is
unreachable through a normal parse and is defensive only.

If you are matching an error, check which layer produced it. A schema failure names
the expected format; the guard names the Designer.

On a percent canvas the same field is authored as a percent — see
[`timelines-and-groups.md`](timelines-and-groups.md).

## `splitText`

The Mask dropdown offers "None" plus the option matching the split type, and
choosing None omits `mask` rather than storing a value. So the only object forms
the panel writes are `{type}` or `{type, mask}` with the two equal.

Two layers again.

`[REJECTED]` at schema: `mask: 'none'`, or any value outside the mask enum.
`splitTextMaskSchema` is `z.enum(['chars', 'words', 'lines']).optional()`, so
`'none'` never reaches the guard. Choosing None in the panel omits `mask` rather
than storing a value, which is why there is no `'none'` member. **Omit the key**
instead.

`[REJECTED]` at the guard: an otherwise valid mask that differs from `type`.
Guard: `findActionSplitTextError` · fragment: `must match`

`[REJECTED]` The legacy string form (`splitText: 'chars'`) on create. The panel
reads it for migration but no longer writes it.
Guard: `findActionSplitTextError`

`[LEGACY-OK-ON-UPDATE]` A stored string survives an update when the same action id
echoes the same value. Two extra conditions apply: a duplicated action id is
refused outright, so one stored string cannot authorize a second row claiming the
same id, and changing the value re-enters the reject.

Pass a stored string through untouched. Author the object form for anything new.

SplitText needs a target that **contains text**, whether directly or in a
descendant. The runtime hands the resolved element to GSAP SplitText, which walks
child elements, so a Div wrapping a Paragraph that reads "Hello" is a valid target and
still yields character targets. You do not need to add a text element, or retarget to
the inner one, just to make splitting work.

What does split nothing is a target with **no text anywhere inside it**. An empty Div
or Block saves cleanly and then animates nothing. Creating a Block and trying to
`set_text` onto it is the wrong fix; point the action at something that already holds
copy. The write path does not check element type.

## Panel traps

These are accepted by the write path and invisible in the panel afterwards.

`[PANEL-TRAP]` `timing.duration` on a Set action. The panel disables the Duration
input for Set, but no guard rejects a stored non-zero duration.

`[PANEL-TRAP]` `timing.ease` on a Set action. The Ease row is not rendered for Set.

`[PANEL-TRAP]` `timing.repeat`, `timing.yoyo`, `timing.stagger`, or `splitText` on a
Set action. The whole block is gated behind a non-Set tween type in the panel.

`[PANEL-TRAP]` A `from` slot value on a To tween, or a `to` slot value on a From
tween. The corresponding editor is disabled, so the user cannot clear what you
stored. `validateActionPropertyShape` checks leaf shapes, not slot-versus-tween
consistency.
