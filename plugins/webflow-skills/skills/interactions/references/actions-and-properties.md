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
  name: 'Fade',                  // [REQUIRED]
  tt: 2,                         // optional; omitted = To, which reads only `to`
  timing: {duration: 0.4},       // [REQUIRED] — even on a Set, use {duration: 0}
  properties: {'wf:transform': {opacity: ['100%', '40%']}},
  targets: [{extensionKey: 'wf:class', value: [STYLE_BLOCK_ID]}],
  // splitText: {type: 'words'}  // action-level, NOT timing.splitText
}
```

`id`, `name`, `timing`, `properties`, and `targets` are all required. The two that
are easy to assume optional are not:

`[REJECTED]` An action with no `timing`, including a Set action that has nothing to
time. Fragment: `timelines.0.actions.0.timing: Required`. Send
`timing: {duration: 0}` on a Set.

`[REJECTED]` An action with no `name`. Fragment:
`timelines.0.actions.0.name: Required`.

By contrast, trigger `config.control` **is** optional on a single-group
interaction — `config: {}` is accepted and stored as-is, with nothing stamped. But
omitting it is not the same as sending `play`: the runtime treats a missing
`control` as `restart`. Send `control: 'play'` when you mean play. It becomes
mandatory once the interaction has two or more action groups.

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

### Choosing between From and FromTo for a reveal

Three rules in this pack point different ways on this, so state it once:

- A **reveal** — element hidden at rest, animating to whatever its stylesheet says
  — is a **From (`tt: 1`)** carrying **only a from value**: `opacity: ['0%']` or
  `['0%', null]`. GSAP animates from that value to the element's live value, so
  there is no `to` to supply.
- Adding a `to` value to a From is a `[PANEL-TRAP]`, not an error. It stores, and
  the panel's To editor is disabled, so the user can neither see nor clear it. See
  [`panel-traps.md`](panel-traps.md).
- Use **FromTo (`tt: 2`)** when you genuinely want both endpoints pinned, and the
  end state is _not_ the element's resting style — a hover that lifts to `-8px`
  and returns, for instance.

So "use `tt: 1` for a reveal" and "use `tt: 2` whenever the animation needs a
start value" are both right, and neither means "send `[from, to]` on a From".

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

**The Designer panel does mark it, though.** Verified in the Interactions panel on
an interaction stored with `tt` omitted and a `[from, to]` pair: the unused _from_
field renders greyed out. So this is invisible to the API and to a read, but a
human looking at the panel can see the discarded slot. If a user reports an
animation that "does nothing", pointing them at a greyed field is faster than
re-reading the payload.

This is the most common reason a scroll-scrub payload looks inert: both endpoints are
authored, one is used, and the visible delta is whatever sits between the element's
current state and the `to` value. **Author `tt: 2` whenever the animation needs a
start value.** Reserve `tt: 0` for "from wherever it is now".

The mirror case is dropped rather than half-applied. A To carrying only a from value
(`y: [40, null]`) leaves `config.to` empty, and the action is skipped outright:
`if (tweenType === 0 && !hasToProps) continue`.

The panel disables the editor for the unused slot, so the user cannot clear a stored
value there either — see [`panel-traps.md`](panel-traps.md).

### A later From/FromTo does not park the element at its from-state

When two actions in the same interaction touch the same property on the same
target — the usual hover in / hover out pair — only the first records a rest
state. The second does not apply its from-value on load.

Verified on a published page with a two-trigger hover split: the leave action was
`tt: 2` with `y: ['-8px', '0px']`, and at rest the element measured
`translateY(0)`, not `-8px`. It moved `0 → -8` on enter and `-8 → 0` on leave.

So authoring the out-direction as a FromTo mirror of the in-direction is safe
inside one interaction, and does not leave the element visibly displaced before
the user interacts. Two _separate_ interactions have no such ordering
relationship — there, prefer a To for the out-direction.

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

## `wf:class` — the Class operation

The only `wf:class` property is `class`, and it is non-animatable, so it lives in a
Set action (`tt: 3`). The value is `null` (unset / reset — the runtime treats it as
a no-op) or an object carrying **both** keys:

```js
{
  tt: 3,
  timing: {duration: 0},
  properties: {
    'wf:class': {
      class: {operation: 'addClass', selectors: [STYLE_BLOCK_ID]},
    },
  },
}
```

`operation` is `addClass` / `removeClass` / `toggleClass`. `selectors` is an array
of non-empty style-block id strings.

**`selectors` is not combo-expanded.** Unlike a `wf:class` _target_ value, where
the host walks the chain and adds the combo's parents for you, a `selectors` entry
applies exactly the one class it names. Verified on a published page: passing the
combo leaf id for `is-featured` turned `class="pg-card"` into
`class="pg-card is-featured"` — the leaf and nothing else. So name the class you
want applied, and if the visual result depends on a parent already being present,
make sure the element carries it.

Every rejection below comes from `validateWfClassPropertyValue`, except the last.

`[REJECTED]` A property name other than `class` under `wf:class`.
Guard: `validateActionPropertyShape` · fragment: `is not a supported`

`[REJECTED]` A bare array or string value. Fragment:
`value must be null or an object {operation, selectors}`

`[REJECTED]` An extra key alongside `operation` / `selectors`. Fragment:
`does not support property`

`[REJECTED]` Only one of the two keys. Fragment:
`must include both "operation" and "selectors"`

`[REJECTED]` An operation outside the three. Fragment:
`operation must be one of addClass, removeClass, toggleClass`

`[REJECTED]` `selectors` not an array, or containing an empty string. Fragments:
`selectors must be an array of style-block id strings` and
`must be an array of non-empty style-block id strings`

`[REJECTED]` The whole property on an animated tween. Because `class` is
non-animatable it is Set-only.
Guard: `validateActionPropertyShape` · fragment:
`non-animatable and must only be used in a Set action (tt: 3)`

Guessing this shape from the tool schema costs four round trips — each message is
precise, but they only arrive one at a time.

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

**That rule is namespace-scoped, not global.** It holds for `wf:transform`,
`wf:style`, and `wf:class`. It is inverted for two plugin namespaces:
`wf:lottie.lottie` and every `wf:spline` channel **require** a `{from?, to?}`
object and refuse an array. Read as an absolute, this rule makes both namespaces
unauthorable. See the plugin value shapes below.

### `wf:style` value shapes

Seven properties, in two groups. The three colours animate; the other four do not
and are Set-only (`tt: 3`).

| Property          | Animatable | Value                                                                          |
| ----------------- | ---------- | ------------------------------------------------------------------------------ |
| `backgroundColor` | yes        | `'#rrggbb'`                                                                    |
| `borderColor`     | yes        | `'#rrggbb'`                                                                    |
| `color`           | yes        | `'#rrggbb'`                                                                    |
| `zIndex`          | **no**     | unitless number, e.g. `10`                                                     |
| `position`        | **no**     | `static` \| `relative` \| `absolute` \| `fixed` \| `sticky` (default `static`) |
| `overflow`        | **no**     | `visible` \| `hidden` \| `scroll` \| `auto` \| `clip` (default `visible`)      |
| `pointerEvents`   | **no**     | `auto` \| `none` (default `auto`)                                              |

```js
// Set the four non-animatable ones together
{
  tt: 3,
  timing: {duration: 0},
  properties: {'wf:style': {zIndex: 10, position: 'absolute', pointerEvents: 'none'}},
}
```

Note the asymmetry worth remembering: `display` is non-animatable but lives under
`wf:transform`, while these four are non-animatable and live under `wf:style`.
Non-animatable is a property fact, not a namespace fact.

### Colour and rotation value formats

**Colours are hex strings.** The three `wf:style` colour properties
(`backgroundColor`, `borderColor`, `color`) take `'#rrggbb'`. Verified accepted as
a bare scalar (`'#1a1a2e'`) and as a `[from, to]` pair; the pair is what
interpolates, and `['#ffffff', '#f2eee6']` was measured animating a published
`body` to `rgb(242, 238, 230)`. A bare scalar on a To reads the `to` slot and
tweens from the element's live colour.

**Rotation is in degrees, as a bare number.** `rotation: [0, 8]` is eight degrees,
not radians and not a `'deg'` string. Verified by measurement: the published
element reported `matrix(0.990268, 0.139173, …)`, which is `cos 8°` / `sin 8°`.

### On a Set action, a bare scalar is enough

A Set (`tt: 3`) reads only the `to` slot, and a bare scalar occupies it. Both of
these are accepted **and** applied at runtime — verified on a published page,
where `.pg-card` went from `display: block` to `display: none`:

```js
properties: {'wf:transform': {display: 'none'}}            // bare scalar
properties: {'wf:transform': {display: ['block', 'none']}} // pair, to slot wins
```

Prefer the bare scalar on a Set: there is no from-state to express, so a pair
invites the reader to think the first value does something. `display` takes a CSS
display keyword as a string; `'none'` and `'block'` are both confirmed.

## `wf:lottie` value shapes

Two properties. Both are validated; neither takes the tuple form used everywhere
else.

| Property         | Value                                                                                                                                             |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `lottie`         | an **object**, not an array. `from` and `to` are **both required** and must be numbers (or variable references). May also carry `manualDuration`. |
| `manualDuration` | **boolean** — a flag, not a duration                                                                                                              |

```js
properties: {'wf:lottie': {lottie: {from: 0, to: 1}, manualDuration: true}}
```

Every rejection comes from `validateLottieNested`.

`[REJECTED]` An array, or any non-object. Fragment:
`value must be an object with from/to`

`[REJECTED]` Only one of the two. Fragment:
`must include both "from" and "to"`

`[REJECTED]` A key other than `from` / `to` / `manualDuration`. Fragment:
`supported keys: from, to, manualDuration`

`[REJECTED]` A non-numeric `from` / `to`. Fragment:
`from/to must be numbers or variable references`

`[REJECTED]` A non-boolean `manualDuration`, at either level. Fragment:
`must be a boolean`

## `wf:spline` value shapes

Three properties.

| Property         | Value                                                                            |
| ---------------- | -------------------------------------------------------------------------------- |
| `spline`         | an object of animatable **channels**, each channel its own `{from?, to?}` object |
| `objectId`       | string                                                                           |
| `animatingState` | **boolean** — the state _name_ travels in the `stateName` channel, not here      |

The fourteen channels: `positionX` `positionY` `positionZ` `rotationX`
`rotationY` `rotationZ` `scaleX` `scaleY` `scaleZ` `intensity` `opacity` `zoom`
`color` `stateName`.

```js
properties: {'wf:spline': {
  spline: {positionX: {from: 0, to: 10}, opacity: {from: 1, to: 0.5}},
  objectId: 'my-object',
  animatingState: true,
}}
```

Note the asymmetry with `wf:lottie`: a spline channel takes `{from?, to?}` with
**both optional**, while `lottie` requires both. Every rejection comes from
`validateSplineNested`.

`[REJECTED]` An array, or any non-object, for `spline`. Fragment:
`value must be an object of animatable channels`

`[REJECTED]` A channel name outside the fourteen. Fragment:
`does not support channel` — the message then lists all fourteen, which is the
only place that list appears at runtime.

`[REJECTED]` A channel given a tuple or scalar instead of an object. Fragment:
`must be a {from?, to?} object`

`[REJECTED]` A field other than `from` / `to` inside a channel. Fragment:
`only supports from/to fields`

## Random and additive

The Designer stores Random and Relative wrappers as the `to` leaf of a
`[from, to]` tuple, so capability checks run per authored leaf rather than only on
a top-level wrapper.

### Wrapper shapes

Three wrappers. **The unit is always its own field — never baked into the value.**
That is the one that costs attempts: `{type: 'ix3-additive', value: '40px'}` is
refused, because `value` is numeric and `px` belongs in `unit`.

| `type`             | Fields                                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------------------ |
| `ix3-random`       | `min` (number, required), `max` (number, required), `step?` (number, snap increment), `unit?` (string) |
| `ix3-additive`     | `value` (**number**, or a nested `ix3-random` wrapper), `unit?` (string)                               |
| `ix3-random-array` | `values` (array of numbers, or comma-free strings for colours), `unit?` (string)                       |

```js
// pick a value in a range each time it plays
{type: 'ix3-random', min: -100, max: 100, unit: 'px'}

// relative: the runtime emits GSAP `+=`, so re-firing accumulates
{type: 'ix3-additive', value: 40, unit: 'px'}

// pick from a fixed set; colours are value-set only
{type: 'ix3-random-array', values: ['#1a1a2e', '#7a4de8'], unit: undefined}
```

`ix3-additive` composes: `{type: 'ix3-additive', value: {type: 'ix3-random',
min: 0, max: 10}}` emits `+=random(0, 10)`.

`[REJECTED]` A wrapper missing a required field. Fragments: `malformed
ix3-random`, `malformed ix3-additive`, `malformed ix3-random-array`. These name
the wrapper but not the missing field, so check the table above rather than
guessing variants.

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

## `timing.ease` — the Ease field

**`ease` is a number, not a string.** `easeConfigSchema` is
`z.union([z.number().int().nonnegative(), advancedEaseSchema])`.

This one is worth reading carefully, because the rejection teaches you nothing.
It is a Zod union failure, so the message is a bare `Invalid input` at
`timing.ease` with no branch detail and no enum — the only non-enumerating
validation message on this surface. A dogfood run spent seven attempts on it
(four string forms, a bezier array, two object shapes) and never landed it.

`[REJECTED]` Any string: `'power1.out'`, `'power2.out'`, `'ease-out'`, `'linear'`.
Layer: Zod (`easeConfigSchema`) · fragment: `Invalid input`

`[REJECTED]` A 4-number bezier array such as `[0.25, 0.1, 0.25, 1]`.
`customBezierSchema` exists but is deprecated and is **not** part of
`easeConfigSchema`. Use `{type: 'customEase', bezierCurve}`.

`[SILENTLY-DROPPED]` `easing` in place of `ease`. `timingConfigSchema` is a
non-strict object, so the misspelling is stripped and the animation ships with
default easing. Nothing reports it. Same failure mode as the trigger `config`
strip in [`envelope-and-targets.md`](envelope-and-targets.md).

### Built-in easing index

The integer indexes `EASING_NAMES` in
`packages/systems/ix3/runtime/src/utils.ts`. The panel's "Linear" is `0`; its
"Power 1 out" is `2`.

| Index | Name                    | Index | Name           | Index | Name            |
| ----- | ----------------------- | ----- | -------------- | ----- | --------------- |
| 0     | `none` (panel "Linear") | 11    | `power4.out`   | 22    | `elastic.in`    |
| 1     | `power1.in`             | 12    | `power4.inOut` | 23    | `elastic.out`   |
| 2     | `power1.out`            | 13    | `back.in`      | 24    | `elastic.inOut` |
| 3     | `power1.inOut`          | 14    | `back.out`     | 25    | `expo.in`       |
| 4     | `power2.in`             | 15    | `back.inOut`   | 26    | `expo.out`      |
| 5     | `power2.out`            | 16    | `bounce.in`    | 27    | `expo.inOut`    |
| 6     | `power2.inOut`          | 17    | `bounce.out`   | 28    | `sine.in`       |
| 7     | `power3.in`             | 18    | `bounce.inOut` | 29    | `sine.out`      |
| 8     | `power3.out`            | 19    | `circ.in`      | 30    | `sine.inOut`    |
| 9     | `power3.inOut`          | 20    | `circ.out`     |       |                 |
| 10    | `power4.in`             | 21    | `circ.inOut`   |       |                 |

```js
timing: {duration: 0.4, ease: 2}
```

### Advanced eases

Objects discriminated on `type`, each `.strict()`. `[FLAG]` behind
`ff-styl-1612-ix3-advanced-easing`. You cannot read that flag from the payload,
so **attempt the write and handle a refusal** rather than refusing up front — a
`{type: 'back', curve: 'out', power: 1.7}` ease was accepted and stored on a
live site, so pre-emptively declining costs the user a capability that works.

| `type`         | Fields                                                                                 |
| -------------- | -------------------------------------------------------------------------------------- |
| `back`         | `curve`, `power`                                                                       |
| `elastic`      | `curve`, `amplitude`, `period`                                                         |
| `steps`        | `stepCount` (int)                                                                      |
| `rough`        | `templateCurve`, `points` (int), `strength`, `taper`, `randomizePoints`, `clampPoints` |
| `slowMo`       | `linearRatio`, `power`, `yoyoMode`                                                     |
| `expoScale`    | `startingScale`, `endingScale`, `templateCurve`                                        |
| `customWiggle` | `wiggles` (int), `wiggleType`                                                          |
| `customBounce` | `strength`, `squash`, `endAtStart`                                                     |
| `customEase`   | `bezierCurve` (string)                                                                 |

`curve` is `in` / `out` / `inOut`. `taper` is `none` / `in` / `out` / `both`.
`wiggleType` is `easeOut` / `easeInOut` / `anticipate` / `uniform` / `random`.
`templateCurve` is a `"family.direction"` string; the `rough` set covers every
family, the `expoScale` set omits back / bounce / circ / elastic.

```js
timing: {duration: 0.4, ease: {type: 'back', curve: 'out', power: 1.7}}
```

`timing.stagger.ease` takes the identical union.

`[PANEL-TRAP]` `timing.ease` on a Set action. The Ease row is not rendered for
Set, so a stored value is invisible and uneditable.

## `timing.stagger` — the Stagger block

`staggerConfigSchema` is an object. A bare number is rejected.

| Field    | Shape                                                                          |
| -------- | ------------------------------------------------------------------------------ |
| `each`   | seconds or an `"Nms"` string — the panel's "Offset time"                       |
| `amount` | seconds or an `"Nms"` string — total spread, alternative to `each`             |
| `axis`   | `'x'` / `'y'`                                                                  |
| `ease`   | same union as `timing.ease`                                                    |
| `from`   | `'start'` / `'center'` / `'end'` / `'edges'` / `'random'`, a number, or `null` |
| `grid`   | `'auto'`, a `[columns, rows]` number pair, or `null`                           |

`[REJECTED]` A bare number for `stagger`. Layer: Zod · fragment:
`Expected object, received number`

`[REJECTED]` `grid: 'none'`. The panel's Grid "None" is the absent / `null` state,
not a string. Layer: Zod · fragment: `Invalid input`

`[REJECTED]` `stagger.ease` as a string, per the ease rules above.

```js
timing: {
  duration: 0.5,
  stagger: {each: 0.05, from: 'start', grid: [2, 2], ease: 0},
}
```

`[PANEL-TRAP]` `stagger` on a Set action — the repeat / yoyo / stagger / splitText
block is gated behind a non-Set tween type.

## `splitText`

**`splitText` is an action-level field**, a sibling of `timing`, `properties`, and
`targets` — **not** `timing.splitText`. Getting that wrong is a
`[SILENTLY-DROPPED]`, not a rejection: `timingConfigSchema` is non-strict, so a
misplaced `splitText` is stripped and the text ships unsplit with no error.

```js
{
  id: 'a1',
  name: 'Reveal words',
  tt: 1,
  splitText: {type: 'words'},          // <- here, beside timing
  timing: {duration: 0.5, stagger: {each: 0.05}},
  properties: {'wf:transform': {opacity: ['0%']}},  // From: from slot only
  targets: [{extensionKey: 'wf:class', value: [STYLE_BLOCK_ID]}],
}
```

Where the panel-trap table lists "`timing.repeat` / `yoyo` / `stagger` /
`splitText` on a Set action", the first three are `timing` keys and the fourth is
not; they share a trap, not a parent.

### The target needs text, not a particular element type

The constraint is that copy exists inside the target — in the element itself or a
descendant. It is **not** that the target be a Heading, Paragraph, or Text.
Verified on a published page: a Block whose text is a child String node
(`.pg-card` containing "Card one") produced two `gsap_split_word` spans, while a
Paragraph in the same run produced twenty.

What does fail is a target with no text anywhere inside it. That saves, reads back
intact, and animates nothing — no error, because nothing structural is wrong with
the payload.

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
