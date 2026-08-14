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

Plugin keys without a deep property list (`wf:lottie`, `wf:spline`,
`wf:mouse-follow`) skip the property-name check entirely — the namespace gate
handles unknown extension keys instead.

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

`[PENDING]` The legacy string form (`splitText: 'chars'`) is **accepted today**, on
create as well as update. `findActionSplitTextError` skips any non-object value,
and the docblock states that whether to reject it on write is a separate decision.
Rejecting it is part of DES-7448 and has not landed.

The panel no longer writes the string form, so prefer the object form. Do not
expect an error if you send a string, and do not rewrite a stored string during a
read-then-write.

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
